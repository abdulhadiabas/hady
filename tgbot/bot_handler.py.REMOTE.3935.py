# -*- coding: utf-8 -*-
import logging
import random
from django.contrib.auth.models import User
from telegram import Emoji
from telegram import ForceReply
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from deep.constants import *
from tgbot.models import Record, Text, People, Score

maintenance_state = False
logger = logging.getLogger(__name__)


def start_msg_and_keyboard(bot, chat_id, people):
    '''
    when user comes to the bot, this function will check that user submitted it's own age and gender or not
    :param bot: bot object
    :param chat_id: unique identifier of user in telegram
    :param people: people object
    :return: age_message or gender_message or random_text
    '''
    if people.age and people.gender:
        send_random_text(bot, chat_id, people)
    else:
        if not people.age:
            send_age_message(bot, chat_id)
        elif not people.gender:
            send_gender_message(bot, chat_id)
        else:
            send_random_text(bot, chat_id, people)
            return


def myscore(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    msg = '🎗 جمع امتیازاتت: %s' \
          '\n' \
          'جمع امتیازاتت رو زیاد کن تا توی قرعه‌کشی شرکت داده بشی!' \
          '\n\n' \
          '@deepBot' % people.total_scores()
    bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply())


def next_question(bot, update):
    '''
    /next command in bot will call this function
    :param bot:
    :param update:
    :return:
    '''
    print("called next question..")
    print(update)
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    send_random_text(bot, chat_id, people)


def start(bot, update):
    '''
    when bot starts, this function will be called first -> /start
    :param bot:
    :param update:
    :return:
    '''
    print("called start..")
    print(update)
    from_user = update.message.from_user
    chat_id = update.message.chat_id
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name, tg_username=from_user.username)
    start_msg_and_keyboard(bot, chat_id, people)


def send_random_text(bot, chat_id, people):
    '''
    Get a random txt from text that user didn't read
    :param bot: bot object
    :param chat_id: unique identifier of user in telegram
    :param people: people object
    :return:
    '''
    people_records = people.records.all()
    all_unseen_text = Text.objects.all().exclude(id__in=people_records.values_list('text_id', flat=True))
    if not all_unseen_text.exists():
        all_unseen_text = Text.objects.all()
    random_text_obj = all_unseen_text[random.randint(0, all_unseen_text.count() - 1)]

    people.sentence_is_reading = random_text_obj.code
    people.save()
    reply_keyboard = [['می‌خونم'], ['برو جمله‌ی بعدی']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    bot.sendMessage(chat_id, text='🎤 جمله:\n\n'
                                  '«%s»\n\n'
                                  'می‌خونی یا بره جمله‌ی بعدی؟'
                                  '\n\n@deepBot' % random_text_obj.text, reply_markup=reply_markup)
    bot.sendVoice(chat_id, open(random_text_obj.sample_voice.url, 'rb'), caption='نمونه صدا')


def send_specific_text(bot, chat_id, selected_text, bad_voice=False):
    '''
    when we are goin to send specific text to the user
    :param bot: bot telegram
    :param chat_id: unique identifier of user in telegram
    :param selected_text: text_object
    :param bad_voice: if voice quality is not good this will be true and inform user
    :return:
    '''
    default_msg = '🎤 لطفا جمله زیر را به با نگه داشتن دکمه میکروفون به صورت شمرده بخوانید\n'
    bad_voice_msg = 'کیفیت صدا مناسب نیست، لطفا مجددا متن را کامل و با صدای بلندتر بخوانید.\n'
    msg = '%s' \
          '\n«<b>%s</b>»' \
          '\n' \
          '\nکد «%s»' \
          % (bad_voice_msg if bad_voice else default_msg, selected_text.text,
             selected_text.code,)
    bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply(), parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    bot.sendVoice(chat_id, open(selected_text.sample_voice.url, 'rb'), caption='نمونه صدا')


def record_again(bot, chat_id, people, record_obj, bad_voice=False):
    record_obj.delete()
    people.records.filter(state=RECORD_STATES_DEFAULT).delete()
    send_specific_text(bot, chat_id, record_obj.text, bad_voice)


def record_accepted(bot, chat_id, people, record_obj):
    record_obj.state = RECORD_STATES_ACCEPTED
    record_obj.save()
    people.records.filter(state=RECORD_STATES_DEFAULT).delete()
    people.scores.create(record=record_obj, score=50)
    bot.sendMessage(chat_id, text='✅ با تشکر، صدای شما ثبت شد.'
                                  '\n'
                                  '🎁 ۵۰ امتیاز بابت خوندن این متن گرفتی!'
                                  '\n'
                                  '🎗 جمع امتیازاتت: %s'
                                  '\n\n🇮🇷 @deepBot' % people.total_scores())
    send_random_text(bot, chat_id, people)


def energy(samples):
    return sum([x**2 for x in samples])


def handle_text(bot, update):
    print("handle text....")
    print(update)
    chat_id = update.message.chat_id
    text = update.message.text

    people = check_user(update.message.chat_id)

    record_obj = Record.objects.filter(people=people, state=RECORD_STATES_DEFAULT)
    if record_obj.exists():
        people.sentence_is_reading = None
        people.save()
        record_obj = record_obj[0]
        if text == 'آره':
            record_accepted(bot, chat_id, people, record_obj)
        elif text == 'نه دوباره می‌خوام بخونم':
            record_again(bot, chat_id, people, record_obj)

    elif text == 'سن':
        send_age_message(bot, chat_id)
        people.sentence_is_reading = None
        people.save()

    elif text == 'مرد' or text == 'زن':
        people.gender = GENDER_MEN if text == 'مرد' else GENDER_WOMAN
        people.save()
        bot.sendMessage(chat_id, text='جنسیت شما ثبت شد')
        if people.age:
            send_random_text(bot, chat_id, people)
        if not people.age:
            send_age_message(bot, chat_id)

        people.sentence_is_reading = None
        people.save()

    elif text == 'جنسیت':
        send_gender_message(bot, chat_id)
        people.sentence_is_reading = None
        people.save()

    elif text in [AGE[i][1] for i in range(len(AGE))]:
        key = [key for key, value in dict(AGE).items() if value == text][0]
        people.age = key
        people.save()
        bot.sendMessage(chat_id, text='سن شما ثبت شد.')
        if people.gender:
            send_random_text(bot, chat_id, people)
        if not people.gender:
            send_gender_message(bot, chat_id)

        people.sentence_is_reading = None
        people.save()

    elif text == 'می‌خونم':
        text_code = people.sentence_is_reading
        if text_code is None:
            bot.sendMessage(chat_id, text="کد متن مورد نظر یافت نشد!")
            send_random_text(bot, chat_id, people)

        text_obj = Text.objects.get(code=text_code)
        msg = '🎤 لطفا جمله زیر را به با نگه داشتن دکمه میکروفون به صورت شمرده بخوانید.\n' \
              '\n«<b>%s</b>»' \
              '\n' \
              '\nکد «%s»' \
              % (text_obj.text,
                 text_obj.code)

        bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply(), parse_mode=ParseMode.HTML, disable_web_page_preview=False)
        bot.sendVoice(chat_id, open(text_obj.sample_voice.url, 'rb'), caption='نمونه صدا')

    elif text == 'جمله‌ی بعدی' or text == 'برو جمله‌ی بعدی':
        people.records.filter(state=RECORD_STATES_DEFAULT).delete()
        people.sentence_is_reading = None
        people.save()
        send_random_text(bot, chat_id, people)
    else:
        people.sentence_is_reading = None
        people.save()
        bot.sendMessage(chat_id, text='درخواست معتبر نیست!')
        start(bot, update)


def return_name():
    import uuid
    return "%s.ogg" % uuid.uuid4()


def filter_record(path, bot, chat_id, text_obj):
    print("in filter record...")
    print(path)
    import soundfile as sf
    from datetime import datetime
    import ffmpy, os

    t1 = datetime.now().timestamp()
    temp_dest = path[:path.rfind('.')] + '_temp.wav'
    dest = path[:path.rfind('.')] + '.wav'

    ff = ffmpy.FFmpeg(inputs={path: None}, outputs={temp_dest: None})
    ff.run()

    os.remove(path)

    t2 = datetime.now().timestamp()
    print("Time:")
    print(t2 - t1)
    print(temp_dest)

    samples, samplerate = sf.read(temp_dest)
    signal_duration = len(samples) / samplerate

    print(signal_duration)

    print("url...")
    print(text_obj.sample_voice.url)
    ref_samples, ref_samplerate = sf.read(text_obj.sample_voice.url)
    print("ref samples o gereft...")
    ref_duration = len(ref_samples) / ref_samplerate

    print("ref duration..")
    print(ref_duration)

    signal_energy = energy(samples)
    ref_energy = energy(ref_samples)

    print('Ref Energy:')
    print(ref_energy)
    print('Signal Energy:')
    print(signal_energy)

    if signal_energy <= 0.1 * ref_energy:
        print("inside of signal energy..")
        bad_voice_msg = 'کیفیت صدا مناسب نیست، لطفا مجددا متن را با صدای بلندتر بخوانید.\n'
        msg = '%s' \
              '\n«<b>%s</b>»' \
              '\n' \
              '\nکد «%s»' \
              % (bad_voice_msg, text_obj.text,
                 text_obj.code)
        bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply(), parse_mode=ParseMode.HTML)
        bot.sendVoice(chat_id, open(text_obj.sample_voice.url, 'rb'), caption='نمونه صدا')
        print("removed file because of low energy...")
        return False

    if signal_duration <= 0.3 * ref_duration or signal_duration > 2 * ref_duration:
        print("inside of signal duration..")
        bad_voice_msg = 'کیفیت صدا مناسب نیست، لطفا مجددا متن را شمرده و کامل بخوانید.\n'
        msg = '%s' \
              '\n«<b>%s</b>»' \
              '\n' \
              '\nکد «%s»' \
              % (bad_voice_msg, text_obj.text,
                 text_obj.code,)
        bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply(), parse_mode=ParseMode.HTML)
        bot.sendVoice(chat_id, open(text_obj.sample_voice.url, 'rb'), caption='نمونه صدا')
        print("removed file because of sort duration...")
        return False

    bashCommand = "ffmpeg -i %s -ar 16000 %s" % (temp_dest, dest)
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    process.kill()

    print("signal quality is ok!")
    os.remove(temp_dest)
    return True, dest, signal_energy


def handle_voice(bot, update):
    print("handle voice....")
    print(update)
    chat_id = update.message.chat_id
    voice = update.message.voice
    file_id = voice.file_id
    is_reply = update.message.reply_to_message
    people = check_user(chat_id)

    if not (people.age and people.gender):
        start_msg_and_keyboard(bot, chat_id, people)
        return

    file = bot.getFile(file_id=file_id)
    if is_reply:
        text = update.message.reply_to_message.text
        text_id = text[text.rfind('«')+1: text.rfind('»')]
        text_obj = Text.objects.get(code=text_id)

        import os
        if not os.path.exists('media/downloaded_voices/%s' % chat_id):
            os.mkdir('media/downloaded_voices/%s' % chat_id)

        file_name = return_name()
        # downloaded_file_path = 'media/downloaded_voices/%s/%s' % (chat_id, file_name)
        downloaded_file_path = 'media/downloaded_voices/temp/%s' % file_name
        file.download(custom_path=downloaded_file_path)
        quality_control_check, dest, signal_energy = filter_record(downloaded_file_path, bot, chat_id, text_obj)

        if not quality_control_check:
            return

        record = Record.objects.create(people=people, text=text_obj, energy=signal_energy,
                                       file_size=voice.file_size, duration=voice.duration,
                                       voice_url=file.file_path, tg_file_id=file_id)

        gender_type = 'U'
        if people.gender == GENDER_MEN:
            gender_type = 'M'
        elif people.gender == GENDER_WOMAN:
            gender_type = 'F'

        file_name = '%s%sTG%s' % (1000 + people.id, gender_type, text_obj.code)
        file_name_with_extension = file_name + '.wav'
        print(file_name)
        import os, shutil
        print(dest)

        os.rename(dest, 'media/downloaded_voices/temp/%s' % file_name_with_extension)
        shutil.move('media/downloaded_voices/temp/%s' % file_name_with_extension,
                    'media/downloaded_voices/%s/%s' % (chat_id, file_name_with_extension))

        with open('media/downloaded_voices/%s/%s.wrd' % (chat_id, file_name), 'a') as f:
            f.write(text_obj.text)

        with open('media/downloaded_voices/%s/%s.phn' % (chat_id, file_name), 'a') as f:
            f.write(text_obj.phonetic)

        reply_keyboard = [['آره'], ['نه دوباره می‌خوام بخونم']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id, text='ثبت بشه؟', reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text='باید صدایتان را روی متن مورد نظر به شکل Reply ارسال کنید',
                        reply_markup=ReplyKeyboardRemove())
        send_random_text(bot, chat_id, people)

    print("Successfully got the voice")


def send_gender_message(bot, chat_id):
    print("in send_gender_message")
    reply_keyboard = [['مرد'], ['زن']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.sendMessage(chat_id, text='لطفا جنسیت خود را انتخاب کنید', reply_markup=reply_markup)


def send_age_message(bot, chat_id):
    print("in send_age_message")
    reply_keyboard = [[AGE[AGE_UNDER_10 - 1][1], AGE[AGE_10_20 - 1][1]],
                      [AGE[AGE_20_30 - 1][1], AGE[AGE_30_40 - 1][1]],
                      [AGE[AGE_40_50 - 1][1], AGE[AGE_50_60 - 1][1]],
                      [AGE[AGE_OVER_60 - 1][1]]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.sendMessage(chat_id, text='لطفا بازه‌ی سن خود را انتخاب کنید', reply_markup=reply_markup)


def check_user(tg_id, tg_first_name=None, tg_last_name=None, tg_username=None):
    try:
        people = People.objects.get(user__username=tg_id)
    except (People.DoesNotExist or User.DoesNotExist):
        user = User.objects.create(username=tg_id, first_name=tg_first_name,
                                     last_name=tg_last_name)
        people = People.objects.create(user=user, tg_username=tg_username)

    return people


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

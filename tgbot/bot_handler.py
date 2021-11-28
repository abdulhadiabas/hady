# -*- coding: utf-8 -*-
import logging
from os import path
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Count
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from telegram.error import BadRequest
from telegram.error import Unauthorized

from deep.constants import *
from tgbot.models import Record, Text, People

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


def about(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    msg = 'ئێمە کێین؟' \
          '\n\n' \
          'ئاسۆسافت گرووپێکی توێژینەوەییە کە لە لایەن مامۆستایان و خوێندکارانی کوردەوە  دامەزراوە و لە بواری پەرداوتنی کۆمپیووتەریی زمانی کوردی چالاکی دەکات. زمانی کوردی  یەکێک لەو زمانانەیە کە سەرچاوەی کەمی لە بواری زمانناسی و بە تایبەت زمانناسیی کۆمپیووتەریدا ھەیە. ئەم گرووپە ھەوڵ دەدات سەرچاوە و ئامێر بۆ پەرداوتنی کۆمپیووتەریی زمانی کوردی دابین بکات.  بۆ ئەو مەبەستانەی باس کران، چالاکییەکانی گرووپەکە جۆربەجۆرن کە بەشێکیان لەم خاڵانەی خوارەوەدا دەبینرێن:' \
          '\n' \
          '🔶 ناسینەوەی ئاخاوتنی کوردی (Kurdish Speech Recognition): نەرمامێری تایپی ئۆتۆماتیکی یەکێک لە بەرهەمەکانی ئەم بوارەیە، بە شێوەیەک کە ئەو شتەی بەکارهێنەر دەیڵێت لە لایەن کۆمپیووتەر یان مۆبایلەوە تایپ دەکرێت.' \
          '\n' \
          'کردنی دەق بە ئاخاوتنی کوردی (Kurdish Text-to-Speech): ئەرکی ئەم سیستمە خوێندوەی هەر جۆرە دەقێکی زمانی کوردییە.' \
          '\n' \
          ' 🔶  هەڵەگری ڕێنووسی (Spell Checker)' \
          '\n\n' \
          'پەیوەندی لەگەڵ ئاسۆسافت:' \
          '\n' \
          '💻 ماڵپەڕ: asosoft.com' \
          '\n' \
          '✉️ ئیمەیل:info[at]asosoft[dot]com' \
          '\n\n' \
          '✅ تێلێگرام: https://t.me/asosoft' \
          '\n' \
          '🔵 فەیسبووک: https://www.facebook.com/asosoftku'

    bot.sendMessage(chat_id, text=msg)


def help_msg(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    msg = 'تکایە ...' \
          '\n' \
          '  🎤  بۆ خوێندنەوەی  ڕستەکان میکڕۆفۆنەکە بگرە و لەسەرخۆ بیخوێنەوە.' \
          '\n\n' \
          '👈 لە سەرەتای هەر ڕستەیەکدا چرکەیەک میکرۆفۆنەکە ڕاگرن پاشان دەست بکەن بە خوێندنەوە.' \
          '\n' \
          '  👈  چرکەیەک دوای خوێندنەوەی ڕستەکە دەست لەسەر میکرۆفۆن هەڵگرن.' \
          '\n\n' \
          ' 🔇 لە شوێنی بێدەنگ دەنگەکان تۆمار بکەن.' \
          '\n' \
          '📱 بە مۆبایل دەنگەکان تۆمار بکەن نەک لەپتاپ یان ئامێرێک کە کوالێتیی میکرۆفۆنەکەی لە خوارەوەیە.' \
          '\n\n' \
          ' 😊 هەرچی ڕستەی زیاترمان بۆ بخوێننەوە، یارمەتیی زیاتری توێژینەوەکەتان داوە.' \
          '\n\n' \
          'زۆر سپاس 🙏🙏🙏'
    bot.sendMessage(chat_id, text=msg)


def myscore(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    msg = '🎗 کۆی خاڵەکان: %s' \
          '\n' \
          'کۆی خاڵەکانت زیاد بکە تا بتوانیت لە کێبەرکێی پشک خستندا هاوبەش بیت!' \
          '\n\n' \
          '@speechku_bot' % people.total_scores()
    bot.sendMessage(chat_id, text=msg)


def send_reminder_message(chat_id=None):
    from telegram import Bot
    bot = Bot("2103492201:AAFBZ-7JCPjKROtuLlsnslgfwaSAiow4kE8")
    msg = "هاوڕێیانی خۆشەویستی ئاسۆسافت🌷" \
          "\n" \
          "\n\n" \
          "سپاسی یەک بە یەکتان دەکەین کە لە ماوەی چەند مانگی ڕابردوودا بە تۆمارکردنی دەنگ یارمەتیی بەرەوپێشچوونی پڕۆژەکانی ئاسۆسافتتان دا.🙏🏻 " \
          "\n" \
          "لە ئێستادا کۆکردنەوەی دەنگ لەم قۆناغەدا ڕادەگرین." \
          "\n" \
          "بەو هیوایەی کە  یارمەتییەکانی ئێوە بە پێشکەشکردنی بەرهەمی شیاو بۆ زمانی کوردی قەرەبوو بکەینەوە." \
          "\n\n" \
          "چاوەڕێمان بن.." \
          "\n" \
		  "ڕێز  و سپاس" \
		   "\n" \
          "(گرووپی توێژینەوە و پەرەدانی ئاسۆسافت @AsoSoft)" \
          "\n" \
          "‌"
		  
    count = 0
    for p in People.objects.all():
        if p.records.count() <= 300:
            try:
                bot.sendMessage(p.user.username, msg)
                count += 1
            except (Unauthorized, BadRequest) as err:
                print(err)
            print("Count: %d" % count)

    # inform admin who called the reminder function
    msg = "پیغام برای %d کاربر با موفقیت ارسال شد!" % count
    print(msg)
    if chat_id:
        bot.sendMessage(chat_id, text=msg)


def send_reminder_msg(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    if people.user.username in ['191322468', '90731804', '112285828']:
        bot.sendMessage(chat_id, "شروع ارسال پیغام به کاربران...")
        send_reminder_message(chat_id)
    else:
        bot.sendMessage(chat_id, "شما اجازه‌ی این کار را ندارید!")


def info(bot, update):
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    people = check_user(update.message.chat_id, tg_first_name=from_user.first_name, tg_last_name=from_user.last_name,
                        tg_username=from_user.username)
    total_users = People.objects.all().count()
    total_records = Record.objects.filter(state=RECORD_STATES_ACCEPTED).count()
    msg = 'Total Users: %s' \
          '\n' \
          'Total Records: %s' % (total_users, total_records)
    bot.sendMessage(chat_id, text=msg)


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
    all_recorded_texts = Record.objects.values('text__code').annotate(dcount=Count('text__code', disctinct=True)).values_list('text__code', flat=True)
    people_records = people.records.all()
    all_unseen_text = Text.objects.all().exclude(code__in=people_records.values_list('text__code', flat=True)).exclude(code__in=all_recorded_texts)
    if not all_unseen_text.exists():
        all_unseen_text = Text.objects.all().exclude(code__in=people_records.values_list('text__code', flat=True))
    if not all_unseen_text.exists():
        # No more text to read, say thank you
        msg = "زۆر سپاس بۆ یارمەتیتان 🙏🙏" \
              "\n" \
              "دەستان خۆش و دەنگتان بەرز! 🌹🌹"
        bot.sendMessage(chat_id, text=msg)
        return
    random_text_obj = all_unseen_text[random.randint(0, all_unseen_text.count() - 1)]

    people.sentence_is_reading = random_text_obj.code
    people.save()
    bot.sendMessage(chat_id, text='تکایە بۆ خوێندنەوەی ئەم  ڕستەی خوارەوە میکڕۆفۆنەکە 🎤 بگرە و لەسەرخۆ بیخوێنەوە👇\n\n'
                                  '🗣 «%s»\n\n\n'
                                  '⏩ بچۆ بۆ ڕستەی دواتر 👈 /next'
                                  '\n\n@speechku_bot' % random_text_obj.text, reply_markup=ForceReply())
    bot.sendVoice(chat_id, open(random_text_obj.sample_voice.url, 'rb'), caption='دەنگی نموونە')


def send_specific_text(bot, chat_id, people, selected_text):
    '''
    when we are goin to send specific text to the user
    :param bot: bot telegram
    :param chat_id: unique identifier of user in telegram
    :param selected_text: text_object
    :param bad_voice: if voice quality is not good this will be true and inform user
    :return:
    '''
    default_msg = '🎤 تکایە بۆ خوێندنی ڕەستەی خوارۆ میکڕۆفۆنەکە بگرە و بیخوێنە\n'
    people.sentence_is_reading = selected_text.code
    people.save()
    msg = '%s' \
          '\n\n🗣 «%s»\n\n\n' \
          '⏩ بچۆ بۆ ڕستەی دواتر 👈 /next' \
          '\n\n@speechku_bot' % (default_msg, selected_text.text)
    bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply(), disable_web_page_preview=False)
    bot.sendVoice(chat_id, open(selected_text.sample_voice.url, 'rb'), caption='دەنگی نموونە')


def record_again(bot, chat_id, people, record_obj):
    record_obj.delete()
    people.records.filter(state=RECORD_STATES_DEFAULT).delete()
    send_specific_text(bot, chat_id, people, record_obj.text)


def record_accepted(bot, chat_id, people, record_obj):
    record_obj.state = RECORD_STATES_ACCEPTED
    record_obj.save()
    people.records.filter(state=RECORD_STATES_DEFAULT).delete()
    if not people.scores.filter(record__text__code=record_obj.text.code).exists():
        people.scores.create(record=record_obj, score=50)
    bot.sendMessage(chat_id, text='✅ زۆر سپاس، دەنگی ئێوە تۆمار کرا.'
                                  '\n'
                                  '🎁 بۆ خوێندنەوەی ئەم دەقە ٥٠ خاڵت وەرگرت!'
                                  '\n'
                                  '🎗 کۆی خاڵەکان: %s'
                                  '\n\n🎤  @speechku_bot' % people.total_scores())
    send_random_text(bot, chat_id, people)


def energy(samples):
    return sum([x**2 for x in samples])


def handle_text(bot, update):
    print("handle text....")
    print(update)
    chat_id = update.message.chat_id
    text = update.message.text

    people = check_user(update.message.chat_id)

    min_time = datetime.now() - timedelta(minutes=1)
    record_obj = Record.objects.filter(people=people, state=RECORD_STATES_DEFAULT, creation_time__range=(min_time, datetime.now()))
    if record_obj.exists():
        people.sentence_is_reading = None
        people.save()
        record_obj = record_obj[0]
        if text == '✅ بەڵێ':
            record_accepted(bot, chat_id, people, record_obj)
        elif text == '🔁 نا، دیسان دەمهەوێت بخوێنمەوە':
            record_again(bot, chat_id, people, record_obj)

    elif text == 'تەمەن':
        send_age_message(bot, chat_id)

    elif text == 'پیاو' or text == 'ژن':
        people.gender = GENDER_MEN if text == 'پیاو' else GENDER_WOMAN
        people.sentence_is_reading = None
        people.save()
        bot.sendMessage(chat_id, text='ڕەگەزی ئێوە تۆمار کرا.')
        if people.age:
            help_msg(bot, update)
            send_random_text(bot, chat_id, people)
        if not people.age:
            send_age_message(bot, chat_id)

    elif text == 'ڕەگەز':
        send_gender_message(bot, chat_id)

    elif text in [AGE[i][1] for i in range(len(AGE))]:
        key = [key for key, value in dict(AGE).items() if value == text][0]
        people.age = key
        people.sentence_is_reading = None
        people.save()
        bot.sendMessage(chat_id, text='تەمەنی ئێوە تۆمار کرا.')
        if people.gender:
            help_msg(bot, update)
            send_random_text(bot, chat_id, people)
        if not people.gender:
            send_gender_message(bot, chat_id)

    else:
        people.sentence_is_reading = None
        people.save()
        bot.sendMessage(chat_id, text='داوکارییەکەت ڕێگەپێدراو نییە!')
        start(bot, update)


def return_name():
    import uuid # create random name for file
    
    return "%s.ogg" % uuid.uuid4()


def filter_record(path, bot, chat_id, people, text_obj):

    print("in filter record...")
    print(path)
    import soundfile as sf
    from datetime import datetime
    import ffmpy, os,ffmpeg

    t1 = datetime.now().timestamp()
    temp_dest = path[:path.rfind('.')] + '_temp.wav'
    dest = path[:path.rfind('.')] + '.wav'
    ff = ffmpy.FFmpeg(executable='C:\\ffmpeg\\bin\\ffmpeg.exe', inputs={path: None}, outputs={temp_dest:None})
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
    ref_samples, ref_samplerate = sf.read('media/%s' %text_obj.sample_voice.url)
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

    people.sentence_is_reading = text_obj.code
    people.save()
    print("inside of signal energy..")

    if signal_energy <= 0.1 * ref_energy:
        print("inside of signal energy..")
        bad_voice_msg = '❗ کوالێتیی دەنگ باش نییە، تکایە جارێکی تر دەقەکە بە دەنگی بەرزتر بخوێنەوە\n'
        msg = '%s' \
              '\n\n🗣 «%s»\n\n\n' \
              '⏩ بچۆ بۆ ڕستەی دواتر 👈 /next' \
              '\n\n@speechku_bot' % (bad_voice_msg, text_obj.text)
        bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply())
        bot.sendVoice(chat_id, open(text_obj.sample_voice.url, 'rb'), caption='دەنگی نموونە')
        print("removed file because of low energy...")
        return False, dest, signal_energy

    if signal_duration <= 0.3 * ref_duration or signal_duration > 2 * ref_duration:
        print("inside of signal duration..")
        bad_voice_msg = '❗ کوالێتیی دەنگ باش نییە، تکایە جارێکی تر دەقەکە لەسەرخۆتر و بە تەواوی بخوێنەوە\n'
        msg = '%s' \
              '\n\n🗣 «%s»\n\n\n' \
              '⏩ بچۆ بۆ ڕستەی دواتر 👈 /next' \
              '\n\n@speechku_bot' % (bad_voice_msg, text_obj.text)
        bot.sendMessage(chat_id, text=msg, reply_markup=ForceReply())
        bot.sendVoice(chat_id, open(text_obj.sample_voice.url, 'rb'), caption='دەنگی نموونە')
        print("removed file because of sort duration...")
        return False, dest, signal_energy
    




    
    bashCommand = "C:\\ffmpeg\\bin\\ffmpeg.exe -i %s -ar 16000 %s" % (temp_dest, dest)
    print(bashCommand)
    import subprocess
    process = subprocess.Popen(bashCommand.split(), 
                           stdout=subprocess.PIPE, 
                           shell=True,
                         )
    output, error = process.communicate()
    print('ali wara')
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
    print('media/downloaded_voices/%s' % chat_id+"/%s" %voice )
    is_reply = update.message.reply_to_message
  
    people = check_user(chat_id)

    if not (people.age and people.gender):
        start_msg_and_keyboard(bot, chat_id, people)
        return

    file = bot.getFile(file_id=file_id)
    if is_reply:
        print('کۆدی دەق وەرنەگیرا')
        text_code = people.sentence_is_reading
        try:
            text_obj = Text.objects.get(code=text_code)
        except Text.DoesNotExist:
            bot.sendMessage(chat_id, text='کۆدی دەق وەرنەگیرا')
            send_random_text(bot, chat_id, people)
            return

        if text_obj.code in people.records.values_list('text__code', flat=True):
            msg = "زۆر سپاس بۆ یارمەتیتان 🙏🙏" \
                  "\n" \
                  "دەستان خۆش و دەنگتان بەرز! 🌹🌹"
            bot.sendMessage(chat_id, text=msg)
            return

        import os
        if not os.path.exists('media/downloaded_voices/%s' % chat_id):
            os.mkdir('media/downloaded_voices/%s' % chat_id)

        file_name = return_name()
        
        # downloaded_file_path = 'media/downloaded_voices/%s/%s' % (chat_id, file_name)
        
        downloaded_file_path = 'media/downloaded_voices/%s' % chat_id+"/%s" %file_name
        print(file)
        file.download(custom_path=downloaded_file_path)

        quality_control_check, dest, signal_energy = filter_record(downloaded_file_path, bot, chat_id, people, text_obj)
        
        
        if not quality_control_check:
            return
        print('hady')

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
        # if os.path.exists('media/downloaded_voices/%s/%s.wav' % (chat_id, file_name)):
        #     print("file wav hast ba in name")
        #     file_name_with_extension = file_name + '.wav'

        print(file_name_with_extension)
        import os, shutil
        print(text_obj.text)
        x=text_obj.text
        
       

        os.rename(dest, 'media/downloaded_voices/%s' % file_name_with_extension)
        
        shutil.move('media/downloaded_voices/%s' % file_name_with_extension,
                    'media/downloaded_voices/%s/%s' % (chat_id, file_name_with_extension))


        with open('readme.txt', 'w', encoding='utf-8') as f:
            f.write(x)
    
        with open('media/downloaded_voices/%s/%s.txt' % (chat_id, file_name), 'w', encoding='utf-8') as f:
            print(text_obj.text)
            f.write(text_obj.text)

        with open('media/downloaded_voices/%s/%s.phn' % (chat_id, file_name), 'w', encoding='utf-8') as f:
            f.write(text_obj.phonetic)
       

        reply_keyboard = [['✅ بەڵێ'], ['🔁 نا، دیسان دەمهەوێت بخوێنمەوە']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id, text='تۆمار بکرێت؟', reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id, text='تکایە ڕەستەکە  Reply کە و بە دوای ئەوا دەنگەکەت زەبت کە',
                        reply_markup=ReplyKeyboardRemove())
        send_random_text(bot, chat_id, people)

    print("Successfully got the voice")


def send_gender_message(bot, chat_id):
    print("in send_gender_message")
    reply_keyboard = [['پیاو'], ['ژن']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.sendMessage(chat_id, text='تکایە ڕەگەزی خۆتان هەڵبژێرن.', reply_markup=reply_markup)


def send_age_message(bot, chat_id):
    print("in send_age_message")
    reply_keyboard = [[AGE[AGE_UNDER_10 - 1][1], AGE[AGE_10_20 - 1][1]],
                      [AGE[AGE_20_30 - 1][1], AGE[AGE_30_40 - 1][1]],
                      [AGE[AGE_40_50 - 1][1], AGE[AGE_50_60 - 1][1]],
                      [AGE[AGE_OVER_60 - 1][1]]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.sendMessage(chat_id, text='تکایە مەودای تەمەنی خۆتان هەڵبژێرین', reply_markup=reply_markup)


def check_user(tg_id, tg_first_name=None, tg_last_name=None, tg_username=None):
    try:
        people = People.objects.get(user__username=tg_id)
    except (People.DoesNotExist or User.DoesNotExist):
        user = User.objects.create(username=tg_id, first_name=tg_first_name[:25] if tg_first_name else '',
                                     last_name=tg_last_name[:25] if tg_last_name else '')
        people = People.objects.create(user=user, tg_username=tg_username)

    return people


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

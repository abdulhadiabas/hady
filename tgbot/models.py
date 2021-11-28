from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from deep import constants


class People(models.Model):
    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'افراد'

    def __str__(self):
        return '%s - %s' % (self.user.get_full_name(), self.user.username)

    def total_scores(self):
        scores = self.scores.aggregate(total_scores=Sum('score')).get('total_scores', 0)
        return scores if scores else 0

    user = models.OneToOneField(User, related_name='people', on_delete=models.CASCADE)
    tg_username = models.CharField(verbose_name='یوزرنیم تلگرام', max_length=100, blank=True, null=True)
    gender = models.IntegerField(verbose_name='جنسیت', choices=constants.GENDER, null=True, blank=True)
    age = models.IntegerField(verbose_name='سن', choices=constants.AGE, null=True, blank=True)
    sentence_is_reading = models.CharField(verbose_name='کد جمله‌ای که می‌خواهد بخواند', max_length=50, null=True, blank=True)


class Text(models.Model):
    class Meta:
        verbose_name = 'متن'
        verbose_name_plural = 'متن‌ها'
        ordering = ('-creation_time',)

    def __str__(self):
        return '%s' % self.text

    def _get_upload_path(self, filename):
        return "sample_voices/%s" % filename

    text = models.TextField(verbose_name='متن ارسال شده', max_length=700)
    phonetic = models.TextField(verbose_name='آوانویسی', max_length=900, null=True, blank=True)
    code = models.CharField(verbose_name='کد متن', max_length=100, null=True, blank=True)
    sample_voice = models.FileField(verbose_name='صدای نمونه', null=True, blank=True, upload_to=_get_upload_path)
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')


class Record(models.Model):
    class Meta:
        verbose_name = 'رکورد'
        verbose_name_plural = 'رکوردها'
        ordering = ('-creation_time',)

    def __str__(self):
        return '%s - %s - %s' % (self.people, self.text, self.voice_url)

    people = models.ForeignKey(People, verbose_name='کاربر', on_delete=models.CASCADE, related_name='records', null=True, blank=True)
    text = models.ForeignKey(Text, verbose_name='متن ارسال شده', on_delete=models.CASCADE, related_name='records')
    tg_file_id = models.URLField(verbose_name='شناسه‌ی فایل در تلگرام',  null=True, blank=True)
    voice_url = models.URLField(verbose_name='آدرس قابل دانلود',  null=True, blank=True)
    state = models.IntegerField(verbose_name='وضعیت ثبت',  choices=constants.RECORD_STATES, default=constants.RECORD_STATES_DEFAULT, null=True, blank=True)
    duration = models.FloatField(verbose_name='مدت زمان فایل',  null=True, blank=True)
    energy = models.FloatField(verbose_name='انرژی سیگنال',  null=True, blank=True)
    file_size = models.IntegerField(verbose_name='حجم فایل',  null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد', )


class Score(models.Model):
    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
        ordering = ('-creation_time',)

    def __str__(self):
        return '%s امتیاز مربوط به %s - %s' % (self.score, self.people, self.record)

    people = models.ForeignKey(People, verbose_name='بازیکن', on_delete=models.CASCADE, related_name='scores')
    record = models.ForeignKey(Record, verbose_name='رکورد',  on_delete=models.CASCADE,null=True, blank=True, related_name='scores')
    score = models.IntegerField(verbose_name='امتیاز' )
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد' )

from django.contrib import admin
from django.db.models import Count

from tgbot.models import Record, Text, People, Score


class PeopleAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_username', 'gender', 'age', 'total_scores')
    list_filter = ('gender',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'tg_username', 'gender', 'age']


class TextAdmin(admin.ModelAdmin):
    list_display = ('code', 'text', 'total_recs', 'phonetic', 'sample_voice', 'creation_time', )
    readonly_fields = ('creation_time', )
    list_filter = ('creation_time',)
    search_fields = ['text', ]

    def get_queryset(self, request):
        qs = super(TextAdmin, self).get_queryset(request)
        qs = qs.annotate(rec_count=Count('records__id'))
        return qs

    def total_recs(self, obj):
        return obj.rec_count
    total_recs.admin_order_field = 'rec_count'
    total_recs.short_description = '#رکورد‌ها'


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('people', 'record', 'score', 'creation_time')
    readonly_fields = ('creation_time', )
    list_filter = ('creation_time', )
    search_fields = ['people__user__first_name', 'people__user__username', 'record']

    def match_id(self, obj):
        return obj.game.id if obj.game else "ندارد"
    match_id.short_description = 'شناسه بازی'

    def question_code(self, obj):
        return obj.question.question_code if obj.question else "ندارد"
    question_code.short_description = 'کد سوال'


class RecordAdmin(admin.ModelAdmin):
    list_display = ('people', 'text', 'state', 'duration', 'sig_energy', 'file_size', 'creation_time')
    readonly_fields = ('creation_time', )
    list_filter = ('creation_time', 'state', 'text__code')
    search_fields = ['people__user__username', 'text__code']

    def sig_energy(self, obj):
        return '%.3f' % obj.energy if obj.energy else ''
    sig_energy.short_description = 'انرژی'

admin.site.register(People, PeopleAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Score, ScoreAdmin)
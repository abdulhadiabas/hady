import xlrd
from django.core.management.base import NoArgsCommand
from django.db import transaction
from tgbot.models import Text


class Command(NoArgsCommand):

    @transaction.atomic
    def handle_noargs(self, **options):
        print("Loading dataset...")
        book = xlrd.open_workbook("deep/static/dataset_951312.xlsx", encoding_override='utf8')
        sheet1 = book.sheet_by_index(0)

        i = 0
        for row in sheet1.get_rows():
            print("i: %d" % i)
            i += 1
            if i == 1:
                continue

            print("Sentence...")
            sentence = row[0].value
            print(row[1])
            print("phonetic..")
            phonetic = row[1].value
            file_name = row[2].value

            code = 699 + int(file_name[len(file_name) - 3:])
            print("sentence..")
            print(sentence)
            Text.objects.create(text=sentence, phonetic=phonetic, code=code, sample_voice='dataset_files/TestSet2/%s.ogg' % file_name)
            print()

        print("%s Question added successfully!" % i)

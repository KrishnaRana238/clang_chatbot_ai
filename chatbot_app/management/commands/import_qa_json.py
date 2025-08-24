import json
from django.core.management.base import BaseCommand
from chatbot_app.models import QAModel

class Command(BaseCommand):
    help = 'Import Q&A pairs from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file to import.')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as f:
            data = json.load(f)
            count = 0
            skipped = 0
            for item in data:
                question = item.get('question')
                answer = item.get('answer')
                if question and answer:
                    if not QAModel.objects.filter(question=question).exists():
                        QAModel.objects.create(question=question, answer=answer)
                        count += 1
                    else:
                        skipped += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} Q&A pairs from {json_file}, skipped {skipped} duplicates'))

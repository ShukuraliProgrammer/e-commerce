import json
from django.core.management.base import BaseCommand
from core.settings.base import BASE_DIR
from common.models import Country


class Command(BaseCommand):
    help = "Load all countries"

    def handle(self, *args, **kwargs):
        try:
            with open(str(BASE_DIR) + "/data/countries.json") as f:
                countries = json.load(f)
                for country in countries:
                    Country.objects.get_or_create(name=country['name_uz'], code=country['code'])

            self.stdout.write(self.style.SUCCESS("Countries loaded successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

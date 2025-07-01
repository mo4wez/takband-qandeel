# literature/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.db import transaction

from literature.models import (
    Author, AuthorAlias, WorkGroup, Work, Section, Poem, PoemLine,
    Tag, Glossary, PoemTag
)
from literature.factories import PoemFactory

# --- Configuration ---
NUM_AUTHORS = 10
NUM_WORKGROUPS_PER_AUTHOR = 5
NUM_WORKS_PER_WORKGROUP = 3
NUM_POEMS_PER_WORK = 5

class Command(BaseCommand):
    help = "Seeds the database with fake data for poetry models using Farsi language"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")

        # Define all models to be cleared to ensure a clean slate
        models_to_clear = [PoemTag, Glossary, PoemLine, Poem, Section, Work, WorkGroup, AuthorAlias, Author, Tag]
        for m in models_to_clear:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # The creation logic is simple because PoemFactory handles all its dependencies.
        for _ in range(NUM_AUTHORS):
            for _ in range(NUM_WORKGROUPS_PER_AUTHOR):
                for _ in range(NUM_WORKS_PER_WORKGROUP):
                    for i in range(NUM_POEMS_PER_WORK):
                        PoemFactory(order_in_work=i + 1)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with Farsi data!"))

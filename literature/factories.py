# literature/factories.py

import random
from faker import Faker
from slugify import slugify

import factory
from factory.django import DjangoModelFactory, ImageField

from .models import (
    Author, AuthorAlias, WorkGroup, Work, Section,
    Poem, PoemLine, Glossary, Tag, PoemTag
)

# --- Instantiate Faker for Farsi (Iran) ---
fake = Faker('fa_IR')


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('slug',)

    name = factory.Faker('name', locale='fa_IR')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    birth_year = factory.LazyAttribute(lambda o: int(fake.year()))
    death_year = factory.LazyAttribute(lambda o: o.birth_year + random.randint(40, 80) if o.birth_year else int(fake.year()))
    biography = factory.Faker('text', max_nb_chars=1000, locale='fa_IR')
    image = ImageField(color='green')


class AuthorAliasFactory(DjangoModelFactory):
    class Meta:
        model = AuthorAlias

    author = factory.SubFactory(AuthorFactory)
    name = factory.Faker('name', locale='fa_IR')


class WorkGroupFactory(DjangoModelFactory):
    class Meta:
        model = WorkGroup
        django_get_or_create = ('slug',)

    author = factory.SubFactory(AuthorFactory)
    title = factory.LazyAttribute(lambda o: ' '.join(fake.words(nb=3)).title())
    slug = factory.LazyAttribute(lambda o: slugify(f"{o.author.name}-{o.title}"))
    description = factory.Faker('paragraph', nb_sentences=4, locale='fa_IR')


class WorkFactory(DjangoModelFactory):
    class Meta:
        model = Work
        django_get_or_create = ('slug',)

    group = factory.SubFactory(WorkGroupFactory)
    title = factory.LazyAttribute(lambda o: ' '.join(fake.words(nb=4)).title())
    slug = factory.LazyAttribute(lambda o: slugify(f"{o.group.author.name}-{o.title}"))
    description = factory.Faker('paragraph', nb_sentences=5, locale='fa_IR')

    genre = factory.LazyFunction(lambda: random.choice([x[0] for x in Work.GENRE_CHOICES]))
    dialect = factory.LazyFunction(lambda: random.choice(['تهرانی', 'خراسانی', 'شیرازی', 'اصفهانی']))
    era = factory.LazyFunction(lambda: random.choice(['کلاسیک', 'معاصر', 'دوره مشروطه', 'ناشناخته']))
    notes = factory.Faker('text', max_nb_chars=500, locale='fa_IR')
    sources = factory.Faker('text', max_nb_chars=200, locale='fa_IR')


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section
        django_get_or_create = ('slug',)

    work = factory.SubFactory(WorkFactory)
    title = factory.LazyAttribute(lambda o: ' '.join(fake.words(nb=2)).title())
    slug = factory.LazyAttribute(lambda o: slugify(f"{o.work.title}-{o.title}"))
    description = factory.Faker('paragraph', locale='fa_IR')
    order = factory.Sequence(lambda n: n + 1)


class PoemFactory(DjangoModelFactory):
    class Meta:
        model = Poem
        django_get_or_create = ('slug',)

    work = factory.SubFactory(WorkFactory)
    section = factory.SubFactory(SectionFactory)
    title = factory.LazyAttribute(lambda o: ' '.join(fake.words(nb=2)).title())
    slug = factory.LazyAttribute(lambda o: slugify(f"{o.work.title}-{o.title}"))
    intro = factory.Faker('paragraph', nb_sentences=3, locale='fa_IR')
    meter = "مستفعلن مستفعلن مستفعلن مستفعلن"
    rhyme = "یار"
    date_written = factory.Faker('year')
    order_in_work = factory.Sequence(lambda n: int(n))
    raw_text = factory.Faker('text', max_nb_chars=2000, locale='fa_IR')
    is_published = True

    @factory.post_generation
    def create_related_objects(obj, create, extracted, **kwargs):
        if not create:
            return

        stanza_type = random.choice([PoemLine.STANZA_TYPE_COUPLET, PoemLine.STANZA_TYPE_QUATRAIN])
        lines_per_stanza = 2 if stanza_type == PoemLine.STANZA_TYPE_COUPLET else 4
        num_stanzas = random.randint(5, 10)
        total_lines = num_stanzas * lines_per_stanza

        for i in range(1, total_lines + 1):
            current_stanza_num = (i + lines_per_stanza - 1) // lines_per_stanza
            PoemLineFactory(
                poem=obj,
                line_number=i,
                stanza=current_stanza_num,
                stanza_type=stanza_type
            )

        for _ in range(random.randint(3, 8)):
            GlossaryFactory(poem=obj)

        for _ in range(random.randint(2, 4)):
            PoemTagFactory(poem=obj)


class PoemLineFactory(DjangoModelFactory):
    class Meta:
        model = PoemLine
        django_get_or_create = ('poem', 'line_number')

    poem = factory.SubFactory(PoemFactory)
    line_number = factory.Sequence(lambda n: int(n))
    stanza = 1
    stanza_type = PoemLine.STANZA_TYPE_COUPLET
    text = factory.Faker('sentence', nb_words=8, locale='fa_IR')
    transliteration = factory.Faker('sentence', locale='en_US')
    translation = factory.Faker('sentence', locale='en_US')


class GlossaryFactory(DjangoModelFactory):
    class Meta:
        model = Glossary

    poem = factory.SubFactory(PoemFactory)
    word = factory.Faker('word', locale='fa_IR')
    meaning = factory.Faker('sentence', nb_words=10, locale='fa_IR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word', locale='fa_IR')
    description = factory.Faker('sentence', locale='fa_IR')


class PoemTagFactory(DjangoModelFactory):
    class Meta:
        model = PoemTag
        django_get_or_create = ('poem', 'tag')

    poem = factory.SubFactory(PoemFactory)
    tag = factory.SubFactory(TagFactory)
    note = factory.Faker('sentence', nb_words=5, locale='fa_IR')

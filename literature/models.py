from django.db import models


# If an author is known by multiple spellings or pen names
class AuthorAlias(models.Model):
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, related_name='aliases')
    name = models.CharField(max_length=255)


class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    biography = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors/', blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class WorkGroup(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='workgroups')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.author.name}"
    

class Work(models.Model):
    GENRE_CHOICES = [
        ('epic', 'Epic'),
        ('ghazal', 'Ghazal'),
        ('rubai', 'Rubāʿī'),
        ('folk', 'Folk'),
        ('free', 'Free Verse'),
        ('qasida', 'Qasida'),
        ('other', 'Other'),
    ]

    group = models.ForeignKey(to=WorkGroup, on_delete=models.CASCADE, related_name='works')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)

    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, help_text="Optional: Epic, Rubāʿī, etc.")
    dialect = models.CharField(max_length=100, blank=True, help_text="Optional: Southern, Eastern Balochi...")
    era = models.CharField(max_length=100, blank=True, help_text="Optional: Classical, Modern, Unknown")
    notes = models.TextField(blank=True, help_text="Scholarly commentary or section intro")
    sources = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    work = models.ForeignKey(to=Work, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Poem(models.Model):
    work = models.ForeignKey(to=Work, on_delete=models.CASCADE, related_name='poems')
    section = models.ForeignKey(to=Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='poems')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    intro = models.TextField(blank=True) # poet's preface
    meter = models.CharField(max_length=100, blank=True, null=True, help_text="وزن (poetic meter)")
    rhyme = models.CharField(max_length=100, blank=True, null=True, help_text="قافیه")
    date_written = models.CharField(max_length=50, blank=True)
    order_in_work = models.PositiveIntegerField(default=0)

    raw_text = models.TextField(blank=True, help_text="Paste your full poem here (2 lines per beyt)")

    is_published = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order_in_work']

    def __str__(self):
        return self.title
    

class PoemLine(models.Model):
    STANZA_TYPE_COUPLET = 'couplet'
    STANZA_TYPE_QUATRAIN = 'quatrain'
    STANZA_TYPE_FREE = 'free'
    STANZA_TYPE_OTHER = 'other'

    STANZA_TYPE_CHOICES = [
        (STANZA_TYPE_COUPLET,'Couplet (2 lines per verse)'),
        (STANZA_TYPE_QUATRAIN,'Quatrain (4 lines per verse)'),
        (STANZA_TYPE_FREE,'Free Verse (arbitrary line groups)'),
        (STANZA_TYPE_OTHER,'Other'),
    ]
    poem = models.ForeignKey(to=Poem, on_delete=models.CASCADE, related_name='lines')
    line_number = models.PositiveIntegerField(help_text='Order of line in entire poem.')
    stanza = models.PositiveIntegerField(default=1, help_text='Logical group or verse.')
    stanza_type = models.CharField(max_length=30, choices=STANZA_TYPE_CHOICES, default=STANZA_TYPE_COUPLET)
    text = models.TextField()
    transliteration = models.TextField(blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['line_number']

    def __str__(self):
        return f"Poem: {self.poem.title} | Line {self.line_number}"    


class Glossary(models.Model):
    poem = models.ForeignKey(to=Poem, on_delete=models.CASCADE, related_name='glossary')
    word = models.CharField(max_length=100)
    meaning = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.word} in {self.poem.title}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class PoemTag(models.Model):
    poem = models.ForeignKey(to=Poem, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('poem', 'tag')
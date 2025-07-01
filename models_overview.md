# 📘 Literature App – Model Documentation

This document outlines the data model structure for the **Takband Qandeel** project, a digital archive of Balochi poetry and literature, inspired by Ganjoor.net but tailored for the unique characteristics of Balochi literary tradition.

---

## 👤 Author

Represents a poet or scholar.

| Field                                   | Type         | Description             |
| --------------------------------------- | ------------ | ----------------------- |
| `name`                                  | CharField    | Full name of the author |
| `slug`                                  | SlugField    | Unique slug for URLs    |
| `birth_year` / `death_year`             | IntegerField | Optional life dates     |
| `biography`                             | TextField    | Short bio               |
| `image`                                 | ImageField   | Optional photo          |
| `datetime_created`, `datetime_modified` | DateTime     | Timestamps              |

---

## 🔁 AuthorAlias

Captures alternative names for an author (pen names, different spellings).

| Field    | Type                | Description                   |
| -------- | ------------------- | ----------------------------- |
| `author` | ForeignKey → Author | Related author                |
| `name`   | CharField           | The alias or alternative name |

---

## 📚 WorkGroup

A book, collection, or general anthology associated with an author (e.g., _میراث_).

| Field         | Type                | Description                |
| ------------- | ------------------- | -------------------------- |
| `author`      | ForeignKey → Author | Owner of the work group    |
| `title`       | CharField           | Title of the book or group |
| `slug`        | SlugField           | URL-friendly identifier    |
| `description` | TextField           | Optional description       |

---

## 🧩 Work

A categorized section within a `WorkGroup` (e.g., Epic poems, Ghazals).

| Field            | Type                   | Description                    |
| ---------------- | ---------------------- | ------------------------------ |
| `group`          | ForeignKey → WorkGroup | Belongs to a group             |
| `title`, `slug`  | Char/Slug              | Metadata                       |
| `genre`          | CharField              | Epic, Ghazal, Rubāʿī, etc.     |
| `dialect`, `era` | CharField              | Optional: Classical, Modern... |
| `notes`          | TextField              | Scholarly commentary           |
| `sources`        | TextField              | Research sources               |

---

## 📁 Section

Optional subdivisions within a `Work`, for large anthologies or thematically grouped poems.

| Field           | Type              | Description       |
| --------------- | ----------------- | ----------------- |
| `work`          | ForeignKey → Work | Belongs to a Work |
| `title`, `slug` | Char/Slug         | Section title/URL |
| `description`   | TextField         | Optional intro    |
| `order`         | PositiveInteger   | Sort order        |

---

## 📝 Poem

Represents a single poem.

| Field                                   | Type                    | Description                |
| --------------------------------------- | ----------------------- | -------------------------- |
| `work`                                  | ForeignKey → Work       | Source work                |
| `section`                               | FK → Section (optional) | Section it belongs to      |
| `title`, `slug`                         | Char/Slug               | Poem title/URL             |
| `intro`                                 | TextField               | Preface or intro text      |
| `meter`, `rhyme`                        | CharField               | Optional literary metadata |
| `date_written`                          | CharField               | Human-readable date        |
| `order_in_work`                         | PositiveInt             | Sort order within a work   |
| `raw_text`                              | TextField               | Optional pasted full text  |
| `is_published`                          | Boolean                 | Admin control flag         |
| `datetime_created`, `datetime_modified` | DateTime                | Timestamps                 |

---

## 📜 PoemLine

Each line (مصرع) of a poem.

| Field             | Type              | Description                   |
| ----------------- | ----------------- | ----------------------------- |
| `poem`            | ForeignKey → Poem | Associated poem               |
| `line_number`     | PositiveInt       | Global order in poem          |
| `stanza`          | PositiveInt       | Logical group or beyt number  |
| `stanza_type`     | CharField         | couplet, quatrain, free, etc. |
| `text`            | TextField         | Main poetic line              |
| `transliteration` | TextField         | Optional (e.g., Roman script) |
| `translation`     | TextField         | Optional English gloss        |

**Note**: Supports all poetic forms like Ghazal, Rubāʿī, Free Verse.

---

## 📘 Glossary

Difficult words explained within each poem.

| Field     | Type              | Description               |
| --------- | ----------------- | ------------------------- |
| `poem`    | ForeignKey → Poem | Related poem              |
| `word`    | CharField         | Term needing explanation  |
| `meaning` | TextField         | Meaning or interpretation |

---

## 🏷️ Tag

Reusable thematic labels (e.g. _Heroism_, _Mysticism_, _Exile_).

| Field         | Type      | Description          |
| ------------- | --------- | -------------------- |
| `name`        | CharField | Label name           |
| `description` | TextField | Optional explanation |

---

## 🧩 PoemTag

Intermediate many-to-many table between `Poem` and `Tag`.

| Field  | Type      | Description                  |
| ------ | --------- | ---------------------------- |
| `poem` | FK → Poem | Target poem                  |
| `tag`  | FK → Tag  | Target tag                   |
| `note` | TextField | Optional per-tag explanation |

> **Meta**: `unique_together = ('poem', 'tag')`

---

## 🔗 Model Relationships (Diagram-Like)

```plaintext
Author ─┬─< WorkGroup ─┬─< Work ─┬─< Section ─┬─< Poem ─┬─< PoemLine
        └─< AuthorAlias         │             └────< Glossary
                                └────────────< Tag >──── PoemTag
```

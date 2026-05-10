# Shakespeare Schema Reference Guide

## 1. Schema Summary
This schema contains the complete texts of Shakespeare's works, organized by play/poem with scenes, characters, and dialogue paragraphs.

---

## 2. Table Reference

### Table: `Shakespeare.works`
**Meaning:** Shakespeare's literary works (plays and poems)  
**Synonyms:** plays, titles, compositions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique work identifier | work_id |
| `Title` | VARCHAR | Short title of the work | title, name |
| `LongTitle` | VARCHAR | Full formal title | full_title, complete_title |
| `Date` | BIGINT | Year of composition/publication | year, written_date |
| `GenreType` | VARCHAR | Literary genre classification | genre, type |

**GenreType values:** `Comedy`, `History`, `Poem`, `Sonnet`, `Tragedy`

---

### Table: `Shakespeare.chapters`
**Meaning:** Acts and scenes within works  
**Synonyms:** scenes, acts, divisions, sections

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique chapter identifier | chapter_id |
| `Act` | BIGINT | Act number within the work | act_number |
| `Scene` | BIGINT | Scene number within the act | scene_number |
| `Description` | VARCHAR | Location or setting of the scene | setting, location |
| `work_id` | BIGINT | Foreign key to `works.id` | work_id |

---

### Table: `Shakespeare.characters`
**Meaning:** Named characters in Shakespeare's works  
**Synonyms:** actors, roles, personas, speakers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique character identifier | character_id |
| `CharName` | VARCHAR | Full character name | name, character_name |
| `Abbrev` | VARCHAR | Abbreviated form of character name | abbreviation, short_name |
| `Description` | VARCHAR | Character description or role notes | notes, role_description |

---

### Table: `Shakespeare.paragraphs`
**Meaning:** Individual dialogue lines and stage directions  
**Synonyms:** lines, speeches, utterances, text_blocks

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique paragraph identifier | paragraph_id |
| `ParagraphNum` | BIGINT | Sequential number within the chapter | line_number, sequence |
| `PlainText` | VARCHAR | The actual dialogue or stage direction text | text, content, speech |
| `character_id` | BIGINT | Foreign key to `characters.id` | character_id |
| `chapter_id` | BIGINT | Foreign key to `chapters.id` | chapter_id |

---

## 3. Join Paths

**Works to Chapters:**
```sql
Shakespeare.works w
JOIN Shakespeare.chapters c ON w.id = c.work_id
```

**Chapters to Paragraphs:**
```sql
Shakespeare.chapters c
JOIN Shakespeare.paragraphs p ON c.id = p.chapter_id
```

**Paragraphs to Characters:**
```sql
Shakespeare.paragraphs p
JOIN Shakespeare.characters ch ON p.character_id = ch.id
```

**Full chain (Works → Chapters → Paragraphs → Characters):**
```sql
Shakespeare.works w
JOIN Shakespeare.chapters c ON w.id = c.work_id
JOIN Shakespeare.paragraphs p ON c.id = p.chapter_id
JOIN Shakespeare.characters ch ON p.character_id = ch.id
```

---

## 4. Business Rules as SQL
*(No explicit business rules provided in schema documentation)*

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| play, work | `Shakespeare.works` |
| scene, chapter | `Shakespeare.chapters` |
| character, actor, role | `Shakespeare.characters` |
| line, dialogue, speech, text | `Shakespeare.paragraphs` |
| act number | `chapters.Act` |
| scene number | `chapters.Scene` |
| setting, location | `chapters.Description` |
| character name | `characters.CharName` |
| character abbreviation | `characters.Abbrev` |
| dialogue text | `paragraphs.PlainText` |
| genre | `works.GenreType` |
| publication year | `works.Date` |
| comedy | `WHERE works.GenreType = 'Comedy'` |
| tragedy | `WHERE works.GenreType = 'Tragedy'` |
| history | `WHERE works.GenreType = 'History'` |
| poem | `WHERE works.GenreType = 'Poem'` |
| sonnet | `WHERE works.GenreType = 'Sonnet'` |
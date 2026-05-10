# Shakespeare Schema Reference Guide

## Schema Summary
This schema contains the complete text of Shakespeare's works, organized by play/poem, with scenes, characters, and individual dialogue paragraphs.

---

## Join Paths

**Works → Chapters → Paragraphs:**
```sql
FROM Shakespeare.works w
JOIN Shakespeare.chapters c ON w.id = c.work_id
JOIN Shakespeare.paragraphs p ON c.id = p.chapter_id
```

**Paragraphs → Characters:**
```sql
FROM Shakespeare.paragraphs p
JOIN Shakespeare.characters ch ON p.character_id = ch.id
```

**Full text with metadata:**
```sql
FROM Shakespeare.paragraphs p
JOIN Shakespeare.chapters c ON p.chapter_id = c.id
JOIN Shakespeare.works w ON c.work_id = w.id
JOIN Shakespeare.characters ch ON p.character_id = ch.id
```

---

## Table Reference

### `Shakespeare.works`
Complete plays and poems.

| Column | Notes |
|--------|-------|
| `Title` | Short title (e.g., "Twelfth Night") |
| `LongTitle` | Full formal title |
| `Date` | Year of composition/publication |
| `GenreType` | Enum: `Comedy`, `History`, `Poem`, `Sonnet`, `Tragedy` |

### `Shakespeare.chapters`
Scenes within works, identified by Act and Scene number.

| Column | Notes |
|--------|-------|
| `Act` | Act number (1-indexed) |
| `Scene` | Scene number within act (1-indexed) |
| `Description` | Location/setting (e.g., "DUKE ORSINO's palace") |
| `work_id` | Foreign key to `Shakespeare.works.id` |

### `Shakespeare.paragraphs`
Individual dialogue lines and stage directions.

| Column | Notes |
|--------|-------|
| `ParagraphNum` | Sequential line number within chapter |
| `PlainText` | Dialogue or stage direction text |
| `character_id` | Foreign key to `Shakespeare.characters.id` |
| `chapter_id` | Foreign key to `Shakespeare.chapters.id` |

### `Shakespeare.characters`
Named speakers in the works.

| Column | Notes |
|--------|-------|
| `CharName` | Character name (e.g., "First Apparition", "DUKE ORSINO") |
| `Abbrev` | Abbreviated form (often same as `CharName`) |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| play, work | `Shakespeare.works` |
| scene, act | `Shakespeare.chapters` (use `Act` and `Scene` columns) |
| line, speech, dialogue | `Shakespeare.paragraphs.PlainText` |
| speaker, actor | `Shakespeare.characters.CharName` |
| genre | `Shakespeare.works.GenreType` |
| text content | `Shakespeare.paragraphs.PlainText` |
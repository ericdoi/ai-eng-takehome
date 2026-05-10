# VisualGenome Schema Reference Guide

## Schema Summary
Visual Genome is a structured dataset of images with annotated objects, their attributes, and spatial relationships between objects.

---

## Join Paths

**Objects with their class names:**
```sql
FROM VisualGenome.IMG_OBJ io
JOIN VisualGenome.OBJ_CLASSES oc ON io.OBJ_CLASS_ID = oc.OBJ_CLASS_ID
```

**Objects with their attributes:**
```sql
FROM VisualGenome.IMG_OBJ io
JOIN VisualGenome.IMG_OBJ_ATT ioa ON io.IMG_ID = ioa.IMG_ID AND io.OBJ_SAMPLE_ID = ioa.OBJ_SAMPLE_ID
JOIN VisualGenome.ATT_CLASSES ac ON ioa.ATT_CLASS_ID = ac.ATT_CLASS_ID
```

**Object relationships (subject → predicate → object):**
```sql
FROM VisualGenome.IMG_REL ir
JOIN VisualGenome.IMG_OBJ io1 ON ir.IMG_ID = io1.IMG_ID AND ir.OBJ1_SAMPLE_ID = io1.OBJ_SAMPLE_ID
JOIN VisualGenome.IMG_OBJ io2 ON ir.IMG_ID = io2.IMG_ID AND ir.OBJ2_SAMPLE_ID = io2.OBJ_SAMPLE_ID
JOIN VisualGenome.OBJ_CLASSES oc1 ON io1.OBJ_CLASS_ID = oc1.OBJ_CLASS_ID
JOIN VisualGenome.OBJ_CLASSES oc2 ON io2.OBJ_CLASS_ID = oc2.OBJ_CLASS_ID
JOIN VisualGenome.PRED_CLASSES pc ON ir.PRED_CLASS_ID = pc.PRED_CLASS_ID
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| object bounding box | `X, Y, W, H` in `VisualGenome.IMG_OBJ` |
| object location | `X, Y` (top-left corner); `W, H` (width, height) |
| spatial relationship | `VisualGenome.IMG_REL` with `PRED_CLASS` |
| object property / quality | `VisualGenome.ATT_CLASSES` |
| object type / category | `VisualGenome.OBJ_CLASSES` |

---

## Table Reference

### `VisualGenome.ATT_CLASSES`
Attribute/property class catalog. Maps attribute IDs to human-readable attribute names.

| Column | Notes |
|--------|-------|
| `ATT_CLASS_ID` | Primary key; used in `IMG_OBJ_ATT.ATT_CLASS_ID` |
| `ATT_CLASS` | Attribute name (e.g., "building s", "indoors", "cluttered", "park", "two story") |

---

### `VisualGenome.IMG_OBJ`
Detected objects in images with bounding box coordinates.

| Column | Notes |
|--------|-------|
| `IMG_ID` | Image identifier; links to `IMG_OBJ_ATT`, `IMG_REL` |
| `OBJ_SAMPLE_ID` | Object instance ID within image; unique per (IMG_ID, OBJ_SAMPLE_ID) pair |
| `OBJ_CLASS_ID` | Foreign key to `OBJ_CLASSES.OBJ_CLASS_ID` |
| `X, Y` | Top-left corner of bounding box (pixels) |
| `W, H` | Width and height of bounding box (pixels) |

---

### `VisualGenome.IMG_OBJ_ATT`
Attributes assigned to specific objects in images.

| Column | Notes |
|--------|-------|
| `IMG_ID` | Image identifier |
| `OBJ_SAMPLE_ID` | Object instance ID; links to `IMG_OBJ.OBJ_SAMPLE_ID` |
| `ATT_CLASS_ID` | Foreign key to `ATT_CLASSES.ATT_CLASS_ID` |

---

### `VisualGenome.IMG_REL`
Spatial and semantic relationships between pairs of objects.

| Column | Notes |
|--------|-------|
| `IMG_ID` | Image identifier |
| `OBJ1_SAMPLE_ID` | Subject object; links to `IMG_OBJ.OBJ_SAMPLE_ID` |
| `OBJ2_SAMPLE_ID` | Object (target) of relationship; links to `IMG_OBJ.OBJ_SAMPLE_ID` |
| `PRED_CLASS_ID` | Foreign key to `PRED_CLASSES.PRED_CLASS_ID` |

---

### `VisualGenome.OBJ_CLASSES`
Object class catalog. Maps object IDs to human-readable class names.

| Column | Notes |
|--------|-------|
| `OBJ_CLASS_ID` | Primary key; used in `IMG_OBJ.OBJ_CLASS_ID` |
| `OBJ_CLASS` | Object class name (e.g., "awning", "goggles", "dot", "kitchen", "feathers") |

---

### `VisualGenome.PRED_CLASSES`
Predicate/relationship class catalog. Maps relationship IDs to human-readable relationship names.

| Column | Notes |
|--------|-------|
| `PRED_CLASS_ID` | Primary key; used in `IMG_REL.PRED_CLASS_ID` |
| `PRED_CLASS` | Relationship name (e.g., "playing on", "looking a", "to left of", "beyond", "covers") |
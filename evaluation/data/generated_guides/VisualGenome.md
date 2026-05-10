# VisualGenome Schema Reference Guide

## Schema Summary
The VisualGenome schema contains visual scene data with objects, their attributes, and relationships between objects in images.

---

## Table Reference

### VisualGenome.ATT_CLASSES
**Meaning**: Attribute class definitions (synonyms: attribute types, attribute labels)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| ATT_CLASS_ID | BIGINT | Unique attribute identifier | attribute ID, attr ID |
| ATT_CLASS | VARCHAR | Attribute name/label | attribute name, attribute type |

**Notable values**: "building s", "indoors", "cluttered", "park", "two story"

---

### VisualGenome.IMG_OBJ
**Meaning**: Objects detected in images with bounding box coordinates (synonyms: image objects, detected objects, object instances)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| IMG_ID | BIGINT | Image identifier | image ID |
| OBJ_SAMPLE_ID | BIGINT | Unique object instance identifier within image | object ID, object sample ID, instance ID |
| OBJ_CLASS_ID | BIGINT | Reference to object class | object class ID, class ID |
| X | BIGINT | Bounding box left coordinate (pixels) | x coordinate, left |
| Y | BIGINT | Bounding box top coordinate (pixels) | y coordinate, top |
| W | BIGINT | Bounding box width (pixels) | width |
| H | BIGINT | Bounding box height (pixels) | height |

---

### VisualGenome.IMG_OBJ_ATT
**Meaning**: Attributes assigned to specific objects in images (synonyms: object attributes, attribute assignments)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| IMG_ID | BIGINT | Image identifier | image ID |
| ATT_CLASS_ID | BIGINT | Reference to attribute class | attribute ID, attribute class ID |
| OBJ_SAMPLE_ID | BIGINT | Reference to object instance | object ID, object sample ID |

---

### VisualGenome.IMG_REL
**Meaning**: Relationships/predicates between pairs of objects in images (synonyms: object relationships, predicates, spatial relationships)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| IMG_ID | BIGINT | Image identifier | image ID |
| PRED_CLASS_ID | BIGINT | Reference to predicate/relationship class | predicate ID, relationship ID, pred ID |
| OBJ1_SAMPLE_ID | BIGINT | First object in relationship | subject object, object 1 |
| OBJ2_SAMPLE_ID | BIGINT | Second object in relationship | object object, object 2 |

---

### VisualGenome.OBJ_CLASSES
**Meaning**: Object class definitions (synonyms: object types, object labels, object categories)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| OBJ_CLASS_ID | BIGINT | Unique object class identifier | object class ID, class ID |
| OBJ_CLASS | VARCHAR | Object class name/label | object name, object type, class name |

**Notable values**: "awning", "goggles", "dot", "kitchen", "feathers"

---

### VisualGenome.PRED_CLASSES
**Meaning**: Predicate/relationship class definitions (synonyms: relationship types, relationship labels, predicate types)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| PRED_CLASS_ID | BIGINT | Unique predicate identifier | predicate ID, relationship ID, pred ID |
| PRED_CLASS | VARCHAR | Predicate name/label | predicate name, relationship type, relationship name |

**Notable values**: "playing on", "looking a", "to left of", "beyond", "covers"

---

## Join Paths

**Objects to Object Classes**:
```sql
IMG_OBJ.OBJ_CLASS_ID = OBJ_CLASSES.OBJ_CLASS_ID
```

**Objects to Attributes**:
```sql
IMG_OBJ.IMG_ID = IMG_OBJ_ATT.IMG_ID 
AND IMG_OBJ.OBJ_SAMPLE_ID = IMG_OBJ_ATT.OBJ_SAMPLE_ID
```

**Attributes to Attribute Classes**:
```sql
IMG_OBJ_ATT.ATT_CLASS_ID = ATT_CLASSES.ATT_CLASS_ID
```

**Relationships to Predicate Classes**:
```sql
IMG_REL.PRED_CLASS_ID = PRED_CLASSES.PRED_CLASS_ID
```

**Relationships to Objects (subject)**:
```sql
IMG_REL.IMG_ID = IMG_OBJ.IMG_ID 
AND IMG_REL.OBJ1_SAMPLE_ID = IMG_OBJ.OBJ_SAMPLE_ID
```

**Relationships to Objects (object)**:
```sql
IMG_REL.IMG_ID = IMG_OBJ.IMG_ID 
AND IMG_REL.OBJ2_SAMPLE_ID = IMG_OBJ.OBJ_SAMPLE_ID
```

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| object type | `OBJ_CLASSES.OBJ_CLASS` |
| object class | `OBJ_CLASSES` table |
| attribute type | `ATT_CLASSES.ATT_CLASS` |
| attribute class | `ATT_CLASSES` table |
| relationship type | `PRED_CLASSES.PRED_CLASS` |
| predicate class | `PRED_CLASSES` table |
| bounding box | `IMG_OBJ.X, IMG_OBJ.Y, IMG_OBJ.W, IMG_OBJ.H` |
| object location | `IMG_OBJ.X, IMG_OBJ.Y` |
| object size | `IMG_OBJ.W, IMG_OBJ.H` |
| spatial relationship | `IMG_REL` with `PRED_CLASSES` |
| object instance | `IMG_OBJ.OBJ_SAMPLE_ID` |
| image | `IMG_ID` |
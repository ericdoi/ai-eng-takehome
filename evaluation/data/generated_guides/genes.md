# Genes Schema Reference Guide

## Schema Summary
This schema contains yeast gene annotations, including cellular localization, functional classification, essentiality status, and pairwise gene interactions (genetic and physical).

---

## Join Paths

**Genes with their classification:**
```sql
FROM genes.Genes g
LEFT JOIN genes.Classification c ON g.GeneID = c.GeneID
```

**Gene interactions with both gene details:**
```sql
FROM genes.Interactions i
JOIN genes.Genes g1 ON i.GeneID1 = g1.GeneID
JOIN genes.Genes g2 ON i.GeneID2 = g2.GeneID
```

**Genes by localization (from Genes table):**
```sql
FROM genes.Genes g
WHERE g.Localization = 'cytoplasm'
```

---

## Business Rules as SQL

- **Essential genes only:** `WHERE Essential = 'Essential'`
- **Non-essential genes:** `WHERE Essential = 'Non-Essential'`
- **Ambiguous essentiality:** `WHERE Essential = 'Ambiguous-Essential'`
- **Strong expression correlation:** `WHERE Expression_Corr >= 0.9`
- **Genetic interactions only:** `WHERE Type = 'Genetic'`
- **Physical interactions only:** `WHERE Type = 'Physical'`
- **Combined genetic-physical interactions:** `WHERE Type = 'Genetic-Physical'`

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| subcellular location | `Localization` |
| gene role | `Function` |
| gene class | `Class` |
| protein complex | `Complex` |
| mutation effect | `Phenotype` |
| protein motif | `Motif` |
| gene pair interaction | `genes.Interactions` |
| interaction strength | `Expression_Corr` |

---

## Table Reference

### `genes.Genes`
**Meaning:** Primary gene annotation table with functional and localization metadata.

| Column | Notes |
|--------|-------|
| `GeneID` | Unique gene identifier (e.g., `G234064`) |
| `Essential` | Enum: `Essential`, `Non-Essential`, `Ambiguous-Essential`, `?` |
| `Class` | Functional protein class (e.g., `GTP/GDP-exchange factors (GEFs)`, `ATPases`) |
| `Complex` | Protein complex membership (e.g., `Translation complexes`) |
| `Phenotype` | Observable mutation effect. Enum: `?`, `Auxotrophies`, `Cell cycle defects`, `Mating and sporulation defects`, `Nucleic acid metabolism defects`, `Sensitivity to antibiotics`, `Stress response defects`, `Unknown`, others |
| `Motif` | Protein sequence motif identifier (e.g., `PS00824`) |
| `Chromosome` | Chromosomal location (integer) |
| `Function` | Functional category. Enum: `CELL GROWTH`, `CELL DIVISION AND DNA SYNTHESIS`, `CELLULAR COMMUNICATION/SIGNAL TRANSDUCTION`, `CELLULAR ORGANIZATION (proteins are localized to the corresponding organelle)`, `CELLULAR TRANSPORT AND TRANSPORTMECHANISMS`, `ENERGY`, `METABOLISM`, `PROTEIN SYNTHESIS`, `TRANSCRIPTION`, others |
| `Localization` | Subcellular compartment. Enum: `cytoplasm`, `nucleus`, `mitochondria`, `ER`, `golgi`, `plasma membrane`, `cell wall`, `cytoskeleton`, `endosome`, `extracellular`, `integral membrane`, `lipid particles`, `peroxisome`, `transport vesicles`, `vacuole` |

### `genes.Classification`
**Meaning:** Localization assignments for genes (may differ from `genes.Genes.Localization` due to different annotation sources).

| Column | Notes |
|--------|-------|
| `GeneID` | Foreign key to `genes.Genes.GeneID` |
| `Localization` | Subcellular compartment (same enum as `genes.Genes.Localization`) |

### `genes.Interactions`
**Meaning:** Pairwise gene interactions with interaction type and expression correlation.

| Column | Notes |
|--------|-------|
| `GeneID1` | First gene in interaction pair |
| `GeneID2` | Second gene in interaction pair |
| `Type` | Interaction category. Enum: `Genetic`, `Physical`, `Genetic-Physical` |
| `Expression_Corr` | Pearson correlation of expression profiles (range: -1 to 1; higher = stronger co-expression) |
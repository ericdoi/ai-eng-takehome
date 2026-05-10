# SQL Reference Guide: genes Schema

## 1. Schema Summary

The `genes` schema contains genomic data for yeast genes, including their functional classifications, cellular localizations, phenotypic properties, and interaction networks.

---

## 2. Table Reference

### Table: `genes.Genes`
**Meaning:** Core gene records with functional and phenotypic annotations.  
**Synonyms:** Gene catalog, gene registry

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `GeneID` | VARCHAR | Unique gene identifier | Gene ID, gene name |
| `Essential` | VARCHAR | Gene essentiality classification | Essentiality status |
| `Class` | VARCHAR | Functional protein class | Protein class, gene class |
| `Complex` | VARCHAR | Protein complex membership | Complex name |
| `Phenotype` | VARCHAR | Observable phenotypic effect when mutated | Mutant phenotype, phenotypic class |
| `Motif` | VARCHAR | Protein sequence motif identifier | Motif ID, sequence motif |
| `Chromosome` | BIGINT | Chromosome number where gene is located | Chromosomal location |
| `Function` | VARCHAR | Broad functional category | Gene function, functional role |
| `Localization` | VARCHAR | Cellular compartment where protein localizes | Protein localization, cellular location |

**Notable Enumeration Values:**
- `Essential`: `Essential`, `Non-Essential`, `Ambiguous-Essential`, `?`
- `Phenotype`: `Auxotrophies`, `Carbohydrate and lipid biosynthesis defects`, `Cell cycle defects`, `Cell morphology and organelle mutants`, `Conditional phenotypes`, `Mating and sporulation defects`, `Nucleic acid metabolism defects`, `Sensitivity to aminoacid analogs and other drugs`, `Sensitivity to antibiotics`, `Sensitivity to immunosuppressants`, `Stress response defects`, `Unknown`, `?`
- `Function`: `CELL GROWTH`, `CELL DIVISION AND DNA SYNTHESIS`, `CELL RESCUE, DEFENSE, CELL DEATH AND AGEING`, `CELLULAR BIOGENESIS (proteins are not localized to the corresponding organelle)`, `CELLULAR COMMUNICATION/SIGNAL TRANSDUCTION`, `CELLULAR ORGANIZATION (proteins are localized to the corresponding organelle)`, `CELLULAR TRANSPORT AND TRANSPORTMECHANISMS`, `ENERGY`, `IONIC HOMEOSTASIS`, `METABOLISM`, `PROTEIN DESTINATION`, `PROTEIN SYNTHESIS`, `TRANSCRIPTION`, `TRANSPORT FACILITATION`
- `Localization`: `ER`, `cell wall`, `cytoplasm`, `cytoskeleton`, `endosome`, `extracellular`, `golgi`, `integral membrane`, `lipid particles`, `mitochondria`, `nucleus`, `peroxisome`, `plasma membrane`, `transport vesicles`, `vacuole`

---

### Table: `genes.Classification`
**Meaning:** Gene-to-cellular-localization mapping (denormalized from Genes table).  
**Synonyms:** Gene localization, localization index

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `GeneID` | VARCHAR | Unique gene identifier | Gene ID, gene name |
| `Localization` | VARCHAR | Cellular compartment where protein localizes | Protein localization, cellular location |

**Notable Enumeration Values:**
- `Localization`: `ER`, `cell wall`, `cytoplasm`, `cytoskeleton`, `endosome`, `extracellular`, `golgi`, `integral membrane`, `lipid particles`, `mitochondria`, `nucleus`, `peroxisome`, `plasma membrane`, `transport vesicles`, `vacuole`

---

### Table: `genes.Interactions`
**Meaning:** Pairwise gene interactions with interaction type and expression correlation.  
**Synonyms:** Gene interactions, interaction network, gene pairs

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `GeneID1` | VARCHAR | First gene in interaction pair | Gene 1, source gene |
| `GeneID2` | VARCHAR | Second gene in interaction pair | Gene 2, target gene |
| `Type` | VARCHAR | Classification of interaction mechanism | Interaction type, interaction class |
| `Expression_Corr` | DOUBLE | Pearson correlation of gene expression levels | Expression correlation, correlation coefficient |

**Notable Enumeration Values:**
- `Type`: `Genetic`, `Physical`, `Genetic-Physical`

---

## 3. Join Paths

**Genes to Classification (by GeneID):**
```sql
genes.Genes g
INNER JOIN genes.Classification c ON g.GeneID = c.GeneID
```

**Interactions to Genes (first gene):**
```sql
genes.Interactions i
INNER JOIN genes.Genes g1 ON i.GeneID1 = g1.GeneID
```

**Interactions to Genes (second gene):**
```sql
genes.Interactions i
INNER JOIN genes.Genes g2 ON i.GeneID2 = g2.GeneID
```

**Interactions to Genes (both genes):**
```sql
genes.Interactions i
INNER JOIN genes.Genes g1 ON i.GeneID1 = g1.GeneID
INNER JOIN genes.Genes g2 ON i.GeneID2 = g2.GeneID
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Apply standard data integrity assumptions:
- `GeneID` values are non-null and unique within `Genes` table
- `Expression_Corr` values range from -1.0 to 1.0
- `Chromosome` values are positive integers
- Localization values must match enumerated set

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Essential genes | `WHERE genes.Genes.Essential = 'Essential'` |
| Non-essential genes | `WHERE genes.Genes.Essential = 'Non-Essential'` |
| Gene localization | `genes.Genes.Localization` or `genes.Classification.Localization` |
| Protein function | `genes.Genes.Function` |
| Gene interactions | `genes.Interactions` table |
| Genetic interaction | `WHERE genes.Interactions.Type = 'Genetic'` |
| Physical interaction | `WHERE genes.Interactions.Type = 'Physical'` |
| Combined interaction | `WHERE genes.Interactions.Type = 'Genetic-Physical'` |
| Expression correlation | `genes.Interactions.Expression_Corr` |
| Highly correlated | `WHERE genes.Interactions.Expression_Corr > 0.8` |
| Protein complex | `genes.Genes.Complex` |
| Phenotypic class | `genes.Genes.Phenotype` |
| Chromosomal location | `genes.Genes.Chromosome` |
| Sequence motif | `genes.Genes.Motif` |
| Cytoplasmic genes | `WHERE genes.Genes.Localization = 'cytoplasm'` |
| Nuclear genes | `WHERE genes.Genes.Localization = 'nucleus'` |
| Mitochondrial genes | `WHERE genes.Genes.Localization = 'mitochondria'` |
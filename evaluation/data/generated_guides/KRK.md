# KRK Schema Reference Guide

## Schema Summary
This schema contains chess endgame positions with King-Rook-King (KRK) configurations, classifying each position as legal or illegal.

## Join Paths
No joins applicable—single table schema.

## Business Rules as SQL

- **Legal position**: `WHERE KRK.krk.class = 'legal'`
- **Illegal position**: `WHERE KRK.krk.class = 'illegal'`

## Synonym Glossary

| Term | Schema Identifier |
|------|-------------------|
| white king position | `white_king_file`, `white_king_rank` |
| white rook position | `white_rook_file`, `white_rook_rank` |
| black king position | `black_king_file`, `black_king_rank` |
| position validity | `class` |

## Table Reference

### `KRK.krk`
Chess endgame positions in King-Rook-King format.

**Columns:**

| Column | Type | Notes |
|--------|------|-------|
| `white_king_file` | BIGINT | File (column) coordinate of white king; 0–7 |
| `white_king_rank` | BIGINT | Rank (row) coordinate of white king; 0–7 |
| `white_rook_file` | BIGINT | File coordinate of white rook; 0–7 |
| `white_rook_rank` | BIGINT | Rank coordinate of white rook; 0–7 |
| `black_king_file` | BIGINT | File coordinate of black king; 0–7 |
| `black_king_rank` | BIGINT | Rank coordinate of black king; 0–7 |
| `class` | VARCHAR | Position legality classification. Values: `legal`, `illegal` |
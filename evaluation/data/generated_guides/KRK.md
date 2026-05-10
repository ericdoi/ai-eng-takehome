# KRK Schema Reference Guide

## Schema Summary
The KRK schema contains a single table documenting chess positions in King-Rook-King (KRK) endgames, classifying each position as legal or illegal based on chess rules.

---

## Table Reference

### KRK.krk
**Meaning:** King-Rook-King chess endgame positions with legality classification.  
**Synonyms:** KRK positions, endgame states, chess configurations.

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `id` | BIGINT | Unique position identifier | position_id, record_id |
| `white_king_file` | BIGINT | White king's file (column) on chessboard (0–7) | white_king_column, wk_file |
| `white_king_rank` | BIGINT | White king's rank (row) on chessboard (0–7) | white_king_row, wk_rank |
| `white_rook_file` | BIGINT | White rook's file (column) on chessboard (0–7) | white_rook_column, wr_file |
| `white_rook_rank` | BIGINT | White rook's rank (row) on chessboard (0–7) | white_rook_row, wr_rank |
| `black_king_file` | BIGINT | Black king's file (column) on chessboard (0–7) | black_king_column, bk_file |
| `black_king_rank` | BIGINT | Black king's rank (row) on chessboard (0–7) | black_king_row, bk_rank |
| `class` | VARCHAR | Legality classification of the position | legality, position_class, validity |

**Enumeration values for `class`:**
- `legal` — position is valid under chess rules
- `illegal` — position violates chess rules

---

## Join Paths
No joins applicable. Single table schema.

---

## Business Rules as SQL

| Rule | SQL Condition |
|---|---|
| Position is legal | `WHERE class = 'legal'` |
| Position is illegal | `WHERE class = 'illegal'` |
| White king on specific square (file, rank) | `WHERE white_king_file = [file] AND white_king_rank = [rank]` |
| Black king on specific square (file, rank) | `WHERE black_king_file = [file] AND black_king_rank = [rank]` |
| White rook on specific square (file, rank) | `WHERE white_rook_file = [file] AND white_rook_rank = [rank]` |
| Kings adjacent (distance = 1) | `WHERE ABS(white_king_file - black_king_file) <= 1 AND ABS(white_king_rank - black_king_rank) <= 1` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|---|---|
| legal position | `WHERE class = 'legal'` |
| illegal position | `WHERE class = 'illegal'` |
| white king location | `white_king_file`, `white_king_rank` |
| black king location | `black_king_file`, `black_king_rank` |
| white rook location | `white_rook_file`, `white_rook_rank` |
| board coordinate | `file` (0–7), `rank` (0–7) |
| position count | `COUNT(*)` from `KRK.krk` |
| legal positions | `COUNT(*) WHERE class = 'legal'` |
| illegal positions | `COUNT(*) WHERE class = 'illegal'` |
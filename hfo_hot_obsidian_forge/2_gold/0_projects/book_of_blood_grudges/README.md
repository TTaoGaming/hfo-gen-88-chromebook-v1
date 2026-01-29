# Medallion: Gold | Mutation: 0% | HIVE: V

# Book of Blood Grudges (Gen88 v4) — Gold Project

This project is the **machine-checkable** representation of the Book of Blood Grudges.

- Canonical narrative source (cold, hardened): `hfo_cold_obsidian/BOOK_OF_BLOOD_GRUDGES.md`
- This project provides:
  - a structured YAML representation for automation
  - a strict Zod contract for validation
  - a validator script that fails closed

## Validate

- `npm run test:contracts`
- `npx tsx scripts/hfo_validate_book_of_blood_grudges.ts --file hfo_hot_obsidian_forge/2_gold/0_projects/book_of_blood_grudges/book_of_blood_grudges.gen88_v4.v1.yaml`

## Notes

- This is **incomplete by definition**. It is an append-only structure.
- Gold rules: no “completion” claims, only verifiable entries with sources.

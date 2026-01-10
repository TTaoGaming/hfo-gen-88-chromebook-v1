# Code Style & Conventions
- **Medallion Refinement Flow**: 1-way path: Hot Bronze -> Cold Bronze -> Hot Silver -> Cold Silver -> Gold. Promotion requires passing property tests and contract validation.
- **Zod 6.0 Contracts**: Used for all cross-port communication.
- **Stigmergy Signals**: `.jsonl` blackboards for indirect coordination.
- **Immutable Provenance**: Headers on all files including Medallion layer and mutation score.
- **Goldilocks Zone**: Prioritize mutation scoring (Stryker) 88%-98%. Reject < 80%.

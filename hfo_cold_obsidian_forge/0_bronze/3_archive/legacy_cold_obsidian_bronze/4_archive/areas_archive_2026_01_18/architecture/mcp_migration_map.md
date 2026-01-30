# Mapping: HFO Simple Memory -> @modelcontextprotocol/server-memory

## Source: SQLite (hfo_memory_sqlite.db)
- **Table: entities**
  - `name` -> `name` (Entity ID)
  - `type` -> `entityType`
  - `description` + `metadata` -> `observations` (Extract facts from JSON)
- **Table: relations**
  - `from_id` -> `from`
  - `to_id` -> `to`
  - `relation_type` -> `relationType`

## Performance Targets (1.5GB RAM Limit)
- Use standard `npx` execution for transient load.
- Avoid large memory knowledge graphs; periodic pruning required.
- MotherDuck (Official) or standard SQL for the 6.2GB DuckDB substrate to avoid full file locking.

## Medallion: Bronze | Mutation: 0% | HIVE: E

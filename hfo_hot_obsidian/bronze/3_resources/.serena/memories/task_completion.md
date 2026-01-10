# Task Completion Workflow
1. **Validation**: Check against Zod 6.0 contracts.
2. **Testing**: Run `stryker_boot.sh` to ensure mutation score is in the Goldilocks zone (88%-98%).
3. **Blackboard Logging**: Log results/receipts in `hot_obsidian_blackboard.jsonl`.
4. **Promotion**: Move from `hot_bronze` to `cold_bronze` once frozen and verified.
5. **Governance**: Ensure no "Root Pollution" (files outside allowed areas).

# Backup Created: 2025-10-23 23:34:20

## Backup Information
- **Timestamp**: 20251023_233420
- **Reason**: pre_migration
- **Files Backed Up**: 7
- **Total Size**: 1009.82 KB

## Files Included

- `users_data.json` - 981.36 KB - SHA256: 1e1ab9dbdf46ad17...
- `game_master_queue.json` - 6.37 KB - SHA256: e73c044609130f89...
- `leadership_profiles.json` - 10.00 KB - SHA256: 96f7927476a056eb...
- `user_status.json` - 2.07 KB - SHA256: 58fdcb27cccde2ea...
- `config/api_limits.json` - 673.00 B - SHA256: b176ae18a6fc1e45...
- `config/business_games_active_mode.json` - 103.00 B - SHA256: f09c993c2694d0bf...
- `config/business_games_settings.py` - 9.26 KB - SHA256: 778e7b4d5e07d1af...

## Restore Instructions

To restore from this backup:

```bash
python scripts/migration/restore_backup.py "backup_20251023_233420_pre_migration"
```

Or manually copy files back to the main directory.

## Verification

To verify backup integrity:

```bash
python scripts/migration/verify_backup.py "backup_20251023_233420_pre_migration"
```

"""
Backup System - Full JSON Backup
Tworzy pełny backup wszystkich plików JSON przed migracją
"""

import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import sys
import os

# Dodaj główny katalog do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def calculate_checksum(file_path):
    """Oblicza SHA256 checksum pliku"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_size(file_path):
    """Zwraca rozmiar pliku w bajtach"""
    return os.path.getsize(file_path)


def format_size(size_bytes):
    """Formatuje rozmiar do czytelnej postaci"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def create_full_backup(reason="manual"):
    """
    Tworzy pełny backup wszystkich plików JSON
    
    Args:
        reason: Powód utworzenia backupu (np. "pre_migration", "manual", "scheduled")
    
    Returns:
        str: Ścieżka do katalogu z backupem
    """
    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Katalog backupu
    backup_dir = Path(__file__).parent.parent.parent / "backups" / f"backup_{timestamp}_{reason}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("🔒 FULL BACKUP SYSTEM")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Reason: {reason}")
    print(f"Backup directory: {backup_dir}")
    print("="*60)
    print()
    
    # Pliki do backupu
    base_path = Path(__file__).parent.parent.parent
    files_to_backup = [
        "users_data.json",
        "game_master_queue.json",
        "leadership_profiles.json",
        "user_status.json",
        "config/api_limits.json",
        "config/business_games_active_mode.json",
        "config/business_games_settings.py",
    ]
    
    # Manifest backupu
    backup_manifest = {
        "timestamp": timestamp,
        "datetime": datetime.now().isoformat(),
        "reason": reason,
        "files": [],
        "checksums": {},
        "sizes": {},
        "total_size": 0,
        "errors": []
    }
    
    total_size = 0
    files_backed_up = 0
    
    # Backup każdego pliku
    for file_rel in files_to_backup:
        file_path = base_path / file_rel
        
        if file_path.exists():
            try:
                # Stwórz strukturę katalogów w backupie
                dest_file = backup_dir / file_rel
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Kopiuj plik
                shutil.copy2(file_path, dest_file)
                
                # Oblicz checksum
                checksum = calculate_checksum(file_path)
                file_size = get_file_size(file_path)
                
                # Zapisz metadane
                backup_manifest["files"].append(file_rel)
                backup_manifest["checksums"][file_rel] = checksum
                backup_manifest["sizes"][file_rel] = file_size
                total_size += file_size
                
                files_backed_up += 1
                
                print(f"✅ Backed up: {file_rel:<50} {format_size(file_size):>10}")
                
            except Exception as e:
                error_msg = f"Failed to backup {file_rel}: {str(e)}"
                print(f"❌ {error_msg}")
                backup_manifest["errors"].append({
                    "file": file_rel,
                    "error": str(e)
                })
        else:
            print(f"⚠️  Not found: {file_rel:<50} (skipped)")
            backup_manifest["errors"].append({
                "file": file_rel,
                "error": "File not found"
            })
    
    backup_manifest["total_size"] = total_size
    backup_manifest["files_backed_up"] = files_backed_up
    
    # Zapisz manifest
    manifest_path = backup_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(backup_manifest, f, indent=2, ensure_ascii=False)
    
    # Stwórz README
    readme_content = f"""# Backup Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Backup Information
- **Timestamp**: {timestamp}
- **Reason**: {reason}
- **Files Backed Up**: {files_backed_up}
- **Total Size**: {format_size(total_size)}

## Files Included
"""
    
    for file_rel in backup_manifest["files"]:
        size = backup_manifest["sizes"].get(file_rel, 0)
        checksum = backup_manifest["checksums"].get(file_rel, "N/A")[:16]
        readme_content += f"\n- `{file_rel}` - {format_size(size)} - SHA256: {checksum}..."
    
    if backup_manifest["errors"]:
        readme_content += "\n\n## Errors/Warnings\n"
        for error in backup_manifest["errors"]:
            readme_content += f"\n- {error['file']}: {error['error']}"
    
    readme_content += f"""

## Restore Instructions

To restore from this backup:

```bash
python scripts/migration/restore_backup.py "{backup_dir.name}"
```

Or manually copy files back to the main directory.

## Verification

To verify backup integrity:

```bash
python scripts/migration/verify_backup.py "{backup_dir.name}"
```
"""
    
    readme_path = backup_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Podsumowanie
    print()
    print("="*60)
    print("📊 BACKUP SUMMARY")
    print("="*60)
    print(f"Total files backed up: {files_backed_up}")
    print(f"Total size: {format_size(total_size)}")
    print(f"Backup location: {backup_dir}")
    print(f"Manifest: {manifest_path}")
    
    if backup_manifest["errors"]:
        print(f"\n⚠️  Warnings/Errors: {len(backup_manifest['errors'])}")
        for error in backup_manifest["errors"]:
            print(f"  - {error['file']}: {error['error']}")
    
    print("\n✅ Backup completed successfully!")
    print("="*60)
    
    return str(backup_dir)


def list_backups():
    """Wyświetla listę dostępnych backupów"""
    backup_base = Path(__file__).parent.parent.parent / "backups"
    
    if not backup_base.exists():
        print("No backups found.")
        return
    
    backups = sorted(backup_base.glob("backup_*"), reverse=True)
    
    if not backups:
        print("No backups found.")
        return
    
    print("="*80)
    print("📦 AVAILABLE BACKUPS")
    print("="*80)
    print(f"{'#':<4} {'Timestamp':<20} {'Reason':<15} {'Files':<8} {'Size':<12}")
    print("-"*80)
    
    for idx, backup_dir in enumerate(backups, 1):
        manifest_path = backup_dir / "manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            timestamp = manifest.get('datetime', 'Unknown')[:19]
            reason = manifest.get('reason', 'Unknown')
            files_count = manifest.get('files_backed_up', 0)
            total_size = manifest.get('total_size', 0)
            
            print(f"{idx:<4} {timestamp:<20} {reason:<15} {files_count:<8} {format_size(total_size):<12}")
        else:
            print(f"{idx:<4} {backup_dir.name:<20} {'Unknown':<15} {'N/A':<8} {'N/A':<12}")
    
    print("="*80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create full backup of JSON files")
    parser.add_argument("--reason", default="manual", help="Reason for backup (e.g., pre_migration)")
    parser.add_argument("--list", action="store_true", help="List all available backups")
    
    args = parser.parse_args()
    
    if args.list:
        list_backups()
    else:
        try:
            backup_path = create_full_backup(reason=args.reason)
            print(f"\n💾 Backup saved to: {backup_path}")
        except Exception as e:
            print(f"\n❌ Backup failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

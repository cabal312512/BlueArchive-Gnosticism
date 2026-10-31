"""Restore the published compressed database without replacing an existing database."""
from pathlib import Path
import gzip
import hashlib
import json
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    folder = ROOT / '02_corpus'
    target = folder / 'story_index.db'
    package = folder / 'story_index.db.gz'
    metadata = json.loads((folder / 'database_package.json').read_text(encoding='utf-8'))
    if target.exists():
        print('story_index.db already exists; kept unchanged.')
        return
    expected = metadata['database_sha256']
    digest = hashlib.sha256()
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=folder, prefix='restore-', suffix='.tmp', delete=False) as output:
            temp_path = Path(output.name)
            with gzip.open(package, 'rb') as source:
                while chunk := source.read(1024 * 1024):
                    digest.update(chunk)
                    output.write(chunk)
        if digest.hexdigest() != expected:
            raise ValueError('Database checksum mismatch; original database was not replaced.')
        # Windows rename refuses to replace an existing destination.
        if target.exists():
            raise FileExistsError('A database appeared during restoration; kept unchanged.')
        os.rename(temp_path, target)
        temp_path = None
        print('Restored 02_corpus/story_index.db; SHA256 verified.')
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

if __name__ == '__main__':
    main()

from app.ingestion.pr_loader import get_pr_diff
from app.ingestion.diff_parser import parse_diff

diff = get_pr_diff("psf", "requests-html", pr_number=608)
parsed = parse_diff(diff)

print(f"Files changed: {len(parsed)}")
for file_diff in parsed:
    print(f"\n--- {file_diff['file']} ---")
    print(f"Lines added: {len(file_diff['added'])}")
    print(f"Lines removed: {len(file_diff['removed'])}")
    print(f"Sample added: {file_diff['added'][:2]}")
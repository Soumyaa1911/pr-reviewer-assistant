import re


def parse_diff(diff_text: str) -> list[dict]:
    """Parse a raw git diff into structured chunks per file."""
    file_diffs = []
    current_file = None
    current_changes = []

    for line in diff_text.splitlines():
        # Detect new file in diff
        if line.startswith("diff --git"):
            if current_file:
                file_diffs.append({
                    "file": current_file,
                    "changes": "\n".join(current_changes),
                    "added": [l[1:] for l in current_changes if l.startswith("+")],
                    "removed": [l[1:] for l in current_changes if l.startswith("-")],
                })
            current_file = line.split(" b/")[-1]
            current_changes = []

        # Collect added/removed lines
        elif line.startswith("+") or line.startswith("-"):
            if not line.startswith("+++") and not line.startswith("---"):
                current_changes.append(line)

    # Don't forget the last file
    if current_file:
        file_diffs.append({
            "file": current_file,
            "changes": "\n".join(current_changes),
            "added": [l[1:] for l in current_changes if l.startswith("+")],
            "removed": [l[1:] for l in current_changes if l.startswith("-")],
        })

    return file_diffs
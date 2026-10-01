"""Replace the generated part of this repository with the ProptechOS agent prompt store's export.

The export names the paths it owns (managedPaths) and the files to write there. Exactly those paths
are deleted and rewritten; nothing else in the repository is touched, so README, LICENSE and the
guidelines stay hand-written.

    python3 .github/scripts/apply_export.py export.json
"""

import json
import pathlib
import shutil
import sys


def safe(path):
    parts = path.split("/")
    return (
        path
        and not path.startswith("/")
        and "\\" not in path
        and all(part and part not in (".", "..") for part in parts)
        and not parts[0].startswith(".")
    )


def main(export_file):
    export = json.loads(pathlib.Path(export_file).read_text(encoding="utf-8"))
    managed = export["managedPaths"]
    files = export["files"]

    unsafe = [path for path in managed + [file["path"] for file in files] if not safe(path)]
    if unsafe:
        sys.exit(f"refusing unsafe paths: {unsafe}")

    outside = [
        file["path"]
        for file in files
        if not any(file["path"] == path or file["path"].startswith(path + "/") for path in managed)
    ]
    if outside:
        sys.exit(f"refusing files outside the managed paths: {outside}")

    # An empty or truncated export must never wipe the prompts.
    if not any(file["path"].startswith("experts/") for file in files):
        sys.exit("the export has no expert prompts; leaving the repository as it is")

    root = pathlib.Path.cwd()
    for path in managed:
        target = root / path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    for file in files:
        target = root / file["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        # newline="" writes the content byte for byte, line endings included.
        with open(target, "w", encoding="utf-8", newline="") as output:
            output.write(file["content"])

    print(f"wrote {len(files)} files under {', '.join(managed)}")


if __name__ == "__main__":
    main(sys.argv[1])

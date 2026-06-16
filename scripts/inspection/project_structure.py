from pathlib import Path
import os

ROOT = Path.cwd()  # run from project root

OUTPUT_FILE = "project_structure.txt"

total_files = 0
total_dirs = 0
total_size = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write("=" * 100 + "\n")
    f.write(f"PROJECT STRUCTURE: {ROOT}\n")
    f.write("=" * 100 + "\n\n")

    for root, dirs, files in os.walk(ROOT):

        level = root.replace(str(ROOT), "").count(os.sep)

        indent = "│   " * level

        folder_name = os.path.basename(root)

        if level == 0:
            f.write(f"{ROOT.name}/\n")
        else:
            f.write(f"{indent}├── {folder_name}/\n")

        total_dirs += 1

        sub_indent = "│   " * (level + 1)

        for file in sorted(files):

            path = os.path.join(root, file)

            try:
                size_mb = os.path.getsize(path) / (1024 * 1024)
                total_size += os.path.getsize(path)

                f.write(
                    f"{sub_indent}├── {file} "
                    f"({size_mb:.2f} MB)\n"
                )

                total_files += 1

            except Exception as e:
                f.write(
                    f"{sub_indent}├── {file} "
                    f"(ERROR: {e})\n"
                )

    f.write("\n")
    f.write("=" * 100 + "\n")
    f.write("SUMMARY\n")
    f.write("=" * 100 + "\n")
    f.write(f"Folders: {total_dirs}\n")
    f.write(f"Files: {total_files}\n")
    f.write(f"Total Size: {total_size / (1024**3):.2f} GB\n")

print(f"\nSaved project tree to: {OUTPUT_FILE}")
print("Open the file and paste its contents here.")
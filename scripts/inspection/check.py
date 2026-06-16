from pathlib import Path

for p in Path.cwd().iterdir():
    if p.is_dir():
        try:
            files = [x.name for x in p.iterdir()]
            if any(
                keyword in " ".join(files).lower()
                for keyword in [
                    "models",
                    "processed",
                    "firewall",
                    "network",
                    "autogluon",
                    "scripts"
                ]
            ):
                print("\nFOUND CANDIDATE:")
                print(p)
        except:
            pass
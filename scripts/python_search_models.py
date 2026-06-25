import os

extensions = {
    ".cbm",
    ".pkl",
    ".keras",
    ".json"
}

for root, dirs, files in os.walk("."):
    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            print(os.path.join(root, file))
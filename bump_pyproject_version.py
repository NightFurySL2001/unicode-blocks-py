import sys
import re

def bump_version(version_str):
    # Validate and parse semver
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
    if not match:
        print("Invalid version format. Use MAJOR.MINOR.PATCH")
        sys.exit(1)
    return version_str

def update_pyproject_version(new_version, filename="pyproject.toml"):
    file_contents = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("version = "):
                line = f'version = "{new_version}"\n'
            file_contents.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(file_contents)
    print(f"Updated version to {new_version} in {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_pyproject_version.py <new_version>")
        sys.exit(1)
    new_version = bump_version(sys.argv[1])
    update_pyproject_version(new_version)
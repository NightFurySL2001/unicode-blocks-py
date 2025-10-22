$versions = @(
"16.0.0"
"15.1.0"
"15.0.0"
"14.0.0"
"13.0.0"
"12.1.0"
"12.0.0"
"11.0.0"
"10.0.0"
"9.0.0"
"8.0.0"
"7.0.0"
"6.3.0"
"6.2.0"
"6.1.0"
"6.0.0"
"5.2.0"
"5.1.0"
"5.0.0") # Replace with your semver versions

foreach ($version in $versions) {
    echo "Bumping version to $version"
    python bump_pyproject_version.py $version
    python build_blocks.py
    pytest
}


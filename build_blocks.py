import contextlib
import urllib.request
import tomllib
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent


# Read the original __init__.py file and save a copy
MODULE_ROOT_INIT_PATH = CURRENT_DIR / "src" / "unicode_blocks" / "__init__.py"
MODULE_ROOT_INIT_CODE = open(MODULE_ROOT_INIT_PATH).readlines()


@contextlib.contextmanager
def clear_module_root_init():
    """Clear the module root __init__.py file to prevent importing cjk.py and globals.py, which depends on the generated blocks.py."""
    try:
        with open(MODULE_ROOT_INIT_PATH, "w") as f:
            f.write("")
        yield
    finally:
        # Restore the original __init__.py file
        with open(MODULE_ROOT_INIT_PATH, "w") as f:
            f.writelines(MODULE_ROOT_INIT_CODE)


with clear_module_root_init():
    # Clear module root __init__.py file before importing to prevent errors
    sys.path.insert(0, str(CURRENT_DIR / "src"))
    from unicode_blocks.unicodeBlock import UnicodeBlock


# Load the version from pyproject.toml
pyproject_path = CURRENT_DIR / "pyproject.toml"
pyproject_data = tomllib.load(open(pyproject_path, "rb"))
VERSION = pyproject_data["project"]["version"]


def get_cjk_block_categories(blocks: list[UnicodeBlock]) -> dict[str, list[str]]:
    """List block variable names for various CJK-related blocks. Modify this to include new extensions."""
    ideo_blocks = [
        "KANGXI_RADICALS",
        "CJK_RADICALS_SUPPLEMENT",
        "CJK_COMPATIBILITY_IDEOGRAPHS",
        "CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT",
        *(
            block.variable_name
            for block in blocks
            if block.variable_name.startswith("CJK_UNIFIED_IDEOGRAPHS")
        ),
    ]
    jpan_blocks = [
        "CJK_COMPATIBILITY",
        "HIRAGANA",
        "KATAKANA",
        "KATAKANA_PHONETIC_EXTENSIONS",
        "KANA_SUPPLEMENT",
        "KANA_EXTENDED_A",
        "KANA_EXTENDED_B",
        "SMALL_KANA_EXTENSION",
    ]
    kore_blocks = [
        "HANGUL_SYLLABLES",
        "HANGUL_JAMO",
        "HANGUL_COMPATIBILITY_JAMO",
        "HANGUL_JAMO_EXTENDED_A",
        "HANGUL_JAMO_EXTENDED_B",
    ]
    punc_blocks = [
        "CJK_COMPATIBILITY",
        "CJK_COMPATIBILITY_FORMS",
        "CJK_STROKES",
        "CJK_SYMBOLS_AND_PUNCTUATION",
        "HALFWIDTH_AND_FULLWIDTH_FORMS",
        "ENCLOSED_CJK_LETTERS_AND_MONTHS",
        "ENCLOSED_IDEOGRAPHIC_SUPPLEMENT",
        "IDEOGRAPHIC_DESCRIPTION_CHARACTERS",
    ]

    return {
        "IDEO_BLOCKS": ideo_blocks,
        "JPAN_BLOCKS": jpan_blocks,
        "KORE_BLOCKS": kore_blocks,
        "PUNC_BLOCKS": punc_blocks,
    }


def get_file_contents(url: str) -> str:
    """
    Download a file from the given URL and return its content as a string.
    """
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")

    if content.strip() == "":
        raise ValueError(f"Empty content for {url}")

    return content


def parse_blocks_txt(content: str) -> list[UnicodeBlock]:
    """Parse Blocks.txt content and return a list of UnicodeBlock objects."""
    blocks = []
    for line in content.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        # split data
        block_range, name = line.split(";")
        name = name.strip()
        start, end = map(lambda x: int(x.strip(), 16), block_range.split(".."))

        # add to blocks
        blocks.append(
            UnicodeBlock(
                name=name.strip(),
                start=start,
                end=end,
            )
        )
    return blocks


def parse_property_value_aliases(content: str) -> dict[str, list[str]]:
    """Parse PropertyValueAliases.txt content and return a dictionary of block aliases."""
    property_value_aliases = {}
    for line in content.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        if not line.startswith("blk;"):
            continue
        # split data
        _, *values = line.split(";")
        official_name = UnicodeBlock.to_variable_name(values[1].strip())
        values.pop(1)  # remove official name
        aliases = [alias.strip() for alias in values if alias.strip()]
        # skip if the only alias given is same as official name
        if len(aliases) == 1 and official_name == UnicodeBlock.to_variable_name(
            aliases[0]
        ):
            continue
        property_value_aliases[official_name] = aliases
    return property_value_aliases


def process_unicode_data_ranges(
    unicode_data_content: str, blocks: list[UnicodeBlock]
) -> None:
    """Process UnicodeData.txt to assign character ranges to blocks."""

    def get_next_block(blocks_iter):
        block = next(blocks_iter)
        setattr(block, "characters", [])
        return block

    def handle_ranged_block_first_entry(unidec, current_block, blocks_iter):
        if unidec != current_block.start:
            # Advance to the next block if current one doesn't match
            # because two continuous block ranges (eg:
            # DC00;<Low Surrogate, First>;Cs;0;L;;;;;N;;;;;
            # DFFF;<Low Surrogate, Last>;Cs;0;L;;;;;N;;;;;
            # E000;<Private Use, First>;Co;0;L;;;;;N;;;;;
            # F8FF;<Private Use, Last>;Co;0;L;;;;;N;;;;;
            # ) after <Low Surrogate, Last> the block is moved forward already
            current_block = get_next_block(blocks_iter)
            if unidec != current_block.start:
                raise ValueError(
                    f"Expected start with {current_block.start:#06x}, got {unidec:#06x}"
                )
        setattr(current_block, "characters", unidec)
        return current_block

    def handle_ranged_block_last_entry(unidec, current_block, blocks_iter):
        if unidec not in current_block:
            raise ValueError(
                f"Expected end before {current_block.end:#06x}, got {unidec:#06x}"
            )
        start = getattr(current_block, "characters")
        current_block.assigned_ranges = [(start, unidec)]
        delattr(current_block, "characters")
        return get_next_block(blocks_iter)

    def assign_character_to_block(
        unidec: int, current_block: UnicodeBlock, blocks_iter
    ) -> UnicodeBlock:
        """Assign a character to the appropriate Unicode block."""
        if unidec in current_block:
            getattr(current_block, "characters").append(unidec)
            return current_block

        while unidec not in current_block:
            # advance to the next block
            try:
                current_block = get_next_block(blocks_iter)
                if unidec in current_block:
                    getattr(current_block, "characters").append(unidec)
                    break
            except StopIteration:
                raise ValueError(f"Character {unidec} not found in any block.")
        return current_block

    blocks_iter = iter(blocks)
    current_block = get_next_block(blocks_iter)

    # Group characters into ranges according to blocks
    for line in unicode_data_content.splitlines():
        if not line.strip():
            continue
        # Extract character code and block name
        unihex, char_name, *_ = line.split(";")
        unidec = int(unihex, 16)

        try:
            if char_name.startswith("<"):
                if char_name.endswith("First>"):
                    current_block = handle_ranged_block_first_entry(
                        unidec, current_block, blocks_iter
                    )
                    continue
                elif char_name.endswith("Last>"):
                    current_block = handle_ranged_block_last_entry(
                        unidec, current_block, blocks_iter
                    )
                    continue

            # Find and assign the block this character belongs to
            current_block = assign_character_to_block(
                unidec, current_block, blocks_iter
            )

        except StopIteration:
            # If we reach the end of blocks at the correct codepoint, break the loop
            assert unidec == 0x10FFFD
            break


def collapse_character_ranges(blocks: list[UnicodeBlock]) -> None:
    """Collapse individual characters into ranges for each block."""
    for block in blocks:
        # calculate assigned ranges, skip blocks without characters
        if not hasattr(block, "characters") or not getattr(block, "characters"):
            continue

        # Collapse characters into ranges for each block
        block_chars = getattr(block, "characters", [])
        block_chars.sort()
        collapsed_ranges = []
        range_start = range_end = block_chars[0]

        for char in block_chars[1:]:
            if char == range_end + 1:
                range_end = char
            else:
                collapsed_ranges.append((range_start, range_end))
                range_start = range_end = char

        collapsed_ranges.append((range_start, range_end))
        block.assigned_ranges = collapsed_ranges
        delattr(block, "characters")  # Clear individual characters to save memory


def write_blocks_file(
    blocks: list[UnicodeBlock],
    block_names: list[str],
) -> None:
    """Write the blocks data to the blocks.py file."""
    FILE_HEADER = """# This file is auto-generated on build. Do not edit.
# This code is licensed under the MIT License.
# Modified under Unicode License v3. See https://www.unicode.org/license.txt for details.\n\n"""

    with open(CURRENT_DIR / "src" / "unicode_blocks" / "blocks.py", "w") as f:
        f.write(FILE_HEADER)
        f.write("from .unicodeBlock import UnicodeBlock\n\n")

        f.write(f"VERSION = {VERSION!r}\n\n")

        # default No_Block
        f.write("NO_BLOCK = UnicodeBlock(name='No Block', start=-1, end=-1)\n")

        # write block data
        for block in blocks:
            f.write(f"{block.variable_name} = {block!r}\n")
        f.write("\n")

        # write all blocks
        f.write("ALL_BLOCKS = [\n")
        for block in block_names:
            f.write(f"    {block},\n")
        f.write("]\n")
        f.write("\n")

        # Write CJK helper lists
        cjk_categories = get_cjk_block_categories(blocks)
        for name, current_blocks in cjk_categories.items():
            f.write(f"{name} = [\n")
            for block in current_blocks:
                if (
                    block in block_names
                ):  # check if block name exists for this version of Unicode
                    f.write(f"    {block},\n")
            f.write("]\n")
            f.write("\n")


def build_version(version: str):
    """
    Build the data files for the given version.
    """
    # Download and parse Unicode data files
    block_content = get_file_contents(
        f"https://www.unicode.org/Public/{version}/ucd/Blocks.txt"
    )
    blocks = parse_blocks_txt(block_content)

    property_value_aliases_content = get_file_contents(
        f"https://www.unicode.org/Public/{version}/ucd/PropertyValueAliases.txt"
    )
    property_value_aliases = parse_property_value_aliases(
        property_value_aliases_content
    )

    unicode_data_content = get_file_contents(
        f"https://www.unicode.org/Public/{version}/ucd/UnicodeData.txt"
    )
    process_unicode_data_ranges(unicode_data_content, blocks)

    # Post-process blocks
    block_names = []
    for block in blocks:
        block_names.append(block.variable_name)

        # Add aliases from PropertyValueAliases.txt
        if block.variable_name in property_value_aliases:
            block.aliases = property_value_aliases[block.variable_name]

    collapse_character_ranges(blocks)

    # Write the output file
    write_blocks_file(blocks, block_names)


if __name__ == "__main__":
    # Build the data files for the current version
    with clear_module_root_init():
        build_version(VERSION)
    print(f"Data files for Unicode version {VERSION} built successfully.")

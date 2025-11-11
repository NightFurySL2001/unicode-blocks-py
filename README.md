# 🧱 Unicode_Blocks 🧱

`unicode_blocks` is a simple utility module for working with Unicode blocks data. [Unicode blocks](https://www.unicode.org/versions/latest/core-spec/chapter-3/#G64189) are continuous ranges of code points defined by the Unicode standard, used to group characters with generally similar purposes or origins.

## Usage

Install this package from PyPI:

```sh
pip install unicode-blocks-py
```

The module interface is heavily inspired by Java [`Character.UnicodeBlock`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Character.UnicodeBlock.html) class and Rust [`unicode_blocks`](https://docs.rs/unicode-blocks/latest/unicode_blocks/) module.

```py
>>> import unicode_blocks
>>> unicode_major_version = int(unicode_blocks.__version__.split(".")[0])

# To get Unicode block of a character, input a character string of length 1,
# UTF-8 encoded bytes, or a positive integer representing a Unicode code point.
# The following are the same: they decode the character 'a'.
>>> block = unicode_blocks.of('a')
>>> block2 = unicode_blocks.of(b'\x61')
>>> block3 = unicode_blocks.of(97)
>>> assert block == block2 == block3

# To get Unicode block using name, input the block name.
# Cases, whitespace, dashes, underscrolls and prefix "is" will be ignored for comparison. See UAX44-LM3.
# Block name aliases from PropertyValueAliases are also usable here
>>> ascii_block = unicode_blocks.for_name("BASIC_LATIN")
>>> ascii_block2 = unicode_blocks.for_name("basiclatin")
>>> ascii_block3 = unicode_blocks.for_name("isBasicLatin")
>>> from unicode_blocks import BASIC_LATIN
>>> assert ascii_block == ascii_block2 == ascii_block3 == BASIC_LATIN
>>> if unicode_major_version >= 6:
...     ascii_block4 = unicode_blocks.for_name("ASCII")
...     assert ascii_block4 == BASIC_LATIN

# Unicode characters currently not assigned will receive No_Block object as per
# rule D10b in Section 3.4, *Characters and Encoding*, of Unicode
>>> assert unicode_blocks.of(0xEDCBA) == unicode_blocks.NO_BLOCK

# List through all the defined Unicode blocks at the version
# NO_BLOCK is not in the list of all blocks
>>> for block in unicode_blocks.all():
...     print(block) # doctest: +ELLIPSIS
UnicodeBlock(...)

# Pythonic helpers: comparisons between blocks, where earlier blocks is smaller than later blocks
# useful for sorting a list of UnicodeBlocks
>>> latin1_block = unicode_blocks.for_name("Latin-1 Supplement")
>>> assert ascii_block < latin1_block

# Get the total defined code points in a block. Does not represent if the block is filled in or not.
>>> assert len(ascii_block) == 128

# Additional helpers: check for assigned characters in the block
# Data is loaded from UCD and may change between Unicode versions
>>> assert len(ascii_block.assigned_ranges) == 128
>>> assert 'B' in ascii_block.assigned_ranges

# Example where defined Unicode block range is not fully utilised
>>> bopo_block = unicode_blocks.of('ㄅ')
>>> assert len(bopo_block) == 48
>>> bopo_assigned_count = 41 if unicode_major_version < 10 else 42 if unicode_major_version == 10 else 43
>>> assert len(bopo_block.assigned_ranges) == bopo_assigned_count  # first 5 code points should be unassigned, at least in <=17.0
>>> assert len(bopo_block) != len(bopo_block.assigned_ranges)

```

The lists of Unicode block objects are available directly in the namespace, or under the `blocks` module.

```py
# both are equivalent
>>> from unicode_blocks import BASIC_LATIN
>>> from unicode_blocks.blocks import BASIC_LATIN

```

Various names are also available in the block:

```py
>>> from unicode_blocks import BASIC_LATIN
>>> assert BASIC_LATIN.name == "Basic Latin"  # Official Unicode name as in Blocks.txt
>>> assert BASIC_LATIN.normalised_name == "BASICLATIN"  # Normalised name under UAX44-LM3
>>> assert BASIC_LATIN.variable_name == "BASIC_LATIN"  # Variable name in `unicode_blocks.blocks`
>>> if unicode_major_version >= 6:
...     assert BASIC_LATIN.aliases == ["ASCII"]  # Official block aliases as in PropertyValueAliases.txt

```

Additional utilities for CJK are specially provided referencing the oxidised version of the module. Selected samples are shown below.

```py
>>> from unicode_blocks import cjk
>>> assert cjk.is_cjk('中')
>>> assert cjk.is_japanese_kana('あ')
>>> assert cjk.is_korean_hangul('글')
>>> assert cjk.is_cjk_punctuation('。')

>>> from unicode_blocks import blocks
>>> assert cjk.is_ideographic_block(blocks.CJK_UNIFIED_IDEOGRAPHS)
>>> assert cjk.is_cjk_block(blocks.KANGXI_RADICALS)
>>> assert cjk.is_japanese_block(blocks.KATAKANA_PHONETIC_EXTENSIONS)
>>> assert cjk.is_korean_block(blocks.HANGUL_COMPATIBILITY_JAMO)

```

> [!WARNING]  
> Checking `char in unicode_blocks.for_name("is_CJK")` is **NOT** the same as `cjk.is_cjk(char)`!  
> `unicode_blocks.for_name("is_CJK")` refers to the "CJK" block alias for CJK Unified Ideographs block, while `cjk.is_cjk` checks through (roughly) all Unicode blocks related to CJK including kana, hangul and punctuations.

To check which Unicode version data is used, check against the `__version__` variable in the namespace. (Bug fix release will use `+1` notation)

```sh
$ python3
>>> import unicode_blocks
>>> unicode_blocks.__version__  # doctest: +SKIP
'17.0.0'
```

The version will follow the Unicode semver of the data files, optionally followed by additional numbering from this module for bug fixes after a plus sign, i.e. `<Unicode major.minor.patch>(+<additional numbering>)`.

## Update

To update the blocks data from Unicode Character Database, update the `project.version` key in `pyproject.toml` to the Unicode version number, and then run `python3 build_blocks.py`. This will update the `src/unicode_blocks/blocks.py` file, which is automatically generated from UCD data.

Most of these steps should be directly runnable through GitHub Actions.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Clone the repository and install as development mode:
    ```sh
    git clone https://github.com/NightFurySL2001/unicode-blocks.git
    cd unicode-blocks
    pip install -e .
    ```
2.  Create a new branch for your feature or bug fix.
3.  Work on the feature and run or develop relevant test cases.
4.  Test the changes by running `pytest`.
5.  Ensure this README.md is updated with `python -m doctest README.md`.
6.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

-   [Unicode Consortium](https://unicode.org) for maintaining the Unicode standard and providing the Unicode Character Database (UCD). Data modification are done under [Unicode License v3](https://www.unicode.org/license.txt).

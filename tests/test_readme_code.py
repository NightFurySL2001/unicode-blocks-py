import unittest

import unicode_blocks  # installed unicode_blocks Python module


class TestReadme(unittest.TestCase):
    # IMPORTANT: ASCII alias to BASIC_LATIN block was added in Unicode 5.1.0.

    def test_readme_usage1(self):
        # To get Unicode block of a character, input a character string of length 1,
        # UTF-8 encoded bytes, or a positive integer representing a Unicode code point.
        # The following are the same: they decode the character 'a'.
        block = unicode_blocks.of("a")
        block2 = unicode_blocks.of(b"\x61")
        block3 = unicode_blocks.of(97)
        assert block == block2 == block3

        # To get Unicode block using name, input the block name.
        # Cases, whitespace, dashes, underscrolls and prefix "is" will be ignored for comparison. See UAX44-LM3.
        # Block name aliases from PropertyValueAliases are also usable here
        ascii_block = unicode_blocks.for_name("BASIC_LATIN")
        ascii_block2 = unicode_blocks.for_name("basiclatin")
        ascii_block3 = unicode_blocks.for_name("isBasicLatin")
        ascii_block4 = unicode_blocks.for_name("ASCII")
        from unicode_blocks import BASIC_LATIN

        assert (
            ascii_block == ascii_block2 == ascii_block3 == ascii_block4 == BASIC_LATIN
        )

        # Unicode characters currently not assigned will receive No_Block object as per
        # rule D10b in Section 3.4, *Characters and Encoding*, of Unicode
        assert unicode_blocks.of(0xEDCBA) == unicode_blocks.NO_BLOCK

        # List through all the defined Unicode blocks at the version
        # NO_BLOCK is not in the list of all blocks
        for block in unicode_blocks.all():
            print(block)

        # Pythonic helpers: comparisons between blocks, where earlier blocks is smaller than later blocks
        # useful for sorting a list of UnicodeBlocks
        latin1_block = unicode_blocks.for_name("Latin-1 Supplement")
        assert ascii_block < latin1_block
        # Get the total defined code points in a block. Does not represent if the block is filled in or not.
        assert len(ascii_block) == 128

        # Additional helpers: check for assigned characters in the block
        # Data is loaded from UCD and may change between Unicode versions
        assert len(ascii_block.assigned_ranges) == 128
        assert "B" in ascii_block.assigned_ranges

        # Example where defined Unicode block range is not fully utilised
        bopo_block = unicode_blocks.of("ㄅ")
        assert len(bopo_block) == 48
        assert (
            len(bopo_block.assigned_ranges) == 43
        )  # first 5 code points should be unassigned, at least in <=17.0
        assert len(bopo_block) != len(bopo_block.assigned_ranges)

    def test_readme_usage2(self):
        from unicode_blocks import cjk

        assert cjk.is_cjk("中")
        assert cjk.is_japanese_kana("あ")
        assert cjk.is_korean_hangul("글")
        assert cjk.is_cjk_punctuation("。")

        from unicode_blocks import blocks

        assert cjk.is_ideographic_block(blocks.CJK_UNIFIED_IDEOGRAPHS)
        assert cjk.is_cjk_block(blocks.KANGXI_RADICALS)
        assert cjk.is_japanese_block(blocks.KATAKANA_PHONETIC_EXTENSIONS)
        assert cjk.is_korean_block(blocks.HANGUL_COMPATIBILITY_JAMO)

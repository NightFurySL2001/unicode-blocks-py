"""Unit tests for unicode_blocks globals and functions.
IMPORTANT: CJK alias to CJK Unified Ideographs only exists since Unicode 6.1.0.
"""
import unittest

import unicode_blocks  # installed unicode_blocks Python module

from unicode_blocks.unicodeBlock import UnicodeBlock, AssignedRanges
from unicode_blocks.errors import InvalidUnicodeBlockNameError


class TestGlobals(unittest.TestCase):
    def test_all_returns_all_blocks(self):
        blocks = unicode_blocks.all()
        self.assertIsInstance(blocks, list)
        self.assertTrue(all(isinstance(b, UnicodeBlock) for b in blocks))
        self.assertGreater(len(blocks), 0)

    def test_for_name(self):
        ### Test for a valid block name
        block = unicode_blocks.for_name("Basic Latin")
        self.assertIsNotNone(block)
        self.assertEqual(block, unicode_blocks.BASIC_LATIN)

        # Test for variations of the block name
        variations = [
            # spacing and case variations
            "Basic_Latin",
            "basic_latin",
            "basic latin",
            "BASIC_LATIN",
            "BASIC LATIN",
            "BASIC-LATIN",
            "B a s i c   L a t i n",
            # no space
            "BasicLatin",
            "basiclatin",
            "BaSicLaTiN",
            # with 'is' prefix
            "is_Basic Latin",
            "isBasicLatin",
            "IS BASIC LATIN",
            "IS_BASIC_LATIN",
            # aliases for this block
            "ASCII",
            "ascii",
            " a s c i i",
            "is_ASCII",
            "is ASCII",
            "isascii",
            "is-ascii",
            "iSaScIi",
            "i s as c i-i",
        ]
        for name in variations:
            blk = unicode_blocks.for_name(name)
            self.assertIsNotNone(blk)
            self.assertEqual(blk, unicode_blocks.BASIC_LATIN)

        ### Test for a valid block name with aliases
        block2 = unicode_blocks.for_name("CJK Unified Ideographs")
        self.assertIsNotNone(block2)
        self.assertEqual(block2, unicode_blocks.CJK_UNIFIED_IDEOGRAPHS)

        # Test for variations of the block name with aliases
        variations2 = [
            # spacing and case variations
            "CJK_Unified_Ideographs",
            "cjk_unified_ideographs",
            # with 'is' prefix
            "is_CJK Unified Ideographs",
            "is_CJK_UNIFIED_IDEOGRAPHS",
            # aliases for this block
            "CJK",
            "cjk",
            "is_CJK",
            "i s C J K",
            "is cjk",
        ]
        for name in variations2:
            blk = unicode_blocks.for_name(name)
            self.assertIsNotNone(blk)
            self.assertEqual(blk, unicode_blocks.CJK_UNIFIED_IDEOGRAPHS)

    def test_for_name_invalid(self):
        ### Test for non-existent block name
        with self.assertRaises(InvalidUnicodeBlockNameError):
            unicode_blocks.for_name("XXXXX_NotARealBlockName")

    def test_of_with_str(self):
        # 'A' is in Basic Latin
        block = unicode_blocks.of("A")
        self.assertIsNotNone(block)
        self.assertEqual(block, unicode_blocks.BASIC_LATIN)

        # '中' is in CJK Unified Ideographs
        # Only the first character is used for block determination
        block2 = unicode_blocks.of("中1234")
        self.assertIsNotNone(block2)
        self.assertEqual(block2, unicode_blocks.CJK_UNIFIED_IDEOGRAPHS)

    def test_of_with_int(self):
        # 0x0410 is 'А' (Cyrillic Capital Letter A)
        block = unicode_blocks.of(0x0410)
        self.assertIsNotNone(block)
        self.assertEqual(block, unicode_blocks.CYRILLIC)

        # 0x3007 is '〇' (Ideographic Number Zero)
        block2 = unicode_blocks.of(0x3007)
        self.assertIsNotNone(block2)
        self.assertEqual(block2, unicode_blocks.CJK_SYMBOLS_AND_PUNCTUATION)

    def test_of_with_bytes(self):
        # 'A' as bytes
        block = unicode_blocks.of(b"A")
        self.assertIsNotNone(block)
        self.assertEqual(block, unicode_blocks.BASIC_LATIN)

        # '中' as bytes
        # Note: The bytes must be decoded to str using utf-8
        # only the first character is used for block determination
        block3 = unicode_blocks.of(b"\xe4\xb8\xad\xe6\x96\x87")  # '中文' in UTF-8
        self.assertIsNotNone(block3)
        self.assertEqual(block3, unicode_blocks.CJK_UNIFIED_IDEOGRAPHS)

    def test_assigned_ranges(self):
        block = unicode_blocks.of("A")
        # check if range is a class
        self.assertTrue(isinstance(block.assigned_ranges, AssignedRanges))
        # ASCII Basic Latin block should have 128 assigned characters
        self.assertEqual(len(block.assigned_ranges), 128)
        # Check if 'B' is in the assigned range
        self.assertTrue("B" in block.assigned_ranges)
        # Check if '中' is not in the assigned range
        self.assertFalse("中" in block.assigned_ranges)

    def test_invalid_cases(self):
        # Code point outside Unicode range
        with self.assertRaises(AssertionError):
            unicode_blocks.of(0x110000)

        # Invalid byte sequence
        with self.assertRaises(UnicodeDecodeError):
            unicode_blocks.of(b"\x80\x81")

        # Currently undefined code point
        block = unicode_blocks.of(0xEDCBA)
        self.assertIsNotNone(block)
        self.assertEqual(block, unicode_blocks.NO_BLOCK)

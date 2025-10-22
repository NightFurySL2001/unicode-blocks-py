import unittest

import unicode_blocks  # installed unicode_blocks Python module


class TestCJK(unittest.TestCase):
    def test_find_block(self):
        self.assertEqual(unicode_blocks.CJK_UNIFIED_IDEOGRAPHS, unicode_blocks.of("中"))
        self.assertEqual(
            unicode_blocks.CJK_SYMBOLS_AND_PUNCTUATION, unicode_blocks.of("。")
        )
        self.assertEqual(
            unicode_blocks.HALFWIDTH_AND_FULLWIDTH_FORMS, unicode_blocks.of("，")
        )

    def test_is_cjk(self):
        self.assertFalse(unicode_blocks.is_cjk("1"))
        self.assertFalse(unicode_blocks.is_cjk("a"))
        self.assertFalse(unicode_blocks.is_cjk("â"))
        self.assertFalse(unicode_blocks.is_cjk("/"))
        self.assertFalse(unicode_blocks.is_cjk("ß"))
        self.assertTrue(unicode_blocks.is_cjk("中"))
        self.assertTrue(unicode_blocks.is_cjk("𩸽"))
        self.assertTrue(unicode_blocks.is_cjk("。"))
        self.assertTrue(unicode_blocks.is_cjk("，"))
        self.assertTrue(unicode_blocks.is_cjk("あ"))
        self.assertTrue(unicode_blocks.is_cjk("ア"))
        self.assertTrue(unicode_blocks.is_cjk("を"))
        self.assertTrue(unicode_blocks.is_cjk("ヲ"))
        self.assertTrue(unicode_blocks.is_cjk("ん"))
        self.assertTrue(unicode_blocks.is_cjk("ン"))
        self.assertTrue(unicode_blocks.is_cjk("이"))

    def test_is_cjk_block(self):
        self.assertFalse(unicode_blocks.is_cjk_block(unicode_blocks.of("1")))
        self.assertFalse(unicode_blocks.is_cjk_block(unicode_blocks.of("a")))
        self.assertFalse(unicode_blocks.is_cjk_block(unicode_blocks.of("/")))
        self.assertFalse(unicode_blocks.is_cjk_block(unicode_blocks.of("ß")))
        self.assertTrue(unicode_blocks.is_cjk_block(unicode_blocks.of("中")))
        self.assertTrue(unicode_blocks.is_cjk_block(unicode_blocks.of("。")))
        self.assertTrue(unicode_blocks.is_cjk_block(unicode_blocks.of("，")))

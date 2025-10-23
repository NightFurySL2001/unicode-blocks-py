import unittest

import unicode_blocks  # installed unicode_blocks Python module


class TestInternalValidation(unittest.TestCase):
    def test_unique_block_names(self):
        """Test that all Unicode block names are unique. See definition D10 Block of https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3"""
        unique_names = set(["No_Block"])
        for block in unicode_blocks.all():
            # Normalise the block name to ensure uniqueness
            block_name = block.normalised_name
            if block_name in unique_names:
                self.fail(f"Duplicate block name found: {block_name}")
            unique_names.add(block_name)
            for alias in block.aliases:
                if alias == "ARABICPRESENTATIONFORMSA":
                    print(alias)
                    continue
                block_alias = unicode_blocks.UnicodeBlock.normalise_name(alias)
                if block_alias in unique_names:
                    self.fail(f"Duplicate block alias found: {block_alias}")
                unique_names.add(block_alias)
    
    def test_pairwise_disjoint(self):
        """Test that all Unicode blocks are non-overlapping. See definition D10 Block of https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3"""
        covered_ranges = []
        for block in unicode_blocks.all():
            start, end = block.start, block.end
            for covered in covered_ranges:
                if covered[0] <= end and start <= covered[1]:
                    self.fail(
                        f"Overlapping blocks found: {block.name} overlaps with {covered}"
                    )
            covered_ranges.append((start, end))

    def test_block_name_normalisation(self):
        block = unicode_blocks.for_name("basic_latin")
        self.assertEqual(block, unicode_blocks.BASIC_LATIN)
        self.assertEqual(block.name, "Basic Latin")
        self.assertEqual(block.normalised_name, "BASICLATIN")
        self.assertEqual(block.variable_name, "BASIC_LATIN")
        self.assertEqual(block.aliases, ["ASCII"])

        block2 = unicode_blocks.for_name("latin_1")
        self.assertEqual(block2, unicode_blocks.LATIN_1_SUPPLEMENT)
        self.assertEqual(block2.name, "Latin-1 Supplement")
        self.assertEqual(block2.normalised_name, "LATIN1SUPPLEMENT")
        self.assertEqual(block2.variable_name, "LATIN_1_SUPPLEMENT")

        block3 = unicode_blocks.for_name("CJK")
        self.assertEqual(block3.name, "CJK Unified Ideographs")
        self.assertEqual(block3.normalised_name, "CJKUNIFIEDIDEOGRAPHS")
        self.assertEqual(block3.variable_name, "CJK_UNIFIED_IDEOGRAPHS")
        self.assertEqual(block3.aliases, ["CJK"])
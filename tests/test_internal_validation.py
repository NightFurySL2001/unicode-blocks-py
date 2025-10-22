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
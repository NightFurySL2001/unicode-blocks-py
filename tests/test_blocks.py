import unittest

from unicode_blocks.unicodeBlock import AssignedRanges, UnicodeBlock


class TestAssignedRanges(unittest.TestCase):
    def test_empty_ranges(self):
        ranges = AssignedRanges([])

        self.assertFalse(ranges)
        self.assertEqual(len(ranges), 0)
        self.assertEqual(list(ranges), [])
        self.assertEqual(repr(ranges), "AssignedRanges([])")

    def test_sparse_ranges_iterate_code_points(self):
        ranges = AssignedRanges([(1, 2), (4, 5)])

        self.assertTrue(ranges)
        self.assertEqual(len(ranges), 4)
        self.assertEqual(list(ranges), [1, 2, 4, 5])
        self.assertTrue(1 in ranges)
        self.assertTrue(5 in ranges)
        self.assertFalse(3 in ranges)
        self.assertEqual(
            repr(ranges),
            "AssignedRanges([Range(start=1, end=2), Range(start=4, end=5)])",
        )

    def test_range_boundaries_accept_supported_character_types(self):
        ranges = AssignedRanges([(0x41, 0x42)])

        self.assertTrue("A" in ranges)
        self.assertTrue(0x42 in ranges)
        self.assertTrue(b"B" in ranges)
        self.assertFalse(0x40 in ranges)
        self.assertFalse("C" in ranges)


class TestUnicodeBlock(unittest.TestCase):
    def test_defaults_and_properties(self):
        block = UnicodeBlock("Test Block", 0x10, 0x1F)

        self.assertEqual(block.normalised_name, "TESTBLOCK")
        self.assertEqual(block.variable_name, "TEST_BLOCK")
        self.assertEqual(block.aliases, [])
        self.assertFalse(block.assigned_ranges)
        self.assertEqual(len(block), 0x10)
        self.assertEqual(
            repr(block),
            "UnicodeBlock(name='Test Block', start=0x0010, end=0x001f)",
        )

    def test_assigned_ranges_and_aliases_are_in_repr(self):
        block = UnicodeBlock(
            "Test Block",
            0x10,
            0x1F,
            assigned_ranges=[(0x10, 0x12), (0x15, 0x16)],
            aliases=["TB"],
        )

        self.assertEqual(
            repr(block),
            "UnicodeBlock(name='Test Block', start=0x0010, end=0x001f, "
            "assigned_ranges=[(0x0010, 0x0012), (0x0015, 0x0016)], "
            "aliases=['TB'])",
        )
        self.assertEqual(list(block.assigned_ranges), [0x10, 0x11, 0x12, 0x15, 0x16])

    def test_contains_boundaries_and_supported_character_types(self):
        block = UnicodeBlock("Test Block", 0x41, 0x5A)

        self.assertTrue("A" in block)
        self.assertTrue(0x5A in block)
        self.assertTrue(b"B" in block)
        self.assertFalse(0x40 in block)
        self.assertFalse("[" in block)

    def test_blocks_order_by_start(self):
        earlier = UnicodeBlock("Earlier", 0x10, 0x1F)
        later = UnicodeBlock("Later", 0x20, 0x2F)

        self.assertTrue(earlier < later)
        self.assertTrue(later > earlier)
        self.assertEqual(earlier, UnicodeBlock("Same start", 0x10, 0x2F))
"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import os
from unittest import TestCase

from memtrace import State, parse_log

current_dir = os.path.dirname(__file__)


class TestParse(TestCase):
    def test_parse(self):
        state = State(
            [
                (
                    r"ArchiveEntry __cinit__ (?P<addr>\w+?),\s+?",
                    r"ArchiveEntry __dealloc__ (?P<addr>\w+?),\s+?",
                )
            ]
        )
        parse_log(os.path.join(current_dir, "ok.log"), state)

    def test_leak(self):
        state = State(
            [
                (
                    r"ArchiveEntry __cinit__ (?P<addr>\w+?),\s+?",
                    r"ArchiveEntry __dealloc__ (?P<addr>\w+?),\s+?",
                ),
                (
                    r"ArchiveRead __cinit__ (?P<addr>\w+?),\s+?",
                    r"ArchiveRead __dealloc__ (?P<addr>\w+?),\s+?",
                ),
            ]
        )
        with self.assertRaises(ValueError):
            try:
                parse_log(os.path.join(current_dir, "leak.log"), state)
            except ValueError as e:
                print(e)
                raise e

    def test_nullfree(self):
        state = State(
            [
                (
                    r"ArchiveEntry __cinit__ (?P<addr>\w+?),\s+?",
                    r"ArchiveEntry __dealloc__ (?P<addr>\w+?),\s+?",
                )
            ]
        )
        with self.assertRaises(ValueError):
            try:
                parse_log(os.path.join(current_dir, "nullfree.log"), state)
            except ValueError as e:
                print(e)
                raise e


if __name__ == "__main__":
    import unittest

    unittest.main()

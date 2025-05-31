import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.tests.test_blocks
import src.tests.test_extracts
import src.tests.test_htmlnode
import src.tests.test_leafnode
import src.tests.test_parentnode
import src.tests.test_textnode
import src.tests.test_utils
import src.tests.test_markdown

def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(src.tests.test_blocks))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_extracts))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_htmlnode))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_leafnode))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_parentnode))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_textnode))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_utils))
    suite.addTests(loader.loadTestsFromModule(src.tests.test_markdown))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_all_tests()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import epub

class VersionTest(unittest.TestCase):

    def testVersion(self):
        self.assertEqual(epub.__version__, '0.2.1')

    def testVersionInfo(self):
        self.assertEqual(epub.__version_info__, (0, 2, 1))

if __name__ == '__main__':
    unittest.main()


# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# File   : test_xcofdkse.py
# Author : Farzad Safa (farzad.safa@xcofdk.de)
#
# Copyright (C) 2023 Farzad Safa
# All rights reserved.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import libs / modules
# ------------------------------------------------------------------------------
from unittest import TestCase
from unittest import TestSuite

from xcofdk.tests.startXcoFDK import Main


# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
def load_tests(loader, tests, pattern):
    res = TestSuite() if tests is None else tests

    tcInst = TCStartXcoFDK()
    res.addTest(TCStartXcoFDK())
    print(f'[load_tests] Added TC instance {type(tcInst).__name__}.')

    return res
#END load_tests()


def LoadTests():
    return load_tests(None, None, None)
#END LoadTests()


class TCStartXcoFDK(TestCase):
    def __init__(self):
        TestCase.__init__(self, methodName='RunMain')

    def RunMain(self):
        print()

        retVal = Main()
        self.assertEqual(retVal, 0, f'[TCStartXcoFDK] TC {self._testMethodName} failed.')
        print(f'[TCStartXcoFDK] TC {self._testMethodName} passed.')
#END class TCStartXcoFDK


# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    from unittest import TextTestRunner as _TextTestRunner

    runner = _TextTestRunner()
    runner.run(LoadTests())

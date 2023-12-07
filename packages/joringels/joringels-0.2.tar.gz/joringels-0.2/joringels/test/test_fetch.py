# standard lib imports
import colorama as color

color.init()

import os, re, shutil, sys, time
import yaml
import unittest

# C:\Users\lars\python_venvs\libs\joringels\joringels\test\test_api_handler.py
# test package imports
import joringels.src.settings as sts
import joringels.src.helpers as helpers
import os
from joringels.src.actions import fetch

# print(f"\n__file__: {__file__}")


class Test_UnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.verbose = 0
        # cls.testData = cls.get_test_data(*args, **kwargs)
        cls.safeName = "safe_one"
        cls.encryptPath = os.path.join(sts.testDataDir, "safe_one.yml")
        cls.productName = "haimdall"
        cls.clusterName = "testing_cluster"
        cls.exportDir = os.path.join(sts.testDataDir, "actions")
        os.environ["secrets"] = os.path.join(sts.testDataDir, "joringels.kdbx")
        sts.encryptDir = sts.testDataDir
        cls.kwargs = {
            "safeName": cls.safeName,
            "entryName": "safe_one",
            "productName": cls.productName,
            "clusterName": cls.clusterName,
            "key": sts.testKeyOuter,
            "keyV": sts.testKeyInner,
            "retain": True,
        }

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        if os.path.exists(cls.encryptPath):
            os.remove(cls.encryptPath)

    ########## TEST START ##########

    def test_alloc(self, *args, **kwargs):
        out = fetch.alloc(*[], **self.kwargs)
        self.assertEqual("testing", out.get("password"))


if __name__ == "__main__":
    with helpers.temp_password(pw=sts.testKeyOuter):
        unittest.main()

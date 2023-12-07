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
from joringels.src.actions import load

# print(f"\n__file__: {__file__}")


class Test_UnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.verbose = 0
        # cls.testData = cls.get_test_data(*args, **kwargs)
        cls.safeName = "safe_one"
        cls.prep_enc_path(*args, **kwargs)
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

    @classmethod
    def prep_enc_path(cls, *args, **kwargs):
        cls.encryptPath = os.path.join(sts.testDataDir, "safe_one.yml")
        if os.path.exists(cls.encryptPath):
            return True
        cls.encryptBackup = os.path.join(sts.testDataDir, "#safe_one.yml")
        # copying this file is needed because pre-commit fails on changes
        shutil.copyfile(cls.encryptBackup, cls.encryptPath)

    # @classmethod
    # def get_test_data(cls, *args, **kwargs):
    #     with open(os.path.join(sts.testDataDir, "test_api_handler.yml"), "r") as f:
    #         return yaml.safe_load(f)

    # def test_run(self, *args, **kwargs):
    #     pass


if __name__ == "__main__":
    with helpers.temp_password(pw=sts.testKeyOuter):
        unittest.main()
    print("done")
    exit()

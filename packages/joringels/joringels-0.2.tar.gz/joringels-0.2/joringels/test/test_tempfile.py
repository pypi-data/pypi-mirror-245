# standard lib imports
import colorama as color

color.init()

import os, re, shutil, sys, time
import yaml
import unittest

# C:\Users\lars\python_venvs\libs\joringels\joringels\test\test_tempfile.py
# test package imports
import joringels.src.settings as sts
import joringels.src.helpers as helpers
from joringels.src.actions import tempfile

# print(f"\n__file__: {__file__}")


# jo upload -n safe_one -src kdbx -con scp -pr all
class Test_UnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.verbose = 0
        cls.prep_enc_path(*args, **kwargs)
        # cls.testData = cls.get_test_data(*args, **kwargs)
        os.environ["secrets"] = os.path.join(sts.testDataDir, "joringels.kdbx")
        sts.encryptDir = sts.testDataDir
        cls.creds = {
            "clusterName": "testing_cluster",
            # 'productName': 'haimdall',
            "entryName": "haimdall_server",
            "safeName": "safe_one",
            "key": sts.testKeyOuter,
            "keyV": sts.testKeyInner,
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

    # @classmethod
    # def get_test_data(cls, *args, **kwargs):
    #     with open(os.path.join(sts.testDataDir, "test_tempfile.yml"), "r") as f:
    #         return yaml.safe_load(f)

    def test_temp_secret(self, *args, **kwargs):
        pass
        # expected = {
        #     "password": f"{sts.testKey}",
        #     "title": "haimdall_server",
        #     "url": "123.456.789.0",
        #     "username": "thor",
        # }
        # # filePth has to be full path to tempfile.yml or .json
        # # NOTE: file does not exist yet, and is created by temp_secret
        # filePath = os.path.join(sts.testDataDir, "temp_secret.yml")
        # with tempfile.temp_secret(*args, secretsFilePath=filePath, creds=self.creds,
        #                                             connector="joringels", **kwargs ) as t:
        #     with open(filePath, "r") as f:
        #         content = yaml.safe_load(f)
        # self.assertEqual(expected, content)


if __name__ == "__main__":
    with helpers.temp_password(pw=sts.testKeyOuter):
        unittest.main()

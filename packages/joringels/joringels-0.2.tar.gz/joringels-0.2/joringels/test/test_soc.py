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
import joringels.src.get_soc as soc

# print(f"\n__file__: {__file__}")


# jo upload -n safe_one -src kdbx -con scp -pr all
class Test_UnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.verbose = 0
        cls.safeIp = os.environ.get("DATASAFEIP")
        cls.prep_enc_path(*args, **kwargs)
        cls.testData = cls.get_test_data(*args, **kwargs)
        cls.isIp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        cls.dockerIp = r"172\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        if os.path.exists(cls.encryptPath):
            os.remove(cls.encryptPath)

    @classmethod
    def get_test_data(cls, *args, **kwargs):
        with open(os.path.join(sts.testDataDir, "test_soc.yml"), "r") as f:
            return yaml.safe_load(f)

    @classmethod
    def prep_enc_path(cls, *args, **kwargs):
        cls.encryptPath = os.path.join(sts.testDataDir, "safe_one.yml")
        if os.path.exists(cls.encryptPath):
            return True
        cls.encryptBackup = os.path.join(sts.testDataDir, "#safe_one.yml")
        # copying this file is needed because pre-commit fails on changes
        shutil.copyfile(cls.encryptBackup, cls.encryptPath)

    def test_derrive_host(self, *args, **kwargs):
        self.assertEqual(self.safeIp, soc.derrive_host(connector="joringels"))
        self.assertEqual("oamailer", soc.derrive_host(connector="oamailer"))
        self.assertNotEqual("oamailer", soc.derrive_host())
        self.assertTrue(re.match(self.isIp, soc.derrive_host()))

    def test_get_host(self, *args, **kwargs):
        # test joringels connector
        self.assertEqual(self.safeIp, soc.get_host(self.testData, connector="joringels"))
        self.assertEqual(self.safeIp, soc.get_host(self.testData))
        self.assertTrue(
            re.match(
                r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                soc.get_host(self.testData, host="localhost", connector="joringels"),
            )
        )
        # self.safeIp comes from env: DATASAFEIP and for some reason ipv4 changes frequently
        self.assertEqual(self.safeIp, soc.get_host(self.testData, host="localhost"))

        # if connector is an api (non-joringels), host comes from secrets
        with helpers.temp_ch_host_name(sts.devHost) as h:
            self.assertEqual(self.safeIp, soc.get_host(self.testData, connector="oamailer"))
        # this test assumes that cluster ip for oamailer is fixed
        with helpers.temp_ch_host_name("posix") as h:
            self.assertTrue(
                re.match(self.dockerIp, soc.get_host(self.testData, connector="oamailer"))
            )

        with helpers.temp_ch_host_name(sts.devHost) as h:
            local = soc.get_host(self.testData, host="localhost", connector="oamailer")
            apiHost = soc.get_host(self.testData, connector="oamailer")
            self.assertEqual(local, apiHost)
        with helpers.temp_ch_host_name("posix") as h:
            local = soc.get_host(self.testData, host="localhost", connector="oamailer")
            apiHost = soc.get_host(self.testData, connector="oamailer")
            self.assertNotEqual(local, apiHost)

    def test_get_port(self, *args, **kwargs):
        # locally
        self.assertEqual(7000, soc.get_port(self.testData, connector="joringels"))
        self.assertEqual(7000, soc.get_port(self.testData))
        self.assertEqual(7001, soc.get_port(self.testData, port="7001", connector="joringels"))
        self.assertEqual(7001, soc.get_port(self.testData, port=7001, connector="joringels"))
        self.assertEqual(7007, soc.get_port(self.testData, connector="oamailer"))
        self.assertEqual(7002, soc.get_port(self.testData, port="7002", connector="oamailer"))
        self.assertEqual(7002, soc.get_port(self.testData, port=7002, connector="oamailer"))

    def test_get_allowed_clients(self, *args, **kwargs):
        # the host machine ip address must allways be in allowed clients
        # NOTE: allowed_clients here come from dataSafe: safe_one [testData]
        print(soc.get_local_ip())
        print(", ".join(soc.get_allowed_clients()))
        self.assertIn(soc.get_local_ip(), ["168.172.69.69", "192.168.0.174"])


if __name__ == "__main__":
    with helpers.temp_password(pw=sts.testKeyOuter):
        unittest.main()

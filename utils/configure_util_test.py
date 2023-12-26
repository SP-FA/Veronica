import unittest

from utils.configure_util import ConfLoader


class MyTestCase(unittest.TestCase):
    def test_config_load(self):
        path = "../conf.yaml"
        conf = ConfLoader(path)
        print(conf)


if __name__ == '__main__':
    unittest.main()

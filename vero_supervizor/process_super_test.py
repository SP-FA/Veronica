import unittest

from VeroSuper import Supervisor


class MyTestCase(unittest.TestCase):
    def test_find_process(self):
        super = Supervisor()
        print(super)


if __name__ == '__main__':
    unittest.main()

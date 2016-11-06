import unittest

from WolfEyes import pyon

class testPyon(unittest.TestCase):

    def test_init(this):
        aa = '{"1": 0}'
        a = pyon(aa)

        bb = {1: 0}
        b = pyon(bb)

        this.assertEqual(str(a), str(b))

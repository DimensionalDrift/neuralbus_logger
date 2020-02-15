import unittest
import time
from neuralbus import buslogger

class TestBuslogger(unittest.TestCase):

    def setUp(self):
        self.buslog = buslogger.buslogger()


    def test_buscall_validjson(self):
        data = self.buslog.buscall(3146)

        self.assertIs(type(data), dict)

    def test_buscall_url(self):
        self.buslog.buscall(3146)

        self. assertIs(type(self.buslog.busurl()), str)

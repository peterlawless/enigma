import unittest

from rotors import Rotor


class MiniRotor(Rotor):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F']

    shift = ['D', 'F', 'B', 'E', 'C', 'A']

    turnover = ['D']


class MiniRotorTests(unittest.TestCase):
    def setUp(self):
        self.minirotor1 = MiniRotor()
        self.minirotor2 = MiniRotor()
        self.minirotor2.next_rotor = self.minirotor1

    def test_alphabet(self):
        assert self.minirotor1.alphabet == ['A', 'B', 'C', 'D', 'E', 'F']

    def test_shift(self):
        assert self.minirotor1.shift == ['D', 'F', 'B', 'E', 'C', 'A']

    def test_turnover(self):
        assert self.minirotor1.turnover == ['D']

    def test_wiring(self):
        assert self.minirotor1.wiring == [(3, 'D'), (4, 'F'), (-1, 'B'),
                                          (1, 'E'), (-2, 'C'), (-5, 'A')]

    def test_calibrate_one(self):
        self.minirotor1.calibrate(1)
        assert self.minirotor1.wiring == [(3, 'D'), (4, 'F'), (-1, 'B'),
                                          (1, 'E'), (-2, 'C'), (-5, 'A')]

    def test_calibrate_two(self):
        self.minirotor1.calibrate(2)
        assert self.minirotor1.wiring == [(4, 'F'), (-1, 'B'), (1, 'E'),
                                          (-2, 'C'), (-5, 'A'), (3, 'D')]

    def test_rotate(self):
        self.minirotor1.rotate()
        assert self.minirotor1.wiring == [(4, 'F'), (-1, 'B'), (1, 'E'),
                                          (-2, 'C'), (-5, 'A'), (3, 'D')]

    def test_rotate_turnover(self):
        self.minirotor2.rotate()
        assert self.minirotor1.wiring == [(4, 'F'), (-1, 'B'), (1, 'E'),
                                          (-2, 'C'), (-5, 'A'), (3, 'D')]

    def test_encrypt_connect(self):
        x = self.minirotor1.encrypt_connect(1)
        assert x == 5

    def test_decrypt_connect(self):
        assert self.minirotor1.decrypt_connect(5) == 1

if __name__ == '__main__':
    unittest.main()

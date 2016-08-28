class Rotor:
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

    # The shift in effect defines a Ceasar Cipher for each letter
    # of the alphabet. In this case, each letter is mapped onto itself and
    # the plaintext and ciphertext would be one and the same.
    shift = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # The turnover point is the contact (in reference to the shift) that is
    # visible in the Enigma's rotor window when the rotation notch will rotate
    # the neighboring rotor with its next rotation.
    turnover = ['A']

    def __init__(self, next_rotor=None):
        self.next_rotor = next_rotor
        self.get_wiring()

    def get_wiring(self):
        wiring = []
        for a, s in zip(self.alphabet, self.shift):
            dist = self.alphabet.index(s) - self.alphabet.index(a)
            wire = (dist, s)
            wiring.append(wire)
        self.wiring = wiring

    # The .calibrate() method allows the rotors to be oriented to start on any
    # of their 26 contact points. While the Python code utilizes zero-based
    # indexing, the user experience of this program attempts to be true to the
    # original Enigma by using one-based indexing as the actual rotors
    # were labeled.
    def calibrate(self, num):
        if not isinstance(num, int):
            raise TypeError("NEIN! The .calibrate() method only accepts\
                             integer inputs")
        x = num - 1 % len(self.alphabet)
        rotation = self.wiring[:x]
        self.wiring.extend(rotation)
        del self.wiring[:x]

    def rotate(self):
        x = self.wiring.pop(0)
        if x[1] in self.turnover and isinstance(self.next_rotor, Rotor):
            self.next_rotor.rotate()
        self.wiring.append(x)

    def encrypt_connect(self, num):
        x = (num + self.wiring[num][0]) % len(self.alphabet)
        return x

    def decrypt_connect(self, num):
        for idx, wire in enumerate(self.wiring):
            if ((idx + wire[0]) % len(self.alphabet)) == num:
                return idx


class RotorI(Rotor):
    shift = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O',
             'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J']

    turnover = ['Q']


class RotorII(Rotor):
    shift = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W',
             'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E']

    turnover = ['E']


class RotorIII(Rotor):
    shift = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z',
             'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O']

    turnover = ['V']


class RotorIV(Rotor):
    shift = ['E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R',
             'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B']

    turnover = ['J']


class RotorV(Rotor):
    shift = ['V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N',
             'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K']

    turnover = ['Z']


class RotorVI(Rotor):
    shift = ['J', 'P', 'G', 'V', 'O', 'U', 'M', 'F', 'Y', 'Q', 'B', 'E', 'N',
             'H', 'Z', 'R', 'D', 'K', 'A', 'S', 'X', 'L', 'I', 'C', 'T', 'W']

    turnover = ['Z', 'M']


class RotorVII(Rotor):
    shift = ['N', 'Z', 'J', 'H', 'G', 'R', 'C', 'X', 'M', 'Y', 'S', 'W', 'B',
             'O', 'U', 'F', 'A', 'I', 'V', 'L', 'P', 'E', 'K', 'Q', 'D', 'T']

    turnover = ['Z', 'M']


class RotorVIII(Rotor):
    shift = ['F', 'K', 'Q', 'H', 'T', 'L', 'X', 'O', 'C', 'B', 'J', 'S', 'P',
             'D', 'Z', 'R', 'A', 'M', 'E', 'W', 'N', 'I', 'U', 'Y', 'G', 'V']

    turnover = ['Z', 'M']

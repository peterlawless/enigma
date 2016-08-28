import rotors
import re


# Simulates Enigma M4, which was used exclusively by the U-Boot
# division of the German Navy (Kriegsmarine).
class Enigma:
    # Simulates UKW-B reflector, which was used throughout the war
    reflector = {0: 4, 1: 13, 2: 10, 3: 16, 4: 0, 5: 20, 6: 24, 7: 22, 8: 9,
                 9: 8, 10: 2, 11: 14, 12: 15, 13: 1, 14: 11, 15: 12, 16: 3,
                 17: 23, 18: 25, 19: 21, 20: 5, 21: 19, 22: 7, 23: 17, 24: 6,
                 25: 18}

    entrywheel = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                  'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13,
                  'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
                  'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

    reentry_wheel = {number: letter for letter, number in entrywheel.items()}

    def __init__(self, slow_rotor=rotors.RotorI(),
                 middle_rotor=rotors.RotorII(), fast_rotor=rotors.RotorIII(),
                 initial_settings=(1, 1, 1)):

        if not isinstance(slow_rotor, rotors.Rotor):
            raise TypeError("NEIN! The slow_rotor must be a Rotor object.")
        if not isinstance(middle_rotor, rotors.Rotor):
            raise TypeError("NEIN! The middle_rotor must be a Rotor object")
        if not isinstance(fast_rotor, rotors.Rotor):
            raise TypeError("NEIN! Das schnell_rotor must be a Rotor object")
        if not all([isinstance(x, int) for x in initial_settings]):
            raise TypeError("NEIN! All initial_settings must be integers.")

        self.slow_rotor = slow_rotor
        self.middle_rotor = middle_rotor
        self.fast_rotor = fast_rotor

        # Making the fast and middle rotors aware of their neighbor allows
        # their .rotate() method to rotate their neighbor too when the contact
        # containing the turnover point is rotated (like an odometer rolling
        # over)
        self.fast_rotor.next_rotor = middle_rotor
        self.middle_rotor.next_rotor = slow_rotor

        self.slow_rotor.calibrate(initial_settings[0])
        self.middle_rotor.calibrate(initial_settings[1])
        self.fast_rotor.calibrate(initial_settings[2])

    # Turns input letter into a number on the entry wheel, then passes the
    # number through the three rotors via the .encrypt_connect() method to the
    # reflector, turned back to the rotors then back through the three rotors
    # via the .decrypt_connect() method to the reentry wheel, which is just
    # the dictionary inverse of the entry wheel. This returns an encrypted
    # letter.
    def encrypt(self, letter):
        number = self.entrywheel[letter]
        self.fast_rotor.rotate()
        fr = self.fast_rotor.encrypt_connect(number)
        mr = self.middle_rotor.encrypt_connect(fr)
        sr = self.slow_rotor.encrypt_connect(mr)
        reflection = self.reflector[sr]
        sr_ref = self.slow_rotor.decrypt_connect(reflection)
        mr_ref = self.middle_rotor.decrypt_connect(sr_ref)
        fr_ref = self.fast_rotor.decrypt_connect(mr_ref)
        cipherletter = self.reentry_wheel[fr_ref]
        return cipherletter


def main():
    rotor_dict = {'I': rotors.RotorI(), 'II': rotors.RotorII(),
                  'III': rotors.RotorIII(), 'IV': rotors.RotorIV(),
                  'V': rotors.RotorV(), 'VI': rotors.RotorVI(),
                  'VII': rotors.RotorVII(), 'VIII': rotors.RotorVIII()}

    rotor_selection = input("Enter your rotor labels (roman numerals) from left\
 to right (slow to fast rotor) separated by spaces:\n").upper()

    match = re.search(r'^([IV]{,4})\s([IV]{,4})\s([IV]{,4})$', rotor_selection)

    if match:
        slow_rotor_key, middle_rotor_key, fast_rotor_key = match.groups()
        slow_rotor = rotor_dict[slow_rotor_key]
        middle_rotor = rotor_dict[middle_rotor_key]
        fast_rotor = rotor_dict[fast_rotor_key]

    setting_selection = input("Now enter the intial settings of your rotors\
 (integers 1-26) in the same order separated by spaces:\n")
    match = re.search(r'^([1-2]?[0-9])\s([1-2]?[0-9])\s([1-2]?[0-9])$',
                      setting_selection)

    if match:
        slow_rotor_set, middle_rotor_set, fast_rotor_set = match.groups()

        initial_settings = (int(slow_rotor_set), int(middle_rotor_set),
                            int(fast_rotor_set))

    enigma = Enigma(slow_rotor, middle_rotor, fast_rotor, initial_settings)
    message = input('Enter your message to encrypt: ').upper()
    plaintext = []
    for character in message:
        if character in enigma.entrywheel:
            plaintext.append(character)
    ciphertext = []
    for character in plaintext:
        ciphertext.append(enigma.encrypt(character))
    print(''.join(ciphertext))


if __name__ == '__main__':
    main()

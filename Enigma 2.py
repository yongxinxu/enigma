alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Plugboard:
    def __init__(self, connected_letters):
        self.connection = dict(zip(alphabet, connected_letters))

    def encrypt(self, character):
        return self.connection[character]

    def __repr__(self):
        return str(self.connection)

class Rotor:
    def __init__(self, connected_letters, letter):
        self.initial = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.connected_letters = connected_letters
        self.input_connection = dict(zip(alphabet, connected_letters))
        self.output_connection = dict(zip(connected_letters, alphabet))
        self.turn_over = letter
        self.next_rotate = False

    def encrypt1(self, character): #input
        return self.input_connection[character]

    def encrypt2(self, character): #output
        return self.output_connection[character]

    def rotate(self): #rotate the alphabet
        self.alphabet = self.alphabet[1:] + self.alphabet[0]
        self.input_connection = dict(zip(self.alphabet, self.connected_letters))
        self.output_connection = dict(zip(self.connected_letters, self.alphabet))
        if self.alphabet[0] == self.turn_over: #signals the next rotor to rotate
            self.next_rotate = True

    def reset_rotor(self): #back to the initial setting
        self.input_connection = dict(zip(self.initial, self.connected_letters))
        self.output_connection = dict(zip(self.connected_letters, self.initial))
        self.next_rotate = False
        self.alphabet = self.initial

    def set_to(self, letter): #rotate the rotor to specific letter
        while self.alphabet[0] != letter:
            self.rotate()
        self.next_rotate = False

    def __repr__(self):
        return str(self.input_connection) + "{" + str(self.turn_over) + "}"

class Reflector:
    def __init__(self, connected_letters):
        self.connection = dict(zip(alphabet, connected_letters))

    def encrypt(self, character):
        return self.connection[character]

    def __repr__(self):
        return str(self.connection)

class Enigma:
    def __init__(self, Plugboard, Rotors, Reflector):
        self.plugboard = Plugboard
        self.rotors = Rotors
        self.reflector = Reflector

    def encrypt_text(self, text): #encrypt a long text
        answer = ""
        for letter in text:
            answer += self.encrypt(letter)
            
            self.rotors[0].rotate() #rotor rotates
            if self.rotors[0].next_rotate: #check if the next rotor needs to rotate
                self.rotors[1].rotate()
                self.rotors[0].next_rotate = False
            if self.rotors[1].next_rotate:
                self.rotors[2].rotate()
                self.rotors[1].next_rotate = False
        return answer

    def encrypt(self, character): #encrypt one single character
        x = self.plugboard.encrypt(character)
        x = self.rotors[0].encrypt1(x)
        x = self.rotors[1].encrypt1(x)
        x = self.rotors[2].encrypt1(x)
        x = self.reflector.encrypt(x)
        x = self.rotors[2].encrypt2(x)
        x = self.rotors[1].encrypt2(x)
        x = self.rotors[0].encrypt2(x)
        x = self.plugboard.encrypt(x)
        return x

    def reset(self):
        for rotor in self.rotors:
            rotor.reset_rotor()



class Codebreaker:
    def __init__(self, Enigma, Ciphertext, Crib):
        self.ciphertext = Ciphertext
        self.enigma = Enigma
        self.crib = Crib #plaintext
 
    def decrypt(self):
        answer = []
        for x in alphabet:
            self.enigma.rotors[2].set_to(x)
            for y in alphabet:
                self.enigma.rotors[1].set_to(y)
                for z in alphabet:
                    self.enigma.rotors[0].set_to(z)
                    self.enigma.rotors[2].set_to(x)
                    self.enigma.rotors[1].set_to(y)
                    possible = self.enigma.encrypt_text(self.ciphertext)
                    if self.crib in possible:
                        answer.append(possible)
        return answer
    

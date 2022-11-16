import random


class Password:
    def __init__(self):
        self.password = ""

    def create_pass(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        random.shuffle(letters)
        random.shuffle(numbers)

        new_password = []

        for i in range(8):
            new_password.append(random.choice(letters))
        for i in range(4):
            new_password.append(random.choice(numbers))

        random.shuffle(new_password)
        final = ''.join(new_password)

        self.password = final
        return final

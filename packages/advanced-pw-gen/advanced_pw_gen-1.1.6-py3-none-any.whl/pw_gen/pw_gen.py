import random
from pw_gen_utils import *
class Password():
    def __init__(self, pw_length: int, pw_types:str) -> None:
        self.pw_length: int = pw_length
        self.pw_types: list = Password.createTypes(pw_types)
        self.minus_legible = self.pw_types.copy()
        if 'legible' in self.pw_types:
            self.minus_legible.remove('legible')
    def password(self):
        if (len(self.minus_legible) <= self.pw_length) and Password.validateTypes(self.pw_types):
            return Password.createOutputString(self.createPass())
        else:
            raise PasswordException(self.minus_legible, self.pw_length)
        
    def getAlpha() -> list:
        return read_file('input_tables/alpha_chars.txt').split('\n')
    def getSpecial() -> list:
        return read_file('input_tables/special_chars.txt').split('\n')
    def getLower() -> list:
        lowers = read_file('input_tables/alpha_chars.txt').split('\n')
        return [x.lower() for x in lowers]
    def getTypes() -> list:
        return read_file('input_tables/types.txt').split('\n')
    def getNumbers() -> list:
        return [str(n) for n in range(0,9)]
    def getUnlegibles() -> list:
        return read_file('input_tables/unlegibles.txt').split('\n')
    def randomLegible(type) -> str:
        if type == 'number':
            possibilities = Password.getNumbers()
        elif type == 'upper':
            possibilities = Password.getAlpha()
        elif type == 'lower':
            possibilities = Password.getLower()
        elif type == 'special':
            possibilities = Password.getSpecial()
        for unlegible in Password.getUnlegibles():
            for index, possibility in enumerate(possibilities):
                if unlegible == possibility:
                    possibilities.pop(index)
        return random.choice(possibilities)
    def randomNumber() -> str:
        return str(random.randint(0,9))
    def randomUpper() -> str:
        return random.choice(Password.getAlpha())
    def randomLower() -> str:
        return random.choice(Password.getLower())
    def randomSpecial() -> str:
        return random.choice(Password.getSpecial())
    def validateTypes(types:list) ->list:
        possible_types = Password.getTypes()
        for item in types:
            if item not in possible_types:
                return False
        return True
    def createTypes(types: str) -> list:
        types = types.replace(' ', '')
        return types.split(',')
    def createOutputString(pas: list) -> str:
        return ''.join(pas)
    def replaceUnlegible(self, pass_list:list) -> str:
        for index, char in enumerate(pass_list):
            if char in Password.getUnlegibles():
                if pass_list[index] in Password.getAlpha():
                    Password.randomLegible('upper')
                elif pass_list[index] in Password.getLower():
                    Password.randomLegible('lower')
                elif pass_list[index] in Password.getNumbers():
                    Password.randomLegible('number')
                elif pass_list[index] in Password.getSpecial():
                    Password.randomLegible('special')
                # pass_list[index] = Password.randomLegible(random.choice(self.minus_legible))
        return(pass_list)
    def createPass(self) -> str:
        pass_list = []
        for i in range(self.pw_length):
            random_type = random.choice(self.minus_legible)
            if random_type == 'number':
                pass_list.append(Password.randomNumber())
            if random_type == 'upper':
                pass_list.append(Password.randomUpper())
            if random_type == 'lower':
                pass_list.append(Password.randomLower())
            if random_type == 'special':
                pass_list.append(Password.randomSpecial())
        if 'legible' in self.pw_types:
            pass_list = self.replaceUnlegible(pass_list)
        return pass_list
    def printPasswordTypes() -> None:
        print(read_file('input_tables/types.txt'))
class PasswordException(Exception):
    def __init__(self, pw_types:list, pw_length:int) -> None:
        self.pw_types = pw_types
        self.pw_length = pw_length
        if len(self.pw_types) > self.pw_length:
            self.message = f'There are more password types than the password length.\n{len(pw_types)} > {pw_length}\nMake sure your password length is longer or equivilant to the number of types.'
        elif Password.validateTypes(pw_types) == False:
            self.message = f'You entered an invalid type. Valid types are {Password.getTypes()}'
        super().__init__(self.message)
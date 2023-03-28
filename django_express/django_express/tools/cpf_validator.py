from django.core.exceptions import ValidationError
from colorama import Fore, init
init(autoreset=True)


class Cpfvalidator:

    def __init__(self, cpf):
        self.cpf = cpf
        self.answers = []
        self.numbers = '0123456789'

    def verifysize(self):
        if len(self.cpf) != 10:
            return False
        else:
            return True

    def verifynumbers(self):
        for i in self.cpf:
            if i in self.numbers:
                print(Fore.GREEN + f'I: {i} OK!')
            else:
                print(Fore.RED + f'I: {i} NOK!')
                return False
                break
        return True

    def verify1(self):
        limit = 10
        opsum = 0
        for i in range(len(self.cpf) - 2):
            print(Fore.YELLOW + f'V1-> i: {self.cpf[i]}, limit: {limit}, result: {int(self.cpf[i]) * limit}')
            temp = int(self.cpf[i]) * limit
            limit -= 1
            opsum += temp
        result = (opsum * 10) % 11
        if result == 10:
            result = 0
        if result == int(self.cpf[-2]):
            self.answers.append(True)
        else:
            self.answers.append(False)
        
    def verify2(self):
        if self.answers[0] == True:
            limit = 11
            opsum = 0
            for i in range(len(self.cpf) - 1):
                print(Fore.YELLOW + f'V2-> i: {self.cpf[i]}, limit: {limit}, result: {int(self.cpf[i]) * limit}')
                temp = int(self.cpf[i]) * limit
                limit -= 1
                opsum += temp
            result = (opsum * 10) % 11
            if result == 10:
                result = 0
            if result == int(self.cpf[-1]):
                self.answers.append(True)
        self.answers.append(False)

    def test(self):
        self.verify1()
        self.verify2()
        if self.answers[0] == True and self.answers[1] == True:
            print(Fore.GREEN + 'Valid CPF!')
            return True
        else:
            print(Fore.RED +'Invalid CPF!')
            return False

from lib.error import Error
from tests.testBase import TestBase


class TestBinary(TestBase):
    def test_addition(self):
        code = "print(5 + 5);"
        assert self.interpret(code) == '10.0'

    def test_addition_float(self):
        code = "print(5.5 + 5);"
        assert self.interpret(code) == '10.5'

    def test_subtraction(self):
        code = "print(10 - 5);"
        assert self.interpret(code) == '5.0'

    def test_subtraction_float(self):
        code = "print(10 - 5.5);"
        assert self.interpret(code) == '4.5'

    def test_multiplication(self):
        code = "print(10 * 5);"
        assert self.interpret(code) == '50.0'

    def test_multiplication_float(self):
        code = "print(10.3 * 5.2);"
        assert self.interpret(code) == '53.56'

    def test_division(self):
        code = "print(50 / 5);"
        assert self.interpret(code) == '10.0'

    def test_division_float(self):
        code = "print(55.5 / 4.2);"
        assert self.interpret(code) == '13.214285714285714'
    
    def test_operation_order(self):
        code = "print(10 + 5 / 5 * 3 + 4 / 3);"
        assert self.interpret(code) == '14.333333333333334'

    def test_parentheses_order(self):
        code = "print(10*(5+(50/34)-40+(30/2+5)));"
        assert self.interpret(code) == '-135.29411764705884'
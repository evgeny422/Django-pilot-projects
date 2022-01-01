from django.test import TestCase

from store.logic import operate


class LogicTestCase(TestCase):
    # обязательный синтаксис
    def test_plus(self):
        result = operate(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operate(2, 3, '-')
        self.assertEqual(-1, result)

    def test_multiply(self):
        result = operate(2, 3, '*')
        self.assertEqual(6, result)

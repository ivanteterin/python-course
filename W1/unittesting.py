class TestFactorize(unittest.TestCase):
    
    def test_wrong_types_raise_exception(self):
        cases = ['string', 1.5]
        for b in cases:
            with self.subTest(case=b):
#                 a=list(b)
#                 factorize(a)
                self.assertRaises(TypeError, factorize, b)
    
    def test_negative(self):
        cases = [-1, -10, -100]
        for b in cases:
            with self.subTest(case=b):
                self.assertRaises(ValueError, factorize, b)
                
    def test_zero_and_one_cases(self):
        cases = [0, 1]
        expected = [(0,), (1,)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                a=factorize(cases[i])
                self.assertEqual(a, expected[i])
                
    def test_simple_numbers(self):
        cases = [3, 13, 29]
        expected = [(3,), (13,), (29,)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                a=factorize(cases[i])
                self.assertEqual(a, expected[i])
                
    def test_two_simple_multipliers(self):
        cases = [6, 26, 121]
        expected = [(2, 3), (2, 13), (11, 11)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                a=factorize(cases[i])
                self.assertEqual(a, expected[i])
                
    def test_many_multipliers(self):
        cases = [1001, 9699690]
        expected = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                a=factorize(cases[i])
                self.assertEqual(a, expected[i])
import unittest
from arrendatools.plantillas.filters.numeros import formato_divisa, formato_porcentaje, numero_a_palabras


class TestFunciones(unittest.TestCase):

    def test_formato_divisa(self):
        self.assertEqual(formato_divisa(1234.56), '1.234,56\xa0€')
        self.assertEqual(formato_divisa(1234.56, simbolo='$', locale='en_US'), '$1,234.56')
        self.assertEqual(formato_divisa(1234.56, formato='¤ #,##0.00', redondeo_decimal=False), '€ 1.234,56')

    def test_formato_porcentaje(self):
        self.assertEqual(formato_porcentaje(0.25), '25\xa0%')
        self.assertEqual(formato_porcentaje(0.25, formato='0.00%'), '25,00%')
        self.assertEqual(formato_porcentaje(0.25, locale='en_US'), '25%')

    def test_numero_a_palabras(self):
        self.assertEqual(numero_a_palabras(123.45), 'ciento veintitrés euros con cuarenta y cinco céntimos')
        self.assertEqual(numero_a_palabras(123.45, idioma='en'), 'one hundred and twenty-three euro, forty-five cents')
        self.assertEqual(numero_a_palabras(123, conversor='ordinal'), 'centésimo vigésimo tercero')


if __name__ == '__main__':
    unittest.main()

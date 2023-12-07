import unittest

from i2c_registers.i2c_register_section import I2cRegisterSection


class I2cRegisterSectionTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.section = I2cRegisterSection("test", 0, 7, [0] * 8)

    def test_section_properties(self):
        self.assertEqual("TEST", self.section.name)  # add assertion here
        self.assertEqual(0, self.section.lsb)
        self.assertEqual(7, self.section.msb)
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], self.section.bits)

    def test_lsb_higher_than_msb(self):
        with self.assertRaises(ValueError):
            seg = I2cRegisterSection("test", 7, 0, [0] * 8)

    def test_provided_bits_too_small(self):
        with self.assertRaises(IndexError):
            seg = I2cRegisterSection("test", 0, 7, [0])

    def test_set_bits(self):
        new_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        self.section.set_bits(new_bits)

        self.assertEqual([0, 1, 0, 1, 0, 1, 0, 1], self.section.bits)

    def test_set_bits_error(self):
        new_bits = [1, 0, 1, 0, 2, 0, 1, 0]
        with self.assertRaises(ValueError):
            self.section.set_bits(new_bits)


class I2cRegisterSectionConversionTestCase(unittest.TestCase):

    def test_bits_to_int(self):
        self.section = I2cRegisterSection("test", 0, 7, [0, 0, 0, 1, 0, 0, 0, 0])
        result = self.section.bits_to_int()
        self.assertEqual(16, result)

    def test_bits_to_twos_comp_int(self):
        self.section = I2cRegisterSection("test", 0, 7, [0, 0, 0, 1, 0, 0, 0, 0])
        result = self.section.bits_to_twos_comp_int()
        self.assertEqual(16, result)

    def test_bits_to_int_nibble(self):
        self.section = I2cRegisterSection("test", 0, 3, [0, 1, 0, 0])
        result = self.section.bits_to_int()
        self.assertEqual(4, result)

    def test_bits_to_twos_comp_int_nibble(self):
        self.section = I2cRegisterSection("test", 0, 3, [0, 1, 0, 0])
        result = self.section.bits_to_twos_comp_int()
        self.assertEqual(4, result)


class I2cRegisterSectionToBitsTestCase(unittest.TestCase):
    def test_i2c_register_section_to_bits(self):
        self.assertEqual([0, 0, 0, 0, 1, 1, 0, 0], I2cRegisterSection.to_bits(12, 8))

    def test_i2c_register_section_to_bits_zero(self):
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], I2cRegisterSection.to_bits(0, 8))


class I2cRegisterSectionToTwosCompIntTestCase(unittest.TestCase):
    def test_i2c_register_section_to_twos_comp_int(self):
        self.assertEqual(12, I2cRegisterSection.to_twos_comp_int([0, 0, 1, 1, 0, 0, 0, 0]))

    def test_i2c_register_section_to_twos_comp_int_negative(self):
        self.assertEqual(-6, I2cRegisterSection.to_twos_comp_int([0, 1, 0, 1, 1, 1, 1, 1]))


class I2cRegisterSectionNumBytesForBitsTestCase(unittest.TestCase):
    def test_lower_range(self):
        self.assertEqual(I2cRegisterSection.num_bytes_for_bits(2), 1)

    def test_upper_range(self):
        self.assertEqual(I2cRegisterSection.num_bytes_for_bits(7), 1)

    def test_simple_overflow(self):
        self.assertEqual(I2cRegisterSection.num_bytes_for_bits(9), 2)

    def test_zero(self):
        self.assertEqual(I2cRegisterSection.num_bytes_for_bits(0), 0)


if __name__ == '__main__':
    unittest.main()

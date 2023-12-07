#!/usr/bin/python3
import math


class I2cRegisterSection:

    @staticmethod
    def to_int(bits):
        result = 0
        for bit in bits:
            result = (result << 1) | bit

        return result

    @staticmethod
    def to_bits(number, size):
        bits = size
        if number > 0:
            bits = int(max(size, int(math.log(number, 2)) + 1))

        result = [1 if number & (1 << (bits - 1 - n)) else 0 for n in range(bits)]

        return result

    @staticmethod
    def to_twos_comp_int(bits):
        bits_str = ""

        for b in reversed(bits):
            bits_str += str(b)

        size = len(bits)
        result = int(bits_str, 2)

        if (result & (1 << (size - 1))) != 0:
            result = result - (1 << size)

        return result

    @staticmethod
    def num_bytes_for_bits(bits):
        return int(math.ceil(float(bits) / 8.0))

    @staticmethod
    def to_padded_byte_arr(bits):
        result = []
        byte_slice_lower = 0  # Increases by 8 for each byte

        # Determine how many bytes the provided bits are and loop that many times
        # Each loop "synthesizes" a new byte from the bits array
        for byte_i in range(I2cRegisterSection.num_bytes_for_bits(len(bits))):
            # Check that upper limit isn't too big
            byte_slice_upper = ((byte_i + 1) * 8) - 1  # The index we *want* to slice to
            to_pad = 0  # Used to keep track of how many 0s we need to pad the end of this byte
            if byte_slice_upper > len(bits) - 1:
                # Keep track of the fact that we need to pad the end of this byte with some 0s
                to_pad = byte_slice_upper - (len(bits) - 1)

                # Resize if index we wanted to slice to is too big
                byte_slice_upper = len(bits) - 1

            # Convert
            # Add 1 to byte_slice_upper because upper range of slice is not inclusive
            byte_slice = bits[byte_slice_lower:byte_slice_upper + 1]

            # Append padding
            if to_pad > 0:
                byte_slice.extend([0] * to_pad)

            byte = I2cRegisterSection.to_int(byte_slice[::-1])
            result.append(byte)

            # Add 8 to lower slice bound for next byte
            byte_slice_lower += 8

        return result

    def __init__(self,
                 name: str,
                 lsb: int,
                 msb: int,
                 bits: list[int]) -> None:
        """
        Creates a Register Section instance

        :param name: Name of section
        :param lsb: Index of LSB (the least significant bit)
        :param msb: Index of MSB (the most significant bit)
        :param bits: List of bits, each element of list is either 0 or 1. The bit order: 7 6 5 4 3 2 1 0
        :raises IndexError: If length of bits array is less than that defined by lsb and msb
        :raises ValueError: If lsb or msb is not in the range [0, 7] or lsb and msb are greater or
                          less than each other in wrong way
        """

        self.name = name.upper()

        # Sanity check LSB and MSB indexes
        if lsb > msb:
            msg = "LSB index can not be greater than MSB index, lsb_i: {}, msb_i: {}"
            raise ValueError(msg.format(lsb, msb))

        self.lsb = lsb
        self.msb = msb
        self.bits: list[int] = []
        _bits = bits[:]
        self.set_bits(_bits)

    def __len__(self):
        """
        Get length of register section.

        Uses lsb and msb to calculate.
        :return: The Number of bits represented by RegisterSection.
        """
        return self.msb - self.lsb + 1

    def __str__(self):
        """
        Gets a string representation of the section.
        :return: A formatted string.
        """
        msg = "RegisterSegment<name={}, lsb={}, msb={}, bits={}>"
        bits = self.get_bits()
        return msg.format(self.name, self.lsb, self.msb, bits)

    def bits_to_int(self):
        _bits = self.bits[::-1]
        return I2cRegisterSection.to_int(_bits)

    def bits_to_twos_comp_int(self):
        return I2cRegisterSection.to_twos_comp_int(self.bits)

    def update_bits(self, reg_bytes) -> None:
        """
        Updates the bits for the section from byte values
        :param reg_bytes: The register byte values e.g. [[0xFE],[0xFE]]
        """
        # Check that bytes array contains values inside lsb and msb range
        min_bytes = I2cRegisterSection.num_bytes_for_bits(self.msb + 1)
        if len(reg_bytes) < min_bytes:
            msg = "Provided bytes array does not contain enough bytes to fill MSB, bytes: {}, \
            MSB index: {}, required bytes length: {}"

            raise KeyError(msg.format(reg_bytes, self.msb, min_bytes))

        # Determine start and end byte by dividing lsb & msb by 8 and rounding down
        start_byte = int(math.floor(float(self.lsb) / 8.0))
        end_byte = int(math.floor(float(self.msb) / 8.0))

        # Convert needed bytes into bits
        # Keys will be offset by start_byte
        needed_bytes_as_bits = []

        for byte_ix in range(start_byte, end_byte + 1):
            byte = reg_bytes[byte_ix]
            converted_bits = I2cRegisterSection.to_bits(byte, 8)

            # Convert bits and check bits are all 0 or 1
            for i in range(len(converted_bits)):
                converted_bits[i] = int(converted_bits[i])

            needed_bytes_as_bits.append(converted_bits[::-1])

        # Loop through bits
        for bit_ix in range(self.lsb, self.msb + 1):
            in_byte_i = int(math.floor(float(bit_ix) / 8.0))
            bit_offset = (in_byte_i * 8)  # Used to figure out which bit in the byte we are in

            self.bits[bit_ix - self.lsb] = needed_bytes_as_bits[in_byte_i - start_byte][bit_ix - bit_offset]

        return

    def set_bits(self, bits: list[int]):
        """
        Set section bits

        Runs some sanity checks on the new bits before setting them.

        :param bits: List of bits, each element of list is either 0 or 1. The bit order: 7 6 5 4 3 2 1 0
        :raises IndexError: If length of bits array is less than that defined by lsb and msb
        :raises ValueError: If an element of the provided bits array is not equal to 0 or 1
        """
        if len(bits) != len(self):
            msg = "Default list must be size that specified by lsb and msb, was: {}, should be: {}"
            raise IndexError(msg.format(len(bits), len(self)))

        is_valid_list = [True if b == 1 or b == 0 else False for b in bits]

        if False in is_valid_list:
            msg = "Bits can only have the integer values 0 or 1"
            raise ValueError(msg)

        _bits = bits[:]  # Copy List -> bit order => 7 6 5 4 3 2 1 0
        rev_bits = _bits[::-1]  # Reverse List -> bit order => 0 1 2 3 4 5 6 7
        self.bits = rev_bits  # Assign to property/ attribute

    def get_bits(self) -> list[int]:
        """
        Gets the section bits.
        :return: List of bits, each element of list is either 0 or 1. The bit order: 7 6 5 4 3 2 1 0
        """
        _bits = self.bits[:]

        return _bits[::-1]

    def get_index(self, bit_index):
        """
        Gets the section index from the register bit index
        :param bit_index: The register bit index. The bit order: 7 6 5 4 3 2 1 0
        :return: The corresponding section bit index
        """
        return bit_index - self.lsb

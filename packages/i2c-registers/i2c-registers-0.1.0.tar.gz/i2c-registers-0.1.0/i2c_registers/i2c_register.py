#!/usr/bin/python3
from enum import Flag, auto

from i2c_registers.i2c_register_section import I2cRegisterSection


class RegisterOperations(Flag):
    Read = auto()
    Write = auto()
    ReadWrite = Read | Write


class I2cRegister:
    __parent = None
    __managing_sections = {}

    def __init__(self,
                 name: str,
                 reg_addr: int,
                 op_mode: RegisterOperations,
                 signed: bool,
                 sections: dict[str, I2cRegisterSection]):
        self.name = name.upper()
        self.reg_addr = reg_addr
        self.op_mode = op_mode
        self.signed = signed
        self.sections = {k.upper(): v for k, v in sections.items()}

        return

    @property
    def value(self) -> int:
        return self.get_value()

    def __len__(self):
        """
        Gets the length of register in bits.
        :return: The total number of bits for the register.
        """
        result = 0
        for section in self.sections:
            result += len(self.sections[section])

        return result

    def __str__(self):
        """
        Gets a string representation of the register.
        :return: A formatted string.
        """
        result = "Register<name={}, address={}, op_mode={}, sections={{\n"
        result.format(self.name, self.reg_addr, self.op_mode.name)
        for key in self.sections:
            section = self.sections[key]
            result += "    {}={}\n".format(key, str(section))

        result += "}>"

        return result

    def set_parent(self, parent):
        """
        Sets the Parent Device for the register.
        :param parent: The parent Device (I2cDevice)
        """
        self.__parent = parent

        return

    def len_bytes(self):
        """
        Length of the register in bytes.
        :return: The total number of bytes for the register.
        """
        return I2cRegisterSection.num_bytes_for_bits(len(self))

    def get_section(self, name: str) -> I2cRegisterSection:
        """
        Gets a Register Section by name.
        :param name: The section name.
        :return: The I2cRegisterSection for the name provided.
        :raises KeyError: If the section does not exist.
        """
        key = name.upper()
        if key not in self.sections:
            raise KeyError("No section found with name: \"{}\"".format(name))

        self._check_sections()
        return self.sections[key]

    def add_section(self, name: str, lsb: int, msb: int, bits: list[int]):
        """
        Add Register Section

        :param name: Name of the section
        :param lsb: Index of LSB (the least significant bit)
        :param msb: Index of MSB (the most significant bit)
        :param bits: List of bits, each element of list is either 0 or 1. The bit order: 7 6 5 4 3 2 1 0
        :return: The current Register, for chain adding of I2cRegisterSection to same Register
        :raises KeyError: If the sections has already been added
        """
        key = name.upper()
        if key in self.sections:
            raise KeyError("I2cRegisterSection with name already exists. name: {}".format(name))

        self.sections[key] = I2cRegisterSection(name.upper(), lsb, msb, bits)

        return self

    def add_not_used_section(self, lsb: int, msb: int):
        """
        Add Not Used Register Section

        :param lsb: Index of LSB (the least significant bit)
        :param msb: Index of MSB (the most significant bit)
        :return: The current Register, for chain adding of I2cRegisterSection to same Register
        """
        name = "NU{}_{}".format(lsb, msb)
        self.add_section(name, lsb, msb, [0] * (msb - lsb + 1))

        return self

    def set_section_bits(self, name: str, bits: list[int]) -> None:
        """
        Sets all the bits for the section
        :param name: Name of the section
        :param bits: List of bits, each element of list is either 0 or 1. The bit order: 7 6 5 4 3 2 1 0
        :return: None
        """
        self.get_section(name).set_bits(bits)

        return

    def set_bit(self, bit_index: int) -> None:
        """
        Sets the bit to 1 for the given bit index
        :param bit_index: The bit index of the bit to set
        :return: None
        """
        section = self.get_section_for_index(bit_index)
        section_bit_index = section.get_index(bit_index)
        section.bits[section_bit_index] = 1
        return

    def clear_bit(self, bit_index: int) -> None:
        """
        Clears the bit to 0 for the given bit index
        :param bit_index: The bit index of the bit to set
        :return: None
        """
        section = self.get_section_for_index(bit_index)
        section_bit_index = section.get_index(bit_index)
        section.bits[section_bit_index] = 0
        return

    def get_bit(self, bit_index: int) -> int:
        """
        Gets the value of the bit for the register bit index.
        :param bit_index: The register bit index to retrieve.
        :return: The value for the bit index.
        """
        section = self.get_section_for_index(bit_index)
        section_bit_index = section.get_index(bit_index)
        return section.bits[section_bit_index]

    def set_value(self, value: int, write_after: bool = False) -> None:
        """
        Sets the value of the register.
        :param value: The value to set the register.
        :param write_after: Optional. Write to the physical device after setting the value.
        """
        bytes_count = self.len_bytes()

        value_bytes = value.to_bytes(bytes_count, "big", signed=self.signed)
        value_bytes = value_bytes[::-1]

        for section in self.sections:
            self.sections[section].update_bits(value_bytes)

        if write_after:
            self.write()

        return

    def get_value(self, read_first: bool = False) -> int:
        """
        Gets the value of the register.
        :param read_first: Optional. Perform a physical read first.
        :return: The value of the register.
        """
        if read_first:
            self.read()

        bytes_arr = self._get_bytes()
        reg_val = bytearray(bytes_arr)

        result = int.from_bytes(reg_val, byteorder="little", signed=self.signed)

        return result

    def read(self):
        """
        Performs a physical read of the register.
        :raises SystemError: If the parent device has not been set.
        :raises SystemError: If the read from the physical device fails.
        :raises AttributeError: If the register is marked as write only.
        """
        if RegisterOperations.Read & self.op_mode == RegisterOperations.Read:
            # Get number of bytes to read, will raise AssertionError if sections do not create round number of bytes
            bytes_count = self.len_bytes()
            reg_bytes: list[int]
            if self.__parent is None:
                raise SystemError("No I2C Device set as parent")

            try:
                reg_bytes = self.__parent.i2c.read_bytes(self.__parent.dev_addr, self.reg_addr, bytes_count)

                if self.__parent is not None:
                    if bytes_count > 1 and self.__parent.byte_order == "big":
                        reg_bytes.reverse()

            except Exception as e:
                raise SystemError("Failed to read i2c: {}".format(e))

            # Loop through each byte read and map to elements in RegisterSection bit arrays
            for section in self.sections:
                self.sections[section].update_bits(reg_bytes)  # Raises KeyError if we didn't read enough bytes
        else:
            msg = "Register {} is not set up to allow read operations, op_mode: \"{}\""
            raise AttributeError(msg.format(self.name, self.op_mode.name))

        return

    def write(self):
        """
        Performs a physical read of the register.

        :raises SystemError: If the parent device has not been set.
        :raises SystemError: If the read from the physical device fails.
        :raises AttributeError: If the register is marked as write only.
        """
        if RegisterOperations.Write & self.op_mode == RegisterOperations.Write:

            if self.__parent is None:
                raise SystemError("No I2C Device set as parent")

            reg_bytes = self._get_bytes()
            try:
                bytes_count = len(reg_bytes)
                if self.__parent is not None:
                    if bytes_count > 1 and self.__parent.byte_order == "big":
                        reg_bytes.reverse()

                # Write to i2c
                write_status = self.__parent.i2c.write_bytes(self.__parent.dev_addr, self.reg_addr, reg_bytes)
            except Exception as e:
                raise SystemError("Failed to write to i2c: {}".format(e))

            if write_status == 1:
                raise SystemError("Failed to write to i2c register: {}".format(self.name))

            return
        else:
            msg = "Register {} is not set up to allow write operations, op_mode: \"{}\""
            raise AttributeError(msg.format(self.name, self.op_mode.name))

    def get_section_for_index(self, bit_index: int) -> I2cRegisterSection:
        """
        Gets a Register Section for the bit index.
        :param bit_index: The register bit index
        :return: The I2cRegisterSection for the bit index provided.
        """
        self._check_sections()
        sec_key = self.__managing_sections[bit_index][0]
        return self.sections.get(sec_key)

    def _check_sections(self):

        bits = {}
        max_bit = 0
        managing_sections = {}

        for section in self.sections:
            section = self.sections[section]
            for bit_ix in range(len(section.bits)):
                actual_bit_ix = bit_ix + section.lsb
                # Record maximum bit index for continuous test later
                if actual_bit_ix > max_bit:
                    max_bit = actual_bit_ix

                # Mark which section manages the bit in case of configuration error
                if actual_bit_ix not in managing_sections:
                    managing_sections[actual_bit_ix] = []
                managing_sections[actual_bit_ix].append(section.name)

                bits[actual_bit_ix] = section.bits[bit_ix]

        # Check bits are continuous and only 1 section controls each bit
        cont_check_err_is = []  # Indexes where bit array is not continuous
        managing_section_check_err_is = []  # Indexes where more than 1 RegisterSection is controlling a bit
        for bit_ix in range(max_bit + 1):
            # Continuous check
            if bit_ix not in bits:
                cont_check_err_is.append(bit_ix)

            # Managing Section check
            if (bit_ix in managing_sections) and (len(managing_sections[bit_ix]) > 1):
                managing_section_check_err_is.append(bit_ix)

        # Raise errors if there are any
        if len(cont_check_err_is) > 0:
            msg = "I2cRegisterSection are not configured to make a continuous series of bits, \
                        no values at indexes: {}"
            raise SyntaxError(msg.format(cont_check_err_is))

        if len(managing_section_check_err_is) > 0:
            indexes_msg = ""

            for i in range(len(managing_section_check_err_is)):
                bit_ix = managing_section_check_err_is[i]
                indexes_msg += "{} (competing sections: {})".format(bit_ix, managing_sections[bit_ix])

                if i != len(managing_section_check_err_is) - 1:
                    indexes_msg += ", "

            msg = "More than one I2cRegisterSection is managing the following bit indexes: {}"
            raise KeyError(msg.format(indexes_msg))

        if not self.__managing_sections:
            self.__managing_sections = managing_sections

        return bits, max_bit

    def _get_bytes(self) -> list[int]:

        bits, max_bit = self._check_sections()

        # Convert from bits map to bits array
        bits_arr = [bits[key] for key in sorted(bits.keys())]

        # Create bytes array
        bytes_arr = I2cRegisterSection.to_padded_byte_arr(bits_arr)

        return bytes_arr

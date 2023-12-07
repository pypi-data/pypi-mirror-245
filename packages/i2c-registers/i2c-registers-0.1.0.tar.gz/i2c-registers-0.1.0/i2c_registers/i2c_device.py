#!/usr/bin/python3

from i2c_registers.i2c_register_section import I2cRegisterSection
from i2c_registers.i2c_register import I2cRegister, RegisterOperations


class I2cDevice:

    def __init__(self,
                 dev_addr: int,
                 byteorder: str,
                 i2c,
                 registers: dict[str, I2cRegister]):

        self.dev_addr = dev_addr
        self.byte_order = byteorder
        self.i2c = i2c
        self.registers = {k.upper(): v for k, v in registers.items()}

        return

    def __str__(self):
        """
        Gets a string representation of the device.
        :return: A formatted string.
        """
        out = "I2cDevice<device_address={}, registers={{\n".format(self.dev_addr)

        for k in self.registers:
            v = self.registers[k]
            # Indent output from Register.str
            v = str(v)
            v = v.split("\n")

            new_v = ""
            for i in range(0, len(v)):
                # Don't indent first line
                if i != 0:
                    new_v += "    "

                new_v += v[i]

                # No newline on last line
                if i != len(v) - 1:
                    new_v += "\n"

            out += "    {}={}\n".format(k, new_v)

        out += "}>"
        return out

    def add(self, name: str, address: int, op_mode: RegisterOperations, signed: bool,
            sections: dict[str, I2cRegisterSection]):
        """
        Adds a register to the device.
        :param name: The name of the register.
        :param address: The address of the register
        :param op_mode: The operation mode: Read, Write, ReadWrite
        :param signed: An indicator to determine if the register value iss signed.
        :param sections: The sections of the Register. (Optional; can pass in {})
        :return: A Register object with specified name.
        """
        key = name.upper()
        if key in self.registers:
            raise KeyError("I2cRegister with name already exists. name: {}".format(name))

        register = I2cRegister(name.upper(), address, op_mode, signed, sections)
        register.set_parent(self)

        self.registers[key] = register

        return self.registers[key]

    def get(self, name: str, read_first: bool = False) -> I2cRegister:
        """
        Gets a Register by name.
        :param name: The register name.
        :param read_first: Optional. Perform a physical read first.
        :return: The I2cRegister for the name provided.
        :raises KeyError: If the section does not exist.
        """
        key = name.upper()
        if key not in self.registers:
            raise KeyError("Register with name \"{}\" not found".format(name))

        # Read first if asked
        if read_first:
            self.read(key)

        return self.registers[key]

    def read(self, name: str):
        """
        Performs a physical read for the register name provided.

        :param name: The register name
        """
        self.get(name).read()

        return

    def write(self, name: str):
        """
        Performs a physical write for the register name provided.

        :param name: The register name
        """
        self.get(name).write()

        return

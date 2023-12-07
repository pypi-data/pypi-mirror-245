
# Python I2C Register

Python wrapper library around the common I2C controller register pattern, based on [py-i2c-register](https://github.com/Noah-Huppert/py-i2c-register).

# Table Of Contents
- [Installation](#installation)
- 

# Installation
I2C Register is available as a PIP package with the name `i2c-register`.

Simply use PIP to install:

```bash
pip install --user i2c-register
```

You will then be able to include the `i2c_register` module and its various classes:

```python
from i2c_registers.i2c_device import I2cDevice
from i2c_registers.i2c_register import I2cRegister
from i2c_registers.i2c_register_section import I2cRegisterSection
```

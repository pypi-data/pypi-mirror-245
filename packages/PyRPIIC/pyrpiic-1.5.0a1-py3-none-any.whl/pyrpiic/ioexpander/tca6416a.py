from typing import Union
from enum import Enum
from pyrpio.i2c_register_device import I2CRegisterDevice
from pyrpio.i2c import I2CBase


class GPIODir(str, Enum):
    IN = "IN"
    OUT = "OUT"


class TCA6416A:
    PORT0 = ["P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07"]
    PORT1 = ["P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17"]
    TCA6416A_BASE_INPUT = 0x00
    TCA6416A_PORT0_INPUT = 0x00
    TCA6416A_PORT1_INPUT = 0x01
    TCA6416A_BASE_OUTPUT = 0x02
    TCA6416A_PORT0_OUTPUT = 0x02
    TCA6416A_PORT1_OUTPUT = 0x03
    TCA6416A_BASE_POLARITY = 0x04
    TCA6416A_PORT0_POLARITY = 0x04
    TCA6416A_PORT1_POLARITY = 0x05
    TCA6416A_BASE_CONFIG = 0x06
    TCA6416A_PORT0_CONFIG = 0x06
    TCA6416A_PORT1_CONFIG = 0x07

    def __init__(self, bus: I2CBase, address: int = 0x20):
        self.address = address
        self.i2c_reg = I2CRegisterDevice(bus, address, register_size=1, data_size=1)

    def close(self):
        """Close up access."""
        return 0

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def get_register_bit(self, register: int, bit: int):
        """Get single bit from register."""
        mask = 1 << bit
        value = self.i2c_reg.read_register(register, mask)
        return bool(value >> bit)

    def set_register_bit(self, register: int, bit: int, on: bool):
        """Set single bit of a register."""
        mask = 1 << bit
        pvalue = self.i2c_reg.read_register(register, ~mask)
        self.i2c_reg.write_register(register, pvalue | (int(on) << bit))

    def get_port_index(self, gpio: str) -> int:
        """Get port index for given gpio."""
        if gpio in TCA6416A.PORT0:
            return 0
        if gpio in TCA6416A.PORT1:
            return 1
        raise ValueError(f"GPIO {gpio} is not a valid value")

    def get_gpio_bit_position(self, gpio: str) -> int:
        """Get register bit position for given gpio."""
        if gpio in TCA6416A.PORT0:
            return TCA6416A.PORT0.index(gpio)
        if gpio in TCA6416A.PORT1:
            return TCA6416A.PORT1.index(gpio)
        raise ValueError(f"GPIO {gpio} is not a valid value")

    def get_gpio_direction(self, gpio: str):
        """Get GPIO direction as either in or out."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        value = self.get_register_bit(self.TCA6416A_BASE_CONFIG + port_index, gpio_bit)
        return GPIODir.IN if value else GPIODir.OUT

    def set_gpio_direction(self, gpio: str, gpio_dir: GPIODir):
        """Set GPIO direction as either in or out."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        value = gpio_dir == GPIODir.IN
        self.set_register_bit(self.TCA6416A_BASE_CONFIG + port_index, gpio_bit, value)

    def get_gpio_input(self, gpio: str) -> bool:
        """Read GPIO input value."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        return self.get_register_bit(self.TCA6416A_BASE_INPUT + port_index, gpio_bit)

    def get_gpio_output(self, gpio: str) -> bool:
        """Get currently set GPIO output value."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        return self.get_register_bit(self.TCA6416A_BASE_OUTPUT + port_index, gpio_bit)

    def set_gpio_output(self, gpio: str, high: Union[bool, int]):
        """Pull GPIO output either active high or low."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        self.set_register_bit(
            self.TCA6416A_BASE_OUTPUT + port_index, gpio_bit, bool(high)
        )

    def get_gpio_polarity(self, gpio: str):
        """Get GPIO polarity setting."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        return self.get_register_bit(self.TCA6416A_BASE_POLARITY + port_index, gpio_bit)

    def set_gpio_polarity(self, gpio: str, flipped: bool):
        """Set GPIO polarity setting as either normal or flipped."""
        port_index = self.get_port_index(gpio)
        gpio_bit = self.get_gpio_bit_position(gpio)
        self.set_register_bit(
            self.TCA6416A_BASE_POLARITY + port_index, gpio_bit, flipped
        )

    def get_all_gpio_input(self, sequential=False) -> int:
        """Read GPIO input register pair"""
        if sequential:
            return self._get_gpio_register_pair_sequential(self.TCA6416A_BASE_INPUT)

        return self._get_gpio_register_pair(self.TCA6416A_BASE_INPUT)

    def set_all_gpio_output(self, value: int, sequential=False):
        """Set GPIO output register pair"""
        if sequential:
            self._set_gpio_register_pair_sequential(self.TCA6416A_BASE_OUTPUT, value)
        else:
            self._set_gpio_register_pair(self.TCA6416A_BASE_OUTPUT, value)

    def get_all_gpio_output(self, sequential=False) -> int:
        """Get GPIO output register pair"""
        if sequential:
            return self._get_gpio_register_pair_sequential(self.TCA6416A_BASE_OUTPUT)

        return self._get_gpio_register_pair(self.TCA6416A_BASE_OUTPUT)

    def set_all_gpio_polarity(self, value, sequential=False):
        """Set GPIO polarity register pair"""
        if sequential:
            self._set_gpio_register_pair_sequential(self.TCA6416A_BASE_POLARITY, value)
        else:
            self._set_gpio_register_pair(self.TCA6416A_BASE_POLARITY, value)

    def get_all_gpio_polarity(self, sequential=False) -> int:
        """Get GPIO polarity register pair"""
        if sequential:
            return self._get_gpio_register_pair_sequential(self.TCA6416A_BASE_POLARITY)

        return self._get_gpio_register_pair(self.TCA6416A_BASE_POLARITY)

    def set_all_gpio_direction(self, value: int, sequential=False):
        """Set GPIO configuration register pair"""
        if sequential:
            self._set_gpio_register_pair_sequential(self.TCA6416A_BASE_CONFIG, value)
        else:
            self._set_gpio_register_pair(self.TCA6416A_BASE_CONFIG, value)

    def get_all_gpio_direction(self, sequential=False) -> int:
        """Get GPIO configuration register pair"""
        if sequential:
            return self._get_gpio_register_pair_sequential(self.TCA6416A_BASE_CONFIG)

        return self._get_gpio_register_pair(self.TCA6416A_BASE_CONFIG)

    def _set_gpio_register_pair_sequential(self, base_addr: int, value: int):
        """Set GPIO register pair using sequential writes"""
        self.i2c_reg.write_register_sequential_bytes(
            base_addr, value.to_bytes(2, byteorder="little")
        )

    def _set_gpio_register_pair(self, base_addr: int, value: int):
        """Set GPIO register pair using two different write transactions"""
        self.i2c_reg.write_register(base_addr, (value >> 8) & 0xFF)
        self.i2c_reg.write_register(base_addr + 1, value & 0xFF)

    def _get_gpio_register_pair_sequential(self, base_addr: int) -> int:
        """Get GPIO register pair using sequential reads"""
        data = self.i2c_reg.read_register_sequential_bytes(base_addr, 2)
        return int.from_bytes(data, byteorder="little")

    def _get_gpio_register_pair(self, base_addr: int) -> int:
        """Get GPIO register pair using two different read transactions"""
        value = self.i2c_reg.read_register(base_addr)
        value |= self.i2c_reg.read_register(base_addr + 1) << 8
        return value

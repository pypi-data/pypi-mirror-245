"""Fixtures definitions for pyEGPS tests."""
from __future__ import annotations

from array import array
import pytest

CTRL_IN = 1 << 7


class FakeUsbDevice:
    """A Fake usb.core USB-Device."""

    def __init__(self, product_id: int) -> None:
        """Initiate instance."""
        self._product_id = product_id

    @property
    def idProduct(self) -> int:
        """Return product id."""
        return self._product_id

    @property
    def manufacturer(self) -> str:
        """Return manufacturer."""
        return "AllFake"

    @property
    def product(self) -> str:
        """Return product id."""
        return "Fake-Product"

    def ctrl_transfer(
        self,
        bmRequestType,
        bRequest,
        wValue,
        wIndex,
        data_or_wLength,
        USB_CTRL_TRANSFER_TIMEOUT,
    ) -> bytes | int:
        req_in: bool = (bmRequestType & CTRL_IN) == CTRL_IN
        return array("B", []) if req_in else 0


@pytest.fixture
def fakeUsbDevice() -> FakeUsbDevice:
    """Return a fake USB device with supported product_id."""
    return FakeUsbDevice(product_id=0xFD15)


@pytest.fixture
def fakeUnknownUsbDevice() -> FakeUsbDevice:
    """Return a fake USB device with unsupported product_id."""
    return FakeUsbDevice(product_id=0xFD20)

from __future__ import annotations
import contextlib

import async_timeout

import asyncio
import logging
from collections.abc import Callable
from typing import Optional
from dataclasses import replace

from bleak import BleakClient, BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak_retry_connector import BLEAK_RETRY_EXCEPTIONS as BLEAK_EXCEPTIONS, establish_connection

from .const import EVENT_CHARACTERISTIC_UUID, STATE_CHARACTERISTIC_UUID, UNPAIRED_API_KEY, SYSTEM_ID_DESCRIPTOR_UUID, MODEL_NUMBER_DESCRIPTOR_UUID, SOFTWARE_REVISION_DESCRIPTOR_UUID, MANUFACTURER_DESCRIPTOR_UUID, WAIT_FOR_DEVICE_CONNECTION_TIMEOUT
from .exceptions import DeviceConnectionError, DeviceConnectionTimeoutError, DeviceNotInPairingModeError, IncorrectAPIKeyError
from .models import DecoraBLEDeviceState, DecoraBLEDeviceSummary

_LOGGER = logging.getLogger(__name__)


class DecoraBLEDevice():
    def __init__(self, device: BLEDevice, api_key: str):
        self._device = device
        self._key = bytearray.fromhex(api_key)

        self._running = False
        self._device_connection_future: asyncio.Future[None] | None = None

        self._client = None
        self._summary = None
        self._state = DecoraBLEDeviceState()
        self._connection_callbacks: list[Callable[[
            DecoraBLEDeviceSummary], None]] = []
        self._state_callbacks: list[Callable[[
            DecoraBLEDeviceState], None]] = []

    @staticmethod
    async def get_api_key(device: BLEDevice) -> str:
        async with BleakClient(device) as client:
            await client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, bytearray([0x22, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]), response=True)
            rawkey = await client.read_gatt_char(EVENT_CHARACTERISTIC_UUID)
            _LOGGER.debug("Raw API key from device: %s", repr(rawkey))

            if rawkey[2:6] != UNPAIRED_API_KEY:
                return bytearray(rawkey)[2:].hex()
            else:
                raise DeviceNotInPairingModeError

    async def start(self) -> Callable[[], None]:
        """Start watching for updates."""
        if self._running:
            raise RuntimeError("Already running")
        self._running = True
        self._device_connection_future = asyncio.get_running_loop().create_future()

        def _cancel() -> None:
            self._running = False

        return _cancel

    async def wait_for_device_connection(self) -> None:
        if not self._running:
            raise RuntimeError("Not running")
        if not self._device_connection_future:
            raise RuntimeError("Already waited for first update")
        try:
            async with async_timeout.timeout(WAIT_FOR_DEVICE_CONNECTION_TIMEOUT):
                await self._device_connection_future
        except (asyncio.TimeoutError, asyncio.CancelledError) as ex:
            self._device_connection_future.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._device_connection_future
            raise DeviceConnectionTimeoutError(
                "No advertisement received before timeout"
            ) from ex
        finally:
            self._device_connection_future = None

    def register_connection_callback(
        self, callback: Callable[[DecoraBLEDeviceSummary], None]
    ) -> Callable[[], None]:
        def unregister_callback() -> None:
            self._connection_callbacks.remove(callback)

        self._connection_callbacks.append(callback)

        if self._summary is not None:
            callback(self._summary)

        return unregister_callback

    def register_state_callback(
        self, callback: Callable[[DecoraBLEDeviceState], None]
    ) -> Callable[[], None]:
        def unregister_callback() -> None:
            self._state_callbacks.remove(callback)

        self._state_callbacks.append(callback)

        if self._state is not None:
            callback(self._state)

        return unregister_callback

    @property
    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    @property
    def summary(self) -> Optional[DecoraBLEDeviceSummary]:
        return self._summary

    def update_device(self, device: BLEDevice) -> None:
        self._device = device

    async def connect(self) -> None:
        if self.is_connected:
            return

        device = self._device
        _LOGGER.debug("attempting to connect to %s using %s key",
                      device.address, self._key)

        def disconnected(client):
            _LOGGER.debug("Device disconnected %s", device.address)
            self._disconnect_cleanup()

        try:
            self._client = await establish_connection(
                BleakClient,
                self._device,
                self._device.name,
                disconnected,
                use_services_cache=True,
            )

            await self._unlock()
        except Exception as ex:
            self._handle_device_connection(ex)
            raise DeviceConnectionError(str(ex)) from ex

        try:
            # Issues in unlocking will be seen when first interacting with the device
            await self._register_for_state_notifications()

            self._summary = await self._summarize()
            self._handle_device_connection(None)
            self._fire_connection_callbacks(self._summary)

            await self._read_state()

            _LOGGER.debug("Finished connecting %s", self._client.is_connected)
        except BLEAK_EXCEPTIONS as ex:
            self._handle_device_connection(ex)
            raise IncorrectAPIKeyError

    async def disconnect(self) -> None:
        await self._client.disconnect()

    async def _summarize(self) -> DecoraBLEDeviceSummary:
        system_identifier = await self.read_summary_descriptor(
            "system_identifier", SYSTEM_ID_DESCRIPTOR_UUID)
        manufacturer = await self.read_summary_descriptor(
            "manufacturer", MANUFACTURER_DESCRIPTOR_UUID)
        model = await self.read_summary_descriptor(
            "model", MODEL_NUMBER_DESCRIPTOR_UUID)
        software_revision = await self.read_summary_descriptor(
            "software_revision", SOFTWARE_REVISION_DESCRIPTOR_UUID)

        return DecoraBLEDeviceSummary(
            system_identifier=system_identifier.hex(),
            manufacturer=manufacturer.decode('utf-8'),
            model=model.decode('utf-8'),
            software_revision=self._revision_string(
                software_revision, "Software Revision"),
        )

    async def read_summary_descriptor(self, descriptor: str, descriptor_uuid: str) -> bytearray:
        raw_response = await self._client.read_gatt_char(descriptor_uuid)
        _LOGGER.debug("Raw %s from device: %s", descriptor, repr(raw_response))
        return raw_response

    def _revision_string(self, value: bytearray, prefix: str) -> Optional[str]:
        stripped_value = value.decode('utf-8').removeprefix(prefix)
        if len(stripped_value) > 0:
            return stripped_value.strip()
        else:
            return None

    async def turn_on(self, brightness_level: Optional[int] = None) -> None:
        _LOGGER.debug("Turning on...")
        brightness_level = brightness_level if brightness_level is not None else self._state.brightness_level
        await self._write_state(replace(self._state, is_on=True, brightness_level=brightness_level))

    async def turn_off(self) -> None:
        _LOGGER.debug("Turning off...")
        await self._write_state(replace(self._state, is_on=False))

    async def set_brightness_level(self, brightness_level: int):
        _LOGGER.debug("Setting brightness level to %d...", brightness_level)
        await self._write_state(replace(self._state, brightness_level=brightness_level))

    def _disconnect_cleanup(self):
        self._device = None
        self._key = None
        self._client = None
        self._summary = None
        self._state = DecoraBLEDeviceState()

    async def _unlock(self):
        packet = bytearray([0x11, 0x53, *self._key])
        await self._client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, packet, response=True)

    def _apply_device_state_data(self, data: bytearray) -> None:
        self._state = replace(
            self._state, is_on=data[0] == 1, brightness_level=data[1])
        _LOGGER.debug("State updated: %s", self._state)

    async def _write_state(self, state: DecoraBLEDeviceState) -> None:
        self._state = state
        packet = bytearray([1 if state.is_on else 0, state.brightness_level])
        _LOGGER.debug("Writing state: %s", state)
        await self._client.write_gatt_char(STATE_CHARACTERISTIC_UUID, packet, response=True)

    async def _read_state(self) -> None:
        data = await self._client.read_gatt_char(STATE_CHARACTERISTIC_UUID)
        self._apply_device_state_data(data)
        self._fire_state_callbacks(self._state)

    async def _register_for_state_notifications(self) -> None:
        def callback(sender: BleakGATTCharacteristic, data: bytearray) -> None:
            self._apply_device_state_data(data)
            self._fire_state_callbacks(self._state)

        await self._client.start_notify(STATE_CHARACTERISTIC_UUID, callback)

    def _handle_device_connection(self, exception: Exception | None) -> None:
        """Set the device connection future to resolve it."""
        if not self._device_connection_future:
            return
        if exception:
            self._device_connection_future.set_exception(exception)
        else:
            self._device_connection_future.set_result(None)

    def _fire_connection_callbacks(self, summary: DecoraBLEDeviceSummary) -> None:
        for callback in self._connection_callbacks:
            callback(summary)

    def _fire_state_callbacks(self, state: DecoraBLEDeviceState) -> None:
        for callback in self._state_callbacks:
            callback(state)

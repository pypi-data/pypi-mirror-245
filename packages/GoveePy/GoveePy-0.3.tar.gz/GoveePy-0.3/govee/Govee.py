import requests
from abc import abstractmethod
from typing import List

from .Objects import Color

BASE_URL = "https://developer-api.govee.com"

class GoveeDevice:
    """
    Class representing a Govee device

    :param str device: the unique device id.
    :param str model: the model of the device.
    """
    _model: str
    _device: str
    _name: str

    _controllable: bool
    _retrievable: bool

    _key: str

    _state: bool = None

    def __init__(self,
                 model: str = "",
                 device: str = "",
                 name: str = "",
                 controllable: bool = False,
                 retrievable: bool = False,
                 key: str = ""):
        self._model = model
        self._device = device
        self._name = name

        self._controllable = controllable
        self._retrievable = retrievable

        self._key = key

        self._update()

    def _make_request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        if not kwargs.get("headers", None):
            kwargs["headers"] = {
                "Govee-API-Key": self._key
            }
        response = requests.request(method, url, *args, **kwargs, timeout=60)
        return response.json()

    @abstractmethod
    def _command(self, command):
        pass

    @abstractmethod
    def _update(self):
        pass

    @property
    def model(self):
        """Device Model"""
        return self._model

    @property
    def device(self):
        """Device ID"""
        return self._device

    @property
    def name(self):
        """The Devices Name"""
        return self._name

    @property
    def controllable(self):
        """Whether the device is controllable"""
        return self._controllable

    @property
    def retrievable(self):
        """Whether the device is retrievable"""
        return self._retrievable

    @property
    def on(self):
        """Whether the light is on"""
        return self._state

    @property
    def off(self):
        """Whether the light is off"""
        return not self._state

    def turn_on(self):
        """Turn the light on"""
        self._command(
            {
                "name": "turn",
                "value": "on"
            }
        )
        self._state = True

    def turn_off(self):
        """Turn the light off"""
        self._command(
            {
                "name": "turn",
                "value": "off"
            }
        )
        self._state = False

    def __str__(self):
        return f"<{self.name} [device = {self.device}, model = {self.model}]>"

    def __repr__(self):
        return f"<{self.name} [device = {self.device}, model = {self.model}]>"



class GoveeLight(GoveeDevice):
    """
    Class representing a Govee light.

    You should not need to create this class, I recommend using :meth:`Govee.get_devices` to get a list of devices.
    
    :param str device: the unique device id.
    :param str model: the model of the device.
    :param str name: the name of the device.
    :param bool controllable: whether the device is controllable.
    :param bool retrievable: whether the device is retrievable.
    :param str key: your API key for Govee.
    """

    _online: bool = True
    _brightness: int = 0
    _color: Color = Color(0,0,0)

    def _command(self, command):
        self._make_request(
            "PUT",
            f"{BASE_URL}/v1/devices/control",
            json = {
                "device": self._device,
                "model": self._model,
                "cmd": command
            }
        )

    def _update(self):
        response = self._make_request(
            "GET",
            f"{BASE_URL}/v1/devices/state",
            params={
                "device": self._device,
                "model": self._model
            }
        )
        data = {}
        for i in response["data"]["properties"]:
            for k, v in i.items():
                data[k] = v
        self._state = data.get("powerState") == 'on'
        self._brightness = data.get("brightness", 0)
        self._color = Color(**data.get("color", {"r":0,"g":0,"b":0}))

    def set_brightness(self, brightness: int):
        """Set the brightness of the light (1-100)"""
        self._command({
            "name": "brightness",
            "value": brightness % 101
        })
        self._brightness = brightness % 101

    def set_color(self, r: int, g: int, b: int):
        """Set the color of the light"""
        self._command({
            "name": "color",
            "value": {
                "r": r % 256,
                "g": g % 256,
                "b": b % 256
            }
        })
        self._color = Color(r%256,g%256,b%256)

class GoveeAppliance(GoveeDevice):
    """
    Class representing a Govee appliance.
    
    Note:
        There is currently no good API implementation for Govee appliances.
    """

    def _command(self, command):
        """
        Sends a command to control the Govee appliance.

        Args:
            command (str): The command to send to the Govee appliance.

        Returns:
            None
        """
        self._make_request(
            "PUT",
            f"{BASE_URL}/v1/appliance/devices/control",
            json={
                "device": self._device,
                "model": self._model,
                "cmd": command
            }
        )

    def _update(self):
        """
        Updates the Govee appliance.

        Note:
            There is currently no API implementation for updating the Govee appliance.

        Returns:
            None
        """
        pass


class Govee:
    """
    Represents an instance connected to the Govee API.

    :param str key: Your API Key for Govee.
    """
    _key: str
    _devices: List[GoveeDevice]
    _device_rate_limits: List

    def __init__(self, key: str):
        self._key = key
        self._devices = []

    def _make_request(self, method: str, url: str, *args, **kwargs):
        if not kwargs.get("headers", None):
            kwargs["headers"] = {
                "Govee-API-Key": self._key
            }
        response = requests.request(method, url, *args, **kwargs, timeout=60)
        if response.status_code == 200:
            return response.json()

    def get_devices(self, *, update: bool = False):
        """
        Retrieves the list of devices associated with the Govee account.

        :param bool update: If True, force an update of the device list.
        :return: List of GoveeDevice objects.
        :rtype: List[GoveeDevice]
        """
        if len(self._devices) == 0 or update:
            data = self._make_request(
                "GET",
                f"{BASE_URL}/v1/devices"
            )
            for device in data["data"]["devices"]:
                self._devices.append(
                    GoveeLight(
                        device["model"],
                        device["device"],
                        device["deviceName"],
                        device["controllable"],
                        device["retrievable"],
                        self._key
                    )
                )
        return self._devices
        
    def get_device_by_name(self, name: str) -> GoveeDevice | None:
        """
        Retrieves a device by its name.

        :param str name: The name of the device.
        :return: The GoveeDevice object if found, otherwise None.
        :rtype: GoveeDevice | None
        """
        for device in self._devices:
            if device.name == name:
                return device
        return None
    
    def get_device_by_model(self, model: str) -> GoveeDevice | None:
        """
        Retrieves a device by its model.

        :param str model: The model of the device.
        :return: The GoveeDevice object if found, otherwise None.
        :rtype: GoveeDevice | None
        """
        for device in self._devices:
            if device.model == model:
                return device
        return None
    
    def get_device_by_address(self, address: str) -> GoveeDevice | None:
        """
        Retrieves a device by its address.

        :param str address: The address of the device.
        :return: The GoveeDevice object if found, otherwise None.
        :rtype: GoveeDevice | None
        """
        for device in self._devices:
            if device.device == address:
                return device
        return None
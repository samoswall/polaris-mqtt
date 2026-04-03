"""The Polaris IQ Home component."""
from __future__ import annotations

import asyncio
import logging
import time
import voluptuous as vol
from homeassistant.data_entry_flow import FlowResult
from homeassistant.config_entries import ConfigFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.components import mqtt
from homeassistant.helpers.translation import async_get_translations

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import DEVICEID, DEVICETYPE, DOMAIN, MQTT_ROOT_TOPIC, MQTT_ROOT_TOPIC_DEFAULT, POLARIS_DEVICE
from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class PolarisConfigFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1

    def __init__(self) -> None:
        """Initialize flow."""
        self._serial_number = None
        self._topic_prefix = {}
        self._device_found = {}
        self._device_prefix_topic = {}
        self._unknown_devtype = {}


    async def _get_devtypes_from_mqtt(self):
        await mqtt.async_subscribe(self.hass, "polaris/+/state/mac", self._mqtt_message_newdev)
        await mqtt.async_subscribe(self.hass, "polaris/+/+/state/mac", self._mqtt_message_olddev)
        await mqtt.async_subscribe(self.hass, "rusclimate/+/+/state/mac", self._mqtt_message_rusclidev)

    @callback
    async def _mqtt_message_newdev(self, message: ReceiveMessage):
        unknown_type = "0"
        topic = message.topic
        device_id = topic.split("/")[1]
        topic_check = f"polaris/{device_id}/state/devtype"
        topic_bool = await self.topic_exists(topic_check)
        if not topic_bool:
            self._device_type = "0"
        if int(self._device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("newdevice unknown - %s", self._device_type)
            unknown_type = self._device_type
        if device_id not in self._device_found:
            self._device_found[device_id] = self._device_type
            self._device_prefix_topic[device_id] = device_id
            self._topic_prefix[device_id] = "polaris"
            self._unknown_devtype[device_id] = unknown_type

    @callback
    async def _mqtt_message_olddev(self, message: ReceiveMessage):
        unknown_type = "0"
        topic = message.topic
        device_id = message.payload
        device_type = topic.split("/")[1]
        device_oldid = topic.split("/")[2]
        if int(device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("olddevice unknown - %s", device_type)
            unknown_type = device_type
        if device_id not in self._device_found:
            self._device_found[device_id] = device_type
            self._device_prefix_topic[device_id] = f"{device_type}/{device_oldid}"
            self._topic_prefix[device_id] = "polaris"
            self._unknown_devtype[device_id] = unknown_type

    @callback
    async def _mqtt_message_rusclidev(self, message: ReceiveMessage):
        unknown_type = "0"
        topic = message.topic
        device_id = message.payload
        device_type = str(int(topic.split("/")[1]) + 800)
        device_oldid = topic.split("/")[2]
        if int(device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("rusclidevice unknown - %s", device_type)
            unknown_type = device_type
        if device_id not in self._device_found:
            self._device_found[device_id] = device_type
            self._device_prefix_topic[device_id] = f"{topic.split("/")[1]}/{device_oldid}"
            self._topic_prefix[device_id] = "rusclimate"
            self._unknown_devtype[device_id] = unknown_type

    async def topic_exists(self, topic: str, timeout: float = 1.0) -> bool:
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()

        def message_received(msg):
            if not future.done():
                future.set_result(msg)
        unsub = await mqtt.async_subscribe(self.hass, topic, message_received, qos=0)
        try:
            msg = await asyncio.wait_for(future, timeout)
            self._device_type = msg.payload
        except asyncio.TimeoutError:
            return False
        finally:
            unsub()
        return bool(msg.retain)

    async def get_translated_type(self, device_type_lang):
        language = self.hass.config.language
        translations = await async_get_translations(self.hass, language, "common", {DOMAIN})
        key = f"component.polaris.common.{device_type_lang}"
        return translations.get(key, device_type_lang)
        
    async def async_step_user(self, user_input=None):
        await self._get_devtypes_from_mqtt()
        await self.hass.async_add_executor_job(time.sleep, 2)
        current_entries = self._async_current_entries()
        configured_devices = {
            entry.data[DEVICEID] 
            for entry in current_entries 
            if DEVICEID in entry.data
        }
#        _LOGGER.debug(f"Configured devices: {configured_devices}")
        errors = {}
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(DEVICEID): SelectSelector(
                            SelectSelectorConfig(
                                options=[
                                    SelectOptionDict(
                                        value=dev_mac,
                                        label=f"{await self.get_translated_type(POLARIS_DEVICE[int(dev_type) if int(dev_type) in POLARIS_DEVICE else 0]["class"])} {POLARIS_DEVICE[int(dev_type) if int(dev_type) in POLARIS_DEVICE else 0]["model"].replace('_','/')} (mac: {dev_mac})",
                                    )
                                    for dev_mac, dev_type in self._device_found.items() if dev_mac not in configured_devices
                                ],
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key="config_selector_devicetype",
                            )
                        ),
                    }
                ),
                errors=errors,
            )
        user_input[MQTT_ROOT_TOPIC] = self._topic_prefix[user_input[DEVICEID]]
        user_input[DEVICETYPE] = self._device_found[user_input[DEVICEID]]
        user_input["DEVPREFIXTOPIC"] = self._device_prefix_topic[user_input[DEVICEID]]
        user_input["UNKNOWNTYPE"] = self._unknown_devtype[user_input[DEVICEID]]
        self.oldstep = user_input
        
        if user_input[DEVICETYPE] == "0" or int(user_input["UNKNOWNTYPE"]) > 0:
            return self.async_show_form(
                step_id="undef",
                data_schema=vol.Schema(
                    {
                        vol.Required(DEVICETYPE): SelectSelector(
                            SelectSelectorConfig(
                                options=[
                                    SelectOptionDict(
                                        value=str(dev_id),
                                        label=f'{str(dev_id)} {await self.get_translated_type(POLARIS_DEVICE[int(dev_id)]["class"])} ({POLARIS_DEVICE[int(dev_id)]["model"]})',
                                    )
                                    for dev_id in POLARIS_DEVICE
                                ],
                                mode=SelectSelectorMode.DROPDOWN,
                            )
                        )
                    }
                ),
            )

        title = f"{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['class']}-{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['model']}-{user_input[DEVICEID]}"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured(error="already_configured")
        # Create entities
        return self.async_create_entry(
            error=error,
            title=title,
            data=user_input,
        )
        
    async def async_step_undef(self, user_input):
        if user_input[DEVICETYPE] == "0":
            error = "no_dev"
            return self.async_abort(reason="not_supported")
        self.oldstep[DEVICETYPE] = user_input[DEVICETYPE]
        user_input = self.oldstep
        user_input[MQTT_ROOT_TOPIC] = self._topic_prefix[user_input[DEVICEID]]
        mqtt.publish(self.hass, f'{user_input[MQTT_ROOT_TOPIC]}/{user_input["DEVPREFIXTOPIC"]}/state/devtype', user_input[DEVICETYPE], 0, True)
        title = f"{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['class']}-{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['model']}-{user_input[DEVICEID]}"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured(error="already_configured")
        # Create entities
        return self.async_create_entry(
            title=title,
            data=user_input,
        )
        
    async def async_step_mqtt(self, discovery_info: MqttServiceInfo):# -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        device_mac = discovery_info.payload
        topic_parts = discovery_info.topic.split("/")
    # polaris/+/state/mac + get devtype
        if len(topic_parts) == 4:
            device_id = topic_parts[1]
            topic_check = f"polaris/{device_id}/state/devtype"
            topic_bool = await self.topic_exists(topic_check)
            if not topic_bool:
                device_type = "0"
            else:
                device_type = self._device_type
            prefix_topic = device_id
            root_topic = "polaris"
    # polaris/+/+/state/mac
        elif len(topic_parts) == 5 and topic_parts[0] == "polaris":
            device_type = topic_parts[1]
            device_id = topic_parts[2]
            prefix_topic = f"{device_type}/{device_id}"
            root_topic = "polaris"
    # rusclimate/+/+/state/mac
        elif len(topic_parts) == 5 and topic_parts[0] == "rusclimate":
            device_type = str(int(topic_parts[1]) + 800)
            device_id = topic_parts[2]
            prefix_topic = f"{topic_parts[1]}/{device_id}"
            root_topic = "rusclimate"
        else:
            return self.async_abort(reason="unknown_topic")
        
        # Проверяем, поддерживается ли тип устройства
        if int(device_type) not in POLARIS_DEVICE:
            return self.async_abort(reason="unsupported_device")
        unique_id = f"{POLARIS_DEVICE[int(device_type)]['class']}-{POLARIS_DEVICE[int(device_type)]['model']}-{device_mac}"  # mac или ID ???
        # Проверяем, не настроено ли уже устройство
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        # Сохраняем информацию об устройстве
        self._device_mac = device_mac
        self._device_type = device_type
        self._device_id = device_id
        self._root_topic = root_topic
        self._prefix_topic = prefix_topic
        
        # Показываем форму с информацией об устройстве
        device_info = POLARIS_DEVICE[int(self._device_type)]
        placeholders = {"name": f"{await self.get_translated_type(device_info['class'])} {device_info['model']}"}
        self.context["title_placeholders"] = placeholders

        return await self.async_step_confirm()


    async def async_step_confirm(self, user_input=None):
        """Handle the confirmation step for the discovered device."""
        if user_input is not None:
            data = {
                "DEVICEID": self._device_mac,
                "DEVICETYPE": self._device_type,
                "MQTT_ROOT_TOPIC": self._root_topic,
                "DEVPREFIXTOPIC": self._prefix_topic,
            }
            title = f"{POLARIS_DEVICE[int(self._device_type)]['class']}-{POLARIS_DEVICE[int(self._device_type)]['model']}-{self._device_mac}"
            return self.async_create_entry(
                title=title,
                data=data,
            )

        device_info = POLARIS_DEVICE[int(self._device_type)]
        placeholders = {
            "device": POLARIS_DEVICE[int(self._device_type)]['model'],
            "class": await self.get_translated_type(POLARIS_DEVICE[int(self._device_type)]['class']),
            "mac": self._device_mac
        }

        return self.async_show_form(
            step_id="confirm",
            description_placeholders=placeholders,
        )
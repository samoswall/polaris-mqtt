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
        self._unknown_devtype = 0


    async def _get_devtypes_from_mqtt(self):
        await mqtt.async_subscribe(self.hass, "polaris/+/state/mac", self._mqtt_message_newdev)
        await mqtt.async_subscribe(self.hass, "polaris/+/+/state/mac", self._mqtt_message_olddev)
        await mqtt.async_subscribe(self.hass, "rusclimate/+/+/state/mac", self._mqtt_message_rusclidev)

    @callback
    async def _mqtt_message_newdev(self, message: ReceiveMessage):
        topic = message.topic
        device_id = topic.split("/")[1]
        topic_check = f"polaris/{device_id}/state/devtype"
        topic_bool = await self.topic_exists(topic_check)
        if not topic_bool:
            self._device_type = "0"
        if int(self._device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("newdevice unknown - %s", self._device_type)
            self._unknown_devtype = int(self._device_type)
        if device_id not in self._device_found:
            self._device_found[device_id] = self._device_type
            self._device_prefix_topic[device_id] = device_id
            self._topic_prefix[device_id] = "polaris"

    @callback
    async def _mqtt_message_olddev(self, message: ReceiveMessage):
        topic = message.topic
        device_id = message.payload
        device_type = topic.split("/")[1]
        device_oldid = topic.split("/")[2]
        if int(device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("olddevice unknown - %s", device_type)
            self._unknown_devtype = int(device_type)
        if device_id not in self._device_found:
            self._device_found[device_id] = device_type
            self._device_prefix_topic[device_id] = f"{device_type}/{device_oldid}"
            self._topic_prefix[device_id] = "polaris"

    @callback
    async def _mqtt_message_rusclidev(self, message: ReceiveMessage):
        topic = message.topic
        device_id = message.payload
        device_type = str(int(topic.split("/")[1]) + 800)
        device_oldid = topic.split("/")[2]
        if int(device_type) not in POLARIS_DEVICE:
#            _LOGGER.debug("rusclidevice unknown - %s", device_type)
            self._unknown_devtype = int(device_type)
        if device_id not in self._device_found:
            self._device_found[device_id] = device_type
            self._device_prefix_topic[device_id] = f"{topic.split("/")[1]}/{device_oldid}"
            self._topic_prefix[device_id] = "rusclimate"

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
                                        label=f"{await self.get_translated_type(POLARIS_DEVICE[int(dev_type)]["class"])} {POLARIS_DEVICE[int(dev_type) if int(dev_type) in POLARIS_DEVICE else 0]["model"].replace('_','/')} (mac: {dev_mac})",
                                    )
                                    for dev_mac, dev_type in self._device_found.items()
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
        self.oldstep = user_input
#        _LOGGER.debug("input1 %s", user_input)
        if user_input[DEVICETYPE] == "0" or self._unknown_devtype > 0:
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
        
#        _LOGGER.debug("input3 %s", user_input)
        title = f"{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['class']}-{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['model']}-{user_input[DEVICEID]}"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured(error="already_configured")
        # Create entities
        return self.async_create_entry(
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
#        _LOGGER.debug("input2 %s", user_input)
        mqtt.publish(self.hass, f'{user_input[MQTT_ROOT_TOPIC]}/{user_input["DEVPREFIXTOPIC"]}/state/devtype', user_input[DEVICETYPE], 0, True)
        title = f"{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['class']}-{POLARIS_DEVICE[int(user_input[DEVICETYPE])]['model']}-{user_input[DEVICEID]}"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured(error="already_configured")
        # Create entities
        return self.async_create_entry(
            title=title,
            data=user_input,
        )
        

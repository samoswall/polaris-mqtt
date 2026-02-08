"""The Polaris IQ Home component."""
from __future__ import annotations

import json
import re
import logging
from typing import Iterable
import copy

from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.number import NumberEntity, DOMAIN
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.util import slugify
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .common import PolarisBaseEntity
from homeassistant.const import STATE_UNAVAILABLE

# Import global values.
from .const import (
    MANUFACTURER,
    MQTT_ROOT_TOPIC,
    DEVICEID,
    DEVICETYPE,
    POLARIS_DEVICE,
    NUMBER_HUMIDIFIER,
    NUMBER_RUSCLIMATE_HUMIDIFIER,
    NUMBER_COOKER,
    NUMBERS_COFFEEMAKER,
    NUMBERS_COFFEEMAKER_ROG,
    NUMBERS_AIRCLEANER,
    NUMBERS_IRRIGATOR,
    NUMBERS_HEATER,
    NUMBERS_THERMOSTAT,
    PolarisNumberEntityDescription,
    POLARIS_KETTLE_TYPE,
    POLARIS_KETTLE_WITH_WEIGHT_TYPE,
    POLARIS_HUMIDDIFIER_TYPE,
    POLARIS_HUMIDDIFIER_LOW_FAN_TYPE,
    POLARIS_COOKER_TYPE,
    POLARIS_COFFEEMAKER_TYPE,
    POLARIS_COFFEEMAKER_ROG_TYPE,
    POLARIS_AIRCLEANER_TYPE,
    POLARIS_IRRIGATOR_TYPE,
    POLARIS_HEATER_TYPE,
    POLARIS_THERMOSTAT_TYPE,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback,
) -> None:
    integrationUniqueID = config.unique_id
    mqtt_root = config.data[MQTT_ROOT_TOPIC]
    device_id = config.data["DEVICEID"]
    device_type = config.data[DEVICETYPE]
    device_prefix_topic = config.data["DEVPREFIXTOPIC"]
    numberList = []
    
    if (device_type in POLARIS_HUMIDDIFIER_TYPE):
    # Create humidifier  
        if device_type in {"835","881"}:
            NUMBER_HUMIDIFIER_LC = copy.deepcopy(NUMBER_RUSCLIMATE_HUMIDIFIER)
        else:
            NUMBER_HUMIDIFIER_LC = copy.deepcopy(NUMBER_HUMIDIFIER)
        for description in NUMBER_HUMIDIFIER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COOKER_TYPE):
    # Create cooker  
        NUMBER_COOKER_LC = copy.deepcopy(NUMBER_COOKER)
        for description in NUMBER_COOKER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_TYPE):
    # Create cooker  
        NUMBERS_COFFEEMAKER_LC = copy.deepcopy(NUMBERS_COFFEEMAKER)
        for description in NUMBERS_COFFEEMAKER_LC:
#            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_ROG_TYPE):
    # Create cooker  
        NUMBERS_COFFEEMAKER_ROG_LC = copy.deepcopy(NUMBERS_COFFEEMAKER_ROG)
        for description in NUMBERS_COFFEEMAKER_ROG_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_AIRCLEANER_TYPE): 
    # Create humidifier  
        NUMBERS_AIRCLEANER_LC = copy.deepcopy(NUMBERS_AIRCLEANER)
        for description in NUMBERS_AIRCLEANER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_IRRIGATOR_TYPE): 
    # Create irrigator  
        NUMBERS_IRRIGATOR_LC = copy.deepcopy(NUMBERS_IRRIGATOR)
        for description in NUMBERS_IRRIGATOR_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if ((device_type in POLARIS_HEATER_TYPE) and (device_type not in ("814","849"))):
    # Create Heater  
        NUMBERS_HEATER_LC = copy.deepcopy(NUMBERS_HEATER)
        for description in NUMBERS_HEATER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_THERMOSTAT_TYPE): 
    # Create Heater  
        NUMBERS_THERMOSTAT_LC = copy.deepcopy(NUMBERS_THERMOSTAT)
        for description in NUMBERS_THERMOSTAT_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.device_prefix_topic = device_prefix_topic
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    async_add_entities(numberList, update_before_add=True)


class PolarisNumber(PolarisBaseEntity, NumberEntity):

    entity_description: PolarisNumberEntityDescription
    def __init__(
        self,
        device_friendly_name: str,
        description: PolarisNumberEntityDescription,
        mqtt_root: str,
        device_id: str | None=None,
        device_type: str | None=None,
    ) -> None:
        super().__init__(
            device_friendly_name=device_friendly_name,
            mqtt_root=mqtt_root,
            device_type=device_type,
            device_id=device_id,
        )
        self.entity_description = description
        self._attr_unique_id = slugify(f"{device_id}_{description.name}")
        self.entity_id = f"{DOMAIN}.{POLARIS_DEVICE[int(device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(device_type)]['model'].replace('-', '_').lower()}_{description.key}"
        self._attr_available = False
        self._attr_has_entity_name = True
        self._attr_native_value = self.entity_description.native_value
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "coffeemaker":
            if self.entity_description.name != "display_time":
                self._attr_native_value = STATE_UNAVAILABLE
        if self.device_type in POLARIS_HUMIDDIFIER_LOW_FAN_TYPE:
            self._attr_native_max_value = 3
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "air_fryer":
            self._attr_native_max_value = 220
            self._attr_native_min_value = 35
        if self.device_type in POLARIS_THERMOSTAT_TYPE:
            self._data_zero = "00000000000000000000000000000000000000"


    def set_native_value(self, value: float) -> None:
        if value % 1 > 0:
            self._attr_native_value = STATE_UNAVAILABLE
        elif ((self.entity_description.key == "display_time") or
              (self.entity_description.key == "temperature_difference_antifrost") or
              (self.entity_description.key == "temperature_difference_eco")):
            self._attr_native_value = int(value)
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, f"{int(value):02x}", 0, True)
        elif self.entity_description.name == "time_timer":
            self._attr_native_value = int(value)
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, int(value)*3600)

        elif self.entity_description.translation_key == "power_cable":
            self._attr_native_value = int(value)
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, f"{int(value):04x}"[-2:]+f"{int(value):04x}"[:2])

        elif self.entity_description.translation_key == "bright_backlight":
            self._attr_native_value = int(value)
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, f"{self._data_zero[:2]}{hex(int(value))[2:]}{self._data_zero[4:]}")

        else:
            self._attr_native_value = int(value)
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, int(value))
            
    @property
    def get_state (self) -> int | None:
        return self._attr_native_value
        
    async def async_added_to_hass(self):
        @callback
        def message_received_numb(message):
            if self.entity_description.name == "display_time":
                self._attr_native_value = int(message.payload, 16)
            elif self.entity_description.name == "time_timer":
                self._attr_native_value = int(int(message.payload) / 3600)
            elif self.entity_description.translation_key == "bright_backlight":
                self._data_zero = message.payload
                self._attr_native_value = int(self._data_zero[2:4], 16)
            elif self.entity_description.translation_key == "power_cable":
                self._attr_native_value = int(message.payload[:2],16) + (int(message.payload[-2:],16)*256)
            else:
                if self.entity_description.native_min_value <= int(message.payload):
                    self._attr_native_value = message.payload
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.mqttTopicCurrent,
            message_received_numb,
            1,
        )
        @callback
        async def entity_availability(message):
            if self.entity_description.name != "available":
                if str(message.payload).lower() in ("1", "true"):
                    self._attr_available = False
                else:
                    self._attr_available = True
                self.async_write_ha_state()
            
        await mqtt.async_subscribe(self.hass, f"{self.mqtt_root}/{self.entity_description.device_prefix_topic}/state/error/connection", entity_availability, 1)


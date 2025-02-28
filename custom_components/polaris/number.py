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

# Import global values.
from .const import (
    MANUFACTURER,
    MQTT_ROOT_TOPIC,
    DEVICEID,
    DEVICETYPE,
    POLARIS_DEVICE,
    NUMBER_HUMIDIFIER,
    NUMBER_COOKER,
    PolarisNumberEntityDescription,
    POLARIS_KETTLE_TYPE,
    POLARIS_KETTLE_WITH_WEIGHT_TYPE,
    POLARIS_HUMIDDIFIER_TYPE,
    POLARIS_COOKER_TYPE,
)

#_LOGGER = logging.getLogger(__name__)
#_LOGGER.setLevel(logging.DEBUG)

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
        NUMBER_HUMIDIFIER_LC = copy.deepcopy(NUMBER_HUMIDIFIER)
        for description in NUMBER_HUMIDIFIER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            numberList.append(
                PolarisNumber(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    elif (device_type in POLARIS_COOKER_TYPE):
    # Create cooker  
        NUMBER_COOKER_LC = copy.deepcopy(NUMBER_COOKER)
        for description in NUMBER_COOKER_LC:
            description.mqttTopicCurrent = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrent}" 
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
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
        self.entity_id = f"{DOMAIN}.{POLARIS_DEVICE[int(device_type)]['class']}_{POLARIS_DEVICE[int(device_type)]['model']}_{description.name}"
        self._attr_available = True
        self._attr_has_entity_name = True
        self._attr_native_value = 115

    def set_native_value(self, value: int) -> None:
        self._attr_native_value = int(value)
        self.hass.components.mqtt.publish(self.hass, self.entity_description.mqttTopicCommand, int(value))
        
    @property
    def get_state (self) -> int | None:
        return self._attr_native_value
        
    async def async_added_to_hass(self):
        @callback
        def message_received_numb(message):
            self._attr_native_value = message.payload
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.mqttTopicCurrent,
            message_received_numb,
            1,
        )

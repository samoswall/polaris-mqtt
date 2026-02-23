"""The Polaris IQ Home component."""
from __future__ import annotations

#import json
import re
import logging
from typing import Any
import copy
import math

from homeassistant.components import mqtt
from homeassistant.components.fan import DOMAIN, FanEntity, FanEntityFeature
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.util import slugify
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import async_get as async_get_dev_reg
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)
from homeassistant.util.scaling import int_states_in_range

from .common import PolarisBaseEntity
# Import global values.
from .const import (
    MANUFACTURER,
    MQTT_ROOT_TOPIC,
    DEVICEID,
    DEVICETYPE,
    POLARIS_DEVICE,
    FANS,
    PolarisFanEntityDescription,
    POLARIS_FAN_TYPE
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
    fanList = []

    if (device_type in POLARIS_FAN_TYPE):
        # Create fan
        FANS_LC = copy.deepcopy(FANS)
        for description in FANS_LC:
            description.mqttTopicCurrentFanMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentFanMode}"
            description.mqttTopicCommandFanMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandFanMode}"
            description.mqttTopicCommandPower = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandPower}"
            description.mqttTopicCurrentPresetMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentPresetMode}"
            description.mqttTopicCommandPresetMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandPresetMode}"
            description.device_prefix_topic = device_prefix_topic
            fanList.append(
                PolarisFan(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )

    async_add_entities(fanList, update_before_add=True)

class PolarisFan(PolarisBaseEntity, FanEntity):
    entity_description: PolarisFanEntityDescription
    def __init__(
        self,
        device_friendly_name: str,
        description: PolarisFanEntityDescription,
        mqtt_root: str,
        device_id: str | None=None,
        device_type: str | None=None
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

        self._attr_has_entity_name = True
        self._attr_available = False

        self._percentage_list = self.entity_description.percentage_list
        self._attr_supported_features = self.entity_description.supported_features
        self._attr_preset_modes = list(self.entity_description.preset_modes.keys())
        self._attr_preset_mode = self._attr_preset_modes[0]
        self._attr_speed_count = max(self._percentage_list)
        self._attr_percentage = 100
        self._speed_range = (min(self._percentage_list), max(self._percentage_list))

    async def async_added_to_hass(self):
        @callback
        def preset_mode_message_received(message):
            self._attr_preset_mode = list(self.entity_description.preset_modes.keys())[list(self.entity_description.preset_modes.values()).index(message.payload)]
            self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicCurrentPresetMode, preset_mode_message_received, 1)

        @callback
        def percentage_message_received(message):
            self._attr_percentage = ranged_value_to_percentage(self._speed_range, int(message.payload))
            self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicCurrentFanMode, percentage_message_received, 1)

        @callback
        async def entity_availability(message):
            if self.entity_description.name != "available":
                if str(message.payload).lower() in ("1", "true"):
                    self._attr_available = False
                else:
                    self._attr_available = True
                self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, f"{self.mqtt_root}/{self.entity_description.device_prefix_topic}/state/error/connection", entity_availability, 1)


    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        if percentage:
            await self.async_set_percentage(percentage)
        if preset_mode:
            await self.async_set_preset_mode(preset_mode)
        if percentage == None and preset_mode == None:
            await self.async_set_preset_mode("auto")
        _LOGGER.debug(f"TURN ON % {percentage} preset {preset_mode}")
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        mqtt.publish(self.hass, f"{self.entity_description.mqttTopicCommandPower}", "0")
        self._attr_preset_mode = "off"
        _LOGGER.debug("TURN OFF")
        self.async_write_ha_state()
        
    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        self._attr_preset_mode = preset_mode
        mqtt.publish(self.hass, f"{self.entity_description.mqttTopicCommandPower}", self.entity_description.preset_modes[preset_mode])
        self.async_write_ha_state()
        
    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""   
 #       if percentage > 0:
 #           self._attr_speed_count = percentage_to_ordered_list_item(self._percentage_list, percentage)
        if percentage == 0:
            percentage = 1
        self._attr_speed_count = math.ceil(percentage_to_ranged_value(self._speed_range, percentage))
        self._attr_percentage = percentage
        mqtt.publish(self.hass, f"{self.entity_description.mqttTopicCommandFanMode}", str(self._attr_speed_count))
 #       else:
 #           self._attr_percentage = 0
 #           self._attr_speed_count = 1
 #           mqtt.publish(self.hass, f"{self.entity_description.mqttTopicCommandFanMode}", str(self._attr_speed_count))
 #           mqtt.publish(self.hass, f"{self.entity_description.mqttTopicCommandPresetMode}", "0")
        self.async_write_ha_state()
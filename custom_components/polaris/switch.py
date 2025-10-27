"""The Polaris IQ Home component."""
from __future__ import annotations

import json
import re
import logging
from typing import Iterable
import copy

from homeassistant.components import mqtt
from homeassistant.components.switch import DOMAIN, SwitchEntity
#from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.util import slugify
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import async_get as async_get_dev_reg

from .common import PolarisBaseEntity
# Import global values.
from .const import (
    MANUFACTURER,
    MQTT_ROOT_TOPIC,
    DEVICEID,
    DEVICETYPE,
    POLARIS_DEVICE,
    SWITCHES_ALL_DEVICES,
    SWITCH_KETTLE_BACKLIGHT,
    SWITCH_HUMIDIFIER_BACKLIGHT,
    SWITCH_HUMIDIFIER_IONISER,
    SWITCH_HUMIDIFIER_WARM_STREAM,
    SWITCHES_COOKER,
    SWITCHES_COFFEEMAKER,
    SWITCHES_COFFEEMAKER_ROG,
    SWITCHES_CLIMATE,
    SWITCHES_CLIMATE_200,
    SWITCHES_AIRCLEANER,
    SWITCHES_AIRCLEANER_EAP,
    SWITCHES_VACUUM,
    SWITCHES_WATER_BOILER,
    SWITCHES_IRRIGATOR,
    SWITCHES_HEATER,
    SWITCHES_AIRCONDITIONER,
    PolarisSwitchEntityDescription,
    POLARIS_KETTLE_TYPE,
    POLARIS_KETTLE_WITH_WEIGHT_TYPE,
    POLARIS_KETTLE_WITH_BACKLIGHT_TYPE,
    POLARIS_HUMIDDIFIER_TYPE,
    POLARIS_HUMIDDIFIER_WITH_IONISER_TYPE,
    POLARIS_HUMIDDIFIER_WITH_WARM_STREAM_TYPE,
    POLARIS_COOKER_TYPE,
    POLARIS_COFFEEMAKER_TYPE,
    POLARIS_COFFEEMAKER_ROG_TYPE,
    POLARIS_CLIMATE_TYPE,
    POLARIS_AIRCLEANER_TYPE,
    POLARIS_AIRCLEANER_EAP_TYPE,
    POLARIS_VACUUM_TYPE,
    POLARIS_BOILER_TYPE,
    POLARIS_IRRIGATOR_TYPE,
    POLARIS_HEATER_TYPE,
    POLARIS_AIRCONDITIONER_TYPE,
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
    switchList = []

    if (device_type in POLARIS_KETTLE_TYPE) or (device_type in POLARIS_KETTLE_WITH_WEIGHT_TYPE):
        # Create sensors for all devices
        SWITCHES_ALL_DEVICES_LC = copy.deepcopy(SWITCHES_ALL_DEVICES)
        for description in SWITCHES_ALL_DEVICES_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if device_type in POLARIS_KETTLE_WITH_BACKLIGHT_TYPE:
        # Create sensors for backlight devices
        SWITCH_KETTLE_BACKLIGHT_LC = copy.deepcopy(SWITCH_KETTLE_BACKLIGHT)
        for description in SWITCH_KETTLE_BACKLIGHT_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_HUMIDDIFIER_TYPE):
        # Create switches for all devices
        SWITCHES_ALL_DEVICES_LC = copy.deepcopy(SWITCHES_ALL_DEVICES)
        for description in SWITCHES_ALL_DEVICES_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
        SWITCH_HUMIDIFIER_BACKLIGHT_LC = copy.deepcopy(SWITCH_HUMIDIFIER_BACKLIGHT)
        for description in SWITCH_HUMIDIFIER_BACKLIGHT_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_HUMIDDIFIER_WITH_IONISER_TYPE):
        # Create switch ioniser for humidifiers
        SWITCH_HUMIDIFIER_IONISER_LC = copy.deepcopy(SWITCH_HUMIDIFIER_IONISER)
        for description in SWITCH_HUMIDIFIER_IONISER_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_HUMIDDIFIER_WITH_WARM_STREAM_TYPE):
        # Create switch stream warm for humidifiers
        SWITCH_HUMIDIFIER_WARM_STREAM_LC = copy.deepcopy(SWITCH_HUMIDIFIER_WARM_STREAM)
        for description in SWITCH_HUMIDIFIER_WARM_STREAM_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COOKER_TYPE):
        # Create switches for cooker
        SWITCHES_COOKER_LC = copy.deepcopy(SWITCHES_COOKER)
        for description in SWITCHES_COOKER_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_TYPE):
        # Create switches for coffeemaker
        SWITCHES_COFFEEMAKER_LC = copy.deepcopy(SWITCHES_COFFEEMAKER)
        for description in SWITCHES_COFFEEMAKER_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_ROG_TYPE):
        # Create switches for coffeemaker
        SWITCHES_COFFEEMAKER_ROG_LC = copy.deepcopy(SWITCHES_COFFEEMAKER_ROG)
        for description in SWITCHES_COFFEEMAKER_ROG_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_CLIMATE_TYPE):
        # Create switches for climate
        SWITCHES_CLIMATE_LC = copy.deepcopy(SWITCHES_CLIMATE)
        for description in SWITCHES_CLIMATE_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
        if (device_type == "859"):
            SWITCHES_CLIMATE_200_LC = copy.deepcopy(SWITCHES_CLIMATE_200)
            for description in SWITCHES_CLIMATE_200_LC:
                description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
                description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
                description.device_prefix_topic = device_prefix_topic
                switchList.append(
                    PolarisSwitch(
                        description=description,
                        device_friendly_name=device_id,
                        mqtt_root=mqtt_root,
                        device_type=device_type,
                        device_id=device_id
                    )
                )
    if (device_type in POLARIS_AIRCLEANER_TYPE):
        # Create switches for all devices
        SWITCHES_ALL_DEVICES_LC = copy.deepcopy(SWITCHES_ALL_DEVICES)
        for description in SWITCHES_ALL_DEVICES_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
        SWITCHES_AIRCLEANER_LC = copy.deepcopy(SWITCHES_AIRCLEANER)
        for description in SWITCHES_AIRCLEANER_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_AIRCLEANER_EAP_TYPE):
        SWITCHES_AIRCLEANER_EAP_LC = copy.deepcopy(SWITCHES_AIRCLEANER_EAP)
        for description in SWITCHES_AIRCLEANER_EAP_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_VACUUM_TYPE):
        # Create switches for vacuum
        SWITCHES_VACUUM_LC = copy.deepcopy(SWITCHES_VACUUM)
        for description in SWITCHES_VACUUM_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_BOILER_TYPE):
        # Create switches for boiler
        SWITCHES_WATER_BOILER_LC = copy.deepcopy(SWITCHES_WATER_BOILER)
        for description in SWITCHES_WATER_BOILER_LC:
            if (device_type != "833" or description.translation_key != "child_lock_switch") and (device_type != "833" or description.translation_key != "smart_mode"):
                description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
                description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
                description.device_prefix_topic = device_prefix_topic
                switchList.append(
                    PolarisSwitch(
                        description=description,
                        device_friendly_name=device_id,
                        mqtt_root=mqtt_root,
                        device_type=device_type,
                        device_id=device_id
                    )
                )
    if (device_type in POLARIS_IRRIGATOR_TYPE):
        # Create switches for irrigator
        SWITCHES_IRRIGATOR_LC = copy.deepcopy(SWITCHES_IRRIGATOR)
        for description in SWITCHES_IRRIGATOR_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    if (device_type in POLARIS_HEATER_TYPE):
        # Create switches for heater
        SWITCHES_HEATER_LC = copy.deepcopy(SWITCHES_HEATER)
        for description in SWITCHES_HEATER_LC:
            if (device_type != "806" or description.translation_key != "half_power_heater"):
                description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
                description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
                description.device_prefix_topic = device_prefix_topic
                switchList.append(
                    PolarisSwitch(
                        description=description,
                        device_friendly_name=device_id,
                        mqtt_root=mqtt_root,
                        device_type=device_type,
                        device_id=device_id
                    )
                )
    if (device_type in POLARIS_AIRCONDITIONER_TYPE):
        # Create switches for irrigator
        SWITCHES_AIRCONDITIONER_LC = copy.deepcopy(SWITCHES_AIRCONDITIONER)
        for description in SWITCHES_AIRCONDITIONER_LC:
            description.mqttTopicCommand = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommand}"
            description.mqttTopicCurrentValue = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentValue}"
            description.device_prefix_topic = device_prefix_topic
            switchList.append(
                PolarisSwitch(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id
                )
            )
    async_add_entities(switchList, update_before_add=True)

class PolarisSwitch(PolarisBaseEntity, SwitchEntity):
    entity_description: PolarisSwitchEntityDescription
    def __init__(
        self,
        device_friendly_name: str,
        description: PolarisSwitchEntityDescription,
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
        self.entity_id = f"{DOMAIN}.{POLARIS_DEVICE[int(device_type)]['class']}_{POLARIS_DEVICE[int(device_type)]['model']}_{description.name}"
        self.payload_on=description.payload_on
        self.payload_off=description.payload_off
        self._attr_has_entity_name = True
#        self._old_mode = "0"
        self._attr_available = False
#        self._attr_assumed_state = False
#        self._optimistic = False
#        self._value_template = self.entity_description.mqttTopicCurrentValue
        if device_type == "806":
            self._heater_prog_data0 = "0000"
        else:
            self._heater_prog_data0 = "000000"
        if device_type == "826":
            self._EAP_data0 = "0000"
        if device_type == "813":
            self._swing_message = "00000000"
            if self.entity_description.key == "eco_mode_switch":
                self._attr_available = False
            if self.entity_description.key == "auto_heater_switch":
                self._attr_available = False

    async def async_added_to_hass(self):
        @callback
        def message_received(message):
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "coffeemaker":
                if int(self.device_type) in POLARIS_COFFEEMAKER_ROG_TYPE:
                    if str(message.payload) in ("1", "2", "3", "4", "5", "6"):
                        self._attr_is_on = True
                    else:
                        self._attr_is_on = False
                elif str(message.payload) in ("01", "1", "03", "3"):
                    self._attr_is_on = True
                else:
                    self._attr_is_on = False
            elif self.entity_description.key == "display_off_heater":
                self._heater_prog_data0 = str(message.payload)
                self._attr_is_on = True if (self._heater_prog_data0[2:4] == "01") else False
            elif self.entity_description.key == "half_power_heater":
                self._heater_prog_data0 = str(message.payload)
                self._attr_is_on = True if (self._heater_prog_data0[-2:] == "01") else False
            else:
                if str(message.payload).lower() in ("1", "01", "2", "3", "4", "5", "true"):
                    self._attr_is_on = True
                elif str(message.payload).lower() in ("0", "00", "false"):
                   self._attr_is_on = False
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.mqttTopicCurrentValue,
            message_received,
            1,
        )
        
        @callback
        def mode_message_received(message):
            if self.entity_description.translation_key == "keepwarm_switch":
                if str(message.payload) in ("[]", '[{"mode":1,"time":0,"temperature":0}]'):
                    self._attr_available = False
#                    self._attr_is_on = False
                else:
                    self._attr_available = True
                    self._attr_is_on = True
                self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.mqttTopicCurrentValue.replace("keepwarm", "steps"),
            mode_message_received,
            1,
        )
        
        @callback
        def EAP_data_message_received(message):
            self._EAP_data0 = message.payload
#            _LOGGER.debug("EAP data0 message %s", self._EAP_data0)
        if self.device_type == "826":
            await mqtt.async_subscribe(
                self.hass,
                self.entity_description.mqttTopicCurrentValue.replace("backlight", "program_data/0"),
                EAP_data_message_received,
                1,
            )
            
        @callback
        def mode_conditioner_data_message_received(message):
          if (self.entity_description.key == "auto_heater_switch") or (self.entity_description.key == "eco_mode_switch"):
#            _LOGGER.debug("conditioner mode message %s", message.payload)
            if (message.payload == "4"): #HEAT
#                _LOGGER.debug("conditioner HEAT")
                if self.entity_description.key == "auto_heater_switch":
#                    _LOGGER.debug("conditioner HEAT SW ON")
                    self._attr_available = True
            elif self.entity_description.key == "auto_heater_switch":
#                _LOGGER.debug("conditioner HEAT SW OFF")
                self._attr_available = False
            if (message.payload == "2"): #COOL
                if (self.entity_description.key == "eco_mode_switch"): 
                    self._attr_available = True
            elif self.entity_description.key == "eco_mode_switch":
                self._attr_available = False
            self.async_write_ha_state()
        if self.device_type == "813":
            await mqtt.async_subscribe(
                self.hass,
                self.entity_description.mqttTopicCurrentValue.replace("program_data/0", "mode"),
                mode_conditioner_data_message_received,
                1,
            )
        
        @callback
        def swing_data_message_received(message):
            self._swing_message = message.payload
#            _LOGGER.debug("swing switch data0 message %s", self._swing_message)
            if self.entity_description.key == "eco_mode_switch":
                if message.payload[4:6] == "01":
                    self._attr_is_on = True
                else:
                   self._attr_is_on = False
                self.async_write_ha_state()
            if self.entity_description.key == "auto_heater_switch":
                if message.payload[-2:] == "01":
                    self._attr_is_on = True
                else:
                   self._attr_is_on = False
                self.async_write_ha_state()
        if self.device_type == "813":
            await mqtt.async_subscribe(
                self.hass,
                self.entity_description.mqttTopicCurrentValue,
                swing_data_message_received,
                1,
            )
        
        @callback
        async def entity_availability(message):
            if self.entity_description.name != "available":
                if str(message.payload).lower() in ("1", "true"):
                    self._attr_available = False
                else:
                    if self.entity_description.key != "keepwarm":
                        self._attr_available = True
                self.async_write_ha_state()
            
        await mqtt.async_subscribe(self.hass, f"{self.mqtt_root}/{self.entity_description.device_prefix_topic}/state/error/connection", entity_availability, 1)


    def turn_on(self, **kwargs):
#        self._attr_is_on = True # optimistic mode
        topic = f"{self.entity_description.mqttTopicCommand}"
        if self.entity_description.key == "display_off_heater":
            if self.device_type == "806":
                send_message = self._heater_prog_data0[:2] + self.payload_on
            else:
                send_message = self._heater_prog_data0[:2] + self.payload_on + self._heater_prog_data0[-2:]
        elif self.entity_description.key == "eco_mode_switch":
            send_message = self._swing_message[:4] + self.payload_on + self._swing_message[-2:]
        elif self.entity_description.key == "auto_heater_switch":
            send_message = self._swing_message[:6] + self.payload_on
        elif self.entity_description.key == "half_power_heater":
            send_message = self._heater_prog_data0[:4] + self.payload_on
        elif (self.device_type == "826" and self.entity_description.key == "backlight"):
            self._EAP_data0 = self._EAP_data0[:2] + "01"
#            _LOGGER.debug("EAP data0 backlight ON %s", self._EAP_data0)  # отправить в prog_data
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand.replace("backlight", "program_data/0"), self._EAP_data0)
            send_message = self.payload_on
        else:
            send_message = self.payload_on
        mqtt.publish(self.hass, topic, send_message)


    def turn_off(self, **kwargs):
#        self._attr_is_on = False # optimistic mode
        topic = f"{self.entity_description.mqttTopicCommand}"
        if self.entity_description.key == "display_off_heater":
            if self.device_type == "806":
                send_message = self._heater_prog_data0[:2] + self.payload_off
            else:
                send_message = self._heater_prog_data0[:2] + self.payload_off + self._heater_prog_data0[-2:]
        elif self.entity_description.key == "eco_mode_switch":
            send_message = self._swing_message[:4] + self.payload_off + self._swing_message[-2:]
        elif self.entity_description.key == "auto_heater_switch":
            send_message = self._swing_message[:6] + self.payload_off
        elif self.entity_description.key == "half_power_heater":
            send_message = self._heater_prog_data0[:4] + self.payload_off
        elif (self.device_type == "826" and self.entity_description.key == "backlight"):
            self._EAP_data0 = self._EAP_data0[:2] + "00"
#            _LOGGER.debug("EAP data0 backlight OFF %s", self._EAP_data0)  # отправить в prog_data
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommand.replace("backlight", "program_data/0"), self._EAP_data0)
            send_message = self.payload_off
        else:
            send_message = self.payload_off
        mqtt.publish(self.hass, topic, send_message)




"""The Polaris IQ Home component."""
from __future__ import annotations

import json
import re
import logging
from typing import Iterable
import copy
import datetime
import os
from pathlib import Path
from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage

from homeassistant.components.select import DOMAIN, SelectEntity
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
    CUSTOM_SELECT_FILE_PATH,
    SELECT_KETTLE,
    SELECT_COOKER,
    SELECT_COFFEEMAKER,
    SELECT_COFFEEMAKER_ROG,
    SELECT_CLIMATE,
    SELECT_VACUUM,
    SELECT_IRRIGATOR,
    SELECT_AIRCLEANER_EAP,
    SELECT_AIRCONDITIONER_SWING_HORIZONTAL,
    SELECT_AIRCONDITIONER_SWING_VERTICAL,
    PolarisSelectEntityDescription,
    POLARIS_KETTLE_TYPE,
    POLARIS_KETTLE_WITH_WEIGHT_TYPE,
    POLARIS_HUMIDDIFIER_TYPE,
    POLARIS_COOKER_TYPE,
    POLARIS_COFFEEMAKER_TYPE,
    POLARIS_COFFEEMAKER_ROG_TYPE,
    POLARIS_CLIMATE_TYPE,
    POLARIS_VACUUM_TYPE,
    POLARIS_IRRIGATOR_TYPE,
    POLARIS_AIRCLEANER_EAP_TYPE,
    POLARIS_AIRCONDITIONER_TYPE,
    AIRFRYER_1_MODES,
    AIRFRYER_2_MODES,
    POLARIS_VACUUM_01_MODE_TYPE,
    POLARIS_VACUUM_02_MODE_TYPE,
    POLARIS_VACUUM_03_MODE_TYPE,
    POLARIS_VACUUM_04_MODE_TYPE,
    POLARIS_VACUUM_05_MODE_TYPE,
    POLARIS_VACUUM_06_MODE_TYPE,
    POLARIS_VACUUM_07_MODE_TYPE,
    POLARIS_VACUUM_08_MODE_TYPE,
    POLARIS_VACUUM_09_MODE_TYPE,
    POLARIS_VACUUM_10_MODE_TYPE,
    POLARIS_VACUUM_11_MODE_TYPE,
    POLARIS_VACUUM_12_MODE_TYPE,
    POLARIS_VACUUM_13_MODE_TYPE,
    POLARIS_VACUUM_14_MODE_TYPE,
    POLARIS_VACUUM_15_MODE_TYPE,
    POLARIS_VACUUM_16_MODE_TYPE,
    POLARIS_VACUUM_17_MODE_TYPE,
    POLARIS_VACUUM_18_MODE_TYPE,
    VACUUM_01_MODE,
    VACUUM_02_MODE,
    VACUUM_03_MODE,
    VACUUM_04_MODE,
    VACUUM_05_MODE,
    VACUUM_06_MODE,
    VACUUM_07_MODE,
    VACUUM_08_MODE,
    VACUUM_09_MODE,
    VACUUM_10_MODE,
    VACUUM_11_MODE,
    VACUUM_12_MODE,
    VACUUM_13_MODE,
    VACUUM_14_MODE,
    VACUUM_15_MODE,
    VACUUM_16_MODE,
    VACUUM_17_MODE,
    VACUUM_18_MODE,
    POLARIS_VACUUM_NOT_WATER_TYPE,
    POLARIS_VACUUM_01_WATER_TYPE,
    POLARIS_VACUUM_02_WATER_TYPE,
    POLARIS_VACUUM_03_WATER_TYPE,
    POLARIS_VACUUM_04_WATER_TYPE,
    VACUUM_01_WATER,
    VACUUM_02_WATER,
    VACUUM_03_WATER,
    VACUUM_04_WATER
)


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

async def _async_read_file(hass):
    path = Path(CUSTOM_SELECT_FILE_PATH)
    if not path.exists():
        return None
    text = await hass.async_add_executor_job(path.read_text, "utf-8")
    return json.loads(text)

async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_entities: AddEntitiesCallback,
) -> None:
    integrationUniqueID = config.unique_id
    mqtt_root = config.data[MQTT_ROOT_TOPIC]
    device_id = config.data["DEVICEID"]
    device_type = config.data[DEVICETYPE]
    device_prefix_topic = config.data["DEVPREFIXTOPIC"]
    selectList = []
    
    custom_data_select = await _async_read_file(hass)

    if (device_type in POLARIS_KETTLE_TYPE) or (device_type in POLARIS_KETTLE_WITH_WEIGHT_TYPE):
        SELECT_KETTLE_LC = copy.deepcopy(SELECT_KETTLE)
        for description in SELECT_KETTLE_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.mqttTopicCommandTemperature = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandTemperature}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_COOKER_TYPE):
        SELECT_COOKER_LC = copy.deepcopy(SELECT_COOKER)
        for description in SELECT_COOKER_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.mqttTopicCommandTemperature = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandTemperature}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_TYPE):
        SELECT_COFFEEMAKER_LC = copy.deepcopy(SELECT_COFFEEMAKER)
        for description in SELECT_COFFEEMAKER_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_COFFEEMAKER_ROG_TYPE):
        SELECT_COFFEEMAKER_ROG_LC = copy.deepcopy(SELECT_COFFEEMAKER_ROG)
        for description in SELECT_COFFEEMAKER_ROG_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_CLIMATE_TYPE):
        SELECT_CLIMATE_LC = copy.deepcopy(SELECT_CLIMATE)
        for description in SELECT_CLIMATE_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_VACUUM_TYPE):
        if (int(device_type) not in POLARIS_VACUUM_NOT_WATER_TYPE or description.translation_key != "vacuum_tank"):
            SELECT_VACUUM_LC = copy.deepcopy(SELECT_VACUUM)
            for description in SELECT_VACUUM_LC:
                description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
                description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
                description.device_prefix_topic = device_prefix_topic
                selectList.append(
                    PolarisSelect(
                        description=description,
                        device_friendly_name=device_id,
                        mqtt_root=mqtt_root,
                        device_type=device_type,
                        device_id=device_id,
                        custom_data_select=custom_data_select
                    )
                )
    if (device_type in POLARIS_IRRIGATOR_TYPE):
        SELECT_IRRIGATOR_LC = copy.deepcopy(SELECT_IRRIGATOR)
        for description in SELECT_IRRIGATOR_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_AIRCLEANER_EAP_TYPE):
        SELECT_AIRCLEANER_EAP_LC = copy.deepcopy(SELECT_AIRCLEANER_EAP)
        for description in SELECT_AIRCLEANER_EAP_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_AIRCONDITIONER_TYPE) and (device_type == "813"):
        SELECT_AIRCONDITIONER_SWING_HORIZONTAL_LC = copy.deepcopy(SELECT_AIRCONDITIONER_SWING_HORIZONTAL)
        for description in SELECT_AIRCONDITIONER_SWING_HORIZONTAL_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    if (device_type in POLARIS_AIRCONDITIONER_TYPE) and (device_type == "813"):
        SELECT_AIRCONDITIONER_SWING_VERTICAL_LC = copy.deepcopy(SELECT_AIRCONDITIONER_SWING_VERTICAL)
        for description in SELECT_AIRCONDITIONER_SWING_VERTICAL_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.device_prefix_topic = device_prefix_topic
            selectList.append(
                PolarisSelect(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    custom_data_select=custom_data_select
                )
            )
    async_add_entities(selectList, update_before_add=True)



class PolarisSelect(PolarisBaseEntity, SelectEntity):

    entity_description: PolarisSelectEntityDescription
    def __init__(
        self,
        device_friendly_name: str,
        description: PolarisSelectEntityDescription,
        mqtt_root: str,
        device_id: str | None=None,
        device_type: str | None=None,
        custom_data_select: str | None=None
    ) -> None:
        super().__init__(
            device_friendly_name=device_friendly_name,
            mqtt_root=mqtt_root,
            device_type=device_type,
            device_id=device_id,
        )
        self._custom_data_select = custom_data_select
        self.entity_description = description
        self._attr_unique_id = slugify(f"{device_id}_{description.name}")
        self.entity_id = f"{DOMAIN}.{POLARIS_DEVICE[int(device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(device_type)]['model'].replace('-', '_').lower()}_{description.key}"
        self._attr_has_entity_name = True
        
        if (device_type in ("290","291")):
            self.entity_description.options = AIRFRYER_1_MODES
        if (device_type == "292"):
            self.entity_description.options = AIRFRYER_2_MODES
        if (POLARIS_DEVICE[int(self.device_type)]['class'] == "kettle" or 
            POLARIS_DEVICE[int(self.device_type)]['class'] == "cooker" or 
            POLARIS_DEVICE[int(self.device_type)]['class'] == "coffeemaker" or 
            POLARIS_DEVICE[int(self.device_type)]['class'] == "cleaner" or 
            POLARIS_DEVICE[int(self.device_type)]['class'] == "air_fryer"):
            self._select_options = json.loads(json.dumps(SELECT_COFFEEMAKER[0].options))
        if device_type == "826":
            self._EAP_data0 = "0000"
        if device_type == "813":
            self._conditioner_data0 = "0000"

        if self._custom_data_select is not None:
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "kettle" and "SELECT_KETTLE_options" in self._custom_data_select:
#                self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                for key, value in self._custom_data_select["SELECT_KETTLE_options"].items():
                    self.entity_description.options[key] = value
#                _LOGGER.debug("kettle %s", self.entity_description.options)
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "cooker" and "SELECT_COOKER_options" in self._custom_data_select:
#                self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                for key, value in self._custom_data_select["SELECT_COOKER_options"].items():
                    self.entity_description.options[key] = json.dumps([value])
#                _LOGGER.debug("cooker %s", self.entity_description.options)
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "air_fryer" and "SELECT_AIRFRYER_options" in self._custom_data_select:
#                self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                for key, value in self._custom_data_select["SELECT_AIRFRYER_options"].items():
                    self.entity_description.options[key] = json.dumps([value])
#                _LOGGER.debug("cooker %s", self.entity_description.options)
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "coffeemaker":
                if int(self.device_type) == 45 and "SELECT_COFFEEMAKER_ROG_options" in self._custom_data_select:
#                    self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                    for key, value in self._custom_data_select["SELECT_COFFEEMAKER_ROG_options"].items():
                        self.entity_description.options[key] = json.dumps([value])
#                    _LOGGER.debug("coffee_rog %s", self.entity_description.options)
                elif "SELECT_COFFEEMAKER_options" in self._custom_data_select:
#                    self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                    for key, value in self._custom_data_select["SELECT_COFFEEMAKER_options"].items():
                        self.entity_description.options[key] = json.dumps([value])
#                    _LOGGER.debug("coffee %s", self.entity_description.options)
            if POLARIS_DEVICE[int(self.device_type)]['class'] == "cleaner" and "SELECT_VACUUM_rooms" in self._custom_data_select and self.entity_description.key == "select_room":
#                self.entity_description.options = json.loads(json.dumps(self.entity_description.options))
                for key, value in self._custom_data_select["SELECT_VACUUM_rooms"].items():
                    self.entity_description.options[key] = json.dumps([value])

        if POLARIS_DEVICE[int(self.device_type)]['class'] == "cleaner" and self.entity_description.key == "vacuum_tank":
            if int(self.device_type) in POLARIS_VACUUM_01_WATER_TYPE:
                self.entity_description.options = VACUUM_01_WATER
            if int(self.device_type) in POLARIS_VACUUM_02_WATER_TYPE:
                self.entity_description.options = VACUUM_02_WATER
            if int(self.device_type) in POLARIS_VACUUM_03_WATER_TYPE:
                self.entity_description.options = VACUUM_03_WATER
            if int(self.device_type) in POLARIS_VACUUM_04_WATER_TYPE:
                self.entity_description.options = VACUUM_04_WATER

        if POLARIS_DEVICE[int(self.device_type)]['class'] == "cleaner" and self.entity_description.key == "select_mode_vacuum":
            if int(self.device_type) in POLARIS_VACUUM_01_MODE_TYPE:
                self.entity_description.options = VACUUM_01_MODE
            if int(self.device_type) in POLARIS_VACUUM_02_MODE_TYPE:
                self.entity_description.options = VACUUM_02_MODE
            if int(self.device_type) in POLARIS_VACUUM_03_MODE_TYPE:
                self.entity_description.options = VACUUM_03_MODE
            if int(self.device_type) in POLARIS_VACUUM_04_MODE_TYPE:
                self.entity_description.options = VACUUM_04_MODE
            if int(self.device_type) in POLARIS_VACUUM_05_MODE_TYPE:
                self.entity_description.options = VACUUM_05_MODE
            if int(self.device_type) in POLARIS_VACUUM_06_MODE_TYPE:
                self.entity_description.options = VACUUM_06_MODE
            if int(self.device_type) in POLARIS_VACUUM_07_MODE_TYPE:
                self.entity_description.options = VACUUM_07_MODE
            if int(self.device_type) in POLARIS_VACUUM_08_MODE_TYPE:
                self.entity_description.options = VACUUM_08_MODE
            if int(self.device_type) in POLARIS_VACUUM_09_MODE_TYPE:
                self.entity_description.options = VACUUM_09_MODE
            if int(self.device_type) in POLARIS_VACUUM_10_MODE_TYPE:
                self.entity_description.options = VACUUM_10_MODE
            if int(self.device_type) in POLARIS_VACUUM_11_MODE_TYPE:
                self.entity_description.options = VACUUM_11_MODE
            if int(self.device_type) in POLARIS_VACUUM_12_MODE_TYPE:
                self.entity_description.options = VACUUM_12_MODE
            if int(self.device_type) in POLARIS_VACUUM_13_MODE_TYPE:
                self.entity_description.options = VACUUM_13_MODE
            if int(self.device_type) in POLARIS_VACUUM_14_MODE_TYPE:
                self.entity_description.options = VACUUM_14_MODE
            if int(self.device_type) in POLARIS_VACUUM_15_MODE_TYPE:
                self.entity_description.options = VACUUM_15_MODE
            if int(self.device_type) in POLARIS_VACUUM_16_MODE_TYPE:
                self.entity_description.options = VACUUM_16_MODE
            if int(self.device_type) in POLARIS_VACUUM_17_MODE_TYPE:
                self.entity_description.options = VACUUM_17_MODE
            if int(self.device_type) in POLARIS_VACUUM_18_MODE_TYPE:
                self.entity_description.options = VACUUM_18_MODE
            self._attr_options = list(self.entity_description.options.keys())
            self._attr_options.remove("off")
            self._attr_current_option = "auto"
        else:
            self._attr_options = list(self.entity_description.options.keys())
            self._attr_current_option = self._attr_options[0]
        self._attr_available = False

    def key_from_option(self, option: str):
        try:
            return next(
                key
                for key, value in self.entity_description.options.items()
                if json.loads(value)[0]["mode"] == option
            )
        except StopIteration:
            return None

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "cooker":
            cook_time = json.loads(self.entity_description.options[option])
            service_data = {}
            service_data["entity_id"] = f"time.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_cooking_time"
            service_data["time"] = str(datetime.timedelta(seconds=cook_time[0]["time"]))
            await self.hass.services.async_call("time", "set_value", service_data)
            service_data = {}
            service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_set_temperature"
            service_data["value"] = cook_time[0]["temperature"]
            await self.hass.services.async_call("number", "set_value", service_data)
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "air_fryer":
            cook_time = json.loads(self.entity_description.options[option])
            service_data = {}
            service_data["entity_id"] = f"time.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_cooking_time"
            service_data["time"] = str(datetime.timedelta(seconds=cook_time[0]["time"]))
            await self.hass.services.async_call("time", "set_value", service_data)
            service_data = {}
            service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_set_temperature"
            service_data["value"] = cook_time[0]["temperature"]
            await self.hass.services.async_call("number", "set_value", service_data)
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "kettle":
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandTemperature, self.entity_description.options[option])
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, 3)
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "coffeemaker":
            if int(self.device_type) == 45:
                coffee_mode = json.loads(self.entity_description.options[option])
                
                service_data = {}
                service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_tank"
                if coffee_mode[0]["tank"] != 0:
                   service_data["value"] = str(coffee_mode[0]["tank"])
                else:
                   service_data["value"] = 7.777
                await self.hass.services.async_call("number", "set_value", service_data)
                
                service_data = {}
                service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_amount"
                if coffee_mode[0]["amount"] != 0:
                    service_data["value"] = str(coffee_mode[0]["amount"])
                else:
                    service_data["value"] = 100.777
                await self.hass.services.async_call("number", "set_value", service_data)
                
                service_data = {}
                service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_temperature"
                if coffee_mode[0]["temperature"] != 0:
                    service_data["value"] = str(coffee_mode[0]["temperature"])
                else:
                    service_data["value"] = 100.777
                await self.hass.services.async_call("number", "set_value", service_data)
                
            else:
                coffee_mode = json.loads(self.entity_description.options[option])
                for key, val in coffee_mode[0].items():
                    if key == "mode":
                        mode = val
                    elif val != 0:
                        service_data = {}
                        service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_{key}"
                        service_data["value"] = str(val)
                        await self.hass.services.async_call("number", "set_value", service_data)
                    else:
                        if key == "weight": 
                            val = "7.777"
                        else:
                            val = "55.777"
                        service_data = {}
                        service_data["entity_id"] = f"number.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_{key}"
                        service_data["value"] = val
                        await self.hass.services.async_call("number", "set_value", service_data)
        if self.device_type in POLARIS_CLIMATE_TYPE:
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, self.entity_description.options[option])
        if self.device_type in POLARIS_AIRCONDITIONER_TYPE:
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, self.entity_description.options[option])
            if (int(self.entity_description.options[option]) > 0):
                if self.entity_description.key == "select_swing_horizontal":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode[:-1] + "0", self._conditioner_data0[:2] + "00" + self._conditioner_data0[-4:])
                if self.entity_description.key == "select_swing_vertical":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode[:-1] + "0", "00" + self._conditioner_data0[-6:])
            else:
                if self.entity_description.key == "select_swing_horizontal":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode[:-1] + "0", self._conditioner_data0[:2] + "01" + self._conditioner_data0[-4:])
                if self.entity_description.key == "select_swing_vertical":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode[:-1] + "0", "01" + self._conditioner_data0[-6:])

        if POLARIS_DEVICE[int(self.device_type)]['class'] == "irrigator":
            if self._attr_current_option == "preset3":
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_3[0] == "a" else self._preset_3[0])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_3[1])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_3[2])
            elif self._attr_current_option == "preset2":
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_2[0] == "a" else self._preset_2[0])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_2[1])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_2[2])
            else:
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_1[0] == "a" else self._preset_1[0])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_1[1])
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_1[2])
        if (self.device_type == "826" and self._EAP_data0[:2] == "02"):
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, self._EAP_data0[:3] + str(self.entity_description.options[option]))
        if POLARIS_DEVICE[int(self.device_type)]['class'] == "cleaner":
            if int(self.device_type) not in POLARIS_VACUUM_NOT_WATER_TYPE:
                mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, str(self.entity_description.options[option]))



    async def async_added_to_hass(self):
        @callback
        def message_received_sel(message):
            payload = message.payload
            if payload in ("0", "[]"):
                self._attr_current_option = self._attr_options[0]
                self.async_write_ha_state()
            elif POLARIS_DEVICE[int(self.device_type)]['class'] in ("cooker", "air_fryer"):
                sel_mode = json.loads(payload)[0]["mode"]
          #      if int(sel_mode)>0:
          #          self.switch.set_available(True)
          #      else:
          #          self.switch.set_available(False)
                sel_opt = self.key_from_option(sel_mode)
                self._attr_current_option = sel_opt
                self.async_write_ha_state()
            elif int(self.device_type) == 45:
                sel_opt = self.key_from_option(int(payload))
                self._attr_current_option = sel_opt
                self.async_write_ha_state()
            elif int(self.device_type) == 69:
                self._attr_current_option = self._attr_options[int(payload)]
                self.async_write_ha_state()
            elif int(self.device_type) == 813:
                self._attr_current_option = self._attr_options[int(payload)]
                self.async_write_ha_state()
            elif POLARIS_DEVICE[int(self.device_type)]['class'] == "irrigator":
                self._preset_1 = [payload[1:2], payload[7:8], payload[13:14]]
                self._preset_2 = [payload[3:4], payload[9:10], payload[15:16]]
                self._preset_3 = [payload[5:6], payload[11:12], payload[17:]]
                if self._attr_current_option == "preset3":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_3[0] == "a" else self._preset_3[0])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_3[1])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_3[2])
                elif self._attr_current_option == "preset2":
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_2[0] == "a" else self._preset_2[0])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_2[1])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_2[2])
                else:
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"speed", "10" if self._preset_1[0] == "a" else self._preset_1[0])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"ioniser", self._preset_1[1])
                    mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode+"smart_mode", self._preset_1[2])
            elif self.entity_description.key == "select_mode_vacuum":
                return
            else:
                self._attr_current_option = list(self.entity_description.options.keys())[list(self.entity_description.options.values()).index(payload)]
                self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicCurrentMode, message_received_sel, 1)
        
        @callback
        def EAP_data_message_received(message):
            self._EAP_data0 = message.payload

        if self.device_type == "826":
            await mqtt.async_subscribe(
                self.hass,
                self.entity_description.mqttTopicCurrentMode,
                EAP_data_message_received,
                1,
            )
            
        @callback
        def conditioner_data_message_received(message):
            self._conditioner_data0 = message.payload

        if self.device_type == "813":
            await mqtt.async_subscribe(
                self.hass,
                self.entity_description.mqttTopicCurrentMode[:-1]+"0",
                conditioner_data_message_received,
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


"""The Polaris IQ Home component."""
from __future__ import annotations

import json
import re
import logging
from typing import Iterable, Final, Any
import copy
import datetime
import os
from pathlib import Path
import voluptuous as vol
import struct


from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.vacuum import (
    DOMAIN,
    ATTR_CLEANED_AREA,
    StateVacuumEntity,
    VacuumActivity,
    VacuumEntityFeature,
)
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.const import ATTR_ENTITY_ID, ATTR_ID
from homeassistant.util import slugify
from homeassistant.core import HomeAssistant, callback, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import config_validation as cv, entity_platform
from .common import PolarisBaseEntity
# Import global values.
from .const import (
    MANUFACTURER,
    MQTT_ROOT_TOPIC,
    DEVICEID,
    DEVICETYPE,
    POLARIS_DEVICE,
    VACUUM,
    PolarisSelectEntityDescription,
    POLARIS_VACUUM_TYPE,
    CUSTOM_SELECT_FILE_PATH,
    SELECT_VACUUM,
    POLARIS_VACUUM_01_SPEED_TYPE,
    POLARIS_VACUUM_02_SPEED_TYPE,
    POLARIS_VACUUM_03_SPEED_TYPE,
    POLARIS_VACUUM_04_SPEED_TYPE,
    POLARIS_VACUUM_05_SPEED_TYPE,
    POLARIS_VACUUM_06_SPEED_TYPE,
    VACUUM_01_SPEED,
    VACUUM_02_SPEED,
    VACUUM_03_SPEED,
    VACUUM_04_SPEED,
    VACUUM_05_SPEED,
    VACUUM_06_SPEED,
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
    VACUUM_18_MODE 
)

SERVICE_VACUUM_CLEANING_ROOM: Final = "vacuum_cleaning_room"
ATTR_SELECTED_ROOMS = "rooms"
SELECT_ROOMS = "select_rooms"

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
    vacuumList = []

    custom_data_rooms = await _async_read_file(hass)

    if custom_data_rooms is not None and "SELECT_VACUUM_rooms" in custom_data_rooms:
        custom_data_rooms = json.loads(json.dumps(custom_data_rooms))
        rooms_js = custom_data_rooms["SELECT_VACUUM_rooms"]
#        _LOGGER.debug("rooms_js %s", rooms_js)
    else:
        rooms_js = {"all_rooms": {"id": "00", "coordinate": []}}
    available_rooms = list(rooms_js.keys())
    
    if (device_type in POLARIS_VACUUM_TYPE):
        VACUUM_LC = copy.deepcopy(VACUUM)
        for description in VACUUM_LC:
            description.mqttTopicCurrentMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCurrentMode}"
            description.mqttTopicCommandMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandMode}"
            description.mqttTopicCommandTank = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandTank}"
            description.mqttTopicStateTank = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicStateTank}"
            description.mqttTopicStateFanMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicStateFanMode}"
            description.mqttTopicCommandFanMode = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandFanMode}"
            description.mqttTopicCommandFindMe = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandFindMe}"
            description.mqttTopicCommandGoArea = f"{mqtt_root}/{device_prefix_topic}/{description.mqttTopicCommandGoArea}"
            description.mqttTopicCommandTest = f"{mqtt_root}/{device_prefix_topic}/state"
            description.device_prefix_topic = device_prefix_topic
            vacuumList.append(
                PolarisVacuum(
                    description=description,
                    device_friendly_name=device_id,
                    mqtt_root=mqtt_root,
                    device_type=device_type,
                    device_id=device_id,
                    available_rooms=available_rooms,
                    rooms_js=rooms_js
                )
            )
    async_add_entities(vacuumList, update_before_add=True)
    
    
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        "select_rooms",
        {
        vol.Required(ATTR_ENTITY_ID): cv.entity_ids,
        vol.Required(SELECT_ROOMS): vol.All(cv.string, vol.In(available_rooms))
    },
        "sweep_rooms_wrapper",
    )


class PolarisVacuum(PolarisBaseEntity, StateVacuumEntity):

    entity_description: PolarisVacuumEntityDescription
    
    def __init__(
        self,
        device_friendly_name: str,
        description: PolarisVacuumEntityDescription,
        mqtt_root: str,
        device_id: str | None=None,
        device_type: str | None=None,
        available_rooms: list | None=None,
        rooms_js: str | None=None,
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

        if int(self.device_type) in POLARIS_VACUUM_01_MODE_TYPE:
            self.my_mode_list = VACUUM_01_MODE
        if int(self.device_type) in POLARIS_VACUUM_02_MODE_TYPE:
            self.my_mode_list = VACUUM_02_MODE
        if int(self.device_type) in POLARIS_VACUUM_03_MODE_TYPE:
            self.my_mode_list = VACUUM_03_MODE
        if int(self.device_type) in POLARIS_VACUUM_04_MODE_TYPE:
            self.my_mode_list = VACUUM_04_MODE
        if int(self.device_type) in POLARIS_VACUUM_05_MODE_TYPE:
            self.my_mode_list = VACUUM_05_MODE
        if int(self.device_type) in POLARIS_VACUUM_06_MODE_TYPE:
            self.my_mode_list = VACUUM_06_MODE
        if int(self.device_type) in POLARIS_VACUUM_07_MODE_TYPE:
            self.my_mode_list = VACUUM_07_MODE
        if int(self.device_type) in POLARIS_VACUUM_08_MODE_TYPE:
            self.my_mode_list = VACUUM_08_MODE
        if int(self.device_type) in POLARIS_VACUUM_09_MODE_TYPE:
            self.my_mode_list = VACUUM_09_MODE
        if int(self.device_type) in POLARIS_VACUUM_10_MODE_TYPE:
            self.my_mode_list = VACUUM_10_MODE
        if int(self.device_type) in POLARIS_VACUUM_11_MODE_TYPE:
            self.my_mode_list = VACUUM_11_MODE
        if int(self.device_type) in POLARIS_VACUUM_12_MODE_TYPE:
            self.my_mode_list = VACUUM_12_MODE
        if int(self.device_type) in POLARIS_VACUUM_13_MODE_TYPE:
            self.my_mode_list = VACUUM_13_MODE
        if int(self.device_type) in POLARIS_VACUUM_14_MODE_TYPE:
            self.my_mode_list = VACUUM_14_MODE
        if int(self.device_type) in POLARIS_VACUUM_15_MODE_TYPE:
            self.my_mode_list = VACUUM_15_MODE
        if int(self.device_type) in POLARIS_VACUUM_16_MODE_TYPE:
            self.my_mode_list = VACUUM_16_MODE
        if int(self.device_type) in POLARIS_VACUUM_17_MODE_TYPE:
            self.my_mode_list = VACUUM_17_MODE
        if int(self.device_type) in POLARIS_VACUUM_18_MODE_TYPE:
            self.my_mode_list = VACUUM_18_MODE
            
        if int(self.device_type) in POLARIS_VACUUM_01_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_01_SPEED
        if int(self.device_type) in POLARIS_VACUUM_02_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_02_SPEED
        if int(self.device_type) in POLARIS_VACUUM_03_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_03_SPEED
        if int(self.device_type) in POLARIS_VACUUM_04_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_04_SPEED
        if int(self.device_type) in POLARIS_VACUUM_05_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_05_SPEED
        if int(self.device_type) in POLARIS_VACUUM_06_SPEED_TYPE:
            self.my_fan_speed_list = VACUUM_06_SPEED   
        self._attr_fan_speed_list = list(self.my_fan_speed_list.keys())
        self._attr_fan_speed = self._attr_fan_speed_list[0]
        self._attr_supported_features = (
              VacuumEntityFeature.RETURN_HOME
#            | VacuumEntityFeature.BATTERY
            | VacuumEntityFeature.CLEAN_SPOT
            | VacuumEntityFeature.STOP
#            | VacuumEntityFeature.PAUSE
            | VacuumEntityFeature.START
            | VacuumEntityFeature.LOCATE
            | VacuumEntityFeature.STATE
            | VacuumEntityFeature.SEND_COMMAND
            | VacuumEntityFeature.FAN_SPEED
#            | VacuumEntityFeature.STATUS
            | VacuumEntityFeature.MAP
        )

#        self._attr_battery_icon="mdi:vacuum"
#        self._attr_battery_level=70
#        self._attr_state = "idle"

#    CLEANING = "cleaning"
#    DOCKED = "docked"
#    IDLE = "idle"
#    PAUSED = "paused"
#    RETURNING = "returning"
#    ERROR = "error"



        self._attr_activity = VacuumActivity.DOCKED
        
        self._select_rooms = []
        self._available_rooms = available_rooms
        self._rooms_js = rooms_js
        
    @property
    def select_rooms(self) -> list | None:
        """Return a list of rooms available to clean."""
        if self._select_rooms:
#            _LOGGER.debug("select_rooms : %s", self._select_rooms)
            return self._select_rooms
        return []
 
    @property
    def extra_state_attributes(self):
        """Return a dictionary of device state attributes specific to sharkiq."""
        data = {}
        if self._available_rooms is not None:
            data["available_rooms"] = self._available_rooms
        if self._select_rooms is not None:
            data["select_rooms"] = self._select_rooms
        return data


    def int16_array_to_bytes(self, int16_array, byteorder='little'):
        """
        Преобразует массив int16 обратно в байтовую строку.
        Аргументы:
            int16_array: Массив int16 значений (list of int).
            byteorder: Порядок байтов ('little' или 'big'), по умолчанию 'little'.
        Возвращает:
            Байтовая строка (bytes).
        Вызывает исключение ValueError:
            Если byteorder не является 'little' или 'big'.
        """
        if byteorder not in ('little', 'big'):
            raise ValueError("Неверный порядок байтов. Допустимые значения: 'little', 'big'.")
        endian_prefix = '<' if byteorder == 'little' else '>'
        format_string = endian_prefix + 'h' * len(int16_array)
        return struct.pack(format_string, *int16_array) # * распаковывает массив в аргументы для pack
        
    async def sweep_rooms_wrapper(self, select_rooms):
#        for room in self._room_manager.rooms.keys():
#            self._room_manager.rooms[room] = False
        _LOGGER.debug("room in service %s ", select_rooms)
        #for entry in mysel_rooms:
          #  name = self.hass.states.get(entry).attributes['room_name']
        #    _LOGGER.debug("target_rooms entry %s", entry)
#        await self.sweep_rooms(target_rooms)
#        self.async_schedule_update_ha_state(force_refresh=True)
        
        
    def start(self) -> None:
        """Start or resume the cleaning task."""
#        if self._attr_state != "cleaning":
#            self._attr_state = "cleaning"
        if self._attr_activity != VacuumActivity.CLEANING:
#            self._attr_activity = VacuumActivity.CLEANING
#            self.schedule_update_ha_state()
            state_mode = self.hass.states.get(f"select.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_select_mode_vacuum").state
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, self.my_mode_list[state_mode])

    def stop(self, **kwargs: Any) -> None:
        """Stop the cleaning task, do not return to dock."""
#        self._attr_state = "idle"
#        self._attr_activity = VacuumActivity.IDLE
#        self.schedule_update_ha_state()
        mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, "0")

    def return_to_base(self, **kwargs: Any) -> None:
        """Return dock to charging base."""
#        self._attr_state = "returning"
#        self._attr_activity = VacuumActivity.RETURNING
#        self.schedule_update_ha_state()
        mqtt.publish(self.hass, self.entity_description.mqttTopicCommandMode, self.my_mode_list["recharge"])

    def clean_spot(self, **kwargs: Any) -> None:
        """Perform a spot clean-up."""
#        self._attr_state = "cleaning"
#        self._attr_activity = VacuumActivity.CLEANING
#        self.schedule_update_ha_state()
        select_room = self.hass.states.get(f"select.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_select_room").state
#        _LOGGER.debug("room in select %s ", select_room)
#        _LOGGER.debug("room in select %s ", self._rooms_js[select_room]["coordinate"])
#        _LOGGER.debug("int16_to_bytes %s",self.int16_array_to_bytes(self._rooms_js[select_room]["coordinate"]))
        mqtt.publish(
            self.hass, self.entity_description.mqttTopicCommandGoArea,
            self.int16_array_to_bytes(self._rooms_js[select_room]["coordinate"]),
            1,
            None,
        )

    def set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None:
        """Set the vacuum's fan speed."""
        if fan_speed in self.fan_speed_list:
            self._attr_fan_speed = fan_speed
            self.schedule_update_ha_state()
            mqtt.publish(self.hass, self.entity_description.mqttTopicCommandFanMode, self.my_fan_speed_list[fan_speed])

    async def async_locate(self, **kwargs: Any) -> None:
        """Locate the vacuum's position."""
#        await self.hass.services.async_call(
#            "notify",
#            "persistent_notification",
#            service_data={"message": "I'm here!", "title": "Locate request"},
#        )
#        self._attr_state = "idle"
#        self._attr_activity = VacuumActivity.IDLE
#        self.async_write_ha_state()
        mqtt.publish(self.hass, self.entity_description.mqttTopicCommandFindMe, "true")


    async def async_send_command(
        self,
        command: str,
        params: dict[str, Any] | list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Send a command to the vacuum."""
#        self._attr_state = "idle"
        self._attr_activity = VacuumActivity.IDLE
        self.async_write_ha_state()
        _LOGGER.debug(f"[{self.device_id}] Custom command: {command}")   

    
    async def async_added_to_hass(self):
#        @callback
#        def message_received_batt_state(message):
#            payload = message.payload
#            self._attr_state = payload
#        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicBatteryState, message_received_batt_state, 1)
        
#        @callback
#        def message_received_batt_level(message):
#            payload = message.payload
#            self._attr_battery_level = int(payload)
#            self.async_write_ha_state()
#        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicBatteryLevel, message_received_batt_level, 1)

        @callback
        async def message_received_fan_speed(message):
            payload = message.payload
            self._attr_fan_speed = list(self.my_fan_speed_list.keys())[list(self.my_fan_speed_list.values()).index(payload)]
            self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicStateFanMode, message_received_fan_speed, 1)

        @callback
        async def message_received_mode(message):
            self._current_mode = message.payload
            self._update_activity_from_mode_and_battery()
        await mqtt.async_subscribe(self.hass, self.entity_description.mqttTopicCurrentMode, message_received_mode, 1)
    
        @callback
        async def entity_availability(message):
            if self.entity_description.name != "available":
                if str(message.payload).lower() in ("1", "true"):
                    self._attr_available = False
                else:
                    self._attr_available = True
                self.async_write_ha_state()
        await mqtt.async_subscribe(self.hass, f"{self.mqtt_root}/{self.entity_description.device_prefix_topic}/state/error/connection", entity_availability, 1)

    
    def _update_activity_from_mode_and_battery(self):
        """Update vacuum activity based on mode and battery state."""
        # Получаем состояние батареи из сенсора
        battery_state = None
        battery_entity_id = f"sensor.{POLARIS_DEVICE[int(self.device_type)]['class'].replace('-', '_').lower()}_{POLARIS_DEVICE[int(self.device_type)]['model'].replace('-', '_').lower()}_battery_state"
        battery_state_obj = self.hass.states.get(battery_entity_id)
        if battery_state_obj:
            battery_state = battery_state_obj.state
        
        # Определяем значения режимов из my_mode_list
        off_value = self.my_mode_list.get("off", "0")
        recharge_value = self.my_mode_list.get("recharge")
        
        # Собираем все значения режимов уборки (все кроме off и recharge)
        cleaning_values = set(self.my_mode_list.values())
        cleaning_values.discard(off_value)
        if recharge_value:
            cleaning_values.discard(recharge_value)
        
        _LOGGER.debug(f"[{self.entity_id}] === STATUS UPDATE ===")
        _LOGGER.debug(f"[{self.entity_id}] Mode: {self._current_mode}")
        _LOGGER.debug(f"[{self.entity_id}] Battery state: '{battery_state}'")
        _LOGGER.debug(f"[{self.entity_id}] off_value={off_value}, recharge_value={recharge_value}")
        _LOGGER.debug(f"[{self.entity_id}] cleaning_values={cleaning_values}")
        
        # ===== ОПРЕДЕЛЕНИЕ СТАТУСА =====
        if self._current_mode == off_value:
            # Пылесос выключен - определяем состояние по батарее
            if battery_state == "charge-full":
                # Полностью заряжен на базе -> IDLE (бездействие)
                self._attr_activity = VacuumActivity.IDLE
                _LOGGER.debug(f"[{self.entity_id}] -> IDLE (fully charged)")
            elif battery_state in ["charging", "charging-dock", "charge-dock"]:
                # Заряжается на базе -> DOCKED
                self._attr_activity = VacuumActivity.DOCKED
                _LOGGER.debug(f"[{self.entity_id}] -> DOCKED (charging)")
            elif battery_state == "discharge":
                # Разряжается (не на базе) -> IDLE (остановлен)
                self._attr_activity = VacuumActivity.IDLE
                _LOGGER.debug(f"[{self.entity_id}] -> IDLE (stopped, not on dock)")
            else:
                # Неизвестное состояние батареи -> IDLE
                self._attr_activity = VacuumActivity.IDLE
                _LOGGER.debug(f"[{self.entity_id}] -> IDLE (unknown battery state: {battery_state})")
        elif recharge_value and self._current_mode == recharge_value:
            # Возвращается на базу
            self._attr_activity = VacuumActivity.RETURNING
            _LOGGER.debug(f"[{self.entity_id}] -> RETURNING")
        elif self._current_mode in cleaning_values:
            # Любой режим уборки
            self._attr_activity = VacuumActivity.CLEANING
            _LOGGER.debug(f"[{self.entity_id}] -> CLEANING")
        else:
            # Неизвестный режим - определяем по батарее
            _LOGGER.debug(f"[{self.entity_id}] Unknown mode {self._current_mode}, checking battery")
            if battery_state == "charge-full":
                self._attr_activity = VacuumActivity.IDLE
            elif battery_state in ["charging", "charging-dock", "charge-dock"]:
                self._attr_activity = VacuumActivity.DOCKED
            elif battery_state == "discharge":
                self._attr_activity = VacuumActivity.IDLE
            else:
                self._attr_activity = VacuumActivity.IDLE
        self.async_write_ha_state()

    
#    def _save_log(self, message, topic) -> None:
#        file_path = "vacuum_log.txt"
#        with open(file_path, 'a+', encoding='utf-8') as file:
#            file.write(f"{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {topic} {message}\n")
     
    
        # @callback
        # def message_received_contour(message):
            # payload = message.payload
            # self._save_log(payload, "Log contour:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/contour", message_received_contour, 1, None)
        
        # @callback
        # def message_received_go_area(message):
            # payload = message.payload
            # self._save_log(payload, "Log go_area:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/go_area", message_received_go_area, 1, None)
    
        # @callback
        # def message_received_mode(message):
            # payload = message.payload
            # self._save_log(payload, "Log mode:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/mode", message_received_mode, 1)
    
        # @callback
        # def message_received_map_angle(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_angle:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_angle", message_received_map_angle, 1)
    
        # @callback
        # def message_received_clean_area(message):
            # payload = message.payload
            # self._save_log(payload, "Log clean_area:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/clean_area", message_received_clean_area, 1)
    
        # @callback
        # def message_received_program_data_0(message):
            # payload = message.payload
            # self._save_log(payload, "Log program_data_0:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/program_data/0", message_received_program_data_0, 1)
    
        # @callback
        # def message_received_program_data_1(message):
            # payload = message.payload
            # self._save_log(payload, "Log program_data_1:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/program_data/1", message_received_program_data_1, 1)
    
        # @callback
        # def message_received_program_data_2(message):
            # payload = message.payload
            # self._save_log(payload, "Log program_data_2:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/program_data/2", message_received_program_data_2, 1)
    
        # @callback
        # def message_received_program_data_3(message):
            # payload = message.payload
            # self._save_log(payload, "Log program_data_3:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/program_data/3", message_received_program_data_3, 1)
    
        # @callback
        # def message_received_program_data_4(message):
            # payload = message.payload
            # self._save_log(payload, "Log program_data_4:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/program_data/4", message_received_program_data_4, 1)
    
        # @callback
        # def message_received_location_current(message):
            # payload = message.payload
            # self._save_log(payload, "Log location_current:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/location_current", message_received_location_current, 1)
    
        # @callback
        # def message_received_map_0(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_0:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map/0", message_received_map_0, 1, None)
    
        # @callback
        # def message_received_map_1(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_1:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map/1", message_received_map_1, 1, None)
    
        # @callback
        # def message_received_virtual_wall(message):
            # payload = message.payload
            # self._save_log(payload, "Log virtual_wall:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/virtual_wall", message_received_virtual_wall, 1, None)
    
        # @callback
        # def message_received_no_go_area(message):
            # payload = message.payload
            # self._save_log(payload, "Log no_go_area:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/no_go_area", message_received_no_go_area, 1, None)
    
        # @callback
        # def message_received_map_image(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_image:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_image", message_received_map_image, 1, None)
    
        # @callback
        # def message_received_map_long_0(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_0:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/0", message_received_map_long_0, 1, None)
    
        # @callback
        # def message_received_map_long_1(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_1:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/1", message_received_map_long_1, 1, None)
    
        # @callback
        # def message_received_map_long_2(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_2:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/2", message_received_map_long_2, 1, None)
    
        # @callback
        # def message_received_map_long_3(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_3:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/3", message_received_map_long_3, 1, None)
    
        # @callback
        # def message_received_map_long_4(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_4:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/4", message_received_map_long_4, 1, None)
    
        # @callback
        # def message_received_map_long_5(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_5:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/5", message_received_map_long_5, 1, None)
    
        # @callback
        # def message_received_map_long_6(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_6:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/6", message_received_map_long_6, 1, None)
    
        # @callback
        # def message_received_map_long_7(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_7:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/7", message_received_map_long_7, 1, None)
    
        # @callback
        # def message_received_map_long_8(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_8:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/8", message_received_map_long_8, 1, None)
    
        # @callback
        # def message_received_map_long_9(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_long_9:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_long/9", message_received_map_long_9, 1, None)
    
        # @callback
        # def message_received_map_location_0(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_0:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/0", message_received_map_location_0, 1, None)
    
        # @callback
        # def message_received_map_location_1(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_1:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/1", message_received_map_location_1, 1, None)
    
        # @callback
        # def message_received_map_location_2(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_2:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/2", message_received_map_location_2, 1, None)
    
        # @callback
        # def message_received_map_location_3(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_3:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/3", message_received_map_location_3, 1, None)
    
        # @callback
        # def message_received_map_location_4(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_4:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/4", message_received_map_location_4, 1, None)
    
        # @callback
        # def message_received_map_location_5(message):
            # payload = message.payload
            # self._save_log(payload, "Log map_location_5:")
        # await mqtt.async_subscribe(self.hass, f"{self.entity_description.mqttTopicCommandTest}/map_location/5", message_received_map_location_5, 1, None)
    
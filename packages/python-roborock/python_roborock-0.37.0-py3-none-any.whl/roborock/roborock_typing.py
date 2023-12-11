from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .containers import (
    CleanRecord,
    CleanSummary,
    Consumable,
    DustCollectionMode,
    RoborockBase,
    SmartWashParams,
    Status,
    WashTowelMode,
)


class RoborockCommand(str, Enum):
    APP_CHARGE = "app_charge"
    APP_GET_DRYER_SETTING = "app_get_dryer_setting"
    APP_GET_INIT_STATUS = "app_get_init_status"
    APP_GOTO_TARGET = "app_goto_target"
    APP_PAUSE = "app_pause"
    APP_RC_END = "app_rc_end"
    APP_RC_MOVE = "app_rc_move"
    APP_RC_START = "app_rc_start"
    APP_RC_STOP = "app_rc_stop"
    APP_SEGMENT_CLEAN = "app_segment_clean"
    APP_SET_DRYER_SETTING = "app_set_dryer_setting"
    APP_SET_SMART_CLIFF_FORBIDDEN = "app_set_smart_cliff_forbidden"
    APP_SPOT = "app_spot"
    APP_START = "app_start"
    APP_START_COLLECT_DUST = "app_start_collect_dust"
    APP_START_WASH = "app_start_wash"
    APP_STAT = "app_stat"
    APP_STOP = "app_stop"
    APP_STOP_WASH = "app_stop_wash"
    APP_WAKEUP_ROBOT = "app_wakeup_robot"
    APP_ZONED_CLEAN = "app_zoned_clean"
    CHANGE_SOUND_VOLUME = "change_sound_volume"
    CLOSE_DND_TIMER = "close_dnd_timer"
    CLOSE_VALLEY_ELECTRICITY_TIMER = "close_valley_electricity_timer"
    DNLD_INSTALL_SOUND = "dnld_install_sound"
    ENABLE_LOG_UPLOAD = "enable_log_upload"
    END_EDIT_MAP = "end_edit_map"
    FIND_ME = "find_me"
    GET_CAMERA_STATUS = "get_camera_status"
    GET_CARPET_CLEAN_MODE = "get_carpet_clean_mode"
    GET_CARPET_MODE = "get_carpet_mode"
    GET_CHILD_LOCK_STATUS = "get_child_lock_status"
    GET_CLEAN_RECORD = "get_clean_record"
    GET_CLEAN_RECORD_MAP = "get_clean_record_map"
    GET_CLEAN_SEQUENCE = "get_clean_sequence"
    GET_CLEAN_SUMMARY = "get_clean_summary"
    GET_COLLISION_AVOID_STATUS = "get_collision_avoid_status"
    GET_CONSUMABLE = "get_consumable"
    GET_CURRENT_SOUND = "get_current_sound"
    GET_CUSTOMIZE_CLEAN_MODE = "get_customize_clean_mode"
    GET_CUSTOM_MODE = "get_custom_mode"
    GET_DEVICE_ICE = "get_device_ice"
    GET_DEVICE_SDP = "get_device_sdp"
    GET_DND_TIMER = "get_dnd_timer"
    GET_DUST_COLLECTION_MODE = "get_dust_collection_mode"
    GET_FLOW_LED_STATUS = "get_flow_led_status"
    GET_HOMESEC_CONNECT_STATUS = "get_homesec_connect_status"
    GET_IDENTIFY_FURNITURE_STATUS = "get_identify_furniture_status"
    GET_IDENTIFY_GROUND_MATERIAL_STATUS = "get_identify_ground_material_status"
    GET_LED_STATUS = "get_led_status"
    GET_MAP_V1 = "get_map_v1"
    GET_MOP_TEMPLATE_PARAMS_SUMMARY = "get_mop_template_params_summary"
    GET_MULTI_MAP = "get_multi_map"
    GET_MULTI_MAPS_LIST = "get_multi_maps_list"
    GET_NETWORK_INFO = "get_network_info"
    GET_PROP = "get_prop"
    GET_ROOM_MAPPING = "get_room_mapping"
    GET_SCENES_VALID_TIDS = "get_scenes_valid_tids"
    GET_SERIAL_NUMBER = "get_serial_number"
    GET_SERVER_TIMER = "get_server_timer"
    GET_SMART_WASH_PARAMS = "get_smart_wash_params"
    GET_SOUND_PROGRESS = "get_sound_progress"
    GET_SOUND_VOLUME = "get_sound_volume"
    GET_STATUS = "get_status"
    GET_TIMEZONE = "get_timezone"
    GET_TURN_SERVER = "get_turn_server"
    GET_VALLEY_ELECTRICITY_TIMER = "get_valley_electricity_timer"
    GET_WASH_TOWEL_MODE = "get_wash_towel_mode"
    LOAD_MULTI_MAP = "load_multi_map"
    NAME_SEGMENT = "name_segment"
    REUNION_SCENES = "reunion_scenes"
    RESET_CONSUMABLE = "reset_consumable"
    RESUME_SEGMENT_CLEAN = "resume_segment_clean"
    RESUME_ZONED_CLEAN = "resume_zoned_clean"
    RETRY_REQUEST = "retry_request"
    SAVE_MAP = "save_map"
    SEND_ICE_TO_ROBOT = "send_ice_to_robot"
    SEND_SDP_TO_ROBOT = "send_sdp_to_robot"
    SET_APP_TIMEZONE = "set_app_timezone"
    SET_CAMERA_STATUS = "set_camera_status"
    SET_CARPET_CLEAN_MODE = "set_carpet_clean_mode"
    SET_CARPET_MODE = "set_carpet_mode"
    SET_CHILD_LOCK_STATUS = "set_child_lock_status"
    SET_CLEAN_MOTOR_MODE = "set_clean_motor_mode"
    SET_COLLISION_AVOID_STATUS = "set_collision_avoid_status"
    SET_CUSTOMIZE_CLEAN_MODE = "set_customize_clean_mode"
    SET_CUSTOM_MODE = "set_custom_mode"
    SET_DND_TIMER = "set_dnd_timer"
    SET_DUST_COLLECTION_MODE = "set_dust_collection_mode"
    SET_FDS_ENDPOINT = "set_fds_endpoint"
    SET_FLOW_LED_STATUS = "set_flow_led_status"
    SET_IDENTIFY_FURNITURE_STATUS = "set_identify_furniture_status"
    SET_IDENTIFY_GROUND_MATERIAL_STATUS = "set_identify_ground_material_status"
    SET_LED_STATUS = "set_led_status"
    SET_MOP_MODE = "set_mop_mode"
    SET_SCENES_SEGMENTS = "set_scenes_segments"
    SET_SCENES_ZONES = "set_scenes_zones"
    SET_SERVER_TIMER = "set_server_timer"
    SET_SMART_WASH_PARAMS = "set_smart_wash_params"
    SET_TIMEZONE = "set_timezone"
    SET_VALLEY_ELECTRICITY_TIMER = "set_valley_electricity_timer"
    SET_WASH_TOWEL_MODE = "set_wash_towel_mode"
    SET_WATER_BOX_CUSTOM_MODE = "set_water_box_custom_mode"
    START_CAMERA_PREVIEW = "start_camera_preview"
    START_EDIT_MAP = "start_edit_map"
    START_VOICE_CHAT = "start_voice_chat"
    START_WASH_THEN_CHARGE = "start_wash_then_charge"
    STOP_CAMERA_PREVIEW = "stop_camera_preview"
    SWITCH_WATER_MARK = "switch_water_mark"
    TEST_SOUND_VOLUME = "test_sound_volume"
    UPD_SERVER_TIMER = "upd_server_timer"
    DEL_SERVER_TIMER = "del_server_timer"


@dataclass
class CommandInfo:
    params: list | dict | int | None = None


CommandInfoMap: dict[RoborockCommand | None, CommandInfo] = {
    RoborockCommand.APP_CHARGE: CommandInfo(params=[]),
    RoborockCommand.APP_GET_DRYER_SETTING: CommandInfo(params=None),
    RoborockCommand.APP_GET_INIT_STATUS: CommandInfo(params=[]),
    RoborockCommand.APP_GOTO_TARGET: CommandInfo(params=[25000, 24850]),
    RoborockCommand.APP_PAUSE: CommandInfo(params=[]),
    RoborockCommand.APP_RC_END: CommandInfo(params=[]),
    RoborockCommand.APP_RC_MOVE: CommandInfo(params=None),
    RoborockCommand.APP_RC_START: CommandInfo(params=[]),
    RoborockCommand.APP_RC_STOP: CommandInfo(params=[]),
    RoborockCommand.APP_SEGMENT_CLEAN: CommandInfo(params=[{"segments": 16, "repeat": 2}]),
    # RoborockCommand.APP_SEGMENT_CLEAN: CommandInfo(prefix=b"\x00\x00\x00\x87", params=None),
    RoborockCommand.APP_SET_DRYER_SETTING: CommandInfo(params=None),
    RoborockCommand.APP_SET_SMART_CLIFF_FORBIDDEN: CommandInfo(params={"zones": [], "map_index": 0}),
    RoborockCommand.APP_SPOT: CommandInfo(params=[]),
    RoborockCommand.APP_START: CommandInfo(params=None),
    # RoborockCommand.APP_START: CommandInfo(prefix=b"\x00\x00\x00\x87", params=[{"use_new_map": 1}]),
    RoborockCommand.APP_START_COLLECT_DUST: CommandInfo(params=None),
    RoborockCommand.APP_START_WASH: CommandInfo(params=None),
    RoborockCommand.APP_STAT: CommandInfo(
        params=[
            {
                "ver": "0.1",
                "data": [
                    {
                        "times": [1682723478],
                        "data": {
                            "region": "America/Sao_Paulo",
                            "pluginVersion": "2820",
                            "mnc": "*",
                            "os": "ios",
                            "osVersion": "16.1",
                            "mcc": "not-cn",
                            "language": "en_BR",
                            "mobileBrand": "*",
                            "appType": "roborock",
                            "mobileModel": "iPhone13,1",
                        },
                        "type": 2,
                    }
                ],
            }
        ],
    ),
    RoborockCommand.APP_STOP: CommandInfo(params=[]),
    RoborockCommand.APP_STOP_WASH: CommandInfo(params=None),
    RoborockCommand.APP_WAKEUP_ROBOT: CommandInfo(params=[]),
    RoborockCommand.APP_ZONED_CLEAN: CommandInfo(params=[[24900, 25100, 26300, 26450, 1]]),
    RoborockCommand.CHANGE_SOUND_VOLUME: CommandInfo(params=None),
    RoborockCommand.CLOSE_DND_TIMER: CommandInfo(params=[]),
    RoborockCommand.CLOSE_VALLEY_ELECTRICITY_TIMER: CommandInfo(params=[]),
    RoborockCommand.DNLD_INSTALL_SOUND: CommandInfo(
        params={"url": "https://awsusor0.fds.api.xiaomi.com/app/topazsv/voice-pkg/package/en.pkg", "sid": 3, "sver": 5},
    ),
    RoborockCommand.ENABLE_LOG_UPLOAD: CommandInfo(params=[9, 2]),
    RoborockCommand.END_EDIT_MAP: CommandInfo(params=[]),
    RoborockCommand.FIND_ME: CommandInfo(params=None),
    RoborockCommand.GET_CAMERA_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_CARPET_CLEAN_MODE: CommandInfo(params=[]),
    RoborockCommand.GET_CARPET_MODE: CommandInfo(params=[]),
    RoborockCommand.GET_CHILD_LOCK_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_CLEAN_RECORD: CommandInfo(params=[1682257961]),
    RoborockCommand.GET_CLEAN_RECORD_MAP: CommandInfo(params={"start_time": 1682597877}),
    RoborockCommand.GET_CLEAN_SEQUENCE: CommandInfo(params=[]),
    RoborockCommand.GET_CLEAN_SUMMARY: CommandInfo(params=[]),
    RoborockCommand.GET_COLLISION_AVOID_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_CONSUMABLE: CommandInfo(params=[]),
    RoborockCommand.GET_CURRENT_SOUND: CommandInfo(params=[]),
    RoborockCommand.GET_CUSTOMIZE_CLEAN_MODE: CommandInfo(params=[]),
    RoborockCommand.GET_CUSTOM_MODE: CommandInfo(params=None),
    RoborockCommand.GET_DEVICE_ICE: CommandInfo(params=[]),
    RoborockCommand.GET_DEVICE_SDP: CommandInfo(params=[]),
    RoborockCommand.GET_DND_TIMER: CommandInfo(params=[]),
    RoborockCommand.GET_DUST_COLLECTION_MODE: CommandInfo(params=None),
    RoborockCommand.GET_FLOW_LED_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_HOMESEC_CONNECT_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_IDENTIFY_FURNITURE_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_IDENTIFY_GROUND_MATERIAL_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_LED_STATUS: CommandInfo(params=[]),
    RoborockCommand.GET_MAP_V1: CommandInfo(params={}),
    RoborockCommand.GET_MOP_TEMPLATE_PARAMS_SUMMARY: CommandInfo(params={}),
    RoborockCommand.GET_MULTI_MAP: CommandInfo(params={"map_index": 0}),
    RoborockCommand.GET_MULTI_MAPS_LIST: CommandInfo(params=[]),
    RoborockCommand.GET_NETWORK_INFO: CommandInfo(params=[]),
    RoborockCommand.GET_PROP: CommandInfo(params=["get_status"]),
    RoborockCommand.GET_ROOM_MAPPING: CommandInfo(params=[]),
    RoborockCommand.GET_SCENES_VALID_TIDS: CommandInfo(params={}),
    RoborockCommand.GET_SERIAL_NUMBER: CommandInfo(params=[]),
    RoborockCommand.GET_SERVER_TIMER: CommandInfo(params=[]),
    RoborockCommand.GET_SMART_WASH_PARAMS: CommandInfo(params=None),
    RoborockCommand.GET_SOUND_PROGRESS: CommandInfo(params=[]),
    RoborockCommand.GET_SOUND_VOLUME: CommandInfo(params=[]),
    RoborockCommand.GET_STATUS: CommandInfo(params=None),
    RoborockCommand.GET_TIMEZONE: CommandInfo(params=[]),
    RoborockCommand.GET_TURN_SERVER: CommandInfo(params=[]),
    RoborockCommand.GET_VALLEY_ELECTRICITY_TIMER: CommandInfo(params=[]),
    RoborockCommand.GET_WASH_TOWEL_MODE: CommandInfo(params=None),
    RoborockCommand.LOAD_MULTI_MAP: CommandInfo(params=None),
    RoborockCommand.NAME_SEGMENT: CommandInfo(params=None),
    RoborockCommand.REUNION_SCENES: CommandInfo(params={"data": [{"tid": "1687830208457"}]}),
    RoborockCommand.RESET_CONSUMABLE: CommandInfo(params=None),
    RoborockCommand.RESUME_SEGMENT_CLEAN: CommandInfo(params=None),
    RoborockCommand.RESUME_ZONED_CLEAN: CommandInfo(params=None),
    RoborockCommand.RETRY_REQUEST: CommandInfo(params={"retry_id": 439374, "retry_count": 8, "method": "save_map"}),
    RoborockCommand.SAVE_MAP: CommandInfo(
        params={
            "data": [
                [1, 25043, 24952, 26167, 24952],
                [0, 25043, 25514, 26167, 25514, 26167, 24390, 25043, 24390],
                [2, 25038, 26782, 26162, 26782, 26162, 25658, 25038, 25658],
                [100, 0],
            ],
            "need_retry": 1,
        },
    ),
    RoborockCommand.SEND_ICE_TO_ROBOT: CommandInfo(
        params={
            "app_ice": "eyJjYW5kaWRhdGUiOiAiY2FuZGlkYXRlOjE1MzE5NzE5NTEgMSB1ZHAgNDE4MTk5MDMgNTQuMTc0LjE4Ni4yNDkgNTQxNzU"
            "gdHlwIHJlbGF5IHJhZGRyIDE3Ny4xOC4xMzQuOTkgcnBvcnQgNjQ2OTEgZ2VuZXJhdGlvbiAwIHVmcmFnIDVOMVogbmV0d2"
            "9yay1pZCAxIG5ldHdvcmstY29zdCAxMCIsICJzZHBNTGluZUluZGV4IjogMSwgInNkcE1pZCI6ICIxIn0="
        },
    ),
    RoborockCommand.SET_APP_TIMEZONE: CommandInfo(params=["America/Sao_Paulo", 2]),
    RoborockCommand.SET_CAMERA_STATUS: CommandInfo(params=[3493]),
    RoborockCommand.SET_CARPET_CLEAN_MODE: CommandInfo(params={"carpet_clean_mode": 0}),
    RoborockCommand.SET_CARPET_MODE: CommandInfo(
        params=[{"enable": 1, "current_high": 500, "current_integral": 450, "current_low": 400, "stall_time": 10}],
    ),
    RoborockCommand.SET_CHILD_LOCK_STATUS: CommandInfo(params={"lock_status": 0}),
    RoborockCommand.SET_CLEAN_MOTOR_MODE: CommandInfo(
        params=[{"fan_power": 106, "mop_mode": 302, "water_box_mode": 204}]
    ),
    RoborockCommand.SET_COLLISION_AVOID_STATUS: CommandInfo(params={"status": 1}),
    RoborockCommand.SET_CUSTOMIZE_CLEAN_MODE: CommandInfo(params={"data": [], "need_retry": 1}),
    RoborockCommand.SET_CUSTOM_MODE: CommandInfo(params=[108]),
    RoborockCommand.SET_DND_TIMER: CommandInfo(params=[22, 0, 8, 0]),
    RoborockCommand.SET_DUST_COLLECTION_MODE: CommandInfo(params=None),
    RoborockCommand.SET_FDS_ENDPOINT: CommandInfo(params=["awsusor0.fds.api.xiaomi.com"]),
    RoborockCommand.SET_FLOW_LED_STATUS: CommandInfo(params={"status": 1}),
    RoborockCommand.SET_IDENTIFY_FURNITURE_STATUS: CommandInfo(params={"status": 1}),
    RoborockCommand.SET_IDENTIFY_GROUND_MATERIAL_STATUS: CommandInfo(params={"status": 1}),
    RoborockCommand.SET_LED_STATUS: CommandInfo(params=[1]),
    RoborockCommand.SET_MOP_MODE: CommandInfo(params=None),
    RoborockCommand.SET_SCENES_SEGMENTS: CommandInfo(
        params={"data": [{"tid": "1687831528786", "segs": [{"sid": 22}, {"sid": 18}]}]}
    ),
    RoborockCommand.SET_SCENES_ZONES: CommandInfo(
        params={"data": [{"zones": [{"zid": 0, "range": [27700, 23750, 30850, 26900]}], "tid": "1687831073722"}]}
    ),
    RoborockCommand.SET_SERVER_TIMER: CommandInfo(
        params={
            "data": [["1687793948482", ["39 12 * * 0,1,2,3,4,5,6", ["start_clean", 106, "0", -1]]]],
            "need_retry": 1,
        }
    ),
    RoborockCommand.SET_SMART_WASH_PARAMS: CommandInfo(params=None),
    RoborockCommand.SET_TIMEZONE: CommandInfo(params=["America/Sao_Paulo"]),
    RoborockCommand.SET_VALLEY_ELECTRICITY_TIMER: CommandInfo(params=[0, 0, 8, 0]),
    RoborockCommand.SET_WASH_TOWEL_MODE: CommandInfo(params=None),
    RoborockCommand.SET_WATER_BOX_CUSTOM_MODE: CommandInfo(params=[203]),
    RoborockCommand.START_CAMERA_PREVIEW: CommandInfo(params={"client_id": "443f8636", "quality": "SD"}),
    RoborockCommand.START_EDIT_MAP: CommandInfo(params=[]),
    RoborockCommand.START_WASH_THEN_CHARGE: CommandInfo(params=None),
    RoborockCommand.STOP_CAMERA_PREVIEW: CommandInfo(params={"client_id": "443f8636"}),
    RoborockCommand.SWITCH_WATER_MARK: CommandInfo(params={"waterMark": "OFF"}),
    RoborockCommand.TEST_SOUND_VOLUME: CommandInfo(params=None),
    RoborockCommand.UPD_SERVER_TIMER: CommandInfo(params=[["1687793948482", "off"]]),
    RoborockCommand.DEL_SERVER_TIMER: CommandInfo(params=["1687793948482"]),
}


@dataclass
class DockSummary(RoborockBase):
    dust_collection_mode: DustCollectionMode | None = None
    wash_towel_mode: WashTowelMode | None = None
    smart_wash_params: SmartWashParams | None = None


@dataclass
class DeviceProp(RoborockBase):
    status: Status = field(default_factory=Status)
    clean_summary: CleanSummary = field(default_factory=CleanSummary)
    consumable: Consumable = field(default_factory=Consumable)
    last_clean_record: CleanRecord | None = None
    dock_summary: DockSummary | None = None

    def update(self, device_prop: DeviceProp) -> None:
        if device_prop.status:
            self.status = device_prop.status
        if device_prop.clean_summary:
            self.clean_summary = device_prop.clean_summary
        if device_prop.consumable:
            self.consumable = device_prop.consumable
        if device_prop.last_clean_record:
            self.last_clean_record = device_prop.last_clean_record
        if device_prop.dock_summary:
            self.dock_summary = device_prop.dock_summary

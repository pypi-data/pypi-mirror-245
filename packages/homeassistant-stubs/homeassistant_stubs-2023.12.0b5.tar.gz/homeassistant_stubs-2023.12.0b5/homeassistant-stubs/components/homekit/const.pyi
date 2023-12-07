from _typeshed import Incomplete
from homeassistant.const import CONF_DEVICES as CONF_DEVICES

DEBOUNCE_TIMEOUT: float
DEVICE_PRECISION_LEEWAY: int
DOMAIN: str
PERSIST_LOCK_DATA: Incomplete
HOMEKIT_FILE: str
SHUTDOWN_TIMEOUT: int
CONF_ENTRY_INDEX: str
VIDEO_CODEC_COPY: str
VIDEO_CODEC_LIBX264: str
AUDIO_CODEC_OPUS: str
VIDEO_CODEC_H264_OMX: str
VIDEO_CODEC_H264_V4L2M2M: str
VIDEO_PROFILE_NAMES: Incomplete
AUDIO_CODEC_COPY: str
ATTR_DISPLAY_NAME: str
ATTR_VALUE: str
ATTR_INTEGRATION: str
ATTR_KEY_NAME: str
ATTR_OBSTRUCTION_DETECTED: str
CONF_HOMEKIT_MODE: str
CONF_ADVERTISE_IP: str
CONF_AUDIO_CODEC: str
CONF_AUDIO_MAP: str
CONF_AUDIO_PACKET_SIZE: str
CONF_ENTITY_CONFIG: str
CONF_FEATURE: str
CONF_FEATURE_LIST: str
CONF_FILTER: str
CONF_EXCLUDE_ACCESSORY_MODE: str
CONF_LINKED_BATTERY_SENSOR: str
CONF_LINKED_BATTERY_CHARGING_SENSOR: str
CONF_LINKED_DOORBELL_SENSOR: str
CONF_LINKED_MOTION_SENSOR: str
CONF_LINKED_HUMIDITY_SENSOR: str
CONF_LINKED_OBSTRUCTION_SENSOR: str
CONF_LOW_BATTERY_THRESHOLD: str
CONF_MAX_FPS: str
CONF_MAX_HEIGHT: str
CONF_MAX_WIDTH: str
CONF_STREAM_ADDRESS: str
CONF_STREAM_SOURCE: str
CONF_SUPPORT_AUDIO: str
CONF_VIDEO_CODEC: str
CONF_VIDEO_PROFILE_NAMES: str
CONF_VIDEO_MAP: str
CONF_VIDEO_PACKET_SIZE: str
CONF_STREAM_COUNT: str
DEFAULT_SUPPORT_AUDIO: bool
DEFAULT_AUDIO_CODEC = AUDIO_CODEC_OPUS
DEFAULT_AUDIO_MAP: str
DEFAULT_AUDIO_PACKET_SIZE: int
DEFAULT_EXCLUDE_ACCESSORY_MODE: bool
DEFAULT_LOW_BATTERY_THRESHOLD: int
DEFAULT_MAX_FPS: int
DEFAULT_MAX_HEIGHT: int
DEFAULT_MAX_WIDTH: int
DEFAULT_PORT: int
DEFAULT_CONFIG_FLOW_PORT: int
DEFAULT_VIDEO_CODEC = VIDEO_CODEC_LIBX264
DEFAULT_VIDEO_PROFILE_NAMES = VIDEO_PROFILE_NAMES
DEFAULT_VIDEO_MAP: str
DEFAULT_VIDEO_PACKET_SIZE: int
DEFAULT_STREAM_COUNT: int
FEATURE_ON_OFF: str
FEATURE_PLAY_PAUSE: str
FEATURE_PLAY_STOP: str
FEATURE_TOGGLE_MUTE: str
EVENT_HOMEKIT_CHANGED: str
EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED: str
HOMEKIT_MODE_ACCESSORY: str
HOMEKIT_MODE_BRIDGE: str
DEFAULT_HOMEKIT_MODE = HOMEKIT_MODE_BRIDGE
HOMEKIT_MODES: Incomplete
SERVICE_HOMEKIT_RESET_ACCESSORY: str
SERVICE_HOMEKIT_UNPAIR: str
BRIDGE_MODEL: str
BRIDGE_NAME: str
SHORT_BRIDGE_NAME: str
SHORT_ACCESSORY_NAME: str
BRIDGE_SERIAL_NUMBER: str
MANUFACTURER: str
TYPE_FAUCET: str
TYPE_OUTLET: str
TYPE_SHOWER: str
TYPE_SPRINKLER: str
TYPE_SWITCH: str
TYPE_VALVE: str
CATEGORY_RECEIVER: int
SERV_ACCESSORY_INFO: str
SERV_AIR_QUALITY_SENSOR: str
SERV_BATTERY_SERVICE: str
SERV_CAMERA_RTP_STREAM_MANAGEMENT: str
SERV_CARBON_DIOXIDE_SENSOR: str
SERV_CARBON_MONOXIDE_SENSOR: str
SERV_CONTACT_SENSOR: str
SERV_DOOR: str
SERV_DOORBELL: str
SERV_FANV2: str
SERV_GARAGE_DOOR_OPENER: str
SERV_HUMIDIFIER_DEHUMIDIFIER: str
SERV_HUMIDITY_SENSOR: str
SERV_INPUT_SOURCE: str
SERV_LEAK_SENSOR: str
SERV_LIGHT_SENSOR: str
SERV_LIGHTBULB: str
SERV_LOCK: str
SERV_MOTION_SENSOR: str
SERV_OCCUPANCY_SENSOR: str
SERV_OUTLET: str
SERV_SECURITY_SYSTEM: str
SERV_SERVICE_LABEL: str
SERV_SMOKE_SENSOR: str
SERV_SPEAKER: str
SERV_STATELESS_PROGRAMMABLE_SWITCH: str
SERV_SWITCH: str
SERV_TELEVISION: str
SERV_TELEVISION_SPEAKER: str
SERV_TEMPERATURE_SENSOR: str
SERV_THERMOSTAT: str
SERV_VALVE: str
SERV_WINDOW: str
SERV_WINDOW_COVERING: str
CHAR_ACTIVE: str
CHAR_ACTIVE_IDENTIFIER: str
CHAR_AIR_PARTICULATE_DENSITY: str
CHAR_PM25_DENSITY: str
CHAR_PM10_DENSITY: str
CHAR_AIR_QUALITY: str
CHAR_BATTERY_LEVEL: str
CHAR_BRIGHTNESS: str
CHAR_CARBON_DIOXIDE_DETECTED: str
CHAR_CARBON_DIOXIDE_LEVEL: str
CHAR_CARBON_DIOXIDE_PEAK_LEVEL: str
CHAR_CARBON_MONOXIDE_DETECTED: str
CHAR_CARBON_MONOXIDE_LEVEL: str
CHAR_CARBON_MONOXIDE_PEAK_LEVEL: str
CHAR_CHARGING_STATE: str
CHAR_COLOR_TEMPERATURE: str
CHAR_CONFIGURED_NAME: str
CHAR_CONTACT_SENSOR_STATE: str
CHAR_COOLING_THRESHOLD_TEMPERATURE: str
CHAR_CURRENT_AMBIENT_LIGHT_LEVEL: str
CHAR_CURRENT_DOOR_STATE: str
CHAR_CURRENT_FAN_STATE: str
CHAR_CURRENT_HEATING_COOLING: str
CHAR_CURRENT_HUMIDIFIER_DEHUMIDIFIER: str
CHAR_CURRENT_POSITION: str
CHAR_CURRENT_HUMIDITY: str
CHAR_CURRENT_SECURITY_STATE: str
CHAR_CURRENT_TEMPERATURE: str
CHAR_CURRENT_TILT_ANGLE: str
CHAR_CURRENT_VISIBILITY_STATE: str
CHAR_DEHUMIDIFIER_THRESHOLD_HUMIDITY: str
CHAR_FIRMWARE_REVISION: str
CHAR_HARDWARE_REVISION: str
CHAR_HEATING_THRESHOLD_TEMPERATURE: str
CHAR_HUE: str
CHAR_HUMIDIFIER_THRESHOLD_HUMIDITY: str
CHAR_IDENTIFIER: str
CHAR_IN_USE: str
CHAR_INPUT_SOURCE_TYPE: str
CHAR_IS_CONFIGURED: str
CHAR_LEAK_DETECTED: str
CHAR_LOCK_CURRENT_STATE: str
CHAR_LOCK_TARGET_STATE: str
CHAR_LINK_QUALITY: str
CHAR_MANUFACTURER: str
CHAR_MODEL: str
CHAR_MOTION_DETECTED: str
CHAR_MUTE: str
CHAR_NAME: str
CHAR_NITROGEN_DIOXIDE_DENSITY: str
CHAR_OBSTRUCTION_DETECTED: str
CHAR_OCCUPANCY_DETECTED: str
CHAR_ON: str
CHAR_OUTLET_IN_USE: str
CHAR_POSITION_STATE: str
CHAR_PROGRAMMABLE_SWITCH_EVENT: str
CHAR_REMOTE_KEY: str
CHAR_ROTATION_DIRECTION: str
CHAR_ROTATION_SPEED: str
CHAR_SATURATION: str
CHAR_SERIAL_NUMBER: str
CHAR_SERVICE_LABEL_INDEX: str
CHAR_SERVICE_LABEL_NAMESPACE: str
CHAR_SLEEP_DISCOVER_MODE: str
CHAR_SMOKE_DETECTED: str
CHAR_STATUS_LOW_BATTERY: str
CHAR_STREAMING_STRATUS: str
CHAR_SWING_MODE: str
CHAR_TARGET_DOOR_STATE: str
CHAR_TARGET_HEATING_COOLING: str
CHAR_TARGET_POSITION: str
CHAR_TARGET_FAN_STATE: str
CHAR_TARGET_HUMIDIFIER_DEHUMIDIFIER: str
CHAR_TARGET_HUMIDITY: str
CHAR_TARGET_SECURITY_STATE: str
CHAR_TARGET_TEMPERATURE: str
CHAR_TARGET_TILT_ANGLE: str
CHAR_HOLD_POSITION: str
CHAR_TEMP_DISPLAY_UNITS: str
CHAR_VALVE_TYPE: str
CHAR_VOC_DENSITY: str
CHAR_VOLUME: str
CHAR_VOLUME_SELECTOR: str
CHAR_VOLUME_CONTROL_TYPE: str
PROP_MAX_VALUE: str
PROP_MIN_VALUE: str
PROP_MIN_STEP: str
PROP_CELSIUS: Incomplete
PROP_VALID_VALUES: str
THRESHOLD_CO: int
THRESHOLD_CO2: int
DEFAULT_MIN_TEMP_WATER_HEATER: int
DEFAULT_MAX_TEMP_WATER_HEATER: int
KEY_ARROW_DOWN: str
KEY_ARROW_LEFT: str
KEY_ARROW_RIGHT: str
KEY_ARROW_UP: str
KEY_BACK: str
KEY_EXIT: str
KEY_FAST_FORWARD: str
KEY_INFORMATION: str
KEY_NEXT_TRACK: str
KEY_PREVIOUS_TRACK: str
KEY_REWIND: str
KEY_SELECT: str
KEY_PLAY_PAUSE: str
HK_DOOR_OPEN: int
HK_DOOR_CLOSED: int
HK_DOOR_OPENING: int
HK_DOOR_CLOSING: int
HK_DOOR_STOPPED: int
HK_POSITION_GOING_TO_MIN: int
HK_POSITION_GOING_TO_MAX: int
HK_POSITION_STOPPED: int
HK_NOT_CHARGING: int
HK_CHARGING: int
HK_NOT_CHARGABLE: int
CONFIG_OPTIONS: Incomplete
MAX_NAME_LENGTH: int
MAX_SERIAL_LENGTH: int
MAX_MODEL_LENGTH: int
MAX_VERSION_LENGTH: int
MAX_MANUFACTURER_LENGTH: int

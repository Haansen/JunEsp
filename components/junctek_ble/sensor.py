import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client, sensor
from esphome.const import (
    CONF_ID,
    CONF_VOLTAGE,
    UNIT_VOLT,
    ICON_FLASH,
    DEVICE_CLASS_VOLTAGE,
)

CODEOWNERS = ["@yourgithub"]
DEPENDENCIES = ["ble_client"]

junctek_ns = cg.esphome_ns.namespace("junctek")
JunctekBLEClient = junctek_ns.class_("JunctekBLEClient", cg.Component, ble_client.BLEClientNode)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(JunctekBLEClient),
    cv.Required(CONF_ID): cv.use_id(ble_client.BLEClient),
    cv.Required(CONF_VOLTAGE): sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        icon=ICON_FLASH,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
}).extend(cv.COMPONENT_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield ble_client.register_ble_node(var, config[CONF_ID])
    sens = yield sensor.new_sensor(config[CONF_VOLTAGE])
    cg.add(var.set_voltage_sensor(sens))

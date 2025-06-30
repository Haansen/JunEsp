import esphome.codegen as cg
from esphome.components import ble_client
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_THROTTLE

CODEOWNERS = ["@Haansen"]

AUTO_LOAD = ["binary_sensor", "button", "number", "sensor", "switch", "text_sensor"]
MULTI_CONF = True

CONF_JUNCTEK_BLE_ID = "junctek_ble_id"

jk_bms_ble_ns = cg.esphome_ns.namespace("junctek_ble")
JunctekBle = jk_bms_ble_ns.class_(
    "JunctekBle", ble_client.BLEClientNode, cg.PollingComponent
)


JUNCTEK_BLE_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_JUNCTEK_BLE_ID): cv.use_id(JunctekBle),
    }
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JunctekBle),
            cv.Optional(
                CONF_THROTTLE, default="2s"
            ): cv.positive_time_period_milliseconds,
        }
    )
    .extend(ble_client.BLE_CLIENT_SCHEMA)
    .extend(cv.polling_component_schema("5s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)

    cg.add(var.set_throttle(config[CONF_THROTTLE]))

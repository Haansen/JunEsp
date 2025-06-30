import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import CONF_ID

from .. import CONF_JUNCTEK_BLE_ID, JUNCTEK_BLE_COMPONENT_SCHEMA, jk_bms_ble_ns
from ..const import (
    CONF_CHARGING,
    CONF_DISCHARGING
)

DEPENDENCIES = ["junctek_ble"]

CODEOWNERS = ["@Haansen"]

ICON_CHARGING = "mdi:battery-charging-50"
ICON_DISCHARGING = "mdi:battery-charging-50"


SWITCHES = {
    CONF_CHARGING: [0x00, 0x1D, 0x1D],
    CONF_DISCHARGING: [0x00, 0x1E, 0x1E],

}

JunctekSwitch = jk_bms_ble_ns.class_("JunctekSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = JUNCTEK_BLE_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_CHARGING): switch.switch_schema(
            JunctekSwitch,
            icon=ICON_CHARGING,
        ).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_DISCHARGING): switch.switch_schema(
            JunctekSwitch,
            icon=ICON_DISCHARGING,
        ).extend(cv.COMPONENT_SCHEMA),
      
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_JUNCTEK_BLE_ID])
    for key, address in SWITCHES.items():
        if key in config:
            conf = config[key]
            var = cg.new_Pvariable(conf[CONF_ID])
            await cg.register_component(var, conf)
            await switch.register_switch(var, conf)
            cg.add(getattr(hub, f"set_{key}_switch")(var))
            cg.add(var.set_parent(hub))
            cg.add(var.set_jk04_holding_register(address[0]))
            cg.add(var.set_jk02_holding_register(address[1]))
            cg.add(var.set_jk02_32s_holding_register(address[2]))

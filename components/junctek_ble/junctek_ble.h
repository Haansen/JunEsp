#pragma once

#include "esphome/components/ble_client/ble_client.h"
#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace junctek {

class JunctekBLEClient : public esphome::Component, public esphome::ble_client::BLEClientNode {
 public:
  void setup() override;
  void loop() override;
  void on_ble_client_connected() override;
  void on_ble_client_disconnected() override;
  void gattc_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if, esp_ble_gattc_cb_param_t *param) override;

  void set_voltage_sensor(sensor::Sensor *sensor) { voltage_sensor_ = sensor; }

 protected:
  sensor::Sensor *voltage_sensor_{nullptr};
  uint16_t handle_{0};
};

}  // namespace junctek
}  // namespace esphome

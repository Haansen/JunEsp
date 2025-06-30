#include "junctek_ble_client.h"
#include "esphome/core/log.h"

namespace esphome {
namespace junctek {

static const char *const TAG = "JunctekBLE";

void JunctekBLEClient::setup() {
  ESP_LOGI(TAG, "Setting up Junctek BLE client");
}

void JunctekBLEClient::loop() {
}

void JunctekBLEClient::on_ble_client_connected() {
  ESP_LOGI(TAG, "Connected to Junctek device");
  this->node_state = espbt::ClientState::ESTABLISHED;
  this->client_->get_services();
}

void JunctekBLEClient::on_ble_client_disconnected() {
  ESP_LOGW(TAG, "Disconnected from Junctek device");
}

void JunctekBLEClient::gattc_event_handler(esp_gattc_cb_event_t event, esp_gatt_if_t gattc_if,
                                          esp_ble_gattc_cb_param_t *param) {
  if (event == ESP_GATTC_NOTIFY_EVT && param->notify.handle == handle_) {
    auto *data = param->notify.value;
    uint16_t value = (data[1] << 8) | data[0];
    float voltage = value / 100.0f;
    if (voltage_sensor_ != nullptr) voltage_sensor_->publish_state(voltage);
    ESP_LOGD(TAG, "Voltage: %.2fV", voltage);
  }
}

}  // namespace junctek
}  // namespace esphome

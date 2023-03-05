#ifndef MICROPY_INCLUDED_ESP32_MODMACHINE_H
#define MICROPY_INCLUDED_ESP32_MODMACHINE_H

#include "nvs_flash.h"
#include "nvs.h"
#include "py/obj.h"

#define ADC_TIMER_NUM			3	        // Timer used in ADC module
#define ADC_TIMER_DIVIDER       8           // 0.1 us per tick, 10 MHz
#define ADC_TIMER_FREQ          10000000.0  //Timer frequency

typedef enum {
    //MACHINE_WAKE_IDLE=0x01,
    MACHINE_WAKE_SLEEP=0x02,
    MACHINE_WAKE_DEEPSLEEP=0x04
} wake_type_t;

extern const mp_obj_type_t machine_timer_type;
extern const mp_obj_type_t machine_wdt_type;
extern const mp_obj_type_t machine_pin_type;
extern const mp_obj_type_t machine_touchpad_type;
extern const mp_obj_type_t machine_adc_type;
extern const mp_obj_type_t machine_dac_type;
extern const mp_obj_type_t machine_pwm_type;
extern const mp_obj_type_t machine_hw_spi_type;
extern const mp_obj_type_t machine_uart_type;
extern const mp_obj_type_t machine_rtc_type;

extern nvs_handle mpy_nvs_handle;
extern bool i2s_driver_installed;

void machine_pins_init(void);
void machine_pins_deinit(void);
void machine_timer_deinit_all(void);
int machine_pin_get_gpio(mp_obj_t pin_in);

#endif // MICROPY_INCLUDED_ESP32_MODMACHINE_H

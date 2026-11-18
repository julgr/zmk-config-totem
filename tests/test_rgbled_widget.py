"""Run the real widget C against deterministic host GPIO/Zephyr shims.

Requires a C compiler (CC or cc). This checks event ordering and visible LED
output, not nRF power retention or Zephyr scheduling on physical hardware.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/rgbled-widget"

SHIM = r"""
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <setjmp.h>
#include <stdatomic.h>
#include <pthread.h>
#define IS_ENABLED(x) (x)
#define BIT(x) (1u << (x))
#define ARRAY_SIZE(x) (sizeof(x) / sizeof((x)[0]))
#define ARG_UNUSED(x) (void)(x)
#define BUILD_ASSERT(x, ...) _Static_assert(x, #x)
#define LOG_MODULE_DECLARE(...)
#define LOG_INF(...)
#define LOG_DBG(...)
#define LOG_ERR(...)
#define DT_COMPAT_GET_ANY_STATUS_OKAY(x) 0
#define DT_NODE_EXISTS(x) 1
#define DT_ALIAS(x) x
#define led_red 0
#define led_green 1
#define led_blue 2
#define DT_NODE_CHILD_IDX(x) x
struct device { int unused; };
static struct device device;
#define DEVICE_DT_GET(x) (&device)
typedef atomic_int atomic_t;
#define atomic_get(x) atomic_load(x)
#define atomic_set(x, v) atomic_exchange(x, v)
#define atomic_clear(x) atomic_store(x, 0)
#define K_FOREVER -1
#define K_NO_WAIT 0
#define K_MSEC(x) (x)
#define K_SECONDS(x) ((x) * 1000)
#define K_MUTEX_DEFINE(name) pthread_mutex_t name = PTHREAD_MUTEX_INITIALIZER
#define k_mutex_lock(m, t) pthread_mutex_lock(m)
#define k_mutex_unlock(m) pthread_mutex_unlock(m)
#define K_THREAD_DEFINE(...)
#define K_LOWEST_APPLICATION_THREAD_PRIO 0
static jmp_buf stopped;
static bool running;
static int gpio, elapsed, sample_count, stop_after;
static int sample_color[128], sample_duration[128];
static void (*sleep_hook)(void);
static int led_on(const struct device *d, int pin) { gpio |= BIT(pin); return 0; }
static int led_off(const struct device *d, int pin) { gpio &= ~BIT(pin); return 0; }
static void k_sleep(int duration) {
    assert(sample_count < 128);
    sample_color[sample_count] = gpio;
    sample_duration[sample_count++] = duration;
    elapsed += duration;
    if (sleep_hook) sleep_hook();
    if (running && stop_after && sample_count >= stop_after) longjmp(stopped, 1);
}
struct msgq { unsigned char data[16][32]; int count; size_t size; };
#define K_MSGQ_DEFINE(name, item_size, capacity, alignment) \
    static struct msgq name = {.size = item_size}
static int k_msgq_put(struct msgq *q, const void *item, int wait) {
    assert(q->size <= 32);
    if (q->count == 16) return -1;
    memcpy(q->data[q->count++], item, q->size);
    return 0;
}
static int k_msgq_get(struct msgq *q, void *item, int wait) {
    if (!q->count) {
        if (wait == K_FOREVER && running) longjmp(stopped, 1);
        return -1;
    }
    memcpy(item, q->data[0], q->size);
    memmove(q->data, q->data + 1, --q->count * sizeof(q->data[0]));
    return 0;
}
static void k_msgq_purge(struct msgq *q) { q->count = 0; }
struct k_work { int unused; };
struct k_work_delayable { void (*callback)(struct k_work *); };
static void k_work_init_delayable(struct k_work_delayable *w, void (*cb)(struct k_work *)) {
    w->callback = cb;
}
static int k_work_reschedule(struct k_work_delayable *w, int delay) {
    w->callback(NULL);
    return 0;
}
typedef struct { int state, state_of_charge; } zmk_event_t;
struct zmk_activity_state_changed { int state; };
#define ZMK_ACTIVITY_SLEEP 2
#define ZMK_ACTIVITY_IDLE 1
#define ZMK_ACTIVITY_ACTIVE 0
#define as_zmk_activity_state_changed(e) ((const struct zmk_activity_state_changed *)(e))
#define as_zmk_battery_state_changed(e) (e)
#define as_zmk_layer_state_changed(e) (e)
#define ZMK_LISTENER(name, callback) static int (*name)(const zmk_event_t *) = callback
enum { zmk_activity_state_changed, zmk_battery_state_changed, zmk_endpoint_changed,
       zmk_ble_active_profile_changed, zmk_split_peripheral_status_changed,
       zmk_layer_state_changed, event_count };
static int (*listeners[event_count][4])(const zmk_event_t *);
static int listener_count[event_count];
#define ZMK_SUBSCRIPTION(name, event) \
    static void __attribute__((constructor)) subscribe_##name##_##event(void) { \
        listeners[event][listener_count[event]++] = name; \
    }
static void dispatch(int type, const zmk_event_t *event) {
    for (int i = 0; i < listener_count[type]; ++i) listeners[type][i](event);
}
static uint8_t battery = 75, profile, layer;
static bool profile_open;
#define ZMK_BLE_PROFILE_COUNT 5
#define ZMK_SPLIT_BLE_PERIPHERAL_COUNT 1
#define ZMK_TRANSPORT_NONE 0
#define ZMK_TRANSPORT_BLE 1
#define ZMK_TRANSPORT_USB 2
static int transport = ZMK_TRANSPORT_BLE;
struct endpoint { int transport; };
static struct endpoint zmk_endpoint_get_selected(void) { return (struct endpoint){transport}; }
static int zmk_endpoint_get_preferred_transport(void) { return ZMK_TRANSPORT_BLE; }
static uint8_t zmk_ble_active_profile_index(void) { return profile; }
static bool zmk_ble_active_profile_is_open(void) { return profile_open; }
static bool zmk_split_bt_peripheral_is_connected(void) { return transport == ZMK_TRANSPORT_BLE; }
static uint8_t zmk_keymap_highest_layer_active(void) { return layer; }
static uint8_t zmk_battery_state_of_charge(void) { return battery; }
static int zmk_split_central_get_peripheral_battery_level(int i, uint8_t *out) {
    *out = battery; return 0;
}
"""

SCENARIOS = r"""
static void reset(void) {
    gpio = elapsed = sample_count = stop_after = 0;
    sleep_hook = NULL;
    atomic_clear(&led_current_color);
    atomic_clear(&led_sleeping);
    atomic_set(&initialized, true);
    led_layer_color = 0;
    battery = 75;
    k_msgq_purge(&led_msgq);
}
static void run_worker(int samples) {
    stop_after = samples;
    running = true;
    if (!setjmp(stopped)) led_process_thread(NULL, NULL, NULL);
    running = false;
}
static void activity(int state) {
    zmk_event_t event = {.state = state};
    dispatch(zmk_activity_state_changed, &event);
}
static void sleep_during_blink(void) {
    sleep_hook = NULL;
    activity(ZMK_ACTIVITY_SLEEP);
    assert(gpio == 0);
    // A late connectivity callback must not reactivate an LED after shutdown.
    indicate_connectivity_internal();
}
static void recover_battery(void) {
    sleep_hook = NULL;
    battery = 6;
    dispatch(zmk_battery_state_changed, NULL);
}
int main(void) {
    reset();
    const int levels[] = {100, 50, 49, 20, 19, 6, 5, 1, 0};
    const int colors[] = {2, 2, 3, 3, 1, 1, 1, 1, 5};
    for (int i = 0; i < ARRAY_SIZE(levels); ++i)
        assert(get_battery_color(levels[i]) == colors[i]);
    puts("PASS battery boundaries: 0, 1, 5, 6, 19, 20, 49, 50, 100");

    // Sleep interrupts a lit blink before its timed off step. Layer colors are
    // deliberately nonzero to also catch an in-flight worker restoring them.
    reset();
    led_layer_color = 2;
    struct blink_item blink = {.color = 1, .duration_ms = 1000};
    k_msgq_put(&led_msgq, &blink, K_NO_WAIT);
    sleep_hook = sleep_during_blink;
    run_worker(0);
    assert(sample_color[0] == 1);
    assert(gpio == 0);
    for (int i = 1; i < sample_count; ++i) assert(sample_color[i] == 0);
    set_rgb_leds(7, 0);
    assert(gpio == 0);
    activity(ZMK_ACTIVITY_ACTIVE);
    set_rgb_leds(4, 0);
    assert(gpio == 4);
    puts("PASS sleep during blink, late queued writes blocked, active output restored");

    reset();
    battery = 5;
    run_worker(6);
    for (int i = 0; i < 6; ++i) {
        assert(sample_color[i] == (i % 2 ? 0 : 1));
        assert(sample_duration[i] == 1000);
    }
    assert(elapsed == 6000);
    puts("PASS critical warning repeats 1 second on / 1 second off without battery events");

    reset();
    battery = 1;
    sleep_hook = recover_battery;
    run_worker(0);
    assert(sample_count == 2 && gpio == 0);
    assert(sample_color[0] == 1 && sample_color[1] == 0);
    for (int level = 0; level <= 6; level += 6) {
        reset(); battery = level; run_worker(0); assert(sample_count == 0);
    }
    puts("PASS critical recovery above 5%, and no warning for unknown zero");

    reset();
    battery = 5;
    sleep_hook = sleep_during_blink;
    run_worker(0);
    assert(sample_count == 2 && sample_color[1] == 0 && gpio == 0);
    puts("PASS sleep cancels critical warning and prevents restart");

    reset();
    atomic_clear(&initialized);
    battery = 5;
    led_init_thread(NULL, NULL, NULL);
    sample_count = 0;
    run_worker(10);
    assert(sample_color[0] == 1 && sample_duration[0] == 2000);
#if CONFIG_ZMK_SPLIT_ROLE_CENTRAL
    assert(sample_color[2] == 1 && sample_duration[2] == 1000);
    assert(sample_color[4] == 4 && sample_duration[4] == 1000);
    assert(sample_color[6] == 1 && sample_duration[6] == 1000);
#else
    assert(sample_color[2] == 4 && sample_duration[2] == 1000);
    assert(sample_color[4] == 1 && sample_duration[4] == 1000);
#endif
    puts("PASS boot indicators precede repeated critical warning");
    return 0;
}
"""


def configuration(central, layer_colors):
    """Read numeric defaults from the production Kconfig, not a copied palette."""
    text = (MODULE / "Kconfig").read_text()
    colors = dict(re.findall(r"^(COLOR_\w+)\s*:=\s*(\d+)", text, re.M))
    defaults = {}
    for name, body in re.findall(r"^config (\w+)[^\n]*\n(.*?)(?=^config |\Z)", text, re.M | re.S):
        match = re.search(r"^\s+default (\$\(\w+\)|\w+)", body, re.M)
        if match:
            value = match[1]
            defaults[name] = colors[value[2:-1]] if value.startswith("$(") else value
    def resolve(name):
        value = defaults[name]
        return resolve(value) if value in defaults else value
    config = {name: resolve(name) for name in defaults}
    # Model the enabled configuration from this board; unspecified booleans are off.
    source = (MODULE / "src/widget.c").read_text() + (MODULE / "include/zmk_rgbled_widget/widget.h").read_text()
    for name in re.findall(r"CONFIG_(\w+)", source):
        config.setdefault(name, "0")
    for name in ("ZMK_BLE", "ZMK_SPLIT", "ZMK_SPLIT_BLE", "ZMK_BATTERY_REPORTING",
                 "RGBLED_WIDGET_BATTERY_SHOW_SELF"):
        config[name] = "1"
    config["ZMK_SPLIT_ROLE_CENTRAL"] = str(int(central))
    config["RGBLED_WIDGET_SHOW_PROFILE_COLORS"] = str(int(central))
    config["RGBLED_WIDGET_SHOW_LAYER_COLORS"] = str(int(layer_colors))
    return "\n".join(f"#define CONFIG_{key} {value}" for key, value in config.items())


class WidgetBehavior(unittest.TestCase):
    def test_gpio_and_event_sequences(self):
        with tempfile.TemporaryDirectory(prefix="totem-led-test-") as temporary:
            directory = Path(temporary)
            source = (MODULE / "src/widget.c").read_text()
            for include in re.findall(r"#include <([^>]+)>", source):
                if include.startswith(("zephyr/", "zmk/")):
                    header = directory / include
                    header.parent.mkdir(parents=True, exist_ok=True)
                    header.write_text("")
            for central, layer_colors in ((True, False), (False, False), (True, True)):
                with self.subTest(central=central, layer_colors=layer_colors):
                    test = directory / "widget_test.c"
                    test.write_text(configuration(central, layer_colors) + "\n" + SHIM +
                                    f'\n#include "{MODULE / "src/widget.c"}"\n' + SCENARIOS)
                    binary = directory / "widget_test"
                    subprocess.run([os.environ.get("CC", "cc"), "-std=c11", "-pthread",
                                    "-Werror=implicit-function-declaration", "-I", str(directory),
                                    "-I", str(MODULE / "include"), str(test), "-o", str(binary)], check=True)
                    subprocess.run([str(binary)], check=True)


if __name__ == "__main__":
    unittest.main()

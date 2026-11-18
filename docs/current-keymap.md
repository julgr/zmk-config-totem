# TOTEM current source keymap

Snapshot of `config/totem.keymap`, `config/totem.conf`, `build.yaml`, and the shield physical layout. Generated from executable bindings, not the decorative diagrams. This describes repository defaults, not a readback of the flashed keyboard: ZMK Studio settings stored on the keyboard may override them.

## ZMK Studio

- Enabled: `CONFIG_ZMK_STUDIO=y`.
- Locking disabled: `CONFIG_ZMK_STUDIO_LOCKING=n`. **No unlock key is required.** No `&studio_unlock` binding is present in the active keymap.
- The left-half build includes `studio-rpc-usb-uart`; connect the **left half by USB** for the configured Studio connection.
- A Studio physical layout is defined in `config/boards/shields/totem/totem.dtsi`.
- This confirms source configuration only, not which firmware is currently flashed.

## How to read the tables

Each half is shown left-to-right as viewed while typing. Bottom rows include the extra outer pinky key. Thumb rows are also left-to-right, not anatomical inner/outer labels. Numbers are zero-based ZMK key positions, useful for combos.

The tables preserve exact bindings so no modifier side or consumer/keypad distinction is lost:

- `&kp KEY`: press KEY. Letters are ordinary letter keys, not forced uppercase.
- `&mt MOD KEY`: tap KEY; hold MOD. `L`/`R` means left/right. `ALT` = Option on Mac; `GUI` = Command; `CTRL` = Control; `SHFT` = Shift.
- `&lt LAYER KEY`: tap KEY; hold LAYER. Layer 3 = NAV, 4 = SYM, ADJ = 5.
- `&trans`: fall through to the next active lower layer, not necessarily BASE. `&none`: disabled; no fallthrough.
- `&to LAYER`: switch exclusively to that layout, clearing other non-default layers. BASE remains the default fallback.
- `LC(...)`, `RC(...)`, `LS(...)`, `RS(...)`, `LA(...)`, `RA(...)`, `LG(...)`: apply left/right Control, Shift, Alt/Option, or left GUI/Command. Nested functions combine modifiers.
- `&sk ...`: sticky modifier(s) for a subsequent key, not a layer change.
- `&caps_word`: Caps Word mode, distinct from Caps Lock.
- `&navgresc`: normally tap Escape / hold NAV. With either Shift or GUI/Command held, emit Grave instead and retain those modifiers (e.g. Shift+Grave yields tilde on US layout).
- `&td0`: one tap Ctrl+Left; two taps Ctrl+Alt+Left. `&td1`: corresponding Right combinations. Both use left-side modifiers and a 200 ms tap-dance window.

Key-name legend (symbol results assume a US host layout):

| Code(s) | Meaning |
|---|---|
| SEMI, COLON | `;`, `:` |
| LPAR / LEFT_PARENTHESIS, RPAR / RIGHT_PARENTHESIS | `(`, `)` |
| LBKT / LEFT_BRACKET, RBKT / RIGHT_BRACKET | `[`, `]` |
| LBRC, RBRC | `{`, `}` |
| COMMA, DOT, FSLH, BSLH | comma, period, slash, backslash |
| AMPS, HASH, DLLR, PRCNT | ampersand, hash, dollar, percent |
| LT, GT, CARET, AT, EXCL | less-than, greater-than, caret, at, exclamation |
| SQT, DQT, GRAVE, TILDE | single quote, double quote, grave, tilde |
| PIPE, QMARK, UNDER | vertical bar, question mark, underscore |
| MINUS, PLUS, EQUAL, ASTRK | minus, plus, equals, asterisk |
| N0–N9 | ordinary number-row digits, not keypad digits |
| KP_MINUS, KP_PLUS | keypad minus and plus |
| BSPC, DEL, INS, PG_UP, PG_DN | Backspace, forward Delete, Insert, Page Up, Page Down |
| GLOBE | consumer AC Next Keyboard Layout Select; not native Apple vendor Fn |
| C_AC_BACK, C_AC_FWD | consumer Back / Forward (`C_AC_FWD` aliases `C_AC_FORWARD`) |
| C_VOL_UP, C_VOL_DN, C_MUTE | volume up, down, mute |
| C_PREV, C_PP, C_NEXT | previous track, play/pause, next track |
| C_PWR | host consumer Power command; host-dependent |

## Layer access from BASE / QWERTY

- Left thumbs: position 32 = tap Delete / hold ADJ; 33 = tap Enter / hold SYM; 34 = `navgresc` (normally tap Escape / hold NAV).
- Right thumbs: position 35 = tap Backspace / hold NAV; 36 = tap Space / hold SYM; 37 = tap Tab / hold ADJ.
- Layouts are selected by the combos below. There is no automatic NAV+SYM tri-layer definition.

## Layer 0: BASE

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&kp Q`<br>1: `&kp W`<br>2: `&kp F`<br>3: `&kp P`<br>4: `&kp G` | 5: `&kp J`<br>6: `&kp L`<br>7: `&kp U`<br>8: `&kp Y`<br>9: `&kp SEMI` |
| Home | 10: `&mt LALT A`<br>11: `&mt LCTRL R`<br>12: `&mt LGUI S`<br>13: `&mt LSHFT T`<br>14: `&kp D` | 15: `&kp H`<br>16: `&mt RSHFT N`<br>17: `&mt RGUI E`<br>18: `&mt RCTRL I`<br>19: `&mt RALT O` |
| Bottom + outer pinky | 20: `&kp LPAR`<br>21: `&kp Z`<br>22: `&kp X`<br>23: `&kp C`<br>24: `&kp V`<br>25: `&kp B` | 26: `&kp K`<br>27: `&kp M`<br>28: `&kp COMMA`<br>29: `&kp DOT`<br>30: `&kp FSLH`<br>31: `&kp RPAR` |
| Thumbs | 32: `&lt ADJ DEL`<br>33: `&lt 4 ENTER`<br>34: `&navgresc` | 35: `&lt 3 BSPC`<br>36: `&lt 4 SPACE`<br>37: `&lt ADJ TAB` |

## Layer 1: QWERTY

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&kp Q`<br>1: `&kp W`<br>2: `&kp E`<br>3: `&kp R`<br>4: `&kp T` | 5: `&kp Y`<br>6: `&kp U`<br>7: `&kp I`<br>8: `&kp O`<br>9: `&kp P` |
| Home | 10: `&mt LALT A`<br>11: `&mt LCTRL S`<br>12: `&mt LGUI D`<br>13: `&mt LSHFT F`<br>14: `&kp G` | 15: `&kp H`<br>16: `&mt RSHFT J`<br>17: `&mt RGUI K`<br>18: `&mt RCTRL L`<br>19: `&mt RALT SEMI` |
| Bottom + outer pinky | 20: `&kp LEFT_PARENTHESIS`<br>21: `&kp Z`<br>22: `&kp X`<br>23: `&kp C`<br>24: `&kp V`<br>25: `&kp B` | 26: `&kp N`<br>27: `&kp M`<br>28: `&kp COMMA`<br>29: `&kp DOT`<br>30: `&kp FSLH`<br>31: `&kp RIGHT_PARENTHESIS` |
| Thumbs | 32: `&lt ADJ DEL`<br>33: `&lt 4 ENTER`<br>34: `&navgresc` | 35: `&lt 3 BSPC`<br>36: `&lt 4 SPACE`<br>37: `&lt ADJ TAB` |

## Layer 2: WASD

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&kp TAB`<br>1: `&kp Q`<br>2: `&kp W`<br>3: `&kp E`<br>4: `&kp R` | 5: `&kp ESC`<br>6: `&kp N7`<br>7: `&kp N8`<br>8: `&kp N9`<br>9: `&none` |
| Home | 10: `&kp CAPS`<br>11: `&kp A`<br>12: `&kp S`<br>13: `&kp D`<br>14: `&kp F` | 15: `&kp GRAVE`<br>16: `&kp N4`<br>17: `&kp N5`<br>18: `&kp N6`<br>19: `&none` |
| Bottom + outer pinky | 20: `&to QWERTY`<br>21: `&kp LSHFT`<br>22: `&kp Z`<br>23: `&kp X`<br>24: `&kp C`<br>25: `&kp V` | 26: `&kp N0`<br>27: `&kp N1`<br>28: `&kp N2`<br>29: `&kp N3`<br>30: `&none`<br>31: `&to BASE` |
| Thumbs | 32: `&kp LCTRL`<br>33: `&kp SPACE`<br>34: `&kp LALT` | 35: `&kp BSPC`<br>36: `&kp SPACE`<br>37: `&kp ENTER` |

## Layer 3: NAV

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&kp CAPS`<br>1: `&kp HOME`<br>2: `&kp UP`<br>3: `&kp PG_UP`<br>4: `&kp RC(UP)` | 5: `&kp FSLH`<br>6: `&kp N7`<br>7: `&kp N8`<br>8: `&kp N9`<br>9: `&kp KP_MINUS` |
| Home | 10: `&caps_word`<br>11: `&kp LEFT`<br>12: `&kp DOWN`<br>13: `&kp RIGHT`<br>14: `&kp C_AC_BACK` | 15: `&kp ASTRK`<br>16: `&mt RSHFT N4`<br>17: `&mt RGUI N5`<br>18: `&mt LCTRL N6`<br>19: `&mt RALT KP_PLUS` |
| Bottom + outer pinky | 20: `&td0`<br>21: `&kp GLOBE`<br>22: `&kp END`<br>23: `&kp INS`<br>24: `&kp PG_DN`<br>25: `&kp C_AC_FWD` | 26: `&kp N0`<br>27: `&kp N1`<br>28: `&kp N2`<br>29: `&kp N3`<br>30: `&kp EQUAL`<br>31: `&td1` |
| Thumbs | 32: `&trans`<br>33: `&trans`<br>34: `&trans` | 35: `&trans`<br>36: `&trans`<br>37: `&trans` |

## Layer 4: SYM

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&kp AMPS`<br>1: `&kp HASH`<br>2: `&kp DLLR`<br>3: `&kp PRCNT`<br>4: `&kp LT` | 5: `&kp GT`<br>6: `&kp CARET`<br>7: `&kp AMPS`<br>8: `&kp ASTRK`<br>9: `&kp COLON` |
| Home | 10: `&mt LALT AT`<br>11: `&mt LCTRL EXCL`<br>12: `&mt LGUI SQT`<br>13: `&mt LSHFT LPAR`<br>14: `&kp LBKT` | 15: `&kp RBKT`<br>16: `&mt RSHFT RPAR`<br>17: `&mt RGUI MINUS`<br>18: `&mt RCTRL EQUAL`<br>19: `&mt RALT BSLH` |
| Bottom + outer pinky | 20: `&kp LEFT_BRACKET`<br>21: `&kp PIPE`<br>22: `&kp QMARK`<br>23: `&kp DQT`<br>24: `&kp GRAVE`<br>25: `&kp LBRC` | 26: `&kp RBRC`<br>27: `&kp TILDE`<br>28: `&kp UNDER`<br>29: `&kp PLUS`<br>30: `&kp FSLH`<br>31: `&kp RIGHT_BRACKET` |
| Thumbs | 32: `&trans`<br>33: `&kp UNDER`<br>34: `&trans` | 35: `&trans`<br>36: `&kp UNDER`<br>37: `&trans` |

## Layer 5: ADJ

| Row | Left half — left to right | Right half — left to right |
|---|---|---|
| Top | 0: `&out OUT_TOG`<br>1: `&bt BT_CLR`<br>2: `&bt BT_PRV`<br>3: `&bt BT_NXT`<br>4: `&kp C_VOL_UP` | 5: `&kp F1`<br>6: `&kp F4`<br>7: `&kp F7`<br>8: `&kp F10`<br>9: `&kp F13` |
| Home | 10: `&bt BT_SEL 0`<br>11: `&bt BT_SEL 1`<br>12: `&bt BT_SEL 2`<br>13: `&bt BT_SEL 3`<br>14: `&kp C_VOL_DN` | 15: `&kp F2`<br>16: `&kp F5`<br>17: `&kp F8`<br>18: `&kp F11`<br>19: `&kp F14` |
| Bottom + outer pinky | 20: `&kp C_PWR`<br>21: `&soft_off`<br>22: `&kp C_PREV`<br>23: `&kp C_PP`<br>24: `&kp C_NEXT`<br>25: `&kp C_MUTE` | 26: `&kp F3`<br>27: `&kp F6`<br>28: `&kp F9`<br>29: `&kp F12`<br>30: `&kp F15`<br>31: `&kp F24` |
| Thumbs | 32: `&trans`<br>33: `&sk LS(LC(LALT))`<br>34: `&sk LS(LC(LA(LGUI)))` | 35: `&sk RS(RC(RA(RGUI)))`<br>36: `&sk RS(RC(RALT))`<br>37: `&trans` |

## Combos

All combos have a 100 ms press window and require 500 ms prior idle time.

| Name | Positions / physical keys | Allowed layers | Action |
|---|---|---|---|
| Caps Word | 34 + 35: left rightmost thumb + right leftmost thumb | BASE, QWERTY, WASD | `&caps_word` |
| Alfred | 33 + 36: both middle thumbs | BASE, QWERTY, WASD | Ctrl+Space (`&kp LC(SPACE)`); launches Alfred only if the host assigns it |
| WASD | 22 + 23 + 24: left bottom X + C + V on BASE/QWERTY | BASE, QWERTY | Switch exclusively to WASD |
| BASE | 32 + 33 + 34: all three left thumbs | BASE, QWERTY, WASD, NAV | Switch exclusively to BASE |
| QWERTY | 35 + 36 + 37: all three right thumbs | BASE, QWERTY, WASD, SYM | Switch exclusively to QWERTY |

WASD also has single-key exits: left outer pinky selects QWERTY; right outer pinky selects BASE. Repeating a layout-selection combo keeps that layout selected, rather than toggling it off.

## ADJ controls

- `&out OUT_TOG`: toggle USB/Bluetooth output preference.
- `&bt BT_CLR`: clear the selected Bluetooth profile's pairing; this is not a profile-selection key.
- `&bt BT_PRV` / `BT_NXT`: previous/next Bluetooth profile.
- `&bt BT_SEL 0` through `3`: select zero-based Bluetooth profiles 0–3.
- `&soft_off`: keyboard soft power-off, requiring a 1000 ms hold.
- Thumb 33: sticky left Shift+Ctrl+Alt (Meh).
- Thumb 34: sticky left Shift+Ctrl+Alt+GUI (Hyper).
- Thumb 35: sticky right Shift+Ctrl+Alt+GUI (Hyper).
- Thumb 36: sticky right Shift+Ctrl+Alt (Meh).
- F24 is position 31, the right outer pinky key, on ADJ.

## Bluetooth profile LED colors

The left half blinks the selected profile's color for one second, pauses for 500 ms, then shows the connection-status blink for one second. This happens on boot (after battery status), profile/connection changes, and on-demand connection indication. The LED then turns off, except for the repeating critical-battery warning described below.

| Zero-based Bluetooth profile | Profile color | Existing selection |
|---|---|---|
| 0 | Red | ADJ left home-row first key |
| 1 | Green | ADJ left home-row second key |
| 2 | Blue | ADJ left home-row third key |
| 3 | Magenta | ADJ left home-row fourth key |
| 4 | Cyan | Previous/next profile keys |

The second blink retains the widget's status colors: blue = connected, yellow = an open profile advertising for pairing, red = disconnected. These colors intentionally overlap the profile colors; their position in the sequence distinguishes their meaning. The right half shows its split-connection status, not the selected host profile.

The enabled option is `CONFIG_RGBLED_WIDGET_SHOW_PROFILE_COLORS=y` in the left shield's `.conf`. Color defaults and blink duration live in `modules/rgbled-widget/Kconfig`; color IDs are red=1, green=2, yellow=3, blue=4, magenta=5, cyan=6, white=7.

### Battery indications and sleep

Each half shows its own battery level for two seconds at startup and when battery indication is requested:

| Reported charge | Color / behavior |
|---|---|
| 50–100% | Green |
| 20–49% | Yellow |
| 6–19% | Red |
| 1–5% | Red; after startup indications, repeat one second on / one second off while awake |
| 0 / unknown | Magenta; a zero reading is treated as unavailable, not as a critical reading |

The critical warning repeats without requiring additional battery events. Normal requested/profile/connectivity indications take precedence over warning cycles. The next warning cycle stops once the reported charge exceeds 5% or becomes unknown.

At startup—including wake from deep sleep—the left half shows **battery → profile → connection status**. The right half shows **battery → split-connection status**. Waking from ordinary idle does not reboot or repeat the startup sequence.

Entering sleep immediately turns all LED channels off, even during an in-progress blink. Queued and late-arriving indications cannot turn them back on while asleep. This applies independently of layer-color settings and suppresses critical warnings during sleep.

Host regression checks: `python3 tests/test_rgbled_widget.py` (requires Python 3 and a C compiler). These compile and execute the widget with simulated GPIO/events for both halves and optional layer colors; they do not replace a firmware build or physical sleep/wake verification.

## Flashing without losing Studio changes

- Flash only the normal firmware UF2, not `settings_reset`; do not erase settings or use Studio's Restore Stock Settings.
- Existing Studio key bindings remain stored on the keyboard. The firmware combo changes and LED behavior do not require resetting those bindings.
- If Studio has saved the old WASD outer-pinky mappings, update only those two positions in Studio: WASD position 20 → To Layer 1 (QWERTY), position 31 → To Layer 0 (BASE). The firmware combos already provide exits independently.
- These changes do not reorder layers or keys, rename custom behaviors, change Bluetooth profile selection bindings, or change the Studio locking setting.

The RGB widget is vendored from [caksoylar/zmk-rgbled-widget](https://github.com/caksoylar/zmk-rgbled-widget) at commit `e6b467792a1dabef8cfa5c9fd26bfefc9c16662b`, with its MIT license. Local changes add profile colors through the existing LED queue, unconditional serialized sleep shutdown, and repeated critical-battery warnings through the same LED worker. No separate LED-writing timer or unpublished remote fork is required. The root `zephyr/module.yml` makes the existing ZMK build workflow load this local module.

## Tap/hold timing

- Mod-tap (`&mt`): balanced flavor, 300 ms tapping term, 175 ms quick tap, global quick tap, 200 ms required prior idle.
- Layer-tap (`&lt`): tap-preferred flavor, 200 ms tapping term, 175 ms quick tap, global quick tap, 200 ms required prior idle.
- Actual tap/hold decisions also depend on typing order and these flavor/idle settings; duration alone does not determine every result.

## Differences from the source's decorative diagrams

- BASE/QWERTY diagrams reverse NAV/SYM thumb labels relative to actual bindings. Enter/Space hold SYM; Escape/Backspace hold NAV.
- QWERTY actually has home-row modifiers and parentheses on the outer pinky keys.
- NAV's “MC” position sends right Ctrl+Up, not the unused `MSNCTL` macro. Its right home row includes mod-taps.
- SYM outer pinkies send square brackets. Right home-row position 18 taps equals, not plus; right bottom position 29 sends plus, not equals. SYM also has home-row modifiers.
- ADJ top-left keys are output toggle then Bluetooth clear, opposite the diagram.

Updated for exclusive layout switching and Bluetooth profile color indications; unrelated key bindings are unchanged.

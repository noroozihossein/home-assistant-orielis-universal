# Mr Smart — Orielis TS0601 Universal Knob Blueprint

**Home Assistant + Zigbee2MQTT · v0.3.0 · by Hossein / Mr Smart**

A GUI-configured Home Assistant automation blueprint for the **Orielis / Tuya TS0601 Smart Scene Knob**, with **eight independent rotary-control profiles and four scene buttons**. Control lighting, CCT, audio volume, blinds, climate setpoints and numeric entities without creating helpers or writing YAML.

[![Import blueprint into Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fnoroozihossein%2Fhome-assistant-orielis-universal%2Fblob%2Fmain%2Fmrsmart_orielis_universal.yaml)

[Download YAML](mrsmart_orielis_universal.yaml) · [Installation and setup](#installation) · [Testing and limitations](TESTING.md) · [Report an issue](https://github.com/noroozihossein/home-assistant-orielis-universal/issues)

<img src="https://www.zigbee2mqtt.io/images/devices/TS0601_smart_scene_knob.png" alt="Orielis Tuya TS0601 four-button metal smart scene rotary knob" width="280">

Product reference image linked from Zigbee2MQTT. Product appearance/branding may vary; identify your hardware by its fingerprint. Image rights remain with their respective owner; the project code license does not cover this externally hosted image.

## Exact device

| Field | Value |
|---|---|
| Brand / retail name | Orielis Smart Scene Knob |
| Zigbee model | `TS0601` |
| Tested manufacturer fingerprint | `_TZE284_nj7sfid2` |
| Zigbee2MQTT definition | `TS0601_smart_scene_knob` |
| Controls | Four physical directional buttons and a rotary ring |

**TS0601 alone is not a compatibility guarantee.** Many unrelated Tuya products use that model identifier.

Upstream device support and setup: **[official Zigbee2MQTT device page](https://www.zigbee2mqtt.io/devices/TS0601_smart_scene_knob.html)**. This blueprint consumes upstream actions; it is not a replacement Zigbee converter. Thanks to the Zigbee2MQTT / zigbee-herdsman-converters contributors for native device support.

## Three independent modes

| Remote mode | Blueprint sections | Available input |
|---|---|---|
| Mode 1 — GREEN LED | Four independent universal channels | On/off press, normal rotation, separate colour-temperature rotation gesture |
| Mode 2 — BLUE LED | Four more independent universal channels | Start/stop press and rotation |
| Scene — RED LED | Four independent custom-action buttons | `scene_1` to `scene_4` only; **no rotation** |

The hardware calls green “Light” and blue “Curtain”. **Neither mode is restricted to that product category in this blueprint.** For example, Green channel 1 can control a light group, Blue channel 1 can control an amplifier, and Red button 1 can run a leaving-home scene.

Observed button positions: **1 top (12 o'clock), 2 left (9), 3 bottom (6), 4 right (3)**.

## Per-channel configuration

Each green/blue profile provides:

- Control type: Automatic/mixed, Lighting, Audio/music, Curtains/blinds, Climate setpoint, Numeric, or Custom actions only.
- Multiple target entities, with automatic domain/capability filtering.
- **Synchronized / Relative** group mode, independently selected per profile.
- Editable brightness %, CCT Kelvin, volume %, cover-position %, temperature and numeric steps.
- Reverse direction and primary/secondary rotation selection.
- An enable switch and optional custom Home Assistant action sequence for every actual input event.

Custom overrides replace automatic handling for that event. Scene buttons use the standard Home Assistant action editor. No external helpers are required. Create one automation per remote and choose the correct MQTT device from the dropdown.

### Default action mapping

| Target | Primary rotation | Secondary rotation | Green on/off | Blue start/stop |
|---|---|---|---|---|
| Light | Brightness | CCT, when supported | On / off | On / off |
| Media player | Volume | Next / previous track, when supported | Play / pause | Play / pause |
| Cover | Position | No built-in action | Open / close | Open / **stop** |
| Climate | Single target setpoint | No built-in action | Custom actions needed | Custom actions needed |
| Number / input_number | Numeric value | No built-in action | Custom actions needed | Custom actions needed |

Green's separate `colortemp` gesture continues to select CCT / track control. Blue has one rotation gesture: choose Primary or Secondary in its profile. HVAC modes, fan speed, source selection and other services can be assigned as custom actions; they are not automatic built-ins.

### Group behaviour

**Relative** (compatibility default): each member changes from its own reported state.

**Synchronized**: the first available eligible target in selection order is the reference for each property. One new value is calculated before commands are sent, then sent to all eligible members. Mixed domains form separate property groups: lights share brightness, players share volume, and so on. CCT, setpoints and numeric values use the intersection of member limits. If there is no common range, that adjustment is skipped. Device rounding/resolution can affect reported values.

Synchronized play/pause means the same command is sent to each supported player. It **does not** create multiroom groups, align audio clocks or ensure identical tracks.

## Installation

Requirements: Home Assistant **2024.12.5 or newer**, working MQTT integration, and Zigbee2MQTT with native support for this definition. The hardware test environment used Zigbee2MQTT 2.14.1 and a SONOFF Dongle-P. ZHA is not supported by this blueprint.

1. Pair and configure the remote in Zigbee2MQTT. Confirm that real action messages appear for the modes you intend to use. Follow the upstream device page for binding modes and learning the base group ID. Do not copy another remote's group ID.
2. Enable Zigbee2MQTT Home Assistant discovery and confirm the remote appears under the MQTT integration. Exercise its gestures so discovery can expose the corresponding device triggers.
3. Click **Import blueprint** above. If requested, set your Home Assistant instance URL in My Home Assistant, then approve the import in Home Assistant. This opens the import dialog; it does not bypass confirmation or configure targets automatically.
4. Create an automation from the blueprint and select your Orielis remote.
5. Open the relevant **GREEN / BLUE channel** section. Choose Control type, targets, Group mode and steps. Configure RED scene actions if needed.
6. Save, enable and test. Keep only one active copy for the same remote unless you intentionally design non-overlapping automations.

Alternative: Settings → Automations & scenes → Blueprints → Import blueprint; paste:

```text
https://github.com/noroozihossein/home-assistant-orielis-universal/blob/main/mrsmart_orielis_universal.yaml
```

### Upgrade from v0.2.x

Back up your automation and replace/re-import the blueprint at the same path. Reload automations and reopen the editor. Existing channel targets, steps and grouping remain associated with **GREEN**. **BLUE targets start empty** and must be selected independently. Existing event-specific custom overrides and RED actions keep their identifiers. Verify the title shows v0.3.0 before saving.

## Important behaviour and troubleshooting

- The tested unit initially sent Scene actions but no useful green/blue actions. Pairing it to a Tuya gateway, using it there, then pairing it back to Zigbee2MQTT resolved this. This is an **observed workaround for one unit**, not a proven prerequisite for all devices. The exact initialization command is unknown.
- The device's own state determines whether it sends rotation events. After inactivity, the tested unit sometimes needed two presses before action/rotation messages arrived. Do not assume a confirmed sleep mechanism. A blueprint cannot process an event the remote did not send.
- The upstream documentation also notes rotation restrictions associated with the remote's Light on/off state. See the linked device page.
- By default, rotation does not switch on an off light. Enable **Rotation may turn on an off light** if desired. It does not change the remote's internal state or wake it remotely.
- Steps apply per **received event**, not necessarily per mechanical detent. Execution is single-mode with an adjustable short cooldown; input during an active run is dropped, not queued. Long custom actions block subsequent events until finished.
- Unknown, unavailable and unsupported automatic targets are skipped. Relative adjustments requiring a missing current value are not invented.
- An empty device dropdown indicates a Home Assistant MQTT discovery/registry or filter issue. Check that the device is present in Home Assistant itself; Zigbee2MQTT identification alone is insufficient.
- For problems, include the blueprint/HA/Zigbee2MQTT versions, selected mode, exact action payload and automation trace. Remove private addresses, tokens and credentials before sharing.

## Validation and scope

The maintainer reported successful light/CCT tests on channels 1 and 2, amplifier volume and play/pause in green mode, and separation of the three modes in v0.3.0. The automated suite passed **190 cases using the actual Home Assistant 2024.12.5 schema/template/script engine with simulated service endpoints**. Those tests are not 190 physical-device tests. See [TESTING.md](TESTING.md).

## Project links and search terms

[Mr Smart / noroozihossein](https://github.com/noroozihossein) · [Mr Smart MOES Rotary Blueprint](https://github.com/noroozihossein/home-assistant-moes-rotary) · [Zigbee2MQTT device integration](https://www.zigbee2mqtt.io/devices/TS0601_smart_scene_knob.html)

Orielis, Oriolis, Tuya TS0601 smart scene knob, `_TZE284_nj7sfid2`, Home Assistant blueprint, Zigbee2MQTT rotary controller, CCT dimmer, audio volume, blinds, Mr Smart.

Optional sharing hashtags: **#MrSmart #Orielis #Tuya #TS0601 #HomeAssistant #Zigbee2MQTT #Blueprint #RotaryKnob #SmartHome**.

Independent community project; not an official Tuya, Orielis or Home Assistant product. MIT license for this repository's original code and documentation; third-party branding and linked images remain their owners' property.

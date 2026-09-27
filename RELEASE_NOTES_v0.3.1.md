# v0.3.1 — GREEN dimming limits and BLUE curtain-first profiles

Orielis / Tuya TS0601 smart scene knob (_TZE284_nj7sfid2), Home Assistant + Zigbee2MQTT, by Hossein / Mr Smart.

This update builds on the published v0.3.0 baseline. It adds independent minimum/maximum brightness settings per GREEN channel, clamps dimming above zero, and makes BLUE curtain-first while keeping audio, climate, numeric and fully custom actions.

## Changes
- GREEN minimum/maximum brightness defaults: 1% / 100%, configurable through the UI.
- Synchronized and Relative groups both respect their channel's brightness limits.
- Rotation cannot switch a light off by reaching zero; the off-button action remains.
- BLUE built-in lighting selection and dispatch are removed; move light targets to GREEN.
- BLUE defaults to Curtains/blinds for new configurations. Existing saved choices must be reviewed.
- BLUE retains start/stop/rotation custom overrides. It has no independent CCT gesture.
- GREEN CCT, RED scene buttons, triggers, cooldown and single execution mode remain unchanged.

## Install / upgrade
[Import into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fnoroozihossein%2Fhome-assistant-orielis-universal%2Fblob%2Fmain%2Fmrsmart_orielis_universal.yaml)

Back up and replace/re-import the blueprint at the same path, reload automations and confirm v0.3.1 in the editor. Keep one active automation per remote. Review BLUE targets and configure GREEN limits.

[Full README](README.md) · [Changelog](CHANGELOG.md) · [Validation](TESTING.md) · [راهنمای فارسی](README-FA.md)

## Validation
1,582 cases passed using Home Assistant 2024.12.5's actual schema/template/script engine with simulated service endpoints. The tested rc1 and published executable content are identical. This update has not yet received physical-hardware acceptance; earlier successful hardware reports describe v0.3.0.

Limits apply to all selected lights per GREEN channel, not separately per member, and only to automatic brightness rotation. Custom actions and manual commands remain independent. Group play/pause does not provide multiroom audio-clock synchronization.

[Native Zigbee2MQTT device support](https://www.zigbee2mqtt.io/devices/TS0601_smart_scene_knob.html)

#MrSmart #Orielis #Tuya #TS0601 #HomeAssistant #Zigbee2MQTT #Blueprint #RotaryKnob #CCT #SmartHome

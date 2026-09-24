# Validation report — v0.3.0

## Hardware observations reported by the maintainer

- Green channels 1 and 2: light power, dimming and CCT operated successfully.
- An amplifier assigned to a green profile: volume rotation and play/pause operated successfully.
- v0.3.0: green and blue profiles were reported independent; red exposed four press-only scene actions.
- Initialization workaround on the tested `_TZE284_nj7sfid2`: Tuya gateway pairing/use followed by Zigbee2MQTT re-pairing enabled previously missing light/curtain behaviour. Cause not confirmed.

These observations do not establish full physical verification of every cover, climate, numeric or multi-player target, or of all hardware/firmware variants.

## Software tests

190 cases executed through Home Assistant 2024.12.5's actual blueprint, automation-schema, template and script engines. Services were simulated; there was no MQTT broker or Zigbee radio in the test harness.

Coverage includes all 44 custom event overrides, four green and four blue profiles, per-event disable, domain filtering, empty/offline targets, on/off capability filtering, CCT lower/upper limits, no shared CCT range, group reference selection, 10-light synchronization, relative behaviour, pre-command state snapshots, audio volume/play/pause, cover position/open/stop, temperature/numeric clamping, mode isolation, scene isolation, reverse direction, custom-only mode and concurrent input rejection.

A simulated unavailable endpoint deliberately produces an error log; the test verifies other eligible targets still receive commands. No physical device outcome is inferred from that simulation.

## Reproduce

From the repository root with Python 3.12:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install homeassistant==2024.12.5
python tests/validate_blueprint.py
```

## Recommended site acceptance checks

Verify each configured target type, group mode and supported action on your installation. Include externally changing a target state, unavailable members and manual light-off followed by rotation. Check that only the selected hardware-mode/channel profile responds. Confirm multiroom playback separately using the audio system's own grouping mechanism.

# Validation: v0.3.1

Published YAML SHA256: 31f72f924b745d1477c880adbe8f8d11149cc708f637fd8c2496b09633aacb25
Baseline: GitHub noroozihossein/home-assistant-orielis-universal, main blueprint fetched 2026-09-26; v0.3.0; blob bc9536fe4a3a34debce2963cc633bed94e5d8bd1.
Runtime: Home Assistant 2024.12.5, Python 3.12.
Result: 1582 script cases passed using the actual candidate file. Service endpoints were simulated; there was no connection to physical lights or the remote.

Validated:
- Blueprint, automation schema and recursive action validation.
- All four GREEN channels, synchronized and relative modes.
- Bounds 1–100, 10–80, reversed 80–10, and equal 50–50.
- Current brightness below, at, near and above boundaries; steps 1, 10 and 100 percent, both directions.
- Groups with different initial brightness; synchronized common output and relative individual outputs.
- Brightness rotation never requests zero; off button still calls light.turn_off.
- Baseline CCT limits, unsupported entities, unavailable entities, audio, cover, climate, numbers and custom overrides.
- BLUE default cover, no built-in lighting even with legacy/mixed light targets, custom actions for all BLUE events.
- No queued commands in the baseline concurrent-event test; failing service endpoint does not prevent remaining targets.
- Structural check: original triggers, single execution mode, final cooldown, existing GREEN selectors and RED sections preserved.

One logged error saying 'Simulated disconnected endpoint' is deliberately injected by the resilience test and is expected.
Numeric selectors retain mode: box. Actual browser keyboard interaction was not tested.
New dim bounds are per GREEN channel, shared by its selected lights; they do not apply to manual UI commands or custom overrides.
The 1,582-case suite ran on rc1. The publication YAML differs only in its version title and release-status description; a structural comparison confirmed all inputs and executable content are identical. Physical device timing and radio behavior are not simulated.

Reproduce:
python tests/structure.py
python tests/validate_blueprint.py

Install requirements for the script test with Home Assistant 2024.12.5 under Python 3.12. The structural test uses PyYAML.

## Historical v0.3.0 evidence


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


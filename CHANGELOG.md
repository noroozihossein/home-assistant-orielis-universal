# Changelog

## v0.3.1 — Configurable GREEN dimming limits and BLUE scope update — 2026-09-26

### Added
- Independent GUI minimum/maximum brightness settings for each of the four GREEN channels (defaults 1% / 100%).
- Bounds applied to both synchronized and relative automatic brightness rotation.
- Boundary, mode-isolation and custom-action regression tests; 1,582 HA script cases passed.
- Upgrade instructions, explicit BLUE capability notes and Persian installation guide.

### Fixed
- Brightness reduction clamps above zero instead of switching a light off at the bottom of its range.
- Relative light adjustments now send a bounded absolute brightness calculated from each light's reported state.

### Changed
- BLUE defaults to Curtains/blinds for newly created configurations.
- Removed Lighting from BLUE built-in control choices and light entities from BLUE target selectors.
- BLUE runtime dispatch also ignores legacy or mixed lighting targets.
- Removed unused BLUE brightness/CCT step controls. Audio, cover, climate, numeric and custom actions remain.

### Preserved
- Published v0.3.0 triggers, single execution mode, cooldown, GREEN CCT behavior, RED scenes, event identifiers and custom overrides.
- No experimental BLUE sensitivity algorithm, timing changes or queueing changes were carried forward.

### Upgrade and validation
- Replace the blueprint at the same path; reload automations and verify v0.3.1 in the editor.
- Move built-in BLUE lighting targets to GREEN and explicitly review BLUE Control type.
- Dimming limits are per channel and shared by selected lights; manual changes and custom overrides remain independent.
- Tested with Home Assistant 2024.12.5 and simulated service endpoints. Hardware validation of this update is still pending.
- Code behavior matches v0.3.1-rc1; publication changes the version title and documentation only.

## v0.3.0 — First public release

- Independent Mode 1 / GREEN and Mode 2 / BLUE profiles: four universal channels per mode.
- Four separate Scene / RED action buttons; no invented rotation events.
- Per-profile control type and primary/secondary rotation selectors.
- Synchronized/Relative groups with common limits and pre-command snapshots.
- UI-adjustable steps and custom overrides for all 44 supported events.
- Green configuration and event-override identifiers preserved from v0.2.x; blue target lists are independent.

## v0.2.1 — Local test release

- Added synchronized group control per channel while preserving relative handlers.

## v0.2.0 — Local test release

- Corrected execution configuration and target dispatch; added capability checks and full custom overrides.


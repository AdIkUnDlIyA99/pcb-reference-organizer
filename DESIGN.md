# Design document: PCB Reference Organizer

## Problem and objective

Large PCB layouts become difficult to inspect when references are assigned in an arbitrary order. This plugin provides a small, deterministic workflow for organizing references on the PCB while leaving unselected footprints unchanged.

## Architecture

```text
KiCad PCB Editor
      |
      v
ActionPlugin registration (__init__.py)
      |
      v
ReferenceOrganizerPlugin.Run()
      |
      +--> collect_plan(board)
      |      +--> selected footprints
      |      +--> prefix grouping
      |      +--> coordinate sorting
      |
      +--> preview / user confirmation (wx)
      |
      +--> apply_plan(plan)
             +--> temporary references
             +--> final references
             +--> pcbnew.Refresh()
```

## Module breakdown

`SimpleRenamer/__init__.py` is the discovery entry point. Importing the implementation registers the plugin with KiCad.

`SimpleRenamer/simple_plugin.py` contains the UI boundary, planning algorithm, and KiCad API calls. `prefix()` parses the electrical reference prefix. `position_key()` provides a stable top-to-bottom, left-to-right order using KiCad's internal coordinate units. `collect_plan()` is a pure planning phase: it does not modify the board. `apply_plan()` is the mutation phase.

## Collision-safe update

Directly changing `R1` to `R2` while another selected footprint changes from `R2` to `R1` can create a duplicate intermediate state. The plugin first assigns each item a unique temporary reference (`__PRO_TMP_n__`) and then assigns final references. This makes the update safe for swaps and supports deterministic testing.

## API and data flow

The plugin uses `pcbnew.ActionPlugin`, `pcbnew.GetBoard()`, `board.GetFootprints()`, `footprint.IsSelected()`, `footprint.GetReference()`, `footprint.SetReference()`, and `pcbnew.Refresh()`. `wx.MessageBox` supplies confirmation and status feedback. The only non-standard libraries are the KiCad-provided `pcbnew` and `wx` modules.

## Complexity

For `n` selected footprints, grouping is O(n) and sorting is O(n log n) overall. Memory use is O(n). The complete board is scanned once to obtain selected footprints.

## Compatibility and limitations

The implementation targets KiCad 9's Python ActionPlugin API and Python 3 syntax. It is intentionally limited to PCB footprint references and does not annotate schematics. KiCad itself should be used for the final schematic/PCB annotation consistency check.

## Extension plan

The architecture leaves clear extension points for a direction selector, configurable starting numbers, CSV audit logs, a KiCad undo transaction, and cross-checking references against a schematic.

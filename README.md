# PCB Reference Organizer

PCB Reference Organizer is a KiCad 9 PCB Editor ActionPlugin developed for Task 6 of the eSim Semester Long Internship.

It organizes selected PCB footprint reference designators by their alphabetic prefix, such as `R`, `C`, and `U`. Each group is ordered according to the footprint's board position, previewed for the user, and updated only after confirmation.

The project combines electronics concepts such as footprints, reference designators, and PCB coordinates with computer science concepts including plugin architecture, deterministic sorting, modular design, and collision-safe state updates.

## Features

- Processes only the footprints selected by the user.
- Groups components by reference prefix, such as `R`, `C`, and `U`.
- Orders each group from top to bottom and then from left to right.
- Shows a preview before changing the board.
- Uses temporary references to prevent collisions when selected references swap.
- Supports multiple reference prefixes in one selection.
- Works without external Python packages or network access.
- Provides a simple KiCad toolbar/plugin action.

## Compatibility

- KiCad 9 PCB Editor
- Python 3 included with KiCad
- KiCad-provided `pcbnew` and `wx` modules

The plugin has not been designed for KiCad versions earlier than KiCad 9.

## Installation

Close KiCad PCB Editor before installing the plugin.

### Windows

Create or locate:

```text
%APPDATA%\kicad\9.0\scripting\plugins\
```

### Linux

Create or locate:

```text
~/.local/share/kicad/9.0/scripting/plugins/
```

### macOS

Create or locate:

```text
~/Library/Preferences/kicad/9.0/scripting/plugins/
```

Copy the complete `SimpleRenamer` directory from this repository into the `plugins` directory.

The installed structure should look like this:

```text
plugins/
└── SimpleRenamer/
    ├── __init__.py
    ├── simple_plugin.py
    ├── icon.png
    └── create_icon.py
```

Restart KiCad PCB Editor and open a `.kicad_pcb` board. The **PCB Reference Organizer** action should then be available in the plugin menu or toolbar.

No `pip install` command is required.

## Usage

1. Open a `.kicad_pcb` board in KiCad PCB Editor.
2. Select the footprints that should be organized.
3. Run **PCB Reference Organizer** from the plugin menu or toolbar.
4. Review the proposed reference changes in the preview dialog.
5. Select **Yes** to apply the changes or **No** to cancel.
6. Save the board after verifying the result.

The plugin organizes each prefix independently. For example, selected resistors may become `R1`, `R2`, and `R3`, while selected capacitors become `C1`, `C2`, and `C3`.

## Ordering logic

The plugin sorts selected footprints using their PCB coordinates:

1. Smaller Y coordinate first, producing top-to-bottom ordering.
2. Smaller X coordinate next, producing left-to-right ordering.
3. Existing reference text is used as a stable tie-breaker.

This makes the result deterministic for the same board and selection.

## Testing procedure

Test the plugin with a copy of a board.

Recommended test cases include:

- One selected footprint.
- Multiple footprints with the same prefix.
- Mixed prefixes such as `R`, `C`, and `U`.
- Footprints with unassigned references such as `R?` or `C?`.
- A selection that is already correctly numbered.
- Empty selection.
- References that need to swap positions.
- Footprints located at different X and Y coordinates.
- Saving, closing, and reopening the board after applying changes.
- Cancelling from the preview dialog and confirming that no references change.

## Project files

```text
SimpleRenamer/
├── __init__.py
├── simple_plugin.py
├── icon.png
└── create_icon.py
```

- `SimpleRenamer/__init__.py`: KiCad plugin package entry point.
- `SimpleRenamer/simple_plugin.py`: plugin implementation and registration.
- `SimpleRenamer/icon.png`: toolbar icon.
- `SimpleRenamer/create_icon.py`: optional icon-generation helper.
- `DESIGN.md`: architecture and design decisions.

## Technical design

The plugin separates planning from mutation:

1. Selected footprints are collected from the active board.
2. Footprints are grouped by reference prefix.
3. Each group is sorted by board position.
4. A proposed rename plan is generated.
5. The plan is shown to the user.
6. Temporary references are assigned to selected footprints.
7. Final references are assigned.
8. The PCB view is refreshed.

The temporary-reference step prevents duplicate intermediate references when two selected footprints exchange references.

## Limitations

The current prototype changes PCB footprint references only. It does not annotate a schematic or replace KiCad's complete schematic annotation workflow.

The current version also does not provide:

- Configurable numbering direction.
- Custom starting numbers.
- Undo transaction support.
- CSV export.
- Schematic-to-PCB reference consistency checking.
- Automatic processing of unselected footprints.

These features can be added in future versions.

## Future improvements

Possible future extensions include:

- A settings dialog for numbering direction and starting values.
- Exporting a rename audit log.
- Integration with KiCad undo operations.
- Warnings for conflicts with unselected footprints.
- Schematic and PCB reference consistency checks.
- Filtering by footprint type, value, or layer.

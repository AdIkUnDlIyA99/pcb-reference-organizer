# PCB Reference Organizer

PCB Reference Organizer is a KiCad 9 PCB Editor ActionPlugin developed for Task 6 of the eSim Semester Long Internship.

It groups selected PCB footprints by their alphabetic prefix (`R`, `C`, `U`, etc.), orders each group according to board position, previews the proposed changes, and applies them only after confirmation.

It combines electronics concepts (footprints, reference designators, PCB coordinates) with software concepts (plugin architecture, deterministic sorting, collision-safe transactions, and separation of planning from mutation).

## Features

- Works on selected footprints only; the rest of the board is untouched.
- Deterministic position-based numbering, useful for readable assembly and review.
- Preview dialog before any board mutation.
- Two-phase temporary renaming prevents collisions among selected footprints when references swap.
- Supports mixed prefixes in one selection.
- No external dependencies or network access.

## KiCad 9 installation

1. Close KiCad PCB Editor.
2. Locate the KiCad 9 user plugin directory:
   - Windows: `%APPDATA%\kicad\9.0\scripting\plugins\`
   - Linux: `~/.local/share/kicad/9.0/scripting/plugins/`
   - macOS: `~/Library/Preferences/kicad/9.0/scripting/plugins/`
3. Copy the complete `SimpleRenamer` directory into that `plugins` directory.
4. Start PCB Editor and open a `.kicad_pcb` file. The **PCB Reference Organizer** action appears in the plugin menu or toolbar.

The bundled `icon.png` is the toolbar icon. No `pip install` step is required because KiCad supplies Python, `pcbnew`, and `wx`.

## Usage

1. Make a copy of a board before testing.
2. Select several resistor, capacitor, or IC footprints.
3. Run **PCB Reference Organizer**.
4. Check the preview list, then choose **Yes**.
5. Confirm that each prefix is numbered from top to bottom, with left-to-right ordering within a row.
6. Save the board after verifying the result.

## Testing procedure

Recommended test cases include one footprint, mixed prefixes, an already organized selection, a selection containing `?` references, an empty selection, references that need to swap positions, and saving/reopening the board after applying changes.

## Project files

- `SimpleRenamer/simple_plugin.py`: implementation and ActionPlugin registration.
- `SimpleRenamer/__init__.py`: package entry point.
- `DESIGN.md`: architecture and design decisions.

## Technical design

The plugin separates planning from mutation. It collects selected footprints, groups them by prefix, sorts each group by board position, generates a rename plan, shows the plan for confirmation, assigns unique temporary references, assigns final references, and refreshes the PCB view.

The temporary-reference step prevents duplicate intermediate references when two selected footprints exchange references.

## Limitations and next steps

The prototype changes PCB footprint references only. It does not annotate a schematic or replace KiCad's full schematic annotation workflow. It also does not yet provide configurable numbering direction, custom starting numbers, undo transaction support, CSV export, or schematic/PCB consistency checks.

Future versions can add these features, along with warnings for conflicts with unselected footprints.


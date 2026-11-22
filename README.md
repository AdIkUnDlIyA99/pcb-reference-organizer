# PCB Reference Organizer

PCB Reference Organizer is a KiCad 9 PCB Editor ActionPlugin that makes reference designators predictable and reviewable. It groups selected footprints by their alphabetic prefix (`R`, `C`, `U`, etc.), orders each group top-to-bottom and left-to-right, previews the proposed changes, and applies them only after confirmation.

This is an educational prototype for Task 6. It combines electronics concepts (footprints, reference designators, PCB coordinates) with software concepts (plugin architecture, deterministic sorting, collision-safe transactions, and separation of planning from mutation).

## Features

- Works on selected footprints only; the rest of the board is untouched.
- Deterministic position-based numbering, useful for readable assembly and review.
- Preview dialog before any board mutation.
- Two-phase temporary renaming prevents collisions when references swap.
- Supports mixed prefixes in one selection.
- No external dependencies or network access.

## KiCad 9 installation

1. Close KiCad PCB Editor.
2. Locate the KiCad 9 user plugin directory:
   - Windows: `%APPDATA%\\kicad\\9.0\\scripting\\plugins\\`
   - Linux: `~/.local/share/kicad/9.0/scripting/plugins/`
   - macOS: `~/Library/Preferences/kicad/9.0/scripting/plugins/`
3. Copy the complete `SimpleRenamer` directory into that `plugins` directory.
4. Start PCB Editor and open a `.kicad_pcb` file. The **PCB Reference Organizer** action appears in the toolbar/plugin menu.

The bundled `icon.png` is the toolbar icon. No `pip install` step is required because KiCad supplies Python, `pcbnew`, and `wx`.

## Usage and test procedure

1. Make a copy of a board before testing.
2. Select several resistor, capacitor, or IC footprints.
3. Run **PCB Reference Organizer**.
4. Check the preview list, then choose **Yes**.
5. Confirm that each prefix is numbered from the top row to the bottom row, with left-to-right ordering within a row.
6. Save, close, and reopen the board to verify persistence.

Test cases include one footprint, mixed prefixes, an already organized selection, a selection containing `?` references, an empty selection, and a board with existing references that would otherwise collide.

## Project files

- `SimpleRenamer/simple_plugin.py`: implementation and ActionPlugin registration.
- `SimpleRenamer/__init__.py`: package entry point.
- `DESIGN.md`: architecture and design decisions.
- `SUBMISSION_PROPOSAL.md`: proposal text for approval email.
- `EMAIL_DRAFT.md`: ready-to-edit submission email templates.

## Limitations and next steps

The prototype changes PCB references only; it does not annotate a schematic or replace KiCad's full annotation workflow. A future version can add a numbering direction setting, undo integration, CSV export, and schematic/PCB consistency checks.


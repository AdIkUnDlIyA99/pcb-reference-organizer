"""PCB Reference Organizer for KiCad 9."""
from collections import defaultdict
import re
import pcbnew
import wx


class ReferenceOrganizerPlugin(pcbnew.ActionPlugin):
    """Preview and renumber selected footprints by board position."""

    def __init__(self):
        super().__init__()
        self.name = "PCB Reference Organizer"
        self.category = "Modify PCB"
        self.description = "Preview and renumber selected footprints by position"
        self.show_toolbar_button = True
        self.icon_file_name = "icon.png"

    def defaults(self):
        pass

    @staticmethod
    def prefix(reference):
        match = re.match(r"^([A-Za-z]+)", reference or "")
        return match.group(1).upper() if match else "X"

    @staticmethod
    def position_key(footprint):
        position = footprint.GetPosition()
        return (position.y, position.x, footprint.GetReference().upper())

    def collect_plan(self, board):
        groups = defaultdict(list)
        for footprint in board.GetFootprints():
            if footprint.IsSelected():
                groups[self.prefix(footprint.GetReference())].append(footprint)
        plan = []
        for prefix in sorted(groups):
            ordered = sorted(groups[prefix], key=self.position_key)
            for number, footprint in enumerate(ordered, 1):
                old = footprint.GetReference()
                new = f"{prefix}{number}"
                if old != new:
                    plan.append((footprint, old, new))
        return plan

    @staticmethod
    def format_plan(plan, limit=15):
        lines = [f"{old}  ->  {new}" for _, old, new in plan[:limit]]
        if len(plan) > limit:
            lines.append(f"... and {len(plan) - limit} more")
        return "\n".join(lines)

    @staticmethod
    def apply_plan(plan):
        """Use temporary unique references so swaps cannot collide."""
        for index, (footprint, _, _) in enumerate(plan):
            footprint.SetReference(f"__PRO_TMP_{index}__")
        for footprint, _, new in plan:
            footprint.SetReference(new)

    def Run(self):
        board = pcbnew.GetBoard()
        if board is None:
            wx.MessageBox("Open a .kicad_pcb board first.", self.name, wx.OK | wx.ICON_ERROR)
            return
        plan = self.collect_plan(board)
        if not plan:
            wx.MessageBox("Select one or more footprints with references to organize.", self.name,
                          wx.OK | wx.ICON_INFORMATION)
            return
        message = (f"{len(plan)} reference(s) will be updated.\n\n{self.format_plan(plan)}\n\n"
                    "Apply these changes?")
        if wx.MessageBox(message, self.name, wx.YES_NO | wx.ICON_QUESTION) != wx.YES:
            return
        self.apply_plan(plan)
        pcbnew.Refresh()
        wx.MessageBox(f"Updated {len(plan)} reference(s).", self.name, wx.OK | wx.ICON_INFORMATION)


ReferenceOrganizerPlugin().register()

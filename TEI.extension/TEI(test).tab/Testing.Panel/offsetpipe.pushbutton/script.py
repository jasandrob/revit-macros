# -*- coding: utf-8 -*-
"""
Pipe Offset Splitter
--------------------
Splits a selected pipe at a chosen point, inserts a parallel offset run,
and connects both ends with elbow fittings automatically.

Place this file inside a pyRevit pushbutton folder:
  MyExtension.extension/
    Piping.tab/
      Pipe Offset.panel/
        PipeOffsetSplit.pushbutton/
          script.py
          icon.png
"""

from pyrevit import revit, DB, forms, script
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

# -- helpers ------------------------------------------------------------------

def mm_to_ft(mm):
    return mm / 304.8


def get_connector_at(element, point, tol=0.05):
    """Return the connector on element closest to point (in feet)."""
    cm = element.ConnectorManager
    best, best_d = None, float("inf")
    for c in cm.Connectors:
        d = c.Origin.DistanceTo(point)
        if d < best_d:
            best_d, best = d, c
    return best if best_d < tol else None


def set_diameter(pipe_elem, diameter_ft):
    """
    Set pipe diameter from a plain float (internal feet).
    Must be called INSIDE an open transaction.
    RBS_PIPE_DIAMETER_PARAM is read-only on some pipe types - in that
    case Revit sizes the pipe from the connector, so we silently skip.
    """
    p = pipe_elem.get_Parameter(DB.BuiltInParameter.RBS_PIPE_DIAMETER_PARAM)
    if p is not None and not p.IsReadOnly:
        p.Set(diameter_ft)


# -- dialog -------------------------------------------------------------------

class OffsetDialog(forms.WPFWindow):

    XAML = """
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Pipe Offset Parameters"
        Width="340" SizeToContent="Height"
        WindowStartupLocation="CenterScreen"
        ResizeMode="NoResize">
  <Window.Resources>
    <Style TargetType="TextBox">
      <Setter Property="Margin" Value="0,4,0,8"/>
      <Setter Property="Padding" Value="6,4"/>
      <Setter Property="FontSize" Value="13"/>
      <Setter Property="BorderBrush" Value="#CCCCCC"/>
    </Style>
    <Style TargetType="Label">
      <Setter Property="FontSize" Value="12"/>
      <Setter Property="Foreground" Value="#555555"/>
      <Setter Property="Padding" Value="0,0,0,0"/>
    </Style>
    <Style TargetType="ComboBox">
      <Setter Property="Margin" Value="0,4,0,8"/>
      <Setter Property="Padding" Value="6,4"/>
      <Setter Property="FontSize" Value="13"/>
    </Style>
    <Style TargetType="Button">
      <Setter Property="Padding" Value="18,8"/>
      <Setter Property="FontSize" Value="13"/>
      <Setter Property="Margin" Value="4,0"/>
      <Setter Property="Cursor" Value="Hand"/>
    </Style>
  </Window.Resources>
  <StackPanel Margin="20">
    <TextBlock FontSize="15" FontWeight="SemiBold" Margin="0,0,0,12"
               Foreground="#1A1A2E">Pipe Offset Splitter</TextBlock>

    <Label>Lateral offset distance (mm)</Label>
    <TextBox x:Name="TxtLateral" Text="150"/>

    <Label>Offset run length (mm)</Label>
    <TextBox x:Name="TxtLength" Text="600"/>

    <Label>Offset direction</Label>
    <ComboBox x:Name="CmbDir" SelectedIndex="2">
      <ComboBoxItem Content="+Y  (up)"/>
      <ComboBoxItem Content="-Y  (down)"/>
      <ComboBoxItem Content="+X  (right)"/>
      <ComboBoxItem Content="-X  (left)"/>
      <ComboBoxItem Content="+Z  (forward)"/>
      <ComboBoxItem Content="-Z  (back)"/>
    </ComboBox>

    <Label>Split position</Label>
    <ComboBox x:Name="CmbSplit" SelectedIndex="1">
      <ComboBoxItem Content="Pick point on pipe"/>
      <ComboBoxItem Content="Midpoint of pipe"/>
      <ComboBoxItem Content="1/3 along pipe"/>
      <ComboBoxItem Content="2/3 along pipe"/>
    </ComboBox>

    <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" Margin="0,12,0,0">
      <Button x:Name="BtnCancel" Content="Cancel" IsCancel="True"/>
      <Button x:Name="BtnOK" Content="Place Offset" IsDefault="True"
              Background="#1B6CA8" Foreground="White"/>
    </StackPanel>
  </StackPanel>
</Window>
"""

    def __init__(self):
        forms.WPFWindow.__init__(self, self.XAML, literal_string=True)
        self.result = None
        self.BtnOK.Click     += self._ok
        self.BtnCancel.Click += self._cancel

    def _ok(self, s, e):
        try:
            self.result = dict(
                lateral_mm = float(self.TxtLateral.Text),
                length_mm  = float(self.TxtLength.Text),
                dir_idx    = self.CmbDir.SelectedIndex,
                split_idx  = self.CmbSplit.SelectedIndex,
            )
            self.Close()
        except ValueError:
            forms.alert("Enter valid numbers for distances.", exitscript=False)

    def _cancel(self, s, e):
        self.Close()


# -- direction vectors --------------------------------------------------------

DIR_VECTORS = {
    0: DB.XYZ( 0,  1,  0),
    1: DB.XYZ( 0, -1,  0),
    2: DB.XYZ( 1,  0,  0),
    3: DB.XYZ(-1,  0,  0),
    4: DB.XYZ( 0,  0,  1),
    5: DB.XYZ( 0,  0, -1),
}


# -- split parameter ----------------------------------------------------------

def compute_split_param(split_idx, uidoc, pipe):
    """
    Returns normalised t in [0, 1] along the pipe curve.
    Uses PickPoint (returns XYZ directly) - no .GlobalPoint crash.
    """
    if split_idx == 0:
        picked_pt = uidoc.Selection.PickPoint(
            "Click near the pipe to set split location"
        )
        result = pipe.Location.Curve.Project(picked_pt)
        return result.Parameter

    return {1: 0.5, 2: 1.0 / 3.0, 3: 2.0 / 3.0}[split_idx]


# -- main ---------------------------------------------------------------------

def run():
    uidoc = revit.uidoc
    doc   = revit.doc

    # 1. Dialog
    dlg = OffsetDialog()
    dlg.ShowDialog()
    if dlg.result is None:
        script.exit()

    p          = dlg.result
    lateral_ft = mm_to_ft(p["lateral_mm"])
    offset_dir = DIR_VECTORS[p["dir_idx"]]
    split_idx  = p["split_idx"]

    # 2. Pick pipe, validate category
    try:
        ref  = uidoc.Selection.PickObject(ObjectType.Element, "Select a pipe to split")
        pipe = doc.GetElement(ref.ElementId)
    except Exception:
        script.exit()

    # if (pipe.Category is None or
            # pipe.Category.Id.IntegerValue != int(DB.BuiltInCategory.OST_PipeCurves)):
        # forms.alert("Selected element is not a pipe.", exitscript=True)
    if (pipe.Category is None):
        forms.alert("Selected element is not a pipe.", exitscript=True)

    # 3. Read ALL pipe properties as plain Python values BEFORE the transaction.
    #    Parameter objects become invalid once the pipe is deleted - read
    #    AsDouble() now and store a plain float.
    curve      = pipe.Location.Curve
    pipe_start = curve.GetEndPoint(0)
    pipe_end   = curve.GetEndPoint(1)
    print(pipe_start,pipe_end)
    print(pipe_start.X)
    print(pipe_start.CrossProduct(pipe_end))

    pipe_type_id   = pipe.GetTypeId()
    level_id       = pipe.LevelId
    system_type_id = (pipe.MEPSystem.GetTypeId()
                      if pipe.MEPSystem
                      else DB.ElementId.InvalidElementId)

    diam_param  = pipe.get_Parameter(DB.BuiltInParameter.RBS_PIPE_DIAMETER_PARAM)
    diameter_ft = diam_param.AsDouble() if diam_param else None  # plain float

    # 4. Compute split location (PickPoint fires here if needed)
    t        = compute_split_param(split_idx, uidoc, pipe)
    split_pt = curve.Evaluate(t, True)

    # 5. Geometry
    axis     = (pipe_end - pipe_start).Normalize()
    half_gap = lateral_ft

    pt_A  = split_pt - axis.Multiply(half_gap)
    pt_B  = split_pt + axis.Multiply(half_gap)
    pt_O1 = pt_A + offset_dir.Multiply(lateral_ft)
    pt_O2 = pt_B + offset_dir.Multiply(lateral_ft)
    pt_new_end = DB.XYZ(pt_O1.X, pipe_end.Y, pipe_end.Z)

    if pt_A.DistanceTo(pipe_start) < 0.01 or pipe_end.DistanceTo(pt_B) < 0.01:
        forms.alert(
            "Split point too close to pipe end.\n"
            "Increase pipe length or reduce lateral offset distance.",
            exitscript=True,
        )

    # 6. All document changes inside ONE transaction

    with revit.Transaction("Pipe Offset Split"):

        # Split the original pipe at pt_A - returns the Element ID of the new
        # bottom segment. The original pipe becomes the top segment (pipe_start -> pt_A)
        # and the new pipe is the bottom segment (pt_A -> pipe_end).
        # Both end connectors are fully preserved.
        new_pipe_id = PlumbingUtils.BreakCurve(doc, pipe.Id, pt_A)
        top_pipe = doc.GetElement(new_pipe_id)

        # Move the bottom pipe to the offset X position
        new_start = DB.XYZ(pt_O1.X, pt_A.Y,       pt_O1.Z)
        new_end   = DB.XYZ(pt_O1.X, pipe_end.Y,   pt_O1.Z)
        pipe.Location.Curve = DB.Line.CreateBound(new_start, new_end)

        # Horizontal offset run connecting the two
        seg_off = Pipe.Create(doc, system_type_id, pipe_type_id, level_id,
                              pt_A, pt_O1)

        if diameter_ft:
            set_diameter(seg_off, diameter_ft)

        # Elbow 1: bottom of top pipe -> start of seg_off
        c1a = get_connector_at(top_pipe,    pt_A,  tol=0.05)
        c1b = get_connector_at(seg_off, pt_A,  tol=0.05)
        if c1a and c1b:
            doc.Create.NewElbowFitting(c1a, c1b)

        # Elbow 2: end of seg_off -> top of bottom pipe (now at pt_O1)
        c2a = get_connector_at(seg_off,     pt_O1, tol=0.05)
        c2b = get_connector_at(pipe, new_start, tol=0.05)
        if c2a and c2b:
            doc.Create.NewElbowFitting(c2a, c2b)
            
    forms.toast(
        "Done  -  lateral {:.0f} mm".format(p["lateral_mm"]),
        title="Pipe Offset Splitter",
        appid="PipeOffsetSplit",
    )


if __name__ == "__main__":
    run()
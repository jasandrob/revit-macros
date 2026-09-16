
"""
create test code
"""


from pyrevit import revit
from pyrevit import DB, forms\

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType

doc = __revit__.ActiveUIDocument.Document
uidoc = revit.uidoc
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


sel = uidoc.Selection

def convert_to_ft(feet, inches):
    """
    takes a measurement in feet and inches and automatically converts to a decimal in feet
    """
    
    tot_ft = feet + inches * 0.0833
    
    return tot_ft
    
    
def create_rect(pt_initial, width, height):
    """
    creates a rectangle given its upper left corner, a height, and a width

    returns: a list of the line elements in the rectangle
    """
    pt_right = pt_initial + XYZ(width, 0, 0)
    pt_down = pt_initial + XYZ(0, -1*height, 0)
    pt_rightdown = pt_initial + XYZ(width, -1*height, 0)


    list = [pt_initial, pt_right, pt_rightdown, pt_down]
    


    line_list = []
    
    for i in range(len(list)):
        
        #last line of rectangle connects back to first point
        if (i + 1) > (len(list) - 1):
            pt_start = list[i]
            pt_end = list[0]
        else:
            pt_start = list[i]
            pt_end = list[i + 1]
        
        curve = Line.CreateBound(pt_start, pt_end)
        detail_line = doc.Create.NewDetailCurve(active_view, curve)
        
        line_list.append(detail_line)
        
    return line_list



def create_chart_block(pt):
    """
    Creates the chart block given the upper left corner, 
    """
    width = convert_to_ft(48, 7)
    header_height = convert_to_ft(6,2)
    
    subheader_height = convert_to_ft(9, 10)
    subheader_width_1 = width * 0.265
    subheader_width_2 = width * 0.273
    subheader_width_3 = width * 0.462
    
    cat_height = convert_to_ft(3, 10)
    col1_width = subheader_width_1 + subheader_width_2
    
    spacing = convert_to_ft(0, 5)
    full_header_height = header_height + spacing + subheader_height + cat_height
    row_height = convert_to_ft(4, 5)
    
    num_rows = 11
    
    
    
    pt_initial = pt + XYZ(spacing, -1*spacing, 0)
    
    
    #create the header
    create_rect(pt_initial, width, header_height)
    
    #create the subheader
    create_rect(pt_initial - XYZ(0, header_height + spacing, 0), subheader_width_1, subheader_height)
    create_rect(pt_initial + XYZ(subheader_width_1, -1*(header_height + spacing), 0), subheader_width_2, subheader_height)
    create_rect(pt_initial + XYZ(subheader_width_1 + subheader_width_2, -1*(header_height + spacing), 0), subheader_width_3, subheader_height)
    
    #create the row catgeories
    create_rect(pt_initial + XYZ(0, -1*(header_height + subheader_height + spacing), 0), col1_width, cat_height)
    create_rect(pt_initial + XYZ(subheader_width_1 + subheader_width_2, -1*(header_height + subheader_height + spacing), 0), subheader_width_3, cat_height)
    
    #create the rows
    for i in range(num_rows):
        create_rect(pt_initial + XYZ(0, -1 * (full_header_height + i * row_height), 0), col1_width, row_height)
        create_rect(pt_initial + XYZ(col1_width, -1 * (full_header_height + i * row_height), 0), subheader_width_3, row_height)
    
    #create border
    create_rect(pt, width + 2* spacing, full_header_height + row_height * num_rows + 2 * spacing)
    
    
    
    
def center_text(text):
    """
    takes a textnote object and moves it so that it is centered on its current location point
    """





    #gets the bounding box for the text element to find the centerpoint
    box = text.get_BoundingBox(active_view)
    center = (box.Max + box.Min)/2

    #half values for textwidth and textheight
    text_wid = center.X - box.Min.X
    text_height = center.Y - box.Min.Y

    #text location is different than BoundBoxXYZ location, adjust for this
    text_to_boxX = text.Coord - box.Min
    text_to_boxY = box.Max - text.Coord


    ElementTransformUtils.MoveElement(doc, text.Id, XYZ(text_to_boxX.X - text_wid, text_height - text_to_boxY.Y, 0))
    
    
    
    
    
    
with Transaction(doc, "creating") as t:
    t.Start()
    
    pt_sel = sel.PickPoint("Please pick a point to place group")
    # uvpt = UV(pt[0], pt[1])

    
    
    ##create text
    # text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    # text = 'Hello BIM World!'
    
    # Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt, text, text_type_id)
    
    
    
    
    
    # ##create room
    # room = doc.Create.NewRoom(active_level, uvpt)
    # room_link = LinkElementId(room.Id)

    # doc.Create.NewRoomTag(room_link, uvpt, active_view.Id)
    
    
    
    
    # #create line
    # pt_end = sel.PickPoint()
    # curve = Line.CreateBound(pt, pt_end)
    # detail_line = doc.Create.NewDetailCurve(active_view, curve)
    

    
    
    
    # #create wall
    # # pt_end = sel.PickPoint()
    # pt = XYZ(30, 0 , 0)
    # pt_end = XYZ(30, 5, 0)
    # curve = Line.CreateBound(pt, pt_end)
    # wall = Wall.Create(doc, curve, active_level.Id, False)
    
    
    # #create window (doesnt work)
    # pt = XYZ(30, 0 , 0)
    # pt_end = XYZ(30, 5, 0)
    # pt_mid = (pt + pt_end)/2
    # host_wall = doc.GetElement(ElementId(3647784))

    
    # window_type = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType().FirstElement()
    # print(window_type)
    # window = doc.Create.NewFamilyInstance(pt_mid, window_type, host_wall, StructuralType.NonStructural )
    
    
    
    
    # #create NewFamilyInstance (doesnt work)
    # def get_type_by_name(type_name):
        # #CREATE RULE
        # param_type = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
        # f_param = ParameterValueProvider(param_type)
        # evaluator = FilterStringEquals()
        # f_rule = FilterStringRule(f_param, evaluator, type_name) 
        
        # #CREATE FILTER
        # filter_type_name = ElementParameterFilter(f_rule)
        
        # #GET ELEMENTS
        # return FilteredElementCollector(doc).WherePasses(filter_type_name).WhereElementIsElementType().FirstElement()
    
    # #ARGUMENTS
    # symbol = get_type_by_name('Single-Flush')
    # print(symbol)
    # #CREATE AN ELEMENT
    # element = doc.Create.NewFamilyInstance(pt, symbol, StructuralType.NonStructural)
    
    
    
    
    
    
    
    
    # #create viewschedule
    # viewsch = ViewSchedule.CreateViewList(doc)
    # fields = viewsch.Definition.GetSchedulableFields()
    
    
    # def add_field_by_name(name_str, sch_fields, view_sch):
        
    
        # for field in fields:
            # name = field.GetName(doc)
            
            # if name == name_str:
                # view_sch.Definition.AddField(field)
                # break
            
            
    # #print(names)
    # field_names = ['Type', 'Parts Visibility', 'Title on Sheet']
    
    # for fname in field_names:
        # add_field_by_name(fname, fields, viewsch)
    
    
    # ScheduleSheetInstance.Create(doc, active_view.Id, viewsch.Id, pt)
    
    spacing = convert_to_ft(0, 5)
    width = convert_to_ft(48, 7)
    create_chart_block(pt_sel)
    header_height = convert_to_ft(6,2)
    
    
    
    
    

    
    ##create text

    list = FilteredElementCollector(doc).OfClass(TextNoteType)

    text_type_id= FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    
    words = "000000"
    text = Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt_sel + XYZ(width/2 + spacing, -1 * (header_height/2 + spacing), 0), words, text_type_id)
    
    
    
    text_ids = FilteredElementCollector(doc).OfClass(TextNoteType).ToElementIds()
  
    failed = False
    
    
    
    
    for textNoteId in text_ids:
        mytextNote = doc.GetElement(textNoteId)
        paraIndex2 = BuiltInParameter.TEXT_FONT
        
        
        
        
        #FIRST CHECKS IF TEI GAS TITLE FONT ALREADY EXISTS
        if failed is False:
            try:
                noteType = mytextNote.Duplicate("TEI GAS TITLE")
                
                
                

                noteFont = noteType.get_Parameter(paraIndex2)
                

                noteFont.Set("Arial Title")
                
                text.ChangeTypeId(noteType.Id)
                
                break
                
            except:
                failed = True
        
        #IF IT ALREADY EXISTS, FIND THE FONT AND USE IT
        else:
            myNoteFont = mytextNote.get_Parameter(paraIndex2)
            type_name = mytextNote.LookupParameter("Type Name").AsString()

            if myNoteFont.AsString() == 'Arial Title' and type_name == "TEI GAS TITLE":
                text.ChangeTypeId(mytextNote.Id)
                
                break
        
    textType = text.Symbol
    paraIndex = BuiltInParameter.TEXT_SIZE
    textSize = textType.get_Parameter(paraIndex)
    print(textSize)
    print(textSize.AsString())
    
    newSize = (1.0/4) * (1.0 / 12)
    textSize.Set(newSize)
    
    #creates a transparent background for the text, 1 = Transparent and 0 = Opaque
    paraIndex3 = BuiltInParameter.TEXT_BACKGROUND
    textBackground = textType.get_Parameter(paraIndex3)
    
    textBackground.Set(1)
    
    print(text.Name)
    
    # paraIndex4 = BuiltInParameter.TEXT_TEXT
    # textText = text.get_Parameter(paraIndex4)
    
    # print(textText.AsString())
    


                    
    t.Commit()
    
    # #cannot get text properties until commit, so start a new Transaction
    t.Start()
    # wid = text.Width



   
    center_text(text)
    
 
    # text.Coord = coord + XYZ(-1 * wid/2, 0, 0)
    t.Commit()
    

#import traceback
# try:
    # hu = fasdfasd
# except Exception, err:
    # pass

# print(traceback.format_exc())
    
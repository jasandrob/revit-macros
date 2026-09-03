
"""
create test code
"""
import traceback


from pyrevit import revit
from pyrevit import DB, forms

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



def create_chart_block(pt, width, subheader_widths, subheader_height, cat_height):
    """
    Creates the chart block given the upper left corner, 
    
    Inputs:
        subheader_witdths: a list of the subheader widths as a fraction of the total chart width
    """
    header_height = convert_to_ft(6,2)
    

    subheader_width_1 = subheader_widths[0]
    subheader_width_2 = subheader_widths[1]
    subheader_width_3 = subheader_widths[2]
    

    col1_width = subheader_width_1 + subheader_width_2
    
    spacing = convert_to_ft(0, 5)
    full_header_height = header_height + spacing + subheader_height + cat_height
    row_height = convert_to_ft(4, 5)
    
    num_rows = 11
    
    
    
    pt_initial = pt + XYZ(spacing, -1*spacing, 0)
    
    
    #create the header
    create_rect(pt_initial, width, header_height)
    
    #create the subheader
    subheader_pt1 = pt_initial + XYZ(0, -1 * (header_height + spacing), 0)
    subheader_pt2 = pt_initial + XYZ(subheader_width_1, -1*(header_height + spacing), 0)
    subheader_pt3 = pt_initial + XYZ(subheader_width_1 + subheader_width_2, -1*(header_height + spacing), 0)
    
    create_rect(subheader_pt1, subheader_width_1, subheader_height)
    create_rect(subheader_pt2, subheader_width_2, subheader_height)
    create_rect(subheader_pt3, subheader_width_3, subheader_height)
    
    #create the row catgeories
    cat_pt1 = pt_initial + XYZ(0, -1*(header_height + subheader_height + spacing), 0)
    cat_pt2 = pt_initial + XYZ(subheader_width_1 + subheader_width_2, -1*(header_height + subheader_height + spacing), 0)
    create_rect(cat_pt1, col1_width, cat_height)
    create_rect(cat_pt2, subheader_width_3, cat_height)
    
    #create the rows
    col1_pts = []
    col2_pts = []
    for i in range(num_rows):
        col1_pt = pt_initial + XYZ(0, -1 * (full_header_height + i * row_height), 0)
        col2_pt = pt_initial + XYZ(col1_width, -1 * (full_header_height + i * row_height), 0)
        
        col1_row = create_rect(col1_pt, col1_width, row_height)
        col2_row  = create_rect(col2_pt, subheader_width_3, row_height)
        
        col1_pts.append(col1_pt)
        col2_pts.append(col2_pt)
    
    #create border
    create_rect(pt, width + 2* spacing, full_header_height + row_height * num_rows + 2 * spacing)
    
    
    
    subheader_pt_list = [subheader_pt1, subheader_pt2, subheader_pt3]
    cat_pt_list = [cat_pt1, cat_pt2]
    
    
    return subheader_pt_list, cat_pt_list, col1_pts, col2_pts, col1_width
    
    
    
    
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


    
def font_change(text_ids, doc, active_view, pt, words, new_type_name, new_size, new_font):

    id = None
    failed = False
    for textNoteId in text_ids:
    
        #gets the font of each textType
        mytextNote = doc.GetElement(textNoteId)
        paraIndex2 = BuiltInParameter.TEXT_FONT

        
        #FIRST CHECKS IF TEI GAS TITLE FONT ALREADY EXISTS
        if failed is False:
            try:
                #creates a new textType
                noteType = mytextNote.Duplicate(new_type_name)
                
                
                #sets the font here
                noteFont = noteType.get_Parameter(paraIndex2)
                noteFont.Set(new_font)
                
                #sets your text element to the new textType
                type_id = noteType.Id
                text_ele = Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt, words, type_id)
                
                return text_ele, type_id
                
            except:
                failed = True
        
        #IF IT ALREADY EXISTS, FIND THE FONT AND USE IT
        else:
            myNoteFont = mytextNote.get_Parameter(paraIndex2)
            type_name = mytextNote.LookupParameter("Type Name").AsString()
            
            #
            l = len(new_type_name)
            short_string = type_name[:l]

            if myNoteFont.AsString() == new_font and short_string == new_type_name:
                #text_ele.ChangeTypeId(mytextNote.Id)
                type_id = mytextNote.Id
                text_ele = Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt, words, type_id)
                return text_ele, type_id            
            
            

    #IF TEXTTYPE ALREADY EXISTS BUT IS THE WRONG FONT
    for i in range(100):
    
        try:
            new_name = new_type_name + str(i + 2)
        
            #if name already exists will raise an exception error
            noteType = mytextNote.Duplicate(new_name)
            
            noteFont = noteType.get_Parameter(paraIndex2)
            noteFont.Set(new_font)
            
            type_id = noteType.Id
            text_ele = Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt, words, type_id)
            
            duplicate = True
            
            return text_ele, type_id
        except:
            pass
                       
    #could not create font in 100 tries, probably something is wrong
    print("ERROR CREATING FONTS")


    
def create_text(doc, active_view, pt, words, new_type_name, new_size, new_font):
    """
    creates a new textNote element at a given point. Create a new text for each size of text/font.
    
    inputs:
                   pt: XYZ point, where the text is to be inserted
                words: str, what you want the text to say
        new_type_name: str, reprenting the textType
                 size: size of the font of the text
             new_font: str, the name of the font of the text
        
    returns:
        text_ele: the text element you just created
    """


    #search through the existing textTypes to see if the one you want already existing
    text_ids = FilteredElementCollector(doc).OfClass(TextNoteType).ToElementIds()

    text_info = font_change(text_ids, doc, active_view, pt, words, new_type_name, new_size, new_font)
    text_ele = text_info[0]
    type_id = text_info[1]


    
    #this code changes the text sizes
    textType = text_ele.Symbol
    paraIndex = BuiltInParameter.TEXT_SIZE
    textSize = textType.get_Parameter(paraIndex)
    

    textSize.Set(new_size)

    #creates a transparent background for the text, 1 = Transparent and 0 = Opaque
    paraIndex3 = BuiltInParameter.TEXT_BACKGROUND
    textBackground = textType.get_Parameter(paraIndex3)
    
    textBackground.Set(1)
    
    

    
    return text_ele, type_id
    
    
    
#START TRANSACTION TO COMMIT CHANGES
with Transaction(doc, "creating") as t:
    
    #variable to check if rollback has been called
    rollback = False

    t.Start()
    
    pt_sel = sel.PickPoint("Please pick a point to place GAS SIZE CHART")
    # uvpt = UV(pt[0], pt[1])


    header_height = convert_to_ft(6,2)
    width = convert_to_ft(48, 7)
    
    
    subheader_height = convert_to_ft(9, 10)
    subheader_width_fractions = [0.265, 0.273, 0.462]
    subheader_widths = [width * i for i in subheader_width_fractions]
    spacing = convert_to_ft(0, 5)
    
    cat_height = convert_to_ft(3, 10)



    font = "Arial Title"
    font2 = "Arial"
    

    
    #creates the chart block
    [sub_header_pts, cat_pts, col1_pts, col2_pts, col1_width] = create_chart_block(pt_sel, width, subheader_widths, subheader_height, cat_height)

    
    newSize = (3.0/16) * (1.0 / 12)
    
    #create header text
    create_point = pt_sel + XYZ(width/2 + spacing, -1 * (header_height/2 + spacing), 0)
    text_ele1 = create_text(doc, active_view, create_point, 'GAS SIZE CHART', 'TEI GAS TITLE', newSize, 'Arial Title')
    
    #create subheader text
    gen_text_type = 'TEI GAS CHART TEXT'
    subhead_text = ["PRESSURE", "PSI", "XX", "PRESSURE", "DROP", "TO XXX", "MAX DEVELOPED", "LENGTH (FEET)", "XXXX"]
    gen_text_size = (3.0/32) * (1.0 / 12)
    
    
    
    #create the points of each text element in the subheader. Should be as many points as length of subhead_text
    subheader_pts = []
    for i in range(3):
        for j in range(3):
            subheader_pt = sub_header_pts[i] + XYZ(subheader_widths[i]/2, (j+1) * -subheader_height/4, 0)
            subheader_pts.append(subheader_pt)
            
           
    #check if lists are compatible in length
    if len(subhead_text) == len(subheader_pts):
    
        try:
            #creates all the subheader text
            text_elements = []
            for i in range(len(subhead_text)):
                text_ele = create_text(doc, active_view, subheader_pts[i], subhead_text[i], gen_text_type, gen_text_size, 'Arial')
                text_elements.append(text_ele)
        except:
            print("Error creating chart 01")
            t.RollBack()
            rollback = True
    
    else:
        print("Error creating chart 02")
        t.RollBack()
        
        rollback = True
    
    
    
    
    #create category header text
    cat1_text = create_text(doc, active_view, cat_pts[0] + XYZ(col1_width/2 , -cat_height/2, 0), "PIPE SIZE (IPC)", gen_text_type, gen_text_size, 'Arial')
    cat2_text = create_text(doc, active_view, cat_pts[1] + XYZ(subheader_widths[2]/2, -cat_height/2, 0), "MAX LOAD (MBH)", gen_text_type, gen_text_size, 'Arial')
    
    #create row text
    pipe_sizes = ['1/2"', '3/4"', '1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"', '3"', '4"', '6"', '8"']
    pipe_loads = ['147', '307', '579', '1,189', '1,762', '3,434', '5,475', '9,683', '19,759', '57,922', '119,061']
    
    row_text = []
    if len(pipe_sizes) == len(pipe_loads):
        for size, load, col1_pt, col2_pt in zip(pipe_sizes, pipe_loads, col1_pts, col2_pts):
            col1 = create_text(doc, active_view, col1_pt + XYZ(col1_width/2 , -cat_height/2, 0), size, gen_text_type, gen_text_size, 'Arial')
            col2 = create_text(doc, active_view, col2_pt + XYZ(subheader_widths[2]/2, -cat_height/2, 0), load, gen_text_type, gen_text_size, 'Arial')
            
            row_text.append(col1)
            row_text.append(col2)
    
    
    
    
    if rollback is False:
        t.Commit()
        # #cannot get text properties until commit, so start a new Transaction
        t.Start()

        center_text(text_ele1[0])
        center_text(cat1_text[0])
        center_text(cat2_text[0])

        #centers the text elements
        #center_text(text_ele1[1])

        for ele in text_elements:
            center_text(ele[0])

        for text in row_text:
            center_text(text[0])

        t.Commit()


#import traceback
# try:
    # hu = fasdfasd
# except Exception, err:
    # pass

# print(traceback.format_exc())
    
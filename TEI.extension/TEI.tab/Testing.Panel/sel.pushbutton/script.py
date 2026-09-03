
"""
sel test code
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






elid = sel.GetElementIds()
ele = doc.GetElement(elid[0])

for i in elid:
    print(i)
print(ele)
print('-------')


all_ele = revit.query.get_all_elements_in_view(ele)
print(all_ele)

    
# with Transaction(doc, "creating") as t:
    # t.Start()
    
    # pt = sel.PickPoint("Please pick a point to place group")
    # uvpt = UV(pt[0], pt[1])

    
    
    # ##create text
    # # text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
    # # text = 'Hello BIM World!'
    
    # # Autodesk.Revit.DB.TextNote.Create(doc, active_view.Id, pt, text, text_type_id)
    
    
    
    
    
    # # ##create room
    # # room = doc.Create.NewRoom(active_level, uvpt)
    # # room_link = LinkElementId(room.Id)

    # # doc.Create.NewRoomTag(room_link, uvpt, active_view.Id)
    
    
    
    
    # # #create line
    # # pt_end = sel.PickPoint()
    # # curve = Line.CreateBound(pt, pt_end)
    # # detail_line = doc.Create.NewDetailCurve(active_view, curve)
    

    
    
    
    # # #create wall
    # # # pt_end = sel.PickPoint()
    # # pt = XYZ(30, 0 , 0)
    # # pt_end = XYZ(30, 5, 0)
    # # curve = Line.CreateBound(pt, pt_end)
    # # wall = Wall.Create(doc, curve, active_level.Id, False)
    
    
    # # #create window (doesnt work)
    # # pt = XYZ(30, 0 , 0)
    # # pt_end = XYZ(30, 5, 0)
    # # pt_mid = (pt + pt_end)/2
    # # host_wall = doc.GetElement(ElementId(3647784))

    
    # # window_type = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType().FirstElement()
    # # print(window_type)
    # # window = doc.Create.NewFamilyInstance(pt_mid, window_type, host_wall, StructuralType.NonStructural )
    
    
    
    
    # # #create NewFamilyInstance (doesnt work)
    # # def get_type_by_name(type_name):
        # # #CREATE RULE
        # # param_type = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
        # # f_param = ParameterValueProvider(param_type)
        # # evaluator = FilterStringEquals()
        # # f_rule = FilterStringRule(f_param, evaluator, type_name) 
        
        # # #CREATE FILTER
        # # filter_type_name = ElementParameterFilter(f_rule)
        
        # # #GET ELEMENTS
        # # return FilteredElementCollector(doc).WherePasses(filter_type_name).WhereElementIsElementType().FirstElement()
    
    # # #ARGUMENTS
    # # symbol = get_type_by_name('Single-Flush')
    # # print(symbol)
    # # #CREATE AN ELEMENT
    # # element = doc.Create.NewFamilyInstance(pt, symbol, StructuralType.NonStructural)
    
    
    
    
    
    
    
    
    # # #create viewschedule
    # # viewsch = ViewSchedule.CreateViewList(doc)
    # # fields = viewsch.Definition.GetSchedulableFields()
    
    
    # # def add_field_by_name(name_str, sch_fields, view_sch):
        
    
        # # for field in fields:
            # # name = field.GetName(doc)
            
            # # if name == name_str:
                # # view_sch.Definition.AddField(field)
                # # break
            
            
    # # #print(names)
    # # field_names = ['Type', 'Parts Visibility', 'Title on Sheet']
    
    # # for fname in field_names:
        # # add_field_by_name(fname, fields, viewsch)
    
    
    # # ScheduleSheetInstance.Create(doc, active_view.Id, viewsch.Id, pt)
    
    
    
    
    
    
    # # create keySchedule
    # # as user for target key schedule category
    # key_sched_cat = forms.SelectFromList.show(
        # revit.query.get_key_schedule_categories(),
        # name_attr='Name',
        # multiselect=False,
        # title="Select Key-Schedule Category",
        
        # )
        
        
        
        
    # # def has_matching_fields(keysched_def, fields):
        # # """Check if given schedule definition contains any of the fields"""
        # # exist_ksch_fields = set()
        # # for idx in range(keysched_def.GetFieldCount()):
            # # sched_field = keysched_def.GetField(idx)
            # # exist_ksch_fields.add(sched_field.GetName())
        # # other_fields = exist_ksch_fields.difference(set(fields))
        # # return len(other_fields) == 0
        
        
        
        
        
    # # def find_matching_keyschedule(category, fields, doc=None):
        # # """Find any existing key schedules that have matching fields"""
        # # doc = doc or revit.doc
        # # all_schedules = \
            # # revit.query.get_all_views(doc=doc, view_types=[DB.ViewType.Schedule])
        # # # check for existing key schedules (check 1)
        # # matching_keysched = next(
            # # (
                # # x for x in all_schedules
                # # if x.Definition.IsKeySchedule
                # # and x.Definition.CategoryId == category.Id
            # # ),
            # # None
        # # )
        # # if matching_keysched:
            # # if has_matching_fields(matching_keysched.Definition, fields):
                # # return matching_keysched
            
            
    # existing_keyschedule = False
    # # existing_keyschedule = find_matching_keyschedule(category=key_sched_cat, fields=param_names)
            
    
    # if existing_keyschedule:
        # print("Keyschedule already exists")
    
    # else:
        # new_sch = ViewSchedule.CreateKeySchedule(doc, key_sched_cat.Id)
        # #new_sch.Name = "eww"
        # new_sch.KeyScheduleParameterName = "woo woot"
        
        # fields = new_sch.Definition.GetSchedulableFields()

        # for i in range(1, 3):
            # field = fields[i]
            # new_sch.Definition.AddField(field)
        
        
        
        
        # table_data = new_sch.GetTableData()
        # section_data = table_data.GetSectionData(DB.SectionType.Body)
       
        # for _ in range(5):
            # section_data.InsertRow(section_data.LastRowNumber + 1)


        # #removes the key field
        # field_ids = new_sch.Definition.GetFieldOrder()
        # new_sch.Definition.RemoveField(field_ids[0])
        
        # #use_fields = ["1", "2" , "3", 4 ,5]
        # records = [[1], [2]]
        # eles = revit.query.get_all_elements_in_view(new_sch)
        
        # use_fields = []
        # for i in range(0, 1):
            # use_fields.append(eles[i].Name)
            # print(eles[i].Name)
        
        
        
        # for keysched_el, record_data in zip(revit.query.get_all_elements_in_view(new_sch), records):
            # for idx, field_name in enumerate(use_fields):
                # if record_data[idx]:
                    
                    # print(keysched_el.Name)
                    # # p = keysched_el.LookupParameter("1")
                    # # if p and not p.SetValueString(record_data[idx]):
                        # # if p.StorageType == DB.StorageType.Integer:
                            # # p.Set(int(record_data[idx]))
                        # # elif p.StorageType == DB.StorageType.Double:
                            # # p.Set(float(record_data[idx]))
                        # # elif p.StorageType == DB.StorageType.String:
                            # # p.Set(record_data[idx])
                        # # elif p.StorageType == DB.StorageType.ElementId:
                            # # p.Set(DB.ElementId(int(record_data[idx])))
                    # # p.Set(int(record_data[idx]))
                    # params = keysched_el.GetOrderedParameters()
                    # print(params)
                    
                    # print("----------")
                    # for param in params:
                        # string = param.AsString()
                        # print(string)
                        # if string == None:
                            # print('found')
                            # param.Set(100)
                            # print(param.AsString())
                    # print('----------')
                    
                    
                    
                    
    # t.Commit()
    
    
#import traceback
# try:
    # hu = fasdfasd
# except Exception, err:
    # pass

# print(traceback.format_exc())
    
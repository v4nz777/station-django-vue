from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,Border
from openpyxl.styles.borders import Side
from ..models import EquipmentGroup, Equipment

import station.models as station_module



def get_latest_inventory_workbook(filename:str):
    #open new from sample
    wb = load_workbook("technical/inventory/inventory.xlsx")
    sheet = wb["sheet"] #load sheet
    start = 12
    after_title = 1
    #columns
    col_name = "A"  #Name of Equipment
    col_brand = "B"  #Brand
    col_model = "C"  #Model
    col_sn = "D"  #Serial No.
    col_pn = "E"  #Property No.
    col_date_acquired = "F"  #Date Acquired
    col_puchase_cost = "G"  #Purchase Cost
    col_replacement_cost = "H"  #Replacement Cost
    col_ownership = "I"  #MBC or Partner Property
    col_status = "J"  #Status

    #styles
    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

    #fill station info
    station = station_module.Station.objects.first()
    sheet["B2"].value = station.station_name
    sheet["B3"].value = station.address
    sheet["B4"].value = station.call_sign
    sheet["B5"].value = station.frequency
    sheet["B6"].value = (
        str(station.station_manager.first_name).title() + ' ' + str(station.station_manager.last_name).title() 
        if station.station_manager != None else None
    )
    sheet["B7"].value = Equipment.objects.latest('modified').modified.strftime("%m/%d/%Y, %H:%M:%S")

    #get info from database
    groups = EquipmentGroup.objects.all()
    for i in groups:
        #group title
        sheet["A"+str(start)].value = i.group_name.title() + " Equipments"
        sheet["A"+str(start)].font = Font(bold=True)
        start += 2
        sheet[col_name + str(start)].value = "Name of Equipment"
        sheet[col_name + str(start)].font = Font(bold=True)
        sheet[col_name + str(start)].border = thin_border

        sheet[col_brand + str(start)].value = "Brand"
        sheet[col_brand + str(start)].font = Font(bold=True)
        sheet[col_brand + str(start)].border = thin_border

        sheet[col_model + str(start)].value = "Model"
        sheet[col_model + str(start)].font = Font(bold=True)
        sheet[col_model + str(start)].border = thin_border

        sheet[col_sn + str(start)].value = "Serial No."
        sheet[col_sn + str(start)].font = Font(bold=True)
        sheet[col_sn + str(start)].border = thin_border

        sheet[col_pn + str(start)].value = "Property No."
        sheet[col_pn + str(start)].font = Font(bold=True)
        sheet[col_pn + str(start)].border = thin_border

        sheet[col_date_acquired + str(start)].value = "Date Acquired"
        sheet[col_date_acquired + str(start)].font = Font(bold=True)
        sheet[col_date_acquired + str(start)].border = thin_border

        sheet[col_puchase_cost + str(start)].value = "Purchase Cost"
        sheet[col_puchase_cost + str(start)].font = Font(bold=True)
        sheet[col_puchase_cost + str(start)].border = thin_border

        sheet[col_replacement_cost + str(start)].value = "Replacement Cost"
        sheet[col_replacement_cost + str(start)].font = Font(bold=True)
        sheet[col_replacement_cost + str(start)].border = thin_border

        sheet[col_ownership + str(start)].value = "MBC or Partner"
        sheet[col_ownership + str(start)].font = Font(bold=True)
        sheet[col_ownership + str(start)].border = thin_border

        sheet[col_status + str(start)].value = "Status"
        sheet[col_status + str(start)].font = Font(bold=True)
        sheet[col_status + str(start)].border = thin_border

        start +=1
        for e in i.equipments.all():
            print(e)
            
            sheet[col_name + str(start)].value = e.name.title()
            sheet[col_name + str(start)].border = thin_border
            sheet[col_brand + str(start)].value = e.brand.brand_name.title()
            sheet[col_brand + str(start)].border = thin_border
            sheet[col_model + str(start)].value = e.model.title()
            sheet[col_model + str(start)].border = thin_border
            sheet[col_sn + str(start)].value = e.serial_no
            sheet[col_sn + str(start)].border = thin_border
            sheet[col_pn + str(start)].value = e.property_no
            sheet[col_pn + str(start)].border = thin_border
            sheet[col_date_acquired + str(start)].value = e.date_acquired.strftime("%m/%d/%Y") if e.date_acquired else ""
            sheet[col_date_acquired + str(start)].border = thin_border
            sheet[col_puchase_cost + str(start)].value = e.purchase_cost
            sheet[col_puchase_cost + str(start)].border = thin_border
            sheet[col_replacement_cost + str(start)].value = e.purchase_cost
            sheet[col_replacement_cost + str(start)].border = thin_border
            sheet[col_ownership + str(start)].value = e.owner.title() if len(e.owner) > 3 else e.owner.upper()
            sheet[col_ownership + str(start)].border = thin_border
            sheet[col_status + str(start)].value = e.status.title()
            sheet[col_status + str(start)].border = thin_border
            start+=1
        start+=2

    filepath = f"technical/inventory/generated/{filename}.xlsx"
    wb.save(filepath)

    return filepath



    #input to workbook

from openpyxl import Workbook, load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.fonts import Font
from openpyxl.worksheet.dimensions import ColumnDimension
from datetime import datetime
import os

from django.conf import settings
from django.core.files import File
from .models import User, Department, History, MonthlyDTR


def generate_workbook(username, start, end):
    user = User.objects.get(username=username)
    month = start.strftime("%B")
    year = start.strftime("%Y")

    date_start = start.strftime("%d").lstrip("0")
    date_end = end.strftime("%d").lstrip("0")

    records_range = History.objects.filter(user=user,time_in_datetime__range=[start,end])

    if not os.path.exists(f"dtr/output/{username}_{month}_{year}.xlsx"):
        #TODO CREATE WORKBOOK
        new = Workbook()
        new.save(f"dtr/output/{username}_{month}_{year}.xlsx")
    
    workbook = load_workbook("dtr/dtr.xlsx")
    dtrsheet = workbook["dtr"]
    for i in records_range:
        in_col = "C"
        out_col = "D"
        date_as_num = int(i.time_in_datetime.strftime("%d").lstrip("0")) + 16
        if i.time_in[len(i.time_in)-2:] == "PM":
            in_col = "E"
            out_col = "F"

        dtrsheet[f"{in_col}{date_as_num}"].value = i.time_in #IN
        dtrsheet[f"{out_col}{date_as_num}"].value = i.time_out #OUT
        dtrsheet[f"G{date_as_num}"].value = i.ot_in_hr #OT hour
        dtrsheet[f"H{date_as_num}"].value = i.ot_in_mn #OT minute
        dtrsheet[f"I{date_as_num}"].value = i.ot_in_hr #ND hour
        dtrsheet[f"J{date_as_num}"].value = i.ot_in_mn #ND minute

        dtrsheet["B8"].value = user.first_name.title() + " " + user.last_name.title() #Name
        dtrsheet["E11"].value = user.first_name.title() + " " + user.last_name.title() #Month

    workbook.save(f"dtr/output/{username}_{month}_{year}.xlsx")

    # add file to database
    file = MonthlyDTR()
    file.username = username
    file.range_start = start
    file.range_end = end

    with open(f"dtr/output/{username}_{month}_{year}.xlsx", "rb") as f:
        file.file.save(f"{username}_{month}_{year}.xlsx",File(f), save=True)
    file.save()
    return file

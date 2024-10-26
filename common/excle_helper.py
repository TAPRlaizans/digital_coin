import openpyxl
import os

class ExcleHelper(object):
    def save_excle(data_list, filename="data.xlsx", path='./'):
        path = os.path.join(path, filename)
        wb = openpyxl.Workbook()
        sheet = wb.active 
        for row in data_list:
            sheet.append(row)
        wb.save(f'{path}')
    
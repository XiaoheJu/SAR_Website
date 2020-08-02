from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from design.settings import BASE_DIR
from .views_pre import rcbd_pre
import os
import csv
import time
def op(drug_name,drug_num, os):
    drug_names = []
    if len(drug_name) == 1:
        for i in range(drug_num):
            drug_names.append((drug_name[0]) + str(chr(65 + i)))
    else:
        drug_names = [drug_name[i] for i in range(len(drug_name))]
        for i in range(drug_num - len(drug_name)):
            drug_names.append(os + str(chr(65 + i)))
    return drug_names
##默认表头
def build_head(block_num, drug_num,block_name,drug_name,):
    drug_names = op(drug_name, drug_num,'treat')
    block_names = op(block_name, block_num,'block')
    drug_names.insert(0,' ')
    return block_names, drug_names
#生成rcbd_data
def rcbd_data(request, *args):
    try:
        data = []
        rcd_design_result, block_name, drug_name, block_num, drug_num, title = rcbd_pre(request, *args)
        block, drug = build_head(block_num, drug_num, block_name, drug_name)
        data.append(drug)
        for i, j in enumerate(block):
            data_ = []
            data_.append(j)
            for k in range(drug_num):
                data_.append(str(rcd_design_result[i * drug_num + k]))
            data.append(data_)
    except Exception as e:

        print('ppppp',e)
        return -1, -1
    else:
        return data, title
#生成pdf_pre
def rcbd_pdf(data, title):
    row = len(data)
    col = len(data[0])
    width, height = A4
    colWidths = [(width - 2 * inch) / col for i in range(col)]
    rowWidths = [25 for i in range(row)]
    example = []
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    example_title = '<para autoLeading="off" fontSize=18 align=center><b><font>'+ str(title) + '</font></b><br/><br/><br/></para>'
    example.append(Paragraph(example_title, normalStyle))
    example_data = data
    example_table = Table(example_data, colWidths=colWidths, rowHeights=rowWidths)
    example_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('FONTSIZE', (0, 0), (0, -1), 8),
        ('FONTSIZE', (0, 0), (-1, 0), 8),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    example.append(example_table)
    space = Spacer(width, 9)
    example.append(space)
    auther = '<para autoLeading="off" fontSize=8 align=right><b><font>Copyright@SAR Design</font></b></para>'
    example.append(Paragraph(auther, normalStyle))
    path = os.path.join(BASE_DIR, 'file', str(int(time.time())) + '.pdf')
    pdf = SimpleDocTemplate(path)
    pdf.build(example)
    return path
#生成csv
def rcbd_csv_build(request):
    try:
        data = rcbd_data(request)
        path = os.path.join(BASE_DIR, 'file', str(int(time.time())) + '.csv')
        with open(path, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['random block design'])
            for i in data:
                spamwriter.writerow(i)
            spamwriter.writerow(['Copyright@SAR Design'])

    except:
        return -1
    else:
        return path
#生成pdf
def rcbd_pdf_build(request):
    try:
        data, title = rcbd_data(request)
        path = rcbd_pdf(data, title)
    except Exception as e :
        print(e)
        return -1
    else:
        return path





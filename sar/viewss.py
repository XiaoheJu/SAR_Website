from django.views.decorators.csrf import csrf_exempt
from design.settings import BASE_DIR
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
from .sar_design import cr_design
from .sar_design import rcb_design
import os
from .build_file import rcbd_pdf
import csv
import json
import xlrd
import matplotlib.pyplot as plot
from django.http import JsonResponse
import time

#主界面
def index(request):
    return render(request, "index.html")


#完全随机试验
def crd(request):
    return render(request, 'rbd.html')
@csrf_exempt
def crd_json(request):
    try:
        r, group = crd_pre(request)
    except:
        return JsonResponse({'Myerror': 1})
    else:
        try:
            treatments_result, treatment_levels, form = cr_design(r, group)
        except:
            return JsonResponse({'Myerror': 1})
        else:
            return JsonResponse(
                {'Myerror': 0,
                 'treatments_result': treatments_result,
                 'treatment_levels': treatment_levels,
                 'form': form,
                 }, content_type='application/json')







def crd_pre(request):
    if request.is_ajax():
        r=[]
        try:
            dic = list(request.POST.get('dict').split(','))
            flg = int(dic[0])
            group = int(dic[1])
        except:
            return -1
        else:
            if flg == 0:  # 判断每组数量是否相等
                r = [int(dic[2]) for i in range(group)]
            elif flg == 1:
                for i in range(group):
                    r.append(int(dic[i + 2]))
            return r, group


def rcbd_json(request):
    rcd_design_result = rcbd_pre(request)
    if rcd_design_result != -1:
        return JsonResponse(
            {'Myerror': 0,
             'rbd_design_result': rbd_design_result,
             }, content_type='application/json')
    else:
        return JsonResponse({'Myerror': 1})


def rcbd_pre(request):
    if clsaa_jud_ajax(request) == 'rcbd':
        if request.is_ajax():
            try:
                dic = list(request.GET.get('dict').split(','))
                block_num = int(dic[1])
                drug_num = int(dic[0])
            except:
                return -1
            else:
                try:
                    rcd_design_result = rcb_design(block_num, drug_num)
                except:
                    return -1
                else:
                    return rcd_design_result, block_num, drug_num
    else:
        return -1



def pdf_builds(request):
    if clsaa_jud_ajax(request) == 'rcdb':
        path = rcbd_pdf_build(request)
        if path != -1:
            return JsonResponse({'result': str(path[path.rfind('\\') + 1:])})
        else:
            return JsonResponse({'Myerror': 1})

def csv_build(request):
    if clsaa_jud_ajax(request) == 'rcdb':
        path = rcbd_pdf_build(request)
        if path != -1:
            return JsonResponse({'result': str(path[path.rfind('\\') + 1:])})
        else:
            return JsonResponse({'Myerror': 1})











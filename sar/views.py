from design.settings import BASE_DIR
from django.shortcuts import render
from django.http import FileResponse,Http404
from .sar_design import cr_design
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import os
import xlrd
import matplotlib.pyplot as plot
from django.http import JsonResponse
from .views_pre import class_jud_ajax
from .build_file import rcbd_pdf_build, rcbd_csv_build, rcbd_data
from .views_pre import rcbd_pre, name_transfor
from .models import RandomBlockCompletelyDesign
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from sardesign.sar import sar


# Create your views here.
#主界面
def index(request):
    context = {'user': request.user}
    return render(request, "new_index.html", context)
#完全随机试验
def crd(request):
    return render(request, 'ls.html')
def crd_ajax(request):
    if request.is_ajax():
        try:
            dic = list(request.GET.get('dict').split(','))
            flg = int(dic[0])
            group = int(dic[1])
            r = []
        except:
            return JsonResponse({'Myerror': 1})
        if flg == 0: #判断每组数量是否相等
            r = [int(dic[2]) for i in range(group)]
        elif flg == 1:
            for i in range(group):
                r.append(int(dic[i + 2]))
        try:
            treatments_result, treatment_levels, form = cr_design(r, group)
        except:
            return JsonResponse({'Myerror': 1})
        return JsonResponse(
            {'Myerror': 0,
             'treatments_result': treatments_result,
             'treatment_levels': treatment_levels,
             'form': form,
             }, content_type='application/json')
    else:
        raise Http404("It does not exist")
#上传文件
def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        filename = os.path.join(BASE_DIR, 'static', file_obj.name)
        name = str(file_obj.name[:file_obj.name.find('.')] + '.jpg')
        with open(filename, 'wb') as f:
            print(file_obj, type(file_obj))
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        ncols = table.ncols
        lis = []
        for i in range(ncols):
            lis.append(table.cell_value(0, i))
        plot.plot(lis)
        plot.savefig(os.path.join(BASE_DIR, 'sar','static','sar',str(name)))
        return JsonResponse({'name':name}, content_type='application/json')
def upload(request):
    return render(request, 'upload.html')
#随机区组试验
def rcbd(request):
    context = {'user': request.user}
    return render(request, 'rcbd.html',context)

def rcbd_ajax(request):
    rcd_design_result, _, _l, _, _, _= rcbd_pre(request, op=1)
    data, title = rcbd_data(request)
    rcd_design_result=[]
    for dat in data:
        rcd_design_result.extend(dat)
    if rcd_design_result != -1:
        return JsonResponse(
            {'Myerror': 0,
             'rbd_design_result': rcd_design_result,
             }, content_type='application/json')
    else:
        return JsonResponse({'Myerror': 1})
#下载文件
def download(request):

    return render(request, "download.html")
def download_result(request):
    try:
        if request.method == 'POST':
            file_name = request.POST.get('file_result')
            file_path = os.path.join(BASE_DIR, 'file', file_name)

            file = open(file_path, 'rb')
            response = FileResponse(file, )
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
            return response
    except:
        pass
#生成文件
def pdf_build(request):
    if class_jud_ajax(request) == 'rcbd':
        path = rcbd_pdf_build(request)
        if path != -1:
            return JsonResponse({'result': str(path[path.rfind('\\') + 1:])})
        else:
            return JsonResponse({'Myerror': 1})
def csv_build(request):
    if class_jud_ajax(request) == 'rcbd':
        path = rcbd_csv_build(request)
        if path != -1:
            return JsonResponse({'result': str(path[path.rfind('\\') + 1:])})
        else:
            return JsonResponse({'Myerror': 1})

def llogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('sar:index'))
    else:
        render(request,'美化.html')
def login_view(request):
    return render(request, "signin.html")
@login_required
def user_home(request):
    return render(request, 'user.html', {'username':request.user.get_username()})
@login_required
def history(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        try:
            historys = RandomBlockCompletelyDesign.objects.filter(build_user=username)
        except Exception as e:
            print(e)
            raise Http404("History does not exist")
        return render(request, 'user.html', {'historys': historys})
def llogout(request):
    logout(request)
    return redirect(reverse('sar:index'))
@login_required
def detail(request, history_id):
    history = RandomBlockCompletelyDesign.objects.get(pk=history_id)
    clas = name_transfor(history.class_name)
    return render(request, 'history.html', {'history': history, 'class':clas})
@login_required
def history_design(request, history_id, history_class):
    if history_class == 'rcbd':
        data, title = rcbd_data(request, history_id)
        rcd_design_result = []
        for dat in data:
            rcd_design_result.extend(dat)
        if rcd_design_result != -1:
            return JsonResponse(
                {'Myerror': 0,
                 'rbd_design_result': rcd_design_result,
                 'title':title,}, content_type='application/json')
        else:
            return JsonResponse({'Myerror': 1})
    else:
        return JsonResponse({'Myerror': 1})



def ccd(request):
    context = {'user': request.user}
    return render(request, 'ccd.html', context)


def ccd_design(request):

    controller = sar.controller
    ccd = {}
    ccd['data'] = request.POST.get('ccd')
    ccd['cookies'] = request.COOKIES.get('csrftoken')
    output = controller.get_output(ccd, sar.ccd_design_in_deal, sar.ccd_design_out_deal)

    return JsonResponse(
        {'Myerror': 0,
         'ccd_design_result': output,
         }, content_type='application/json')

def ccd_analyze(request):
    controller = sar.controller
    ccd = {}
    ccd['data'] = request.POST.get('ccd')
    ccd['cookies'] = request.COOKIES.get('csrftoken')
    output = controller.get_output(ccd, sar.ccd_analyze_in_deal, sar.ccd_analyze_out_deal)
    Myerror = 0
        # Myerror = 0
    #         # print(e)
    #         # Myerror = 1
    #         # output = {}
    return JsonResponse(
        {'Myerror': Myerror,
         'ccd_analyze': output,
         }, content_type='application/json')







from .sar_design import rcb_design
from .models import RandomBlockCompletelyDesign
#判断类型

def name_transfor(clas_):
    if clas_ == 'rcbd':
        return '随机区组试验'
def class_jud_ajax(request):
    if request.is_ajax():
        try:
            clas = request.POST.get('class')
        except:
            return -1
        else:
            return clas
#crd处理
''''
def crd_pre(requset):
    if class_jud_ajax(requset) == 'crd':
        try:
            dic = list(request.POST.get('dict').split(','))
            flg = int(dic[1])
            group = int(dic[2])
            r = []
        except:
            return -1
        if flg == 0:  # 判断每组数量是否相等
            r = [int(dic[2]) for i in range(group)]
        elif flg == 1:
            for i in range(group):
                r.append(int(dic[i + 3]))
        try:
            treatments_result, treatment_levels, form = cr_design(r, group)
        except:
            return JsonResponse({'Myerror': 1})

    else:
        return -1'''
#rcbd处理

def rcbd_pre(request, *args, **kwargs):
    if request.is_ajax():
        if class_jud_ajax(request) == 'rcbd':
            try:
                clas_ = request.POST.get('class')
                block_num = int(request.POST.get('block_num'))
                drug_num = int(request.POST.get('drug_num'))
                drug_name_ = request.POST.get('drug_name')
                block_name_ = request.POST.get('block_name')
                block_names = list(block_name_.split(','))
                drug_names = list(drug_name_.split(','))
                title = request.POST.get('title')
            except Exception as e:
                print(e)
                return -1
            else:
                try:
                    rcd_design_result = rcb_design(block_num, drug_num)
                except Exception as e:
                    print(e)
                    return -1
                else:
                    if request.user.is_authenticated and kwargs:
                        rcbd = RandomBlockCompletelyDesign()
                        rcbd.drug_name = drug_name_
                        rcbd.block_name = block_name_
                        rcbd.block = block_num
                        rcbd.drug = drug_num
                        rcbd.build_user = request.user.get_username()
                        rcbd.title = title
                        rcbd.class_name = clas_
                        rcbd.save()
                    return rcd_design_result, block_names, drug_names, block_num, drug_num, title
        else:
            return -1
    else:
        if request.user.is_authenticated:
            sql = RandomBlockCompletelyDesign.objects.get(pk=args[0])
            block_names = list(sql.block_name.split(','))
            drug_names = list(sql.drug_name.split(','))
            block_num = int(sql.block)
            drug_num = int(sql.drug)
            title = sql.title
            rcd_design_result = rcb_design(block_num, drug_num)

            return rcd_design_result, block_names, drug_names, block_num, drug_num, title
        else:
            return -1

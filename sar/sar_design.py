import rpy2.robjects as robjects

class ConditionError(Exception):
    pass

def treatment(groupnumber, x = '1'):

    if ((len(x)==1) or x.isalnum() or groupnumber.isdigit() or len(groupnumber)>0) == False:
        #判断是否为数字或者字母，当组别大于26时只能为数字。(待补充)
        return
    x = int(x)
    groupnumber = int(groupnumber)
    groups = []
    for i in range(groupnumber):

        group = "group" + str(x+i)
        groups.append(group)
    return tuple(groups)



def crd(treatment, Replications, serie = 0, seed = 2543):#完全随机试验设计
#    Replications = tuple(Replications.split(',')) #Replications为字符串，转为元组

    Replications = tuple(Replications)
    try:
        library = "library(agricolae)" + str(';')
        treatments = "treatment <-c" + str(treatment) + str(';')
        Replication = "Replications <-c" + str(Replications) + str(';')
        outdesign = "outdesign <-design.crd(trt = treatment,r = Replications,serie=0, seed = 2543)" + str(';')
        design = "design <-outdesign$book"

    except Exception:
        pass
    finally:
        rscript = library+treatments+Replication+outdesign+design
        return rscript

def cr_design(r0, group):

    trt = treatment(group, x='1')
    form = [int(max(r0)), len(r0)]
    rscript = crd(trt, r0)
    pymodels = robjects.r(rscript)
    plots = list(pymodels[0])
    plots = list(map(int, plots))
    r = list(pymodels[1])
    treatments_ = list(pymodels[2])
    treatment_levels = list(pymodels[2].levels)
    treatments_result =  [['' for i in range(int(max(r0)))] for i in range(len(r0))]
    treatments_resul = []
    for i in range(len(treatments_)):
        treatments_result[int(treatments_[i])-1][int(r[i])-1] = plots[i]

    for j in range(form[1]):
        for k in range(form[0]):
            treatments_resul.append(treatments_result[j][k])
    return treatments_resul, treatment_levels, form

def rcbd(block_num, drug_num):
    Treatment = []
    for i in range(drug_num):
        Treatment.append("drug"+str(chr(65+i)))
    trt = ' Treatment<-c' + str(tuple(Treatment)) + ';'
    library = "library(agricolae);"
    outdesign = 'outdesign <-design.rcbd(trt=Treatment,r=' + str(block_num) + ',serie=2,seed=123,"Super-Duper",randomization=TRUE);'
    book = 'book <-outdesign$book;'

    rscript = library + trt + outdesign + book
#    print(rscript)
    return rscript

def rcb_design(block_num, drug_num):
    result = []
    rscript = rcbd(block_num, drug_num)
    if rscript == 'Conditionerror':
        return 'Conditionerror'
    pymodels = robjects.r(rscript)
    Plot = list(pymodels[0])
    Treatment = list(pymodels[2])
    for i in range(block_num):
        for k in range(drug_num):
            for j in range(drug_num):
                if str(k+1) == str(int(Treatment[i*drug_num + j])):
                    result.append(int(Plot[i*drug_num + j]))
    return result


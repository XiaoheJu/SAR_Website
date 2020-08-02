from django.urls import path
from . import views

app_name = 'sar'

urlpatterns = [
    path('', views.index, name='index'), #访问主界面
    path('crd', views.crd, name='crd'), #完全随机试验主界面
    path('crd_ajax', views.crd_ajax, name='crd_json'), #完全随机试验方案的设计
    path('upload', views.upload,name='upload'), #上传文件主界面
    path('upload_ajax', views.upload_ajax, name='upload_ajax'), #上传文件
    path('rcbd_ajax', views.rcbd_ajax, name='rcbd_json'), #随机区组试验主界面
    path('rcbd', views.rcbd, name='rcbd'), #随机区组试验方案设计
    path('download_result', views.download_result, name='download_result'), #下载界面
    path('pdf_build', views.pdf_build, name = 'pdf_build'), #生成PDF文件
    path('csv_build', views.csv_build, name = 'csv_build'), #生成csv文件
    path('login_view', views.login_view, name='login_view'),
    path('llogin', views.llogin,name='llogin'),
    path('user_home', views.user_home, name='user_home'),
    path('history', views.history, name='history'),
    path('llogout', views.llogout, name='llogout'),
    path('ccd/', views.ccd, name='ccd'),
    path('ccd_design', views.ccd_design, name='ccd_design'),
    path('ccd_analyze', views.ccd_analyze, name='ccd_analyze'),
    path('<int:history_id>/', views.detail, name='detail'),
    path('history/<int:history_id>/<str:history_class>', views.history_design, name='history_design'),

]

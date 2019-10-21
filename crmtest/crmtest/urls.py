"""crmtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import  views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^yi/',views.yi),
    # url(r'^er/',views.er),
    #注册
    url(r'^register/', views.register,name='register'),


    #登录
    url(r'^login/', views.login, name='login'),

    #验证码
    url(r'^get_valid_img/', views.get_valid_img, name='get_valid_img'),

    #index页面
    url(r'^index/', views.index, name='index'),

    #customer用户信息展示页面
    url(r'^customer/', views.CustomerView.as_view(), name='customer'),

    #我的私有客户
    # url(r'^mycustomers/', views.mycustomers, name='mycustomers'),
    url(r'^mycustomers/', views.CustomerView.as_view(), name='mycustomers'),

    #添加用户信息页面
    url(r'^addcustomerinfo/', views.addcustomerinfo, name='addcustomerinfo'),

    #修改用户信息页面
    url(r'^updatacustomerinfo/(\d+)/', views.Updatacustomerinfo.as_view(), name='updatacustomerinfo'),

    #删除用户信息页面
    url(r'^deletacustomerinfo/(\d+)/', views.Deletacustomerinfo.as_view(), name='deletacustomerinfo'),

    #搜索栏
    # url(r'^test/', views.test, name='test'),



    # 跟进记录表
    url(r'^gj/', views.Gj.as_view(), name='gj'),

    #单独展示每个顾客的跟进记录
    url(r'^gj-one/(\d+)', views.Gj.as_view(), name='gj-one'),


    #添加跟进记录
    url(r'^add_gj/', views.Update_gj.as_view(), name='add_gj'),

    #修改跟进记录
    url(r'^update_gj/(\d+)/', views.Update_gj.as_view(), name='update_gj'),

    #删除跟进记录
    url(r'^delete_gj/(\d+)/', views.Delete_gj.as_view(), name='delete_gj'),



    #查看角色列表
    url(r'^rolelist/', views.Rolelist.as_view(), name='rolelist'),

    #添加修改角色列表
    url(r'^roleadd/', views.Roleadd.as_view(), name='roleadd'),
    url(r'^roleupdate/(\d+)/', views.Roleadd.as_view(), name='roleupdate'),

    #删除角色列表
    url(r'^roledelete/(\d+)/', views.Roledelete.as_view(), name='roledelete'),


    #班级课程记录表
    url(r'^classstudyrecord/', views.ClassStudyRecord.as_view(), name='classstudyrecord'),
    #学生学习记录表
    url(r'^studyrecord/(\d+)', views.StudyRecordView.as_view(), name='study_decord'),



    #用户角色权限分配修改表
    # url(r'^u_r_p/', views.U_R_P.as_view(), name='u_r_p'),
    url(r'^distribute_permissions2/', views.distribute_permissions2, name='distribute_permissions2'),
    url(r'^get_permissions/', views.get_permissions, name='get_permissions'),

]

import os

from app01 import page  # 导入分页page文件
from app01 import models
from app01 import crmform

from django.views import View
from django.urls import reverse
from  django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect


#权限管理
class Rolelist(View):
    def get(self, request):
        role_obj = models.Role.objects.all()

        return render(request, 'role/rolelist.html', {'role_obj': role_obj})


class Roleadd(View):
    def get(self, request, pk=None):
        obj = models.Role.objects.filter(pk=pk).first()
        role_obj = crmform.Rolelist(instance=obj)
        return render(request, 'role/roleadd.html', {'role_obj': role_obj})

    def post(self, request, pk=None):
        obj = models.Role.objects.filter(pk=pk).first()
        role_obj = crmform.Rolelist(request.POST, instance=obj)
        if role_obj.is_valid():
            role_obj.save()
            return redirect('rolelist')
        else:
            return render(request, 'role/roleadd.html', {'role_obj': role_obj})

class Roledelete(View):
    def get(self, request, pk=None):
        models.Role.objects.filter(pk=pk).delete()
        return redirect('rolelist')

# 注册页面
def register(request):
    if request.method == 'GET':
        form_obj = crmform.UserForm()
        return render(request, 'register.html', {'register': form_obj})

    else:
        form_obj = crmform.UserForm(request.POST)
        print(form_obj)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            data.pop('r_password')
            models.UserInfo.objects.create_user(**data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'register': form_obj})


# 登录页面以及需要导入的内容
from django.contrib import auth

def login(request):
    response_msg = {'code': None, 'msg': None}
    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')

        # 1.验证验证码是否正确
        if valid_code.upper() == request.session.get('valid_str').upper():
            # 2.验证用户是否存在
            user_obj = auth.authenticate(username=username, password=password)
            # 用户名密码正确
            if user_obj:
                auth.login(request, user_obj)
                response_msg['code'] = 1000
                response_msg['msg'] = '登录成功!'
                # permission_input(request,username)
            else:
                response_msg['code'] = 1002
                response_msg['msg'] = '用户名或者密码输入有误!'

        else:
            response_msg['code'] = 1001
            response_msg['msg'] = '验证码输入有误!'

        return JsonResponse(response_msg)


# index页面
def index(request):
    return render(request, 'index.html')


# 查询公共和私有用户信息
class CustomerView(View):
    def get(self, request):
        wd = request.GET.get('wd', '')
        condition = request.GET.get('condition', '')
        # 这是过滤公户的,也就是没有销售的
        print(request.path)
        if request.path == reverse('customer'):  # 判断搜索路径是来自公有还是私有
            flag = 0
            all_customers = models.Customer.objects.filter(consultant__isnull=True)
        else:  # 判断搜索路径是来自公有还是私有
            flag = 1
            all_customers = models.Customer.objects.filter(consultant=request.user)
        if wd:
            q = Q()
            # q.connector = 'or'
            # q.children.append((condition,wd))
            q.children.append((condition, wd))
            # 根据用户查询条件再次进行筛选
            all_customers = all_customers.filter(q)
        current_page_num = request.GET.get('page', 1)

        per_page_numbers = 10
        page_ma_numbers = 5
        print(flag)
        data_numbers = all_customers.count()
        print(data_numbers)
        html_1, start_num, end_num = page.pagenation(request.path, current_page_num, data_numbers, request,
                                                     page_ma_numbers,
                                                     per_page_numbers)

        all_customers = all_customers.order_by('-pk')[start_num:end_num]

        # ret_html = page_obj.page_html()

        return render(request, 'customer/customers.html',
                      {'all_customers': all_customers, 'html_1': html_1, 'flag': flag})

    def post(self, request):
        print(request.POST)
        self.data = request.POST.getlist('selected_id')
        print(self.data)
        action = request.POST.get('action')  # 'batch_delete'
        print(action)
        if hasattr(self, action):
            func = getattr(self, action)
            if callable(func):
                ret = func(request)
                if ret:
                    return ret
                return redirect(request.path)
            else:
                return HttpResponse('不要搞事!!')
        else:
            return HttpResponse('不要搞事!!')

    # 批量删除
    def batch_delete(self, request):
        models.Customer.objects.filter(pk__in=self.data).delete()

    # 批量更新
    def batch_update(self, request):
        # consultant_obj=models.UserInfo.objects.filter(username='景儿').values('id')
        # print(consultant_obj)
        # models.Customer.objects.filter(pk__in=self.data).update(consultant=str(consultant_obj))
        models.Customer.objects.filter(pk__in=self.data).update(name='小奔')

    # 批量公户转私户
    def batch_reverse_gs(self, request):
        batch_gs_customers = models.Customer.objects.filter(pk__in=self.data)

        # 因为可能存在多个用户同时操作公户转私户的操作,所以进行以下操作
        l = []
        for i in batch_gs_customers:
            if i.consultant:  # 查看调取的用户是否已经被别的用户拿走
                print(i.consultant)
                l.append(i)

            else:
                i.consultant = request.user  # 如果没有被拿走,则加入该用户信息表
                i.save()  # 记住modelform信息表必须用save保存
        if l:
            ret_str = ','.join([(i.qq + ':' + i.name) for i in l])
            return HttpResponse(ret_str)

        batch_gs_customers.update(consultant=request.user)

    # 批量私户转公户
    def batch_reverse_sg(self, request):
        models.Customer.objects.filter(pk__in=self.data).update(consultant=None)


class Gj(View):
    def get(self, request, pk=None):
        wd = request.GET.get('wd', '')
        condition = request.GET.get('condition', '')
        print(request.path)
        print(pk)
        gj_obj = models.ConsultRecord.objects.filter(consultant=request.user)

        if pk:
            gj_obj = gj_obj.filter(customer_id=pk)

        if wd:
            q = Q()
            q.children.append((condition, wd))
            gj_obj = gj_obj.filter(q)

        now_page = request.GET.get('page', 1)

        page_ma_numbers = 5
        per_page_numbers = 10
        data_numbers = gj_obj.count()

        html_1, start_num, end_num = page.pagenation(request.path, now_page, data_numbers, request, page_ma_numbers,
                                                     per_page_numbers)

        gj_obj = gj_obj.order_by('-pk')[start_num:end_num]

        return render(request, 'gj/gj.html', {'gj_objs': gj_obj})

    def post(self, request):
        self.data = request.POST.getlist('selected_id')
        action = request.POST.get('action')
        if hasattr(self, action):
            func = getattr(self, action)
            if func:
                ret = func(request)
                if ret:
                    return ret
                return redirect(request.path)
            else:
                return HttpResponse('搜素内容不存在')
        else:
            return HttpResponse('搜素条件不正确')

    # 批量删除
    def batch_delete(self, request):
        models.ConsultRecord.objects.filter(pk__in=self.data).delete()

    # 批量更新
    def batch_update(self, request):
        models.ConsultRecord.objects.filter(pk__in=self.data).update(note='景导牛x')


# 添加修改跟进记录
class Update_gj(View):
    def get(self, request, pk=None):
        form_obj = models.ConsultRecord.objects.filter(pk=pk).first()
        form_obj = crmform.GjConsultRecord(request, instance=form_obj)
        return render(request, 'gj/add_gj.html', {'form_obj': form_obj})

    def post(self, request, pk=None):
        form_obj = models.ConsultRecord.objects.filter(pk=pk).first()
        form_obj = crmform.GjConsultRecord(request, request.POST, instance=form_obj)

        # 在这块加上instance,modelform才会对响应的信息进行修改,不然会直接创建一条新的用户信息
        if form_obj.is_valid():
            print(form_obj)
            form_obj.save()

            return redirect('gj', 1)

        else:

            return render(request, 'gj/add_gj.html', {'form_obj': form_obj})


# 删除跟进记录
class Delete_gj(View):
    def get(self, request, pk):
        models.ConsultRecord.objects.filter(pk=pk).delete()
        return redirect('gj')


##添加用户信息
def addcustomerinfo(request):
    if request.method == 'GET':
        customer_add_obj = crmform.Addmodelform()
        return render(request, 'customer/addcustomerinfo.html', {'customer_add_obj': customer_add_obj})

    else:
        customer_add_obj = crmform.Addmodelform(request.POST)
        if customer_add_obj.is_valid():
            customer_add_obj.save()
            return redirect('customer')

        else:
            return render(request, 'customer/addcustomerinfo.html', {'customer_add_obj': customer_add_obj})


# 修改客户信息
class Updatacustomerinfo(View):
    def get(self, request, pk):
        customer_obj = models.Customer.objects.filter(pk=pk).first()
        customer_obj = crmform.Addmodelform(instance=customer_obj)
        return render(request, 'customer/addcustomerinfo.html', {'customer_add_obj': customer_obj})

    def post(self, request, pk):
        customer_obj = models.Customer.objects.filter(pk=pk).first()

        customer_add_obj = crmform.Addmodelform(request.POST, instance=customer_obj)
        # 在这块加上instance,modelform才会对响应的信息进行修改,不然会直接创建一条新的用户信息
        if customer_add_obj.is_valid():
            customer_add_obj.save()

            if customer_obj.consultant:
                return redirect('mycustomers')
            else:
                return redirect('customer')

        else:
            return render(self.request, 'customer/addcustomerinfo.html', {'customer_add_obj': customer_add_obj})


# 删除客户信息
class Deletacustomerinfo(View):
    def get(self, request, pk):
        customer_obj = models.Customer.objects.filter(pk=pk).first().consultant
        models.Customer.objects.filter(pk=pk).delete()
        if customer_obj:
            return redirect('mycustomers')
        else:
            return redirect('customer')





# 自定义方法展示HTML页面
class ClassStudyRecord(View):
    def get(self, request):
        '''
        获取班级课程记录表的信息并将其呈现在网页上
        :param request:
        :return:
        '''
        classstudy_obj = models.ClassStudyRecord.objects.all()
        print(classstudy_obj)
        return render(request, 'jilu/classstudyrecord.html', {'classstudy_obj': classstudy_obj})

    def post(self, request):
        '''
        从网页上获取用户进行的操作action
        :param request:
        :return:
        '''
        action = request.POST.get('action')
        selected_id = request.POST.get('selected_id')
        if hasattr(self, action):
            print(1)
            getattr(self, action)(selected_id)
        print(self.get(request))
        return self.get(request)

    def batch_delete(self, selected_id):
        '''
        用户在班级课程页面上进行的操作的后台执行流程
        :param selected_id: 代表被选中的班级课程内容
        :return:
        '''
        for em in selected_id:
            all_students = models.ClassStudyRecord.objects.filter(pk=em).first().class_obj.students.all()
            # 通过跨表查询,查询出该班级课程对应的所有学生,正向查询字段名,反向查询小写表名或related_name从定的名字
            l = []
            for student in all_students:
                obj = models.StudentStudyRecord(
                    student=student,
                    classstudyrecord_id=em
                )
                l.append(obj)
            models.StudentStudyRecord.objects.bulk_create(l)


class StudyRecord(View):
    def get(self, request, pk=None):
        score_choices = models.StudentStudyRecord.score_choices
        study_obj = models.StudentStudyRecord.objects.filter(classstudyrecord_id=pk)
        print(study_obj)
        return render(request, 'jilu/studyrecord.html', {'study_obj': study_obj, 'score_choices': score_choices})

    def post(self, request, pk=None):
        data = request.POST
        print(data)
        # < QueryDict: {'csrfmiddlewaretoken': ['YIxgtvivom1ezgtzgMfn01vv7Brz5OONrxFW7GolygyCSh7Q2YwecQWqN1l7jIrX'],
        # 'socre': ['80', '100'], 'homework': ['', ''], '保存': ['提交']} >

        data_dict = {}
        for key, val in data.items():
            print(key, val)
            if key == 'csrfmiddlewaretoken':
                continue

            field, pki = key.rsplit('_', 1)
            if pki in data_dict:
                data_dict[pki][field] = val
            else:
                data_dict[pki] = {
                    field: val
                }

        print(data_dict)

        for i, j in data_dict.items():
            models.StudentStudyRecord.objects.filter(pk=i).update(**j)
        print(pk)
        # return redirect(reverse('studyrecord',args=(pk,)))
        return self.get(request, pk)

        # 分页搜索信息


# 通过formset自动展示HTML页面

from django.forms.models import modelformset_factory


class StudyRecordView(View):
    def get(self, request, pk=None):
        class_obj = models.ClassStudyRecord.objects.filter(pk=pk).first()
        study_obj = models.StudentStudyRecord.objects.filter(classstudyrecord=class_obj)
        form_fa_obj = modelformset_factory(model=models.StudentStudyRecord, form=crmform.StudyRecordModelForm, extra=0)
        # model指向要展示的表,form指向modelform生成的标签,extro表示不用添加示范示例
        formset = form_fa_obj(queryset=study_obj)
        # 放入获取的所有学生学习记录

        return render(request, 'jilu/studyrecord.html', {'formset': formset})

    def post(self, request, pk=None):
        # print(request.POST)
        # form_update_obj=modelformset_factory(model=models.StudentStudyRecord,form=crmform.StudyRecordModelForm,extra=0)
        # print(form_update_obj)
        #
        # update_obj = form_update_obj(request.POST)
        # print(update_obj)
        # if update_obj.is_valid():
        #     update_obj.save()
        # else:
        #     print(update_obj.errors)
        #
        # return redirect(reverse('jilu/tudyrecord.html',args=(pk,)))

        print(request.POST)
        form_fa_obj = modelformset_factory(model=models.StudentStudyRecord, form=crmform.StudyRecordModelForm, extra=0)
        print(form_fa_obj)
        formset = form_fa_obj(request.POST)
        print(formset)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)

        return redirect(reverse('study_decord', args=(pk,)))


# 验证码相关的代码
def get_valid_img(request):
    import random
    from crmtest import settings
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    from PIL import Image, ImageDraw, ImageFont
    img_obj = Image.new('RGB', (200, 34), get_random_color())
    draw_obj = ImageDraw.Draw(img_obj)
    font_path = os.path.join(settings.BASE_DIR, 'statics/font/NAUERT__.TTF')
    font_obj = ImageFont.truetype(font_path, 16)
    sum_str = ''
    for i in range(6):
        a = random.choice(
            [str(random.randint(0, 9)), chr(random.randint(97, 122)), chr(random.randint(65, 90))])  # 4  a  5  D  6  S
        sum_str += a
    print(sum_str)
    draw_obj.text((64, 10), sum_str, fill=get_random_color(), font=font_obj)

    width = 200
    height = 34
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # # 添加噪点
    for i in range(10):
        # 这是添加点，50个点
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        # 下面是添加很小的弧线，看上去类似于一个点，50个小弧线
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    from io import BytesIO
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()

    # 验证码对应的数据保存到session里面
    request.session['valid_str'] = sum_str

    return HttpResponse(data)


def distribute_permissions2(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    user=models.UserInfo.objects.filter(id=uid)
    rid = request.GET.get('rid')

    print()
    if request.method=="POST" and request.POST.get('postType')== 'role':
        print(request.POST.getlist("roles"))
        l=request.POST.getlist("roles")  #[2,3]
        user.first().roles.set(l)

    if request.method=="POST" and request.POST.get('postType')== 'permission':
        print(request.POST.getlist("permission_id"))  #permission_id:[1,2,3,4]
        l=request.POST.getlist("permission_id")  #[2,3]
        models.Role.objects.filter(pk=rid).first().permissions.set(l)

    # 所有用户
    user_objs = models.UserInfo.objects.all()

    # user_has_roles = user.values('id', 'roles')
    #获取所有角色
    role_objs = models.Role.objects.all()


    if uid:
        role_id_list=models.UserInfo.objects.get(pk=uid).roles.all().values_list("pk")
        #[(1,),(2,)]
        role_id_list=[item[0] for item in role_id_list] #[1,2]

        if rid:
            per_id_list = models.Role.objects.filter(pk=rid).values_list("permissions__pk")
            print(1)
            print(per_id_list)
        else:
            per_id_list=models.UserInfo.objects.get(pk=uid).roles.values_list("permissions__pk").distinct()
            print(2)
            print(per_id_list)

        per_id_list=[item[0] for item in per_id_list]
        print("per_id_list",per_id_list)

    return render(request, 'u_r_p.html',locals())




from django.http import JsonResponse
def get_permissions(request):
    '''
    获取第三张权限表所需的内容
    :param request:
    :return:
    '''

    permissions=models.Permission.objects.values('pk','title','url','menus_id','menus__pk','menus__title')


    return JsonResponse(list(permissions),safe=False)
    #JsonResponse不用手动去dumps转换数据,可以直接return返回原数据.
    #list直接将字典数据强转成列表传送,所以后面要设置safe=false

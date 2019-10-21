import re
from django import  forms
from app01 import models
from django.forms import widgets
from django.core.exceptions import ValidationError  #引入django所有错误报错类


#通过formset自动展示HTML页面
class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model=models.StudentStudyRecord
        fields=['score']



class Rolelist(forms.ModelForm):
    '''
    通过modelform生成表单
    '''
    class Meta:
        model=models.Role
        fields='__all__'

    def __init__(self, *args, **kwargs):  # 批量操作
        super().__init__(*args, **kwargs)
        from multiselectfield.forms.fields import MultiSelectFormField
        for field in self.fields.values():   #self.fields.values()查看modelform生成的标签的对象的值
            if not isinstance(field,MultiSelectFormField):    #isinstance判断括号内的第一个参数是不是第二个参数的类型
                field.widget.attrs.update({'class': 'form-control'},)




class Addmodelform(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'

        error_messages={
            'qq': {'required': '不能为空', },
            'name': {'required': '不能为空', },
            'sex': {'required': '不能为空', },
        }


    def __init__(self, *args, **kwargs):  # 批量操作
        super().__init__(*args, **kwargs)
        from multiselectfield.forms.fields import MultiSelectFormField
        for field in self.fields.values():   #self.fields.values()查看modelform生成的标签的对象的值
            if not isinstance(field,MultiSelectFormField):    #isinstance判断括号内的第一个参数是不是第二个参数的类型
                field.widget.attrs.update({'class': 'form-control'},)


class GjConsultRecord(forms.ModelForm):
    class Meta:
        model=models.ConsultRecord
        fields='__all__'


    def __init__(self,request, *args, **kwargs):  # 批量操作
        super().__init__(*args, **kwargs)
        self.fields['consultant'].queryset=models.UserInfo.objects.filter(pk=request.user.pk)
        self.fields['customer'].queryset=models.Customer.objects.filter(consultant=request.user)
        for key,field in self.fields.items():

                field.widget.attrs.update({'class': 'form-control'},)




class  UserForm(forms.Form):
    username=forms.CharField(
        max_length=10,
        min_length=2,
        help_text='用户名长度大于2,小于10呦',
        label='用户名',
        error_messages={'required':'不能为空'},
        widget=forms.widgets.TextInput(attrs={'class':'form-control'})
    )
    password=forms.CharField(
        max_length=10,
        min_length=2,
        label='密码',
        required=False,                    #允许可以为空
        error_messages={'required': '不能为空'},
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    r_password=forms.CharField(
        max_length=10,
        min_length=2,
        label='确认密码',
        required=False,
        error_messages={'required': '不能为空'},
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})

    )
    email=forms.EmailField(
        max_length=32,
        label='邮箱',
        error_messages={'required': '不能为空','invalid':'邮箱格式有误'},
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})

    )


    #这三个都是局部钩子
    def clean_username(self):
        username=self.cleaned_data.get('username')
        print('mingzi')
        user_obj=models.UserInfo.objects.filter(username=username).first()
        if user_obj:
            raise ValidationError('该用户已存在')
        else:
            return username

    def clean_password(self):
        password=self.cleaned_data.get('password')
        print(password)
        if password.isdecimal():
            raise ValidationError('密码不能为纯数字')
        else:
            return password

    def clean_email(self):
        email=self.cleaned_data.get('email')
        print('r_m')
        if re.search('\w+@qq.com$',email):      #正则里的w表示数字字母下划线
            return  email

        else:
            raise ValidationError('邮箱必须是QQ邮箱')


    def clean(self):
        p1=self.cleaned_data.get('password')
        p2=self.cleaned_data.get('r_password')
        print(p1,type(p1))
        print(p2,type(p2))
        if  p1==p2:
            print('dui')
            return  self.cleaned_data
        else:
            print('cuo')
            self.add_error('r_password','两次密码不一致')  #给r_password的错误信息添加信息

    # def __init__(self, *args, **kwargs):           #批量添加样式
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class':'form-control'
    #         })
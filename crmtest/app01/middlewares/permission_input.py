# from  app01 import models
#
# def permission_input(request,username):
#     request.session['username']=username
#     permissions = models.Permission.objects.filter(role__userinfo__username=username).\
#         values('pk','title','url','menus_id','pid','menus__title',)
#
#     permissions_list=[]
#     menu_dict={}
#
#     for i  in  permissions:


from django.utils.deprecation import MiddlewareMixin
class Middle(MiddlewareMixin):
    def process_response(self, _, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"
        return response
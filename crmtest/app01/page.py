#自定义分页

from app01 import models

def pagenation(url,now_page,data_numbers,request,page_ma_numbers=5,per_page_numbers=10):
    '''
    data_numbers  数据总数
    per_page_numbers  每页分多少条数据
    now_page       当前页
    page_ma_numbers  页码的显示个数
    :return:
    '''

    #因为用能存在用户误操作问题,所以要进行异常处理
    try:
        now_page = int(now_page)

    except Exception:
        now_page = 1


    #将传过来的参数进行处理
    now_page = int(now_page)
    page_ma_numbers = int(page_ma_numbers)
    per_page_numbers = int(per_page_numbers)






    # all_objs_list = models.Customer.objects.all()
    # data_numbers = all_objs_list.count()  # 计算数据总个数
    # print(data_numbers)
    print(data_numbers)
    page_number_count,yu=divmod(data_numbers,per_page_numbers)
    print(page_number_count)
                                    #通过divmod方法,计算出总页数,以及余数,若有余数则总页数再加一!!.

    if yu:
        page_number_count += 1



    #对获取的当前页(now_page)数据进行分析处理
    if now_page < 1:
        now_page=1                              #如果它小于1或者大于总页数的情况

    if now_page >  page_number_count :     #注意,在这块有坑,如果查询不到数据,这块的页面总数就为0了,会导致当前页变成0
        now_page = page_number_count






    half_page_ma_numbers=page_ma_numbers // 2     #页码显示一个的一半,取整

    #判断总页数(page_number_count)是否大于页码的显示个数(page_ma_numbers)

    if page_number_count >= page_ma_numbers:
        if  half_page_ma_numbers < now_page <= page_number_count-half_page_ma_numbers:
                                #当前页码处于half_page_ma_numbers和总数减half_page_ma_numbers之间
            start_page=now_page - half_page_ma_numbers
            end_page = now_page + half_page_ma_numbers

        elif    now_page <=half_page_ma_numbers:
            start_page = 1
            end_page = page_ma_numbers

        else:
            start_page = page_number_count - page_ma_numbers +1
            end_page = page_number_count

    else:
        start_page = 1
        end_page = page_number_count



    if  now_page==0:
        now_page=1
    start_num = (now_page - 1) * 10
    end_num = now_page * 10



    import copy
    params = copy.deepcopy(request.GET)  # 因为request.GET的内容不能进行修改,
    # 只有通过深copy,才能进行修改

    #页面分页栏的标签拼接,
    html_1 = ''
    html_1 += '<nav aria-label="Page navigation"><ul class="pagination">'

    # 字节跳转第一页
    params['page']=1
    html_1 += '<li> <a href = "{0}?{1}"> 首页 </a> </li>'.format(url,params.urlencode())

    #上一页标签

    if now_page == 1:
        html_2='<li> <a href = "{0}?{1}" aria-label="Previous">' \
               '<span aria-hidden="true">&laquo;</span> </a> </li>'.format(url,params.urlencode())


    else:
        params['page'] = now_page-1
        html_2 = '<li> <a href = "{0}?{1}" aria-label = "Previous" >' \
                 '<span aria-hidden = "true" >&laquo;</span> </a> </li>'.format(url,params.urlencode())
    html_1 += html_2


    #中间页码
    for i in range(start_page,end_page+1):
        if now_page==i:
            params['page'] = i
            one_ma='<li class="active"> <a href = "{0}?{1}">{2}</a> </li>'.format(url,params.urlencode(),i)
        else:
            params['page'] = i
            one_ma = '<li> <a href = "{0}?{1}"> {2} </a> </li>'.format(url, params.urlencode(),i)
        html_1 += one_ma

    # 下一页标签
    if now_page == page_number_count:
        params['page'] = page_number_count
        html_2 = '<li> <a href = "{0}?{1}" aria-label = "Next" >' \
                 '<span aria-hidden = "true" >&raquo;</span></a></li>'.format(url,params.urlencode())


    else:
        params['page'] = now_page + 1
        html_2 = '<li><a href = "{0}?{1}" aria-label = "Next" >' \
                 '<span aria-hidden = "true">&raquo;</span></a></li>'.format(url, params.urlencode())
    html_1 += html_2

    # 直接跳转最后一页
    params['page'] = page_number_count
    html_1 += '<li> <a href = "{0}?{1}"> 尾页 </a> </li>'.format(url, params.urlencode())

    html_1 += '</ul></nav>'





    return  html_1,start_num,end_num


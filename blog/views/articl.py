
import re

from blog.models import  Blog

from blog.views import returnJson

from django.forms.models import model_to_dict

import json

def get_list(requset):
    dr = re.compile(r'<[^>]+>', re.S)
    articl = Blog.objects.all().order_by('id').values()
    list = []
    for item in articl:
        items = item
        items['reContent'] = dr.sub('', item.get('content'))
        list.append(items)
    return returnJson.json_responre(list)

def get_list_date(request):
    dr = re.compile(r'<[^>]+>', re.S)
    articl = Blog.objects.all().order_by('-creatdate').values()
    dic = dict()
    data = []
    for item in articl:
        item['reContent'] = dr.sub('', item.get('content'))
        date = item['creatdate']
        dateKey = date.strftime("%Y-%m")
        itemData = dic.get(dateKey) if(dic.get(dateKey)) else [] ;
        itemData.append(item)
        dic[dateKey] = itemData
    for key in dic.keys():
        obj = {'date':key,'data':dic.get(key)}
        data.append(obj)
    return  returnJson.json_responre(data)

def get_detail(request):
    fid = json.loads(request.body).get('id')
    try:
        list = Blog.objects.get(id=fid)
        data = model_to_dict(list)
        return returnJson.json_responre(data)
    except:
        return  returnJson.json_error()


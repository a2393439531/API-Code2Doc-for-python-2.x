#-*- coding=utf-8 -*-
#!/usr/bin/env python
import os
import sys
import codecs
import requests
import json
import re
import config
import time
import importlib
importlib.reload(sys)
def getContent(file_path, file_suffix, exclude_file):
    files = os.listdir(file_path)
    data = []
    for file in files:
        if os.path.splitext(
                file)[1] == '.' + file_suffix and os.path.split(
                    file)[-1] not in exclude_file:
            #获取文件文件名
            file_name = os.path.join('%s\%s' % (file_path, file))
            if os.path.isfile(file_name):
                #读取文件
                fopen = codecs.open(file_name, 'r', 'utf-8')
                file_contents = fopen.readlines()
                file_content = ''
                for line in file_contents:
                    file_content += line.strip("\n")
                if file_content:
                    file_content = file_content.replace("\r\n", "")
                    file_content = file_content.replace("\r\t", "")
                    #获取全部注释
                    file_content = file_content.replace(' ', '')
                    if file_suffix == 'php' or file_suffix == 'java':
                        data.append(re.findall("\/\*.*?\*\/", file_content))
                    if file_suffix == 'py':
                        result = re.findall(r'""".*?"""', file_content)
                        if not result:
                           result = re.findall(r"'''.*?'''", file_content)
                        data.append(result)
    fopen.close()
    return data


def getdata(data, file_suffix):
    #接口的状态
    apiStatus = {'work': 0, 'maintain': 1, 'abandoned': 2}
    #请求方式数组
    request_type = {
        'post': '0',
        'get': '1',
        'put': '2',
        'delete': '3',
        'head': '4',
        'options': '5',
        'patch': '6'
    }
    #请求协议数组
    protocol = {'http': 0, 'https': 1}
    #请求参数类型数组
    paramType = {
        'string': '0',
        'file': '1',
        'json': '2',
        'int': '3',
        'float': '4',
        'double': '5',
        'date': '6',
        'datetime': '7',
        'boolean': '8',
        'byte': '9',
        'short': '10',
        'long': '11',
        'array': '12',
		'object':'13'
    }
    data_json = {}
    data_json['apiGroupList'] = []
    childGroup = []
    data_json['apiGroupList'].append({'groupName':'默认分组','apiList':[]})
    for res in data:
        for api in res:
            if ('path' not in api and 'name' not in api):
                continue
            group = {}
            group['apiList'] = []          
            if file_suffix == 'php' or file_suffix == 'java':
                pattern = re.compile('\/\*\*(.*?)\*/', re.S)
                items = re.findall(pattern, api)
                api = items[0].replace("*", "")
            if file_suffix == 'py':
                pattern = re.compile(r'"""(.*?)"""', re.S)
                items = re.findall(pattern, api)
                if not items:
                    pattern = re.compile(r"'''(.*?)'''", re.S)
                    items = re.findall(pattern, api)
                api = items[0]
            if ('childGroup' not in api):
                arr = api.split(';')              
                api = {}
                api['baseInfo'] = {}
                api['headerInfo'] = []
                api['requestInfo'] = []
                api['resultInfo'] = []
                for api_info in arr:
                    api_info = api_info.lstrip()
                    if 'group' == api_info[0:5]:
                        pattern = re.compile(r'group="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        group['groupName'] = items[0]
                    if 'status' == api_info[0:6]:
                        pattern = re.compile(r'status="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiStatus'] = apiStatus[items[0]]
                    if 'protocol' == api_info[0:8]:
                        pattern = re.compile(r'protocol="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiProtocol'] = protocol[items[0]]
                    if 'method' == api_info[0:6]:
                        pattern = re.compile(r'method="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiRequestType'] = request_type[items[0]]
                    if 'path' == api_info[0:4]:
                        pattern = re.compile(r'path="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiURI'] = items[0]
                    if 'name' == api_info[0:4]:
                        pattern = re.compile(r'name="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiName'] = items[0]
                    if 'header' == api_info[0:6]:
                        pattern = re.compile(r'.*?name="(.*?)".*?="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        for item in items:
                            api['headerInfo'].append({
                                'headerName': item[0],
                                'headerValue': item[1]
                            })
                    if 'parameter' == api_info[0:9]:
                        paramter = {}
                        pattern = re.compile(r'.*?name="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramKey'] = items[0]
                        pattern = re.compile(r'.*?type="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramType'] = paramType[items[0]]
                        pattern = re.compile(r'.*?,description="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramName'] = items[0]
                        pattern = re.compile(r'.*?,required=(.*?)}', re.S)
                        items = re.findall(pattern, api_info)
                        if items[0][0:4] == 'true':
                            paramter['paramNotNull'] = 0
                        if items[0][0:5] == 'false':
                            paramter['paramNotNull'] = 1
                        paramter['paramValue'] = ''
                        paramter['paramLimit'] = ''
                        api['requestInfo'].append(paramter)
                    if 'response' == api_info[0:8]:
                        response = {}
                        pattern = re.compile(r'.*?name="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        response['paramKey'] = items[0]
                        pattern = re.compile(r'.*?type="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        response['paramType'] = paramType[items[0]]
                        pattern = re.compile(r'.*?,description="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        response['paramName'] = items[0]
                        pattern = re.compile(r'.*?,required=(.*?)}', re.S)
                        items = re.findall(pattern, api_info)
                        if items[0][0:4] == 'true':
                            response['paramNotNull'] = 0
                        if items[0][0:5] == 'false':
                            response['paramNotNull'] = 1
                        response['paramValue'] = ''
                        response['paramLimit'] = ''
                        api['resultInfo'].append(response)
                    api['baseInfo']['starred'] = '0'
                    api['baseInfo']['apiNoteRaw'] = ''
                    api['baseInfo']['apiNote'] = ''
                    api['baseInfo']['apiRequestParamType'] = 0
                    api['baseInfo']['apiNoteType'] = 0
                    api['baseInfo']['apiSuccessMock'] = ''
                    api['baseInfo']['apiFailureMock'] = ''
                    api['baseInfo']['rule'] = ''
                    api['baseInfo']['result'] = ''
                    api['baseInfo']['apiUpdateTime'] =  time.strftime('%Y-%m-%d %X', time.localtime())
                    if 'apiStatus' not in api['baseInfo']:
                        api['baseInfo']['apiStatus'] = 0
                    if  'apiProtocol' not in api['baseInfo']:
                        api['baseInfo']['apiProtocol'] = 0
                if 'apiURI' in api['baseInfo'] and 'apiName' in api['baseInfo']:
                    group['apiList'].append(api)
                else:
                   continue
                if 'groupName' not in group:
                    group['groupName'] = '默认分组'
                flag = 0
                for i in range(len(data_json['apiGroupList'])):
                    if data_json['apiGroupList'][i]['groupName'] == group['groupName']:
                        del group['groupName']
                        data_json['apiGroupList'][i]['apiList'].append(group['apiList'][0])
                        flag = 1
                        break
                if flag == 0:
                    data_json['apiGroupList'].append(group)
            else:
                arr = api.split(';')                
                api = {}
                api['baseInfo'] = {}
                api['headerInfo'] = []
                api['requestInfo'] = []
                api['resultInfo'] = []
                for api_info in arr:
                    api_info = api_info.lstrip()
                    if 'group' == api_info[0:5]:
                        pattern = re.compile(r'group="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        group['parentGroupName'] = items[0]
                    if 'childGroup' == api_info[0:10]:
                        pattern = re.compile(r'childGroup="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        group['groupName'] = items[0]
                    if 'status' == api_info[0:6]:
                        pattern = re.compile(r'status="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiStatus'] = apiStatus[items[0]]
                    if 'protocol' == api_info[0:8]:
                        pattern = re.compile(r'protocol="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiProtocol'] = protocol[items[0]]
                    if 'method' == api_info[0:6]:
                        pattern = re.compile(r'method="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiRequestType'] = request_type[items[0]]
                    if 'path' == api_info[0:4]:
                        pattern = re.compile(r'path="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiURI'] = items[0]
                    if 'name' == api_info[0:4]:
                        pattern = re.compile(r'name="(.*?)"', re.S)
                        items = re.findall(pattern, api_info)
                        api['baseInfo']['apiName'] = items[0]
                    if 'header' == api_info[0:6]:
                        pattern = re.compile(r'.*?name="(.*?)".*?="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        for item in items:
                            api['headerInfo'].append({
                                'headerName': item[0],
                                'headerValue': item[1]
                            })
                    if 'parameter' == api_info[0:9]:
                        paramter = {}
                        pattern = re.compile(r'.*?name="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramKey'] = items[0]
                        pattern = re.compile(r'.*?type="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramType'] = paramType[items[0]]
                        pattern = re.compile(r'.*?,description="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        paramter['paramName'] = items[0]
                        pattern = re.compile(r'.*?,required=(.*?)}', re.S)
                        items = re.findall(pattern, api_info)
                        if items[0][0:4] == 'true':
                            paramter['paramNotNull'] = 0
                        if items[0][0:5] == 'false':
                            paramter['paramNotNull'] = 1
                        paramter['paramValue'] = ''
                        paramter['paramLimit'] = ''
                        api['requestInfo'].append(paramter)
                    if 'response' == api_info[0:8]:
                        response = {}
                        pattern = re.compile(r'.*?name="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        response['paramKey'] = items[0]
                        pattern = re.compile(r'.*?type="(.*?)".*?', re.S)
                        items = re.findall(pattern, api_info)
                        response['paramType'] = paramType[items[0]]
                        pattern = re.compile(r'.*?,description="(.*?)".*?',
                                             re.S)
                        items = re.findall(pattern, api_info)
                        response['paramName'] = items[0]
                        pattern = re.compile(r'.*?,required=(.*?)}', re.S)
                        items = re.findall(pattern, api_info)
                        if items[0][0:4] == 'true':
                            response['paramNotNull'] = 0
                        if items[0][0:5] == 'false':
                            response['paramNotNull'] = 1
                        response['paramValue'] = ''
                        response['paramLimit'] = ''
                        api['resultInfo'].append(response)
                    api['baseInfo']['starred'] = '0'
                    api['baseInfo']['apiNoteRaw'] = ''
                    api['baseInfo']['apiNote'] = ''
                    api['baseInfo']['apiRequestParamType'] = 0
                    api['baseInfo']['apiNoteType'] = 0
                    api['baseInfo']['apiSuccessMock'] = ''
                    api['baseInfo']['apiFailureMock'] = ''
                    api['baseInfo']['rule'] = ''
                    api['baseInfo']['result'] = ''
                    api['baseInfo']['apiUpdateTime'] =  time.strftime('%Y-%m-%d %X', time.localtime())
                    if 'apiStatus' not in api['baseInfo']:
                        api['baseInfo']['apiStatus'] = 0
                    if 'apiProtocol' not in api['baseInfo']:
                        api['baseInfo']['apiProtocol'] = 0
                if 'apiURI' in api['baseInfo'] and 'apiName' in api['baseInfo']:
                    group['apiList'].append(api)
                else:
                    continue
                if 'parentGroupName' not in group:
                    group['parentGroupName'] = '默认分组'
                flag = 0
                for j in range(len(childGroup)):
                    if(childGroup[j]['parentGroupName'] ==  group['parentGroupName'] and childGroup[j]['groupName'] == group['groupName']):
                        del group['parentGroupName']
                        del group['groupName']
                        childGroup[j]['apiList'].append(group['apiList'][0])
                        flag = 1
                        break
                if flag == 0:
                    childGroup.append(group)
    data = integrationData(data_json['apiGroupList'], childGroup)
    return data
        
def integrationData(parent_group, child_group):
    for k in range(len(child_group)):
        flag = 0
        for index in range(len(parent_group)):
            if 'apiGroupChildList' not in parent_group[index]:
                parent_group[index]['apiGroupChildList'] = []
            if parent_group[index]['groupName'] == child_group[k]['parentGroupName']:
                flag = 1
                parent_group[index]['apiGroupChildList'].append({'groupName':child_group[k]['groupName'],'apiList':child_group[k]['apiList']})
        if flag == 0:
            parent_group.append({'groupName':child_group[k]['parentGroupName'],'apiList':[],'apiGroupChildList':[{'groupName':child_group[k]['groupName'],'apiList':child_group[k]['apiList']}]})
    return parent_group
        
def sendRequest(data, project_key, secret_key, user_name, user_password):
    post_data = {'data': json.dumps(data), 'projectKey': project_key, 'secretKey': secret_key, 'userName': user_name, 'userPassword': user_password}
    message = requests.post('http://api-upload.eolinker.com', data=post_data)
    print(message.text)


if __name__ == '__main__':
    if config.file_path == '' or config.file_suffix == '' or config.project_key == '' or config.secret_key == '' or config.user_name == '' or config.user_password == '':
        print(r"param can't not be null")
    else:
        data = getContent(config.file_path, config.file_suffix,
                        config.exclude_file)
        data = getdata(data, config.file_suffix)
        sendRequest(data, config.project_key, config.secret_key, config.user_name, config.user_password)

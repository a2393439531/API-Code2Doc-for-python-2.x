# Code2Doc��eoLinker AMS ����ע�����ɹ��ߣ�
![����ע��](http://data.eolinker.com//blog/eioasddshengc.jpg)

eoLinker �ṩ�˴Ӵ���ע��ֱ�����ɽӿ��ĵ��Ĺ��ܣ���Ч�ؽ��ӿ��ĵ������ʵ����ͬ������ƪ���½���ϸ�������ͨ��ͨ��eoLinker��Python�ű������������ĵ���

##### ��Ҫ������
1.  eoLinker�û��ʻ�
2.  �Ѿ������ϰ洴����һ����Ŀ
3.  �Ѿ���ȡ��Ŀ��**Project_Key**�Լ�**Secret_Key**
4.  [eoLinkerע�������ĵ��ű�](https://github.com/eolinker/Code2Doc)

##### ��λ�ȡProject_Key�Լ�Secret_Key��
����Ŀ�ſ�ҳ�棬�����������-�Զ������ĵ���ť����������µ�����ʾ��ص�Project_Key�Լ�Secret_Key��
![ʾ���Զ������ĵ�](http://data.eolinker.com//blog/eioasddzidongshengcheng.jpg)
##### ����Ҫ��
Ŀǰ����ע�������ĵ�֧��Python����Ҫ��װ2.7���ϰ汾��Python�����ҿ���re��codes��requestsģ�顣

 ##### ��ع��ߣ�

1.  [eoLinker�Զ������ĵ��ű�](https://github.com/eolinker/Code2Doc)
2.  [eoLinker�������ɴ���ע�͹���](http://tool.eolinker.com/doc2code)
##### �淶��

eoLinkerӵ���Լ����ı�������ԣ�EOML����Ϊ�˼����������̣���ʹ��eoLinker�ṩ��[�������ɴ���ע�͹���](http://tool.eolinker.com/doc2code)��

*   group��[����]��API��������
*   childGroup��[ѡ��]���ӷ������ƣ�������group֮�£�
*   status��[����]���ӿ�״̬��work�����ã�| maintain��ά����| abandoned�����ã�
*   protocol��[����]������Э�飬http|https
*   method��[����]������ʽ��post | get | put | delete | head | options | patch
*   path��[����]��API��ַ
*   name��[����]��API����
*   header��[ѡ��]������ͷ��������ʹ��{}����
    *   name��ͷ������
    *   value��ͷ������ֵ
*   parameter��[ѡ��]���������������ʹ��{}����
    *   name��������
    *   type���������ͣ�string | file | json | int | float | double | date | datetime | boolean | byte | short | long | array | object
    *   required���Ƿ���true���ǣ�|false����
*   response��[ѡ��]�����ز���������ʹ��{}����
    *   name��������
    *   description������
    *   type���������ͣ�string | file | json | int | float | double | date | datetime | boolean | byte | short | long | array | object
    *   required���Ƿ�һ�����أ�true���ǣ�|false����

##### ����һ��ʹ��/**/ע�⣩��

```
/** 
* group = "������"; 
* childGroup = "�ӷ���"; 
* status = "work"; 
* protocol = "http"; 
* method = "POST";
* path = "www.baidu.com";
* name = "����"; 
* header = {name="Accept-Charset",value="utf-8"};
* header = {name="Content-Type",value="application/xml"}; 
* parameter = {name = "userID", type = "string", description = "�û�ID", required = true};
* parameter = {name = "userName", type = "string", description = "�û�����", required = true}; 
* response = {name = "statusCode",description = "״̬��", type = "string", required = true};
*/
```

##### ���Ӷ���ʹ�á������򡱡���ע�⣩��
```
������
group = "������";
childGroup = "�ӷ���";
status = "work"; 
protocol = "http"; 
method = "POST"; 
path = "www.baidu.com6";
name = "����"; 
header = {name="Accept-Charset",value="utf-8"}; 
header = {name="Content-Type",value="application/xml"}; 
parameter = {name = "userID", type = "string", description = "�û�ID", required = true};
parameter = {name = "userName", type = "string", description = "�û�����", required = true};
response = {name = "statusCode",description = "״̬��", type = "string", required = true}; 
������
```
##### �����ļ���

project_key����Ŀkey 
secret_key������key 
file_path����ȡ�ļ���Ŀ¼·��,windowϵͳ�밴��r"c:\test"����"c:\\test"д��д
 file_suffix����ȡ�ļ��ĺ�׺��������php��py��java
 exclude_file���ų��ļ���
 user_name��eoLinker�û��˺� 
user_password���û�����

##### �����ļ����ӣ�

project_key = 'uwiuryomx3asudhcami3y498cy7m2' 
secret_key = '7962h4s83asd' 
file_path = 'C:\\project\\code_upload' 
file_suffix = 'java' 
exclude_file = ['gitignore','config.php'] 
user_name = 'test' 
user_password = '123456'

 **�����������֮������eolinker.py�ű��ȿ��Զ������ĵ������ء��ɹ������Զ����ɳɹ�������ʧ�ܡ�**





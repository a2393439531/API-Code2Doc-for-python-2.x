# Code2Doc（eoLinker AMS 代码注释生成工具）
![代码注释](http://data.eolinker.com//blog/eioasddshengc.jpg)

eoLinker 提供了从代码注释直接生成接口文档的功能，有效地将接口文档与代码实现了同步。本篇文章将详细介绍如何通过通过eoLinker的Python脚本程序来生成文档。

##### 必要条件：
1.  eoLinker用户帐户
2.  已经在线上版创建了一个项目
3.  已经获取项目的**Project_Key**以及**Secret_Key**
4.  [eoLinker注释生成文档脚本](https://github.com/eolinker/Code2Doc)

##### 如何获取Project_Key以及Secret_Key？
在项目概况页面，点击其他功能-自动生成文档按钮，会出现以下弹框，显示相关的Project_Key以及Secret_Key。
![示例自动生成文档](http://data.eolinker.com//blog/eioasddzidongshengcheng.jpg)
##### 环境要求：
目前代码注释生成文档支持Python，需要安装2.7以上版本的Python，并且开启re、codes、requests模块。

 ##### 相关工具：

1.  [eoLinker自动生成文档脚本](https://github.com/eolinker/Code2Doc)
2.  [eoLinker在线生成代码注释工具](http://tool.eolinker.com/doc2code)
##### 规范：

eoLinker拥有自己的文本标记语言（EOML），为了减少输入流程，请使用eoLinker提供的[在线生成代码注释工具](http://tool.eolinker.com/doc2code)。

*   group，[必填]，API分组名称
*   childGroup，[选填]，子分组名称（归属于group之下）
*   status，[必填]，接口状态，work（启用）| maintain（维护）| abandoned（弃用）
*   protocol，[必填]，请求协议，http|https
*   method，[必填]，请求方式，post | get | put | delete | head | options | patch
*   path，[必填]，API地址
*   name，[必填]，API名称
*   header，[选填]，请求头部，内容使用{}包裹
    *   name，头部名称
    *   value，头部参数值
*   parameter，[选填]，请求参数，内容使用{}包裹
    *   name，参数名
    *   type，参数类型，string | file | json | int | float | double | date | datetime | boolean | byte | short | long | array | object
    *   required，是否必填，true（是）|false（否）
*   response，[选填]，返回参数，内容使用{}包裹
    *   name，参数名
    *   description，描述
    *   type，参数类型，string | file | json | int | float | double | date | datetime | boolean | byte | short | long | array | object
    *   required，是否一定返回，true（是）|false（否）

##### 例子一（使用/**/注解）：

```
/** 
* group = "父分组"; 
* childGroup = "子分组"; 
* status = "work"; 
* protocol = "http"; 
* method = "POST";
* path = "www.baidu.com";
* name = "测试"; 
* header = {name="Accept-Charset",value="utf-8"};
* header = {name="Content-Type",value="application/xml"}; 
* parameter = {name = "userID", type = "string", description = "用户ID", required = true};
* parameter = {name = "userName", type = "string", description = "用户名称", required = true}; 
* response = {name = "statusCode",description = "状态码", type = "string", required = true};
*/
```

##### 例子二（使用’’’或”””注解）：
```
”””
group = "父分组";
childGroup = "子分组";
status = "work"; 
protocol = "http"; 
method = "POST"; 
path = "www.baidu.com6";
name = "测试"; 
header = {name="Accept-Charset",value="utf-8"}; 
header = {name="Content-Type",value="application/xml"}; 
parameter = {name = "userID", type = "string", description = "用户ID", required = true};
parameter = {name = "userName", type = "string", description = "用户名称", required = true};
response = {name = "statusCode",description = "状态码", type = "string", required = true}; 
”””
```
##### 配置文件：

project_key，项目key 
secret_key，密码key 
file_path，读取文件的目录路径,window系统请按照r"c:\test"或者"c:\\test"写法写
 file_suffix，读取文件的后缀名，比如php或py或java
 exclude_file，排除文件名
 user_name，eoLinker用户账号 
user_password，用户密码

##### 配置文件例子：

project_key = 'uwiuryomx3asudhcami3y498cy7m2' 
secret_key = '7962h4s83asd' 
file_path = 'C:\\project\\code_upload' 
file_suffix = 'java' 
exclude_file = ['gitignore','config.php'] 
user_name = 'test' 
user_password = '123456'

 **完成以上配置之后，运行eolinker.py脚本既可自动生成文档，返回“成功”则自动生成成功，否则失败。**





# 大智慧远程cookies获取集群接口

## 介绍

* 基于Playwright的远程获取cookies集群，创建可以访问集群的接口，用户可通过调用接口函数创建和操作浏览器，然后获取浏览器Cookies和UA等信息
* 当前版本号 0.1.7
* python包安装：`pip install fincookie -i https://pypi.python.org/simple/`

## APIs

### get_cookies

通过该接口创建和操作集群浏览器，返回Cookies、User-Agent、Proxy等信息  
**Parameters**:

* **appid:** string(required), 用户自定义的浏览器标识,服务器根据该参数为请求分配浏览器，结合renew_interval参数，同一appid的请求在renew_interval时限内会在同一浏览器上继续操作，直到renew_interval过期后关闭该appid的浏览器

* **get_last:** int, 若为`0`通过操作浏览器获取结果，若为`1` 不进行浏览器操作，直接返回appid的上次cookies结果，如果没有则重新获取(其他并发的get_last为1或者2的线程等待)，若为`2`
  清除并重新获取历史结果，其他get_last为1或者2的线程等待结果获取完成之后直接使用，避免多线程重复操作浏览器。默认为`0`。

* **block_timeout:** int, 同appid的多个请求同时操作浏览器时浏览器的阻塞时间(ms)，如果为`0`则不阻塞，若浏览器正在使用直接返回`浏览器繁忙`错误，默认为`0`

* **url:** string, 用户请求网址，如果用户需要请求网址，可传入该参数

* **url_timeout:** int, 用户请求网址的超时时间（ms），如果在该时间内浏览器未完成请求，则请求失败，默认值: 30,000。

* **script:** string, 用户需要在浏览器中执行的JavaScript代码，如果用户需要执行JavaScript代码，可传入该参数

* **wait_for:** string, 用户需要等待的操作，`timeout`等待一定时间, `selector`等待元素选择器出现响应

* **wait_timeout:** int, `wait_for`等待的时间（ms），结合wait_for参数使用, 默认值: 30,000。

* **selector:** string, wait_for参数值为`selector`时对应的元素CSS选择器或者XPath，用于选择需要等待或获取的元素

* **state:** string, wait_for参数为selector时对应的元素等待状态，`visible`: 等待元素在页面中可见 `hidden`: 等待元素在页面中隐藏 `attached`: 等待选择器附加到 DOM 上  `detached`:
  等待选择器从 DOM 上分离

* **action:** string, 等待元素之后对元素进行的操作,`click`: 单击，`dblclick`: 双击，`type`: 输入文字或按键

* **type_string:** string, `action`为`type`时输入的字符

* **renew_interval:** int, appid对应浏览器的保留时间（ms），在保留时间内appid相同的请求会由同一浏览器继续执行后返回，每次请求后刷新, 默认值：3000

**Returns:** -> Dict

* `appid`: string, 用户指定的appid
* `request_id`: string, 用户发起请求的唯一标识
* `message`: string, 响应消息，请求成功时该字段为`success`, 请求失败时，该字段为失败或者错误原因
* `cookies`: dict, 请求成功时浏览器的cookies信息
* `user-agent`: string, 请求成功时浏览器的UA信息
* `proxy`: string, 浏览器当前代理
* `server_ip`: string, 响应请求的服务器IP

**Examples:**

* 示例一

```python
from fincookie import get_cookies

cookie_data = get_cookies(
    appid="1236",  # appid
    url="https://www.baidu.com",  # 请求百度网址
    url_timeout=2000,  # 网址请求等待时间为 2,000 ms
    wait_for='timeout',  # 请求完成后页面等待 1,000 ms
    wait_timeout=1000,
    renew_interval=20000  # 页面于响应完成后保留 20,000 ms, 在这个时间内appid相同的请求仍由该浏览器执行
)
print(cookie_data)
```

响应内容为：

```json
{
  "appid": "1236",
  "request_id": "1847057417",
  "message": "success",
  "cookies": {
    "BAIDUID": "8BB38402215B843E9B9D58914967E56C:FG=1",
    "BAIDUID_BFESS": "8BB38402215B843E9B9D58914967E56C:FG=1",
    "BA_HECTOR": "8501ah2l208l0l840lah0k0n1imtghs1r",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "BD_UPN": "12314753",
    "BIDUPSID": "8BB38402215B843EC80B49F9EA7C0B2E",
    "PSTM": "1701757499",
    "ZFY": "q7bYPBd1:BvMfgIButh0kbvxu8leCLAIh7jgvAS0DfBg:C"
  },
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "proxy": "10.55.9.55:808",
  "server_ip": "10.55.3.205"
}
```

* 示例二：

```python
from fincookie import get_cookies

cookie_data = get_cookies(
    appid='g7gs897g',  # appid
    url="https://www.bilibili.com",  # 请求B站网址
    wait_for="selector",  # 等待class为'nav-search-input'的元素在页面中显示，等待时间为2,000 ms
    selector=".nav-search-input",
    state="visible",
    wait_timeout=2000,
    action='type',  # 获取到元素后向该元素中输入文字："ChatGPT未来将如何发展"
    type_string="ChatGPT未来将如何发展",
    renew_interval=30000  # 页面为该appid保留30,000 ms
)
print(cookie_data)
```

响应如下：

```json
{
  "appid": "g7gs897g",
  "request_id": "1846820623",
  "message": "success",
  "cookies": {
    "_uuid": "89C997FF-FF71-7F108-73F1-DA10944E1267314040infoc",
    "b_lsid": "A911010AB1_18C38A877BF",
    "b_nut": "1701757613",
    "b_ut": "7",
    "browser_resolution": "1792-651",
    "buvid3": "6B27F3AD-7F98-B761-5040-E8AAA298B9C113678infoc",
    "buvid4": "F86D59D9-6E42-CD37-95F5-0C267561533A14432-023120506-",
    "buvid_fp": "fe1cd0dfe5393210d49205fe561b1868",
    "enable_web_push": "DISABLE",
    "header_theme_version": "null",
    "home_feed_column": "5",
    "i-wanna-go-back": "-1",
    "innersign": "0"
  },
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "proxy": "10.55.9.178:808",
  "server_ip": "10.55.3.205"
}
```

* 示例三: 直接获取appid=1236的上次成功请求的历史响应

```python
from fincookie import get_cookies
cookie_data = get_cookies(
    appid='1236',
    get_last=1
)
print(cookie_data)
```

```json
{
  "appid": "1236",
  "request_id": "1847057417",
  "message": "success",
  "cookies": {
    "BAIDUID": "8BB38402215B843E9B9D58914967E56C:FG=1",
    "BAIDUID_BFESS": "8BB38402215B843E9B9D58914967E56C:FG=1",
    "BA_HECTOR": "8501ah2l208l0l840lah0k0n1imtghs1r",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "BD_UPN": "12314753",
    "BIDUPSID": "8BB38402215B843EC80B49F9EA7C0B2E",
    "PSTM": "1701757499",
    "ZFY": "q7bYPBd1:BvMfgIButh0kbvxu8leCLAIh7jgvAS0DfBg:C"
  },
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "proxy": "10.55.9.55:808",
  "server_ip": "10.55.3.205"
}
```

## get_logs

远程Cookies获取集群日志获取API(每次请求操作日志保留7天)  
**Parameters:**

* `appid`: 请求的程序id
* `date_from`: 起始日期，格式:yyyy-mm-dd
* `request_id`: 请求的request_id

**Returns:** -> string  
对应的日志文本

**Examples**

* 实例1:获取appid为1408在2023年11月17日及之后的日志

```python
from fincookie import get_logs

logs = get_logs(appid='1236', date_from='2023-12-05')
print(logs)
```

* outputs:

```text
2023-12-05 14:21:34 | server:10.55.3.205-appid:1236-request:1819720053-新建浏览器，使用代理:10.55.9.63:808
2023-12-05 14:21:34 | server:10.55.3.205-appid:1236-request:1819720053-新建浏览器成功
2023-12-05 14:21:34 | server:10.55.3.205-appid:1236-request:1819720053-发送操作信息
2023-12-05 14:21:34 | server:10.55.3.205-appid:1236-request:1819720053-操作控制发送--访问页面:https://www.baidu.com timeout:2000 ms
2023-12-05 14:21:35 | server:10.55.3.205-appid:1236-request:1819720053-浏览器操作结束
2023-12-05 14:21:35 | server:10.55.3.205-appid:1236-request:1819720053-Cookies获取成功
2023-12-05 14:21:35 | server:10.55.3.205-appid:1236-request:1819720053-UA获取成功
2023-12-05 14:21:35 | server:10.55.3.205-appid:1236-request:1819720053-请求处理完成, 发送响应结果
2023-12-05 14:21:35 | server:main-appid:1236-request:1819720053-刷新响应结果
2023-12-05 14:21:35 | server:main-appid:1236-request:1819720053-刷新历史响应
2023-12-05 14:21:35 | server:main-appid:1236-request:1819720053-获取到响应结果{"appid":"1236","request_id":"1819720053","server_ip":"10.55.3.205","proxy":"10.55.9.63:808","message":"success","cookies":{"BIDUPSID":"A5851B6EFC8DDE9C8D5055FC8BCDE44C","PSTM":"1701757294","BAIDUID":"A5851B6EFC8DDE9CD645AFD0F25D2C04:FG=1","BAIDUID_BFESS":"A5851B6EFC8DDE9CD645AFD0F25D2C04:FG=1","BD_UPN":"12314753","BA_HECTOR":"8h200l0k24002l2l8h2l24al1imtgbf1r","ZFY":"da9yXeGaTthzEO3:AfAyU5mr0pCGCknhBBaoa64UnoV0:C","BDORZ":"B490B5EBF6F3CD402E515D22BCDA1598"},"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
2023-12-05 14:21:35 | server:main-appid:1236-更新响应历史记录
2023-12-05 14:21:55 | server:10.55.3.205-appid:1236-浏览器到期，已关闭
```

* 实例2： 获取request_id为1816728066的请求日志

```python
from fincookie import get_logs

logs = get_logs(request_id='1816728066')
print(logs)
```

```text
2023-12-05 14:23:31 | server:main-appid:12345-request:1816728066-获取到请求流:{"appid":"12345","get_last":0,"block_timeout":0,"url":"https://www.baidu.com","url_timeout":2000,"wait_for":"timeout","wait_timeout":1000,"renew_interval":20000,"ip":"10.17.214.105","api":"http://hive.finchina.local/api/hwy/cookieService/","request_id":"1816728066","request_timeout":6000}
2023-12-05 14:23:31 | server:main-appid:12345-request:1816728066-选择服务器:10.55.3.205
2023-12-05 14:23:31 | server:main-appid:12345-request:1816728066-请求数据流已发送
2023-12-05 14:23:31 | server:10.55.3.205-appid:12345-request:1816728066-开始处理请求
2023-12-05 14:23:31 | server:10.55.3.205-appid:12345-request:1816728066-正在获取浏览器
2023-12-05 14:23:31 | server:10.55.3.205-appid:12345-request:1816728066-新建浏览器，使用代理:10.55.9.87:808
2023-12-05 14:23:32 | server:10.55.3.205-appid:12345-request:1816728066-新建浏览器成功
2023-12-05 14:23:32 | server:10.55.3.205-appid:12345-request:1816728066-发送操作信息
2023-12-05 14:23:32 | server:10.55.3.205-appid:12345-request:1816728066-操作控制发送--访问页面:https://www.baidu.com timeout:2000 ms
2023-12-05 14:23:33 | server:10.55.3.205-appid:12345-request:1816728066-浏览器操作结束
2023-12-05 14:23:33 | server:10.55.3.205-appid:12345-request:1816728066-Cookies获取成功
2023-12-05 14:23:33 | server:10.55.3.205-appid:12345-request:1816728066-UA获取成功
2023-12-05 14:23:33 | server:10.55.3.205-appid:12345-request:1816728066-请求处理完成, 发送响应结果
2023-12-05 14:23:33 | server:main-appid:12345-request:1816728066-刷新响应结果
2023-12-05 14:23:33 | server:main-appid:12345-request:1816728066-刷新历史响应
2023-12-05 14:23:33 | server:main-appid:12345-request:1816728066-获取到响应结果{"appid":"12345","request_id":"1816728066","server_ip":"10.55.3.205","proxy":"10.55.9.87:808","message":"success","cookies":{"BIDUPSID":"1EE73BB8F81478A378F8C8CA9102FB84","PSTM":"1701757412","BAIDUID":"1EE73BB8F81478A307128BB1BBF27E8C:FG=1","BD_UPN":"12314753","BAIDUID_BFESS":"1EE73BB8F81478A307128BB1BBF27E8C:FG=1","BA_HECTOR":"052l058l84a50ga1052k2ga31imtgf51q","ZFY":"evDfcqxEEgugC97RGuUcAnUg4OLOGtfc8yQiXpWhbdA:C","BDORZ":"B490B5EBF6F3CD402E515D22BCDA1598"},"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
```


## ZoomEye-python

`ZoomEye` 是一款网络空间搜索引擎，用户可以使用浏览器方式 <https://www.zoomeye.org> 搜索网络设备。

`ZoomEye-python` 是一款基于 `ZoomEye API` 开发的 Python 库，提供了 `ZoomEye` 命令行模式，同时也可以作为 `SDK` 集成到其他工具中。该库可以让技术人员更便捷地**搜索**、**筛选**、**导出** `ZoomEye` 的数据。


### 0x01 安装步骤
可直接从 `pypi` 进行安装：

	pip3 install zoomeye

也可以通过 `github` 进行安装：

	pip3 install git+https://github.com/knownsec/ZoomEye-python.git


### 0x02 使用cli
在成功安装 `ZoomEye-python` 后，可以直接使用 `zoomeye` 命令，如下：

```
$ zoomeye -h
usage: cli.py [-h] {info,search,init} ...

positional arguments:
  {info,search,init}
    info              Show ZoomEye account info
    search            Search the ZoomEye database
    init              Initialize the token for ZoomEye-python

optional arguments:
  -h, --help          show this help message and exit
```

#### 1.初始化token
在使用 `ZoomEye-python cli` 前需要先初始化用户 `token`，该凭证用于验证用户身份以便从 `ZoomEye` 查询数据；我们提供了两种认证方式：

	1.username/password
	2.APIKEY (推荐)

可以通过 `zoomeye init -h` 查看帮助，下面通过 `APIKEY` 来进行演示：

```
$ zoomeye init -apikey "01234567-acbd-00000-1111-22222222222"
successfully initialized
Role: developer
Quota: 10000
```

用户可以通过登陆 `ZoomEye` 在个人信息中(<https://www.zoomeye.org/profile>) 获取 `APIKEY`；`APIKEY` 不会过期，用户可根据需求在个人信息中进行重置。

除此之外，我们还提供了 `username/password` 的初始化方式，通过这种方式认证后会返回 `JWT-token`，具有一定的时效性，失效后需要用户重新登陆。

#### 2.查询配额
用户可以通过 `info` 命令查询个人信息以及数据配额，如下：

```
$ zoomeye info
Role: developer
Quota: 10000
```

#### 3.搜索
搜索是 `ZoomEye-python` 最核心的功能，通过 `search` 命令进行使用。`search` 命令需要指定搜索关键词(`dork`)，下面我们进行简单的搜索：

```
$ zoomeye search "telnet" -num 1
ip:port       service  country  app                 banner                        
222.*.*.*:23  telnet   Japan    Pocket CMD telnetd  \xff\xfb\x01\xff\xfb\x03\xff\x...

total: 1
```

使用 `search` 命令和使用浏览器在 `ZoomEye` 进行搜索一样简单，在默认情况下我们显示了较为重要的 5 个字段，用户可以使用这些数据了解目标信息：

	1.ip:port  ip地址和端口
	2.service  该端口开放的服务
	3.country  该ip地址所属国家
	4.app      识别出的应用类型
	5.banner   该端口的特征响应报文

在以上演示中，使用 `-num` 参数指定了显示的数量，除此之外，`search` 还支持以下参数(`zoomeye search -h`)，以便用户对数据进行处理，我们将在下文进行说明和演示：

	-num     设置显示/搜索的数量
	-count   查询该 dork 在 ZoomEye 数据库的总量
	-facet   查询该 dork 全量数据的分布情况
	-stat    统计数据结果集的分布情况
	-filter  查询数据结果集中某个字段的详情，或根据内容进行筛选
	-save    可按照筛选条件将结果集进行导出

#### 4.数据数量
通过 `-num` 参数可以指定我们搜索和显示的数量，指定的数目即消耗的配额数量。而通过 `-count` 参数可以查询该 `dork` 在 ZoomEye 数据库的总量，如下：

```
$ zoomeye search "telnet" -count
56903258
```

>需要注意一点，`-num` 参数消耗的配额为 20 的整数倍，这是因为 `ZoomEye API` 单次查询的最小数量为 20 条。

#### 5.数据聚合
我们可以通过 `-facet` 和 `-stat` 进行数据的聚合统计，使用 `-facet` 可以查询该 dork 全量数据的聚合情况(由 `ZoomEye` 聚合统计后通过 `API` 获取)，而 `-stat` 可以对查询到的结果集进行聚合统计。两个命令支持的聚合字段包括：

	app      按应用类型进行统计
	device   按设备类型进行统计
	service  按照服务类型进行统计
	os       按照操作系统类型进行统计
	port     按照端口进行统计
	country  按照国家进行统计
	city     按照城市进行统计

使用 `-facet` 统计全量 `telnet` 设备的应用类型：

```
$ zoomeye search "telnet" -facet app
app                                count
[unknown]                          28317914
BusyBox telnetd                    10176313
Linux telnetd                      3054856
Cisco IOS telnetd                  1505802
Huawei Home Gateway telnetd        1229112
MikroTik router config httpd       1066947
Huawei telnetd                     965378
Busybox telnetd                    962470
Netgear broadband router...        593346
NASLite-SMB/Sveasoft Alc...        491957
```

使用 `-stat` 统计查询出来的 20 条 `telnet` 设备的应用类型：

```
$ zoomeye search "telnet" -stat app
app                                count               
Cisco IOS telnetd                  7
[unknown]                          5
BusyBox telnetd                    4
Linux telnetd                      3
Pocket CMD telnetd                 1
```

#### 6.数据筛选
使用 `-filter` 参数可以查询数据结果集中某个字段的详情，或根据内容进行筛选，该命令支持的字段包括：

	app      显示应用类型详情
	version  显示版本信息详情
	device   显示设备类型详情
	port     显示端口信息详情
	city     显示城市详情
	country  显示国家详情
	asn      显示as number详情
	banner   显示特征响应报文详情
	*        在包含该符号时，显示所有字段详情

相比较默认情况下的省略显示，所以通过 `-filter` 可以查看完整的数据，如下：

```
$ zoomeye search "telnet" -num 1 -filter banner
ip         banner                        
222.*.*.*  \xff\xfb\x01\xff\xfb\x03\xff\xfd\x03TELNET session now in ESTABLISHED state\r\n\r\n

total: 1
```

除此之外，还可以通过 `-filter` 对数据进行筛选，可以对字段按照关键词进行筛选(支持正则表达式)，使用格式为 `field=regexp`，比如我们我们查询在 `banner` 中包含 `telnet` 关键词的数据：

```
$ zooomeye search "telnet" -filter banner=telnet
ip         banner                        
222.*.*.*  \xff\xfb\x01\xff\xfb\x03\xff\xfd\x03TELNET session now in ESTABLISHED state\r\n\r\n

total: 1
```

#### 7.数据导出
`-save` 参数可以对数据进行导出，该参数的语法和 `-filter` 一样，并将结果按行 json 的格式保存到文件中，如下：

```
$ zoomeye search "telnet" -save banner=telnet
save file to telnet_1_1610446755.json successful!

$ cat telnet_1_1610446755.json
{'ip': '218.223.21.91', 'banner': '\\xff\\xfb\\x01\\xff\\xfb\\x03\\xff\\xfd\\x03TELNET session now in ESTABLISHED state\\r\\n\\r\\n'}
```

>如果使用 `-save` 但不带任何参数，则会将查询结果按照 `ZoomEye API` 的 json 格式保存成文件，这种方式一般用于在保留元数据的情况下进行整合数据；该文件可以作为输入通过 `cli` 再次解析处理，如 `zoomeye search "xxxxx.json"`。

#### 8.缓存机制
`ZoomEye-python` 在 `cli` 模式下提供了缓存机制，位于 `~/.config/zoomeye/cache` 下，尽可能的节约用户配额；用户查询过的数据集将在本地缓存 5 天，当用户查询相同的数据集时，不会消耗配额。


### 0x03 演示视频
[![asciicast](https://asciinema.org/a/qyDaJw9qQc7UjffD04HzMApWa.svg)](https://asciinema.org/a/qyDaJw9qQc7UjffD04HzMApWa)


### 0x04 使用SDK
#### 1.初始化token
同样，在 SDK 中也支持 `username/password` 和 `APIKEY` 两种认证方式，如下：

**1.user/pass**

```python
from zoomeye.sdk import ZoomEye

zm = ZoomEye(username="username", password="password")
```

**2.APIKEY**

```python
from zoomeye.sdk import ZoomEye

zm = ZoomEye(api_key="01234567-acbd-00000-1111-22222222222")
```

#### 2.SDK API
以下是 SDK 提供的接口以及说明：

	1.login()
	  使用 username/password 或者 APIKEY 进行认证
	2.dork_search(dork, page=0, resource="host", facets=None)
	  根据 dork 搜索指定页的数据
	3.multi_page_search(dork, page=1, resource="host", facets=None)
	  根据 dork 搜索多页数据
	4.resources_info()
	  获取当前用户的信息
	5.show_count()
	  获取当前 dork 下全部匹配结果的数量
	6.dork_filter(keys)
	  从搜索结果中提取指定字段的数据
	7.get_facet()
	  从搜索结果中获取全量数据的聚合结果
	8.history_ip(ip)
	  查询某个 ip 的历史数据信息
	9.show_site_ip(data)
	  遍历 web-search 结果集，并输出域名和ip地址
	10.show_ip_port(data)
	  遍历 host-search 结果集，并输出ip地址和端口

#### 3.使用示例

```python
$ python3
>>> import zoomeye.sdk as zoomeye
>>> dir(zoomeye)
['ZoomEye', 'ZoomEyeDict', '__builtins__', '__cached__', '__doc__',
'__file__', '__loader__', '__name__', '__package__', '__spec__',
'fields_tables_host', 'fields_tables_web', 'getpass', 'requests',
'show_ip_port', 'show_site_ip', 'zoomeye_api_test']
>>> # Use username and password to login
>>> zm = zoomeye.ZoomEye()
>>> zm.username = 'username@zoomeye.org'
>>> zm.password = 'password'
>>> print(zm.login())
....JIUzI1NiIsInR5cCI6IkpXVCJ9.....
>>> data = zm.dork_search('apache country:cn')
>>> zoomeye.show_site_ip(data)
213.***.***.46.rev.vo***one.pt ['46.***.***.213']
me*****on.o****e.net.pg ['203.***.***.114']
soft********63221110.b***c.net ['126.***.***.110']
soft********26216022.b***c.net ['126.***.***.22']
soft********5084068.b***c.net ['126.***.***.68']
soft********11180040.b***c.net ['126.***.***.40']
...
```

#### 4.数据搜索
如上示例，我们使用 `dork_search()` 进行搜索，我们还可以设置 `facets` 参数，以便获得该 dork 全量数据的聚合统计结果，`facets` 支持的字段请参考 **2.cli使用-4数据聚合**。示例如下：

```python
>>> data = zm.dork_search('telnet', facets='app')
>>> zm.get_facet()
{'product': [{'name': '', 'count': 28323128}, {'name': 'BusyBox telnetd', 'count': 10180912}, {'name': 'Linux telnetd', ......
```

>`multi_page_search()` 同样也可以进行搜索，当需要获取大量数据时使用该函数，其中 `page` 字段表示获取多少页的数据；而 `dork_search()` 仅获取指定页的数据。

#### 5.数据筛选
在 SDK 中提供了 `dork_filter()` 函数，我们可以更加方便对数据进行筛选，提取指定的数据字段，如下：

```python
>>> data = zm.dork_search("telnet")
>>> zm.dork_filter("ip,port")
[['180.*.*.166', 5357], ['180.*.*.6', 5357], ......
```

>由于通过 `web-search` 和 `host-search` 返回的字段不同，在进行过滤时需要填写正确的字段。
>`web-search` 包含的字段有：app / headers / keywords / title / ip / site / city / country
>`host-search` 包含的字段有：app / version / device / ip / port / hostname / city / country / asn / banner


### 0x05 contributions
[r0oike@knownsec 404](https://github.com/r0oike)  
[0x7F@knownsec 404](https://github.com/0x7Fancy)  
[fenix@knownsec 404](https://github.com/13ph03nix)  
[dawu@knownsec 404](https://github.com/d4wu)  


### 0x06 issue
**1.SDK和命令行工具的最小请求数量为 20 条**  
由于 API 的限制导致我们的查询最小单位一次为 20 条数据，对于一个新的 dork 来讲，无论是查看总数量，还是指定只搜索 1 条数据，都将会产生 20 条的开销；当然在命令行模式下我们提供了缓存机制，对于已经搜索过的数据缓存到本地(`~/.config/zoomeye/cache`)，有效期为 5 天，可以大幅度的节省配额。

**2. 为什么在 facet 会出现数据会不一致？**  
下图进行 `telnet` 的全数据统计结果，第一次查询的结果是一天前由命令行工具默认发起 20 条数据的查询请求(其中包含统计结果)，并缓存至本地文件夹中；第二次查询我们设置数量为 21 条，命令行工具将读取缓存的 20 条数据，并发起新的查询请求 1 条(实际为最小单位 20 条，其中也包含统计结果)，第一次查询和第二次查询中间间隔一定的时间，这段时间间隔内由于 ZoomEye 周期性的扫描可能更新了该数据，导致出现了如上的数据不一致的情况，因此命令行工具将以新的统计结果为准。

![image-20210111111035187](../images/image-20210111111035187.png?lastModify=1610354602)

**3.为什么 ZoomEye-python 和浏览器搜索同一个 dork 数据总量可能会不一样？**  
`ZoomEye` 提供了两个搜索接口分别是 :  `/host/search` 和 `/web/search` ，在 `ZoomEye-python` 中只使用了 `/host/search` 。在多数情况下，host 接口所提供的数据可以覆盖 90% 以上甚至 100% 的数据，因此数据的准确性是可以保证的，而在 API 进行请求时，将消耗用户配额，如果要兼容两种接口的话，将会更多的消耗用户配额；因此在命令行工具中，只使用了 `/host/search` 接口进行搜索。

![image-20210111141028072](../images/image-20210111141028072.png?lastModify=1610354602)  
![image-20210111141114558](../images/image-20210111141114558.png?lastModify=1610354602)

**4.通过 info 命令获取配额信息可能和浏览器端不一致？**   
浏览器端显示了免费额度和充值额度(<https://www.zoomeye.org/profile/record>)，而在 `ZoomEye-python` 中仅显示了免费额度的信息，我们将在后续版本修复这一问题。

### 0x07 404StarLink Project

![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

ZoomEye-python 是 404Team [星链计划](https://github.com/knownsec/404StarLink-Project) 中的一环，如果对 ZoomEye-python 有任何疑问又或是想要找小伙伴交流，可以参考星链计划的加群方式。

- [https://github.com/knownsec/404StarLink-Project#community](https://github.com/knownsec/404StarLink-Project#community)

</br>

---------------------------------
References:  
<https://www.zoomeye.org/doc>  

knownsec 404  
Time: 2021.01.12


## **ZoomEye API**

[![Python 2.x|3.x](https://img.shields.io/badge/python-2.x|3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://github.com/ZoomEye/SDK/blob/master/LICENSE) 

[**ZoomEye**](https://www.zoomeye.org/) is a search engine for cyberspace that lets the user find specific network components(ip, services, etc.).

[**ZoomEye API**](https://www.zoomeye.org/api/doc) is a web service that provides convenient access to [**ZoomEye**](https://www.zoomeye.org/) features, data, information over HTTPS. The platform API empowers developers to automate, extend and connected with [**ZoomEye**](https://www.zoomeye.org/). You can use the [**ZoomEye**](https://www.zoomeye.org/) platform API to programmatically create apps, provision some add-ons and perform some automate tasks. Just imagine that what you could do amazing stuff with [**ZoomEye**](https://www.zoomeye.org/).


### **How to install ZoomEye SDK**

```
$ sudo easy_install zoomeye-SDK
```

or

```
$ sudo pip install git+https://github.com/knownsec/ZoomEye.git
```

### **How to use ZoomEye SDK**

locate **zoomeye.py**, and try to execute it as follow:

```
# use API-KEY
$ python zoomeye.py
ZoomEye API-KEY(If you don't use API-KEY , Press Enter): 3******f-b**9-a***c-3**5-28******fd8
ZoomEye Username: 
ZoomEye Password:
{'plan': 'developer', 'resources': {'search': 9360, 'stats': 100, 'interval': 'month'}}
ec2-1*7-**-***-116.compute-1.amazonaws.com ['1*7.**.***.116']
myh****life.com ['**.35.*.5']
...
113.**.**.161 1611
113.**.***.63 1611
...

or

# use username and password to login
$ python zoomeye.py
ZoomEye API-KEY(If you don't use API-KEY , Press Enter): 
ZoomEye Username: username@zoomeye.org
ZoomEye Password:
{'plan': 'developer', 'resources': {'search': 9280, 'stats': 100, 'interval': 'month'}}
ec2-1*7-**-***-116.compute-1.amazonaws.com ['1*7.**.***.116']
myh****life.com ['**.35.*.5']
...
113.***.*.35 1611
113.***.**.162 1611
...
```

**zoomeye.py** can be also a library. You can choose to log in with your account **Username** and **Password** or use **API-KEY** to search. **API-KEY** can be found `https://www.zoomeye.org/profile`. ex:

```
>>> zm = zoomeye.ZoomEye(username=username, password=password)
or
>>> zm = zoomeye.ZoomEye(api_key="3******f-b**9-a***c-3**5-28******fd8")
```

```
$ python3
Python 3.8.5 (default, Aug 19 2020, 14:11:20)
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import zoomeye
>>> dir(zoomeye)
['ZoomEye', '__author__', '__builtins__', '__cached__', '__classes__', '__description__', '__doc__', '__file__', '__funcs__', '__license__', '__loader__', '__name__', '__package__', '__spec__', '__version__', 'getpass', 'raw_input', 'requests', 'show_ip_port', 'show_site_ip', 'sys', 'zoomeye_api_test']
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


>>> # Use API-KEY
>>> zm = zoomeye.ZoomEye(api_key="3******f-b**9-a***c-3**5-28******fd8")
>>> data = zm.dork_search('apache country:cn')
>>> zoomeye.show_site_ip(data)
213.***.***.46.rev.vo***one.pt ['46.***.***.213']
me*****on.o****e.net.pg ['203.***.***.114']
soft********63221110.b***c.net ['126.***.***.110']
soft********26216022.b***c.net ['126.***.***.22']
soft********5084068.b***c.net ['126.***.***.68']
soft********11180040.b***c.net ['126.***.***.40']
```

### **How to use ZoomEye API**

**1. Authenticate**

If a valid ZoomEye credential (username and password), please use the credential for authentication.

```
curl -XPOST https://api.zoomeye.org/user/login -d
'{
    "username": "foo@bar.com",
    "password": "foobar"
}'
```

**2. ZoomEye Dorks**

When everything goes ok, you can try to search [**ZoomEye Dorks**](https://www.zoomeye.org/component) with **ZoomEye API Token**.

```
curl -X GET https://api.zoomeye.org/host/search?query="port:21"&page=1&facet=app,os \
-H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5..."
```

If you want more, please access [ZoomEye API References](https://www.zoomeye.org/doc).

### **Change Log**
| version | date | detail | 
| -- | -- | -- |
|1.0.6   |10 Nov 2020   |Add API-KEY usage<br>Change default search resource type to "host"|


### **Links**

https://www.zoomeye.org/  
https://www.zoomeye.org/doc

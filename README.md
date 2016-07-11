[**ZoomEye**](https://www.zoomeye.org/) is a search engine for cyberspace that lets the user find specific network components(ip, services, etc.). 


## **ZoomEye API**

[**ZoomEye API**](https://www.zoomeye.org/api/doc) is a web service that provides convenient access to [**ZoomEye**](https://www.zoomeye.org/) features, data, information over HTTPS. The platform API empowers developers to automate, extend and connected with [**ZoomEye**](https://www.zoomeye.org/). You can use the [**ZoomEye**](https://www.zoomeye.org/) platform API to programmatically create apps, provision some add-ons and perform some automate tasks. Just imagine that what you could do amazing stuff with [**ZoomEye**](https://www.zoomeye.org/).

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

When everything goes ok, you can try to search [**ZoomEye Dorks**](https://www.zoomeye.org/search/dorks) with [**ZoomEye API Token**]().

```
curl -X GET https://api.zoomeye.org/host/search?query="port:21"&page=1&facet=app,os \
-H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5..."
```

If you want more, please access [ZoomEye API References](https://www.zoomeye.org/api/doc). 


**3. ZoomEye API ThirdParty Interfaces**

If you just want to use it, please try ZoomEye API ThirdParty interfaces created by ZoomEye users from github / bitbucket / ...

**4. Python Demo**

```
$ python zoomeye.py
ZoomEye Username: username@zoomeye.org
ZoomEye Password:
{u'plan': u'developer', u'resources': {u'host-search': 4993, u'web-search': 4963}}
(u'recordrating.com', [u'85.214.142.88'])
(u'receiver.sematext.com', [u'54.227.253.0'])
...
(u'42.159.226.69', 8080)
(u'42.62.7.177', 8080)
...
```

**zoomeye.py** can be also a library.

```
$ python
Python 2.7.10 (default, Oct 23 2015, 19:19:21)
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import zoomeye
>>> dir(zoomeye)
['ZoomEye', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'getpass', 'requests', 'show_ip_port', 'show_site_ip', 'zoomeye_api_test']
>>> zm = zoomeye.ZoomEye()
>>> zm.username = 'username@zoomeye.org'
>>> zm.password = 'password'
>>> print(zm.login())
....JIUzI1NiIsInR5cCI6IkpXVCJ9.....
>>> zm.search('apache country:cn')
>>> data = zm.dork_search('apache country:cn')
>>> zoomeye.show_site_ip(data)
(u'scottlyl.b2b.hc360.com', [u'123.103.76.181'])
(u'scottie.net114.com', [u'59.39.7.61'])
(u'scott.gsegment.com', [u'159.226.88.23'])
(u'scott888.blog.bokee.net', [u'60.191.119.184'])
(u'scott.zgbfw.com', [u'61.164.149.91'])
(u'scotsuka.com', [u'218.89.2.250'])
(u'scotsman.b2b.hc360.com', [u'123.103.76.181'])
(u'scoto.poco.cn', [u'14.18.242.214'])
(u'scotland.h.baike.com', [u'124.243.228.178'])
(u'scotland.baike.com', [u'124.243.228.178'])
```

**Links**

https://www.zoomeye.org/  
https://www.zoomeye.org/api/doc

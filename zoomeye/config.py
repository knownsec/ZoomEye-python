#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: config.py
* Description: command tool config
* Time: 2020.11.30
* Author: wh0am1i
*/
"""
from zoomeye import __version__, __site__

seconds_of_fiveday = 60 * 60 * 24 * 5

# save api key file and json web token file path
ZOOMEYE_CONFIG_PATH = "~/.config/zoomeye/setting"

# save search dork data path
ZOOMEYE_CACHE_PATH = "~/.config/zoomeye/cache"

# cache expired time, five day
EXPIRED_TIME = seconds_of_fiveday

# print data max length
STRING_MAX_LENGTH = 23

# cache file name
FILE_NAME = "/{}_{}.json"


RADIUS = 7

CHARACTER = "# "

BLANK = "  "

COLOR_TABLE = ["\x1b[90m", "\x1b[91m", "\x1b[92m", "\x1b[93m", "\x1b[94m", "\x1b[95m", "\x1b[96m", "\x1b[97m",
               "\x1b[91m", "\x1b[92m"]

COLOR_RESET = "\x1b[0m"

BANNER = """\033[01;33m
         ,----,                                                                 
       .'   .`|                            ____      ,---,.                     
    .'   .'   ;                          ,'  , `.  ,'  .' |                     
  ,---, '    .' ,---.     ,---.       ,-+-,.' _ |,---.'   |                     
  |   :     ./ '   ,'\   '   ,'\   ,-+-. ;   , |||   |   .'                     
  ;   | .'  / /   /   | /   /   | ,--.'|'   |  ||:   :  |-,      .--,   ,---.    \033[01;37m{%s }\033[01;33m
  `---' /  ; .   ; ,. :.   ; ,. :|   |  ,', |  |,:   |  ;/|    /_ ./|  /     \  
    /  ;  /  '   | |: :'   | |: :|   | /  | |--' |   :   .' , ' , ' : /    /  | 
   ;  /  /--,'   | .; :'   | .; :|   : |  | ,    |   |  |-,/___/ \: |.    ' / | 
  /  /  / .`||   :    ||   :    ||   : |  |/     '   :  ;/| .  \  ' |'   ;   /|  
./__;       : \   \  /  \   \  / |   | |`-'      |   |    \  \  ;   :'   |  / | 
|   :     .'   `----'    `----'  |   ;/          |   :   .'   \  \  ;|   :    |  
;   |  .'                        '---'           |   | ,'      :  \  \\   \  /  \033[01;37m %s \033[01;33m
`---'                                            `----'         \  ' ; `----'   
                                                                 `--`           \033[0m\033[4;37m\033[0m

""" % (__version__, __site__)

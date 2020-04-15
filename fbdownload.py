import requests
import re
import urllib
import sys
import os
import time
# https://www.facebook.com/519691891892331/videos/2354691294789484/
name = """\033[1;32;40m
____________________________________________________________
\033[1;36;40m         _____ ____        ____
\033[1;34;40m        |  ___| __ )      |  _ \  _____      ___ __
\033[1;36;40m        | |_  |  _ \ _____| | | |/ _ \ \ /\ / / '_ \ 
\033[1;34;40m        |  _| | |_) |_____| |_| | (_) \ V  V /| | | |
\033[1;36;40m        |_|   |____/      |____/ \___/ \_/\_/ |_| |_|
\033[1;35;40m              [+] Created By Dimal & Hasinthaka
\033[1;32;40m____________________________________________________________
"""
try:
    os.system('mkdir -p /sdcard/FB-VIdeo-Slcoders')
    os.system('clear')
    print(name)
except:
    os.system('clear')
    print(name)
class Stream:
    def __init__(self, url, path, name):
        self.url = url
        self.path = path
        self.name = name
        self.response = requests.get(self.url, stream=True)
        self.total_length = int(self.response.headers.get('content-length'))
        self.start = 0
        self.end = 0
        self.t = 0
    def download(self):
        print('\033[1;0;40m{0} MB \n'.format(int(int(self.total_length)/1024**2)))
        with open(os.path.join(self.path, self.name), 'wb') as f:
            if self.total_length is None:
                f.write(self.response.content)
            else:
                dl = 0
                chnk = int(self.total_length/100)
                for data in self.response.iter_content(chunk_size=chnk):
                    # calculate Duration
                    self.time_dur = time.time() - self.start
                    self.start = time.time()
                    if self.time_dur == time.time():
                        self.time_dur = 0.000001
                    dl += len(data)
                    f.write(data)
                    donedl = int((dl/self.total_length)*100)
                    speed = (len(data)/1024)/self.time_dur
                    print('\n->> \033[1;36;40m{0}% - {1} kbps'.format(donedl,
                                                                         round(speed, 3)), end="")
                    sys.stdout.write("\033[F")
def part2(link):
    parse = urllib.parse.urlparse(link).path.split('/')
    dName = '{0}-{1}-{2}.mp4'.format(parse[1], parse[2], parse[3])
    dPath = '/sdcard/FB-VIdeo-Slcoders'
    html = requests.get(link)
    try:
        url = re.search('hd_src:"(.+?)"', html.text)[1]
        print('\n High Q', end=" - ")
    except:
        url = re.search('sd_src:"(.+?)"', html.text)[1]
        print('\n Normal Q', end=" - ")
    response = requests.get(url, stream=True)
    video = Stream(url, dPath, dName)
    video.download()
    l()
lst = []
def run():
    link = input('\033[1;32;40m [+] Link \n :')
    lst.append(link)
    for lnk in lst:
        part2(lnk)
def l():
    exit = input('\033[1;0;40m [+] Do You Want To Download Video (y/n) : ')
    if exit == 'n' or exit == 'N':
        break
    else:
        run()
l()

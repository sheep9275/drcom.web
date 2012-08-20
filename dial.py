#!/usr/bin python
# -*- coding: utf-8 -*-

import urllib, urllib2
import time
import sys
import re

class Drcom():
    option = {
            'remote' : 'http://192.168.168.168/',
            'logout' : 'F.htm',
            'sleep' : 30,
    }
    param = {}

    def __init__(self):
        self.param = urllib.urlencode({'DDDDD' : sys.argv[1], 'upass' : sys.argv[2], '0MKKey' : '%B5%C7%C2%BC+Login'})

    def do_response(self, data):
        errinfo = {
                1 : 'login failed: wrong username or password!',
                4 : 'login failed: insufficient balance!',
                14 : 'logout successed!',
                'default' : 'uncatched error!'
                }

        try : errno = int(re.search(r'Msg=([0-9]+)', data).group(1))
        except: errno = -1;

        uidptr = data.find(sys.argv[1])
        unfmttime = time.localtime(time.time())
        ltime = time.strftime("%Y-%m-%d %H:%M", unfmttime)

        if errno == -1 and uidptr != -1:
            print 'login successed! @', ltime
            return True

        if errno in errinfo:
            print errinfo[errno],
        else:
            print errinfo['default'],
        print '@', ltime
        return False

    def logout(self):
        doc = urllib2.urlopen(self.option['remote'] + self.option['logout'])
        self.do_response(doc.read())

    def login(self):
        while True:
            doc = urllib2.urlopen(self.option['remote'], data = self.param)
            if not self.do_response(doc.read()):
                sys.exit(-1);
            time.sleep((self.option['sleep'] - 2) * 60)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'argv reads error!'
        sys.exit(-1)

    client = Drcom()

    try : client.login()
    except KeyboardInterrupt : client.logout()

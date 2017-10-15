import subprocess
from time import sleep
import requests
import re

class VPNDial():
    def __init__(self,user, password, dial= 'test'):
        self.dial = dial
        self.user = user
        self.password = password
        self._connect = ['rasdial', self.dial, self.user, self.password]
        self._disconnect = ['rasdial',self.dial, '/disconnect']

    def connect(self):
        popen = subprocess.Popen(self._connect,stdout=subprocess.PIPE)
        data,error = popen.communicate()
        return 0 if not error else 1

    def disconnect(self):
        popen = subprocess.Popen(self._disconnect, stdout=subprocess.PIPE)
        data, error = popen.communicate()
        return 0 if not error else 1

    def getstatus(self):
        popen = subprocess.Popen('rasdial', stdout=subprocess.PIPE)
        data, error = popen.communicate()
        data = data.decode('gbk')
        return 0 if '已连接' in data else 1



if __name__ == '__main__':
    ip = set()
    VPN = VPNDial('txtz', '111')
    while True:
        while VPN.getstatus() == 1:
            VPN.connect()
            sleep(3)
        req = requests.get('http://2017.ip138.com/ic.asp')
        if req.ok:
            data = re.search('\[([0-9\.]+)\]',req.text)
            ip.add(data.group(1))
        print('the length is: %5d' % len(ip))
        VPN.disconnect()






import json
import sys
import time
from urllib import request

from lxml import etree


def toTB(string):
  parts = string.split(' ')
  if parts[1] == 'TB' or parts[1] == 'TiB' or parts[1] == '烫':
    return parts[0]
  if parts[1] == 'GB' or parts[1] == 'GiB':
    return str(float(parts[0]) / 1024)
  if parts[1] == 'MB' or parts[1] == 'MiB':
    return str(float(parts[0]) / 1024 / 1024)
  if parts[1] == 'KB' or parts[1] == 'KiB':
    return str(float(parts[0]) / 1024 / 1024 / 1024)
  
def u2(url, cookie):
  req = request.Request(url)
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
        if f.status != 200:
          return ['0', '0', '0', '0']
        else:
          try:
            content = f.read().decode('utf-8')
            tree = etree.HTML(content)
            ratio = tree.xpath('//span[@class="color_ratio"]')[0].tail.strip();
            upload = toTB(tree.xpath('//span[@class="color_uploaded"]')[0].tail.strip());
            downloaded = toTB(tree.xpath('//span[@class="color_downloaded"]')[0].tail.strip());
            point = tree.xpath('//span[@class="ucoin-symbol ucoin-gold"]')[0].text.strip();
            return [ratio, upload, downloaded, point]
          except:
            return ['0', '0', '0', '0']
def ttg(url, cookie):
  req = request.Request(url)
  req.add_header('user-agent', 'python urllib')
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
        if f.status != 200:
           return ['0', '0', '0', '0']
        else:
          try:
            content = f.read().decode('utf-8')
            tree = etree.HTML(content)
            font = tree.xpath('//td[@class="bottom"]/span[@class="smallfont"][1]/font')
            ratio = font[1].text
            upload = toTB(font[3].xpath('./a')[0].text)
            download = toTB(font[5].xpath('./a')[0].text)
            point = tree.xpath('//td[@class="bottom"]/a')[0].text
            return [ratio, upload, download, point]
          except:
            return ['0', '0', '0', '0']

def pter(url, cookie):
  req = request.Request(url)
  req.add_header('cookie', cookie)
  req.add_header('user-agent', 'python urllib')
  with request.urlopen(req) as f:
        if f.status != 200:
          return ['0', '0', '0', '0']
        else:
          try:
            content = f.read().decode('utf-8')
            tree = etree.HTML(content)
            ratio = tree.xpath('//font[@class="color_ratio"]')[0].tail.strip();
            upload = toTB(tree.xpath('//font[@class="color_uploaded"]')[0].tail.strip());
            downloaded = toTB(tree.xpath('//font[@class="color_downloaded"]')[0].tail.strip());
            point = tree.xpath('//span[@class="medium"]/span[@class="color_bonus"]')[0].tail.strip()
            return [ratio, upload, downloaded, point]
          except:
            return ['0', '0', '0', '0']

def mt_updateLastBrowse(url, authorization):          
  req = request.Request(url + '/updateLastBrowse', method="POST")
  req.add_header('authorization', authorization)
  req.add_header('user-agent', 'python urllib')
  with request.urlopen(req) as f:
    content = f.read().decode('utf-8')

def mt(url, authorization):
  mt_updateLastBrowse(url, authorization)
  req = request.Request(url + '/profile', method="POST")
  req.add_header('authorization', authorization)
  req.add_header('user-agent', 'python urllib')
  with request.urlopen(req) as f:
        if f.status != 200:
          return ['0', '0', '0', '0']
        else:
          try:
            content = f.read().decode('utf-8')
            resp = json.loads(content)
            ratio = str(resp['data']['memberCount']['shareRate'])
            upload = toTB(str(int(resp['data']['memberCount']['uploaded']) / 1024) + ' KB')
            download = toTB(str(int(resp['data']['memberCount']['downloaded']) / 1024) + ' KB')
            point = str(resp['data']['memberCount']['bonus'])
            return [ratio, upload, download, point]
          except Exception as e:
            print("Error while processing response data:", e)
            return ['0', '0', '0', '0']

def haidan(url, cookie):
  req = request.Request(url)
  req.add_header('cookie', cookie)
  req.add_header('user-agent', 'python urllib')
  with request.urlopen(req) as f:
        if f.status != 200:
          return ['0', '0', '0', '0']
        else:
          try:
            content = f.read().decode('utf-8')
            tree = etree.HTML(content)
            ratio = tree.xpath('//font[@class="color_ratio"]')[0].tail.strip();
            upload = toTB(tree.xpath('//font[@class="color_uploaded"]')[0].tail.strip());
            downloaded = toTB(tree.xpath('//font[@class="color_downloaded"]')[0].tail.strip());
            point = tree.xpath('//span[@id="magic_num"]')[0].text.split('(')[0]
            return [ratio, upload, downloaded, point]
          except:
            return ['0', '0', '0', '0']


def main(argv):
  r1 = u2(argv[1], argv[2])
  r2 = ttg(argv[3], argv[4])
  r3 = pter(argv[5], argv[6])
  r4 = mt(argv[7], argv[8])
  r5 = haidan(argv[9], argv[10])
  r = time.strftime("%Y%m%d", time.localtime()) + " u:" + "|".join(r1) + " t:" + "|".join(r2) + " p:" + "|".join(r3) + " m:" + "|".join(r4) + " h:" + "|".join(r5)
  with open('data.txt', 'a') as file:
     file.write(r + '\n')
  

if __name__ == '__main__':
  main(sys.argv)

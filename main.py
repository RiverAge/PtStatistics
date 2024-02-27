import sys
import time
from urllib import request
from lxml import etree

def toTB(string):
  parts = string.split(' ')
  if parts[1] == 'TB' or parts[1] == 'TiB':
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
          return [0, 0, 0]
        else:
          content = f.read().decode('utf-8')
          tree = etree.HTML(content)
          ratio = tree.xpath('//span[@class="color_ratio"]')[0].tail.strip();
          upload = toTB(tree.xpath('//span[@class="color_uploaded"]')[0].tail.strip());
          downloaded = toTB(tree.xpath('//span[@class="color_downloaded"]')[0].tail.strip());
          return [ratio, upload, downloaded]
def ttg(url, cookie):
  req = request.Request(url)
  req.add_header('user-agent', 'python urllib')
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
        if f.status != 200:
           return [0, 0, 0]
        else:
          content = f.read().decode('utf-8')
          tree = etree.HTML(content)
          span = tree.xpath('//td[@class="bottom"]/span[@class="smallfont"][1]/font')
          ratio = span[1].text
          upload = toTB(span[3].xpath('./a')[0].text)
          download = toTB(span[5].xpath('./a')[0].text)
          return [ratio, upload, download]

def pter(url, cookie):
  req = request.Request(url)
  req.add_header('cookie', cookie)
  req.add_header('user-agent', 'python urllib')
  with request.urlopen(req) as f:
        if f.status != 200:
          return [0, 0, 0]
        else:
          content = f.read().decode('utf-8')
          tree = etree.HTML(content)
          ratio = tree.xpath('//font[@class="color_ratio"]')[0].tail.strip();
          upload = toTB(tree.xpath('//font[@class="color_uploaded"]')[0].tail.strip());
          downloaded = toTB(tree.xpath('//font[@class="color_downloaded"]')[0].tail.strip());
          return [ratio, upload, downloaded]  

def main(argv):
  r1 = u2(argv[1], argv[2])
  r2 = ttg(argv[3], argv[4])
  r3 = pter(argv[5], argv[6])
  r = time.strftime("%Y%m%d", time.localtime()) + " u:" + "|".join(r1) + " t:" + "|".join(r2) + " p:" + "|".join(r3)
  with open('data.txt', 'a') as file:
     file.write(r + '\n');

if __name__ == '__main__':
  main(sys.argv)

import sys
import time
from urllib import request
from lxml import etree

def u2(cookie):
  req = request.Request('https://u2.dmhy.org')
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
        if f.status != 200:
          return [0, 0, 0]
        else:
          content = f.read().decode('utf-8')
          print('content', content)
          tree = etree.HTML(content)
          ratio = tree.xpath('//span[@class="color_ratio"]')[0].tail.strip();
          upload = tree.xpath('//span[@class="color_uploaded"]')[0].tail.strip().split(' ')[0];
          downloaded = tree.xpath('//span[@class="color_downloaded"]')[0].tail.strip().split(' ')[0];
          return [ratio, upload, downloaded]
def ttg(cookie):
  req = request.Request('https://totheglory.im')
  req.add_header('user-agent', 'python urllib')
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
        if f.status != 200:
           return [0, 0, 0]
        else:
          content = f.read().decode('utf-8')
          print('content', content)
          tree = etree.HTML(content)
          span = tree.xpath('//td[@class="bottom"]/span[@class="smallfont"][1]/font')
          ratio = span[1].text
          upload = span[3].xpath('./a')[0].text.split(' ')[0]
          download = span[5].xpath('./a')[0].text.split(' ')[0]
          return [ratio, upload, download]
def main(argv):
  print("argv1", len(argv))
  r1 = u2(argv[1])
  r2 = ttg(argv[2])
  r = time.strftime("%Y%m%d", time.localtime()) + " u:" + "|".join(r1) + " t:" + "|".join(r2)
  with open('data.txt', 'a') as file:
     file.write(r + '\n');

if __name__ == '__main__':
  main(sys.argv)

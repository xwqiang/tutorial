# coding:utf-8

import scrapy
import os
import urllib
import zlib


class Comics(scrapy.Spider):
    name = "xiaoming"

    """
    开始
    """

    def start_requests(self):
        urls = ['http://www.dmzj.com/info/xiaoming.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """获取剧情列表"""

    def parse(self, response):
        # 请求返回的html源码
        content = response.body;
        if not content:
            self.log('parse body error.')
            return

        # 找到页面中的连接：如http://www.hanhande.com/manhua/op/1156067.shtml
        url_list = response.xpath('//div[@class="tab-content tab-content-selected zj_list_con autoHeight"]//ul[@class="list_con_li autoHeight"]/li//a/@href').extract()
        if not url_list:
            self.log('no urls found')
            return
        for url in url_list:
            print(url)
            yield scrapy.Request(url=url, callback=self.cartoon_parse)

    """获取每一集的所有漫画"""

    def cartoon_parse(self, response):
        content = response.body;
        if not content:
            self.log('parse comics body error.')
            return;
        # 找到图片连接地址

        img_url = response.xpath('//div[class="btmBtnBox"]//select[@id="page_select"]/option/@value')
        print('imgurl:',img_url)
        # for img in img_url:
        #     print(img)
            # self.saveImg(self,img,'img',img.split('/')[-1])




    def saveImg(self, img, folder, name):
        # 保存漫画的文件夹
        document = '/Users/xuwuqiang/Documents/cartoon/xiaoming/' + folder

        # 每部漫画的文件名以标题命名
        exists = os.path.exists(document)
        if not exists:
            os.makedirs(document)

        # 每张图片以页数命名
        pic_name = document + '/' + name
        print('pic name :', pic_name)

        # 检查图片是否已经下载到本地，若存在则不再重新下载
        exists = os.path.exists(pic_name)
        if exists:
            self.log('pic exists: ' + pic_name)
            return
        try:
            response = urllib.request.urlopen(img)

            # 请求返回到的数据
            data = response.read()
            # 若返回数据为压缩数据需要先进行解压
            if response.info().get('Content-Encoding') == 'gzip':
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

            # 图片保存到本地
            fp = open(pic_name, "wb")
            fp.write(data)
            fp.close

            self.log('save image finished:' + pic_name)

        # urllib.request.urlretrieve(img_url, pic_name)
        except Exception as e:
            self.log('save image error.')
            print('error on saving')
            self.log(e)

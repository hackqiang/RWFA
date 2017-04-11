#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: hackqiang
# version 0.1
# requirement: python2.7 BeautifulSoup lxml

import lxml.html.soupparser as soupparser
import lxml.etree as etree
import re


def genitem(title, post_time, text, tags, cats):
    #print id
    '''
	<item>
		<title>测试恢复XML11</title>
		<dc:creator><![CDATA[qiang]]></dc:creator>
		<description></description>
		<content:encoded><![CDATA[测试恢复ok？<br>测试恢复2ok？]]></content:encoded>
		<wp:post_date><![CDATA[2017-04-10 22:40:56]]></wp:post_date>
		<wp:comment_status><![CDATA[closed]]></wp:comment_status>
		<wp:post_name><![CDATA[测试恢复XML11]]></wp:post_name>
		<wp:status><![CDATA[publish]]></wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type><![CDATA[post]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="post_tag" nicename="测试tag"><![CDATA[测试tag]]></category>
		<category domain="category" nicename="%E6%B5%8B%E8%AF%95category"><![CDATA[测试category]]></category>
	</item>
    '''
    try:
        item = '''
	<item>
		<title>%s</title>
		<dc:creator><![CDATA[qiang]]></dc:creator>
		<description></description>
		<content:encoded><![CDATA[%s]]></content:encoded>
		<wp:post_date><![CDATA[%s]]></wp:post_date>
		<wp:comment_status><![CDATA[closed]]></wp:comment_status>
		<wp:post_name><![CDATA[%s]]></wp:post_name>
		<wp:status><![CDATA[publish]]></wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type><![CDATA[post]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
        ''' % (title, text, post_time, title)
    except Exception as e:
        print e
        return ''

    for tag in tags:
        item += '<category domain="post_tag" nicename="%s"><![CDATA[%s]]></category>' % (tag, tag)

    for cat in cats:
        item += '<category domain="category" nicename="%s"><![CDATA[%s]]></category>' % (cat, cat)

    item += '</item>'

    print item
    return item

def getText(elem):
    t = ''
    for node in elem.itertext():
        if node.strip():
            t += node.strip() + '\n'
    return t

def get_posttime(line):
    # 这篇文章发布于 2015年03月19日，21:33，归类于
    # return 2017-04-10 22:40:56
    nums = re.findall(r'\d+', line)
    try:
        t = '%s-%s-%s %s:%s:00' % (nums[0],nums[1],nums[2],nums[3],nums[4])
    except Exception as e:
        print e
        return ''
    return t
    
def post_parse(id, html):
    
    tree = etree.HTML(html)
    node = tree.xpath("//div[@id='post-%d']"%id)[0]
    node = tree.xpath("descendant::div[@id='post-%d']"%id)[0]
    if len(node):
        contents = getText(node)
        #print contents
        '''
        zRAM分析1：zram设备
zRAM虽然说出来的时间挺长的，但是细节的资料不是很多，我把这几天看到的东西记录下，也方便后人。
zRAM是依赖swap机制的，核心的思想就是将待写入swap分区的页面压缩后写入内存，就要就避免了实际的swap分区，并且速度也相对快，最最关键的是对于一些使用flash设备的友好。
zRAM的主要文件都在drivers/block/zram中，核心文件很少：
zram_drv.c
以及为了减少内存碎片使用的一个内存分配器：
zsmalloc.c
关于这个内存分配器，后面再说。
惯例从init看起：
标签：
kernel
,
zram
这篇文章发布于 2015年03月19日，21:33，归类于
kernel/drivers
,
Linux
。
您可以跳过直接留下评论。目前不允许Pinging。
        '''
        flag = 0
        title = ''
        text = ''
        post_time = ''
        tags = list()
        cats = list()
        #print contents.split('\n')
        for line in contents.split('\n'):
            #print line
            line = line.strip()
            if flag == 0:
                title = line
                flag = 1
            elif flag == 1:
                if line.startswith(u'标签：'):
                    flag = 2
                elif line.startswith(u'这篇文章发布于'):
                    post_time = get_posttime(line)
                    flag = 3
                else:
                    text += line + '\n'
            elif flag == 2:
                if line.startswith(u'这篇文章发布于'):
                    post_time = get_posttime(line)
                    flag = 3
                else:
                    if line == u',' or line == u'。':
                        pass
                    elif line:
                        tags.append(line)
            elif flag == 3:
                #print line
                if line.startswith(u'您可以跳过直接留下评论。'):
                    break
                if line == u',':
                    pass
                elif line == u'。':
                    break
                elif line:
                    cats.append(line)

        #print cats
        return genitem(title, post_time, text, tags, cats)

    return ''

    
if __name__ == "__main__":
    total = 0
    for id in range(1010):
        #id=1003
        try:
            f = open('data/posts_new/post_%d' % id, 'rb')
            html = f.read()
            if html:
                #print ('-%d-'% id)
                item = post_parse(id, html)
                if item:
                    total += 1
                #print '-'*100
        except:
            pass

    print total
    
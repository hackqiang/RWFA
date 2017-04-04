#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: hackqiang
# version 0.1
# requirement: python2.7 

import urllib2
import re
import os
import time
import pickle
import threading
import logging
import logging.handlers


snapshots = ('20110501062202', '20110217075705', '20110219070143', '20110320183632', '20110424010825', '20110601200410', '20110528043050', '20110628175310', '20110802083628', '20111009073439', '20111222084519', '20120222064808', '20120204001751', '20120312204721', '20120704232358', '20120423135855', '20120424191112', '20120711162113', '20120911141653', '20121111145115', '20130118111200', '20130425104951', '20130614095358', '20140126200211', '20140110234117', '20140330044628', '20140401152308', '20141218055018', '20150706001945', '20150827141633', '20151023164622', '20160208072304', '20160306075738', '20160409143852')

all_posts_list = list()

all_posts_db_file = 'data/all_posts'


def load_all_posts_list():
    global all_posts_list
    if os.path.exists(all_posts_db_file):
        f = open(all_posts_db_file, 'rb')
        all_posts_list = pickle.load(f)
        f.close()


def save_all_posts_list():
    global all_posts_list
    f = open(all_posts_db_file, 'wb')
    pickle.dump(all_posts_list, f)
    f.close()


def getHtml(url):
    html = ''
    error_code = 200
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
    try:
        response = urllib2.Request(url, headers=headers)
        f = urllib2.urlopen(response, data=None, timeout=5)
        html = f.read()
    except urllib2.HTTPError as e:
        logging.info(e.code)
        error_code = e.code
    except Exception as e:
        logging.info(e)
        error_code = 1
    #print html
    return error_code, html


def get_posts():
    while True:
        for post in all_posts_list:
            tf = 'data/posts/post_%d' % post
            if not os.path.exists(tf):
                for snapshot in snapshots:
                    url = 'https://web.archive.org/web/%s/http://qiang.ws/?p=%d' % (snapshot, post)
                    logging.info('parse %s' % url)
                    code, html = getHtml(url)
                    logging.debug(code)
                    logging.debug(html)
                    if code == 200:
                            with open(tf, 'wb') as f:
                                f.write(html)
                            continue
                    else:
                        logging.error('request %s fail' % url)
            else:
                logging.info('no need parse %s' % tf)
            time.sleep(3)
            
def get_posts_new():
    while True:
        for i in range(1004):
            tf = 'data/posts_new/post_%d' % i
            if not os.path.exists(tf):
                url = 'https://web.archive.org/web/http://qiang.ws/?p=%d' % i
                logging.info('get %s' % url)
                code, html = getHtml(url)
                logging.debug(code)
                logging.debug(html)
                if code == 200:
                    with open(tf, 'wb') as f:
                        f.write(html)
                        f.close()
                elif code == 404:
                    with open(tf, 'wb') as f:
                        f.write('404')
                        f.close()
                else:
                    logging.error('request %s fail' % url)
            else:
                logging.info('no need parse %s' % tf)
            time.sleep(1)


def get_pages():
    while True:
        for i in range(1,38):
            for snapshot in snapshots:
                tf = 'data/pages/page_%s_%d' % (snapshot, i)
                if not os.path.exists(tf):
                    if i == 1:
                        url = 'https://web.archive.org/web/%s/http://qiang.ws/' % (snapshot)
                    else:
                        url = 'https://web.archive.org/web/%s/http://qiang.ws/?paged=%d' % (snapshot, i)

                    logging.info('parse %s' % url)
                    code, html = getHtml(url)
                    logging.debug(code)
                    logging.debug(html)
                    if code == 200:
                        postlist = re.findall(re.compile('/http://qiang\.ws/\?p=(\d+)'), html)
                        logging.debug(postlist)
                        if postlist:
                            for post in postlist:
                                if post not in all_posts_list:
                                    all_posts_list.append(int(post))
                                    save_all_posts_list()

                            with open(tf, 'wb') as f:
                                f.write(html)
                            continue
                    else:
                        logging.error('request %s fail' % url)
                else:
                    logging.info('no need parse %s' % tf)
            time.sleep(3)


if __name__ == "__main__":
    if not os.path.exists('log'):
        os.mkdir('log')
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/pages'):
        os.mkdir('data/pages')
    if not os.path.exists('data/posts'):
        os.mkdir('data/posts')
    if not os.path.exists('data/posts_new'):
        os.mkdir('data/posts_new')

    logging.basicConfig(level=logging.INFO)
    handler = logging.handlers.RotatingFileHandler('log/main.log', maxBytes=1024*1024*10, backupCount=0)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(handler)

    load_all_posts_list()

    t = threading.Thread(target=get_pages, args=[])
    t.setDaemon(True)
    t.start()
    
    t = threading.Thread(target=get_posts, args=[])
    t.setDaemon(True)
    t.start()
    
    get_posts_new()

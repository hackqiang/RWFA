# RWFA
**R**ecovery **W**ordpress **F**rom **A**rchive.org

主要原理流程：
1. 从web.archive.org上抓blog页面
2. 分析blog页面，提取出文章信息
3. 生成支持wordpress导入的XML格式
4. 从wordpress后台导入XML

https://web.archive.org/web/http://qiang.ws/


http_proxy=192.168.1.3:1080 ./main.py
./postparse.py


今天发现直接请求：
https://web.archive.org/web/http://qiang.ws/?p=888
不用care snapshot了 :)


finish：
1. 标题和内容
2. 发布时间
3. 标签和分类

not finish(估计不会修复了）：
1.文章格式
2.评论
mailRemind
===========================================

使用python语言编写的bitmex委托成交监控并邮件通知程序

通过ccxt框架调用bitmex的get position方法，解析到当前仓位，当仓位变化时发送提醒到指定邮箱

新增爬取苹果官网翻新Ipad有货提醒

在mailbox.txt中配置好要发送到的邮箱、密码、smtp服务器、bitmex apikey和secret，然后执行对应.py即可

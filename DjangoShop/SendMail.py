"""
此脚本只作为邮件发送测试
"""
import smtplib  # 登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText  # 负责构建邮件格式

# 邮件主题
subject = "哗啦啦"
# 邮件内容
content = "哈哈，猜猜我是谁"
# 发送人
sender = "137****2@163.com"
# 接收人(一串)
recver = """bowende_xx@foxmail.com，
996623077@qq.com,
278658559@qq.com
1070649959@qq.com
738389368@qq.com"""

# 授权码
password = ""

# 构造MIMEText对象（邮件），第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性
message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

# 创建SMTP客户端对象，连接smtp服务器
smtp = smtplib.SMTP_SSL("smtp.163.com",994)
# 登录
smtp.login(sender,password)
# 发送邮件，第一个参数是发送人，第二个是接收人，必须是列表，第三个参数是邮件信息，将msg(MIMEText对象或者MIMEMultipart对象)变为str
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
# 关闭客户端连接
smtp.close()
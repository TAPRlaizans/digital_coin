import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHelper:
    def __init__(self) -> None:
        self.sender_email = "1165589123@qq.com"
        self.sender_password = "lqhxddetdwxxicci"
        self.recipient_email = "daip96286@gmail.com"  
        pass
    
    def send_email(self,subject, body):
        try:
            # 设置SMTP服务器及端口（以Gmail为例）
            smtp_server = "smtp.qq.com"
            smtp_port = 587

            # 创建邮件内容
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = subject

            # 添加邮件正文
            message.attach(MIMEText(body, "plain"))

            # 连接到SMTP服务器
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # 启用TLS加密
            server.login(self.sender_email, self.sender_password)  # 登录邮箱

            # 发送邮件
            server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            print("邮件发送成功！")

            # 关闭连接
            server.quit()

        except Exception as e:
            print(f"邮件发送失败：{e}")

# 示例调用
if __name__ == "__main__":
    subject = "测试邮件"
    body = "这是一封通过Python发送的测试邮件。"
    email_helper = EmailHelper()
    email_helper.send_email(subject, body)
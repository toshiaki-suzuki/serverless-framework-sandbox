import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def lambda_handler(event, context):
    # SES クライアントの初期化
    ses_client = boto3.client('ses')

    # メールの設定
    domain = os.environ['SENDER_EMAIL']
    sender = f"test@{domain}"
    recipient = os.environ['RECIPIENT_EMAIL']
    subject = 'Send email with attachment test'
    body_text = "This email was sent with Amazon SES using the AWS SDK for Python (Boto)."

    # メールの構築
    msg = MIMEMultipart()  # メール本文と添付ファイルをまとめる
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # メール本文の追加
    part = MIMEText(body_text, 'plain')
    msg.attach(part)

    # 添付ファイルの追加
    attachment = MIMEText("test attachment data", 'plain')
    attachment.add_header('Content-Disposition',
                          'attachment',
                          filename="test.txt")
    msg.attach(attachment)

    # メールの送信
    try:
        response = ses_client.send_raw_email(
            Source=sender,
            Destinations=[recipient],
            RawMessage={'Data': msg.as_string()}
        )
        return response
    except Exception as e:
        print(e)
        raise e

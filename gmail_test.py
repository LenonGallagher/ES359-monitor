import smtplib
from email.mime.text import MIMEText

# =====================
# 請修改這兩行
# =====================

GMAIL_ADDRESS = "lenonable2012@gmail.com"
APP_PASSWORD = "smgizmlrjrsigbrr"

# =====================

msg = MIMEText("ES359 Monitor 測試成功 🎸")
msg["Subject"] = "ES359 Monitor Test"
msg["From"] = GMAIL_ADDRESS
msg["To"] = GMAIL_ADDRESS

try:

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(
        GMAIL_ADDRESS,
        APP_PASSWORD
    )

    server.send_message(msg)

    server.quit()

    print("Email 發送成功！")

except Exception as e:

    print("錯誤：")
    print(e)
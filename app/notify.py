from email.message import EmailMessage
import smtplib

from app.ev import EV

addresses: list = ["ben.weddle@nashville.gov", "travis.humbert@nashville.gov", "cynthia.moynihan@nashville.gov"]

def send_mail_on_new_file_upload(filename: str):
    for address in addresses:
        message = "The following file has just been uploaded to the BF site: " + filename
        format = EmailMessage()
        format.set_content(message)
        format['Subject'] = "New File Upload: " + filename
        format['From'] = "ben.weddle@nashville.gov"
        format['To'] = address
        try:
            mail = smtplib.SMTP(host=EV().mail_server_external)
            mail.send_message(format)
            mail.quit()
        except ConnectionRefusedError as e:
            print(e)
        except TimeoutError as e:
            print(e)
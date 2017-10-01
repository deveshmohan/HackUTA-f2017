import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys
import ConfigParser


num_faces = int(sys.argv[1])
image = sys.argv[2]
time = sys.argv[3]

cfg = ConfigParser.SafeConfigParser()
cfg.read('email.cfg')

try:
    smtp_host = cfg.get('smtp', 'host')
    smtp_port = cfg.get('smtp', 'port')
    from_addr = cfg.get('smtp', 'from')
    to_addr = cfg.get('smtp', 'to')
except:
    sys.exit()

mail = MIMEMultipart()
mail.preamble = "The attached photo was taken at {0}, and contains {1} detected face(s).".format(
    time, num_faces
)

mail['Subject'] = '{0} faces detected in footage'.format(num_faces)
mail['From'] = from_addr
mail['To'] = to_addr

with open(image, 'rb') as image_file:
    attachment = MIMEImage(image_file.read())
    mail.attach(attachment)

print smtp_host
print smtp_port
smtp = smtplib.SMTP(smtp_host, smtp_port)

if cfg.has_section('login'):
    username = cfg.get('login', 'username')
    password = cfg.get('login', 'password')
    smtp.login(username, password)

smtp.sendmail(from_addr, to_addr, mail)
smtp.quit()

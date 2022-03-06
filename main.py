import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
#file for storing user details, like password
import config

now = datetime.datetime.now()
# email content placeholder
content = ''


# extracting Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:<b>\n' + '<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'vaglin': ''})):
        cnt += ((tag.text + "\n" ) if tag.text != 'More' else '')
    return cnt


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------------<br>')
content += ('<br><br>End of Message')


print('Composing email...')

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = config.sender
TO = config.receiver
PASS = config.password

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initializing Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent...')

server.quit()


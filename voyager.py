from html.parser import HTMLParser
import requests
from discord import Webhook, RequestsWebhookAdapter
import csv
import sys

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == 'a'):
            for attr in attrs:
                if('/view_video' in attr[1]):
                    videos.append(attr[1])

webhook_id = sys.argv[0]
webhook_token = sys.argv[1]
url = sys.argv[2]

webhook = Webhook.partial(webhook_id, webhook_token, adapter=RequestsWebhookAdapter())

req = requests.get(url)
videos = []
oldVideos = []
parser = MyHTMLParser()

#url = 'http://pornhub.com/gay/video/search?search="black+on+white"&o=mr'

parser.feed(req.text)

videos = list(dict.fromkeys(videos))

#webhook_token = 'Ginga07WcMI_c753IHQ3um0gBHkv1xQnLtHketxG1sBqrdzB-jybzooFqyCGosTvQCgN'
#webhook_id = 660467537749868545

with open('mostRecentVideos.csv', 'r+') as myfile:
    reader = csv.reader(myfile)
    oldVideos = list(reader)[0]

videoNumber = 0
while (not (videos[videoNumber] in oldVideos) and (videoNumber < (len(videos) - 1))):
    webhook.send('https://www.pornhub.com/' + videos[videoNumber], username='Voyager')
    videoNumber += 1

with open('mostRecentVideos.csv', 'w+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(videos[0:3])
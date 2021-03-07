import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="news V_Title_Img"]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)
                title[0] = title[0].replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open('{}/{}.txt'.format(today, title), 'w', encoding='utf-8') as f:
                f.write(title[0])
                f.write('\n\n')
                f.write(summary[0])
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError('Error: {}'.format(response.status_code))
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parser = html.fromstring(home)
            links_to_notices = parser.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError('Error: {}'.format(response.status_code))
    except ValueError as ve:
        pass

def run():
    parse_home()

if __name__ == '__main__':
    run()
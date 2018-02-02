import json
import re
from multiprocessing import Pool

import requests
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?class="name".*?data-val="{movieId:.*?">(.*?)</a>'
                         +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?</dd>',re.S)

    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'movie name': item[1],
            'actors': item[2].strip()[3:],
            'release time': item[3].strip()[5:],
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii= False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/6?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*5 for i in range(5)])
    pool.close()
    pool.join()

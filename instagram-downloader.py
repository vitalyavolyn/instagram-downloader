import requests
import os
from sys import argv

def download(url,local_filename):
    r = requests.get(url, stream=True)
    with open(os.getcwd()+"/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename

def main():
    url = argv[1]
    r = requests.get(url + '?__a=1')
    if r.headers['content-type'] != 'application/json':
        raise Exception('wrong link')
    print('Downloaing ' + r.json()['media']['owner']['username'] + '\'s photo')
    print('Dimensions: ' + str(r.json()['media']['dimensions']['width']) + 'x' + str(r.json()['media']['dimensions']['height']))
    print('Saved as ' + download(r.json()['media']['display_src'],r.json()['media']['code'] + '.jpg') + '!')

if __name__ == '__main__':
  main()

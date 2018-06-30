#!/usr/bin/python3
import requests
import os
from sys import argv

def download(url, local_filename):
    r = requests.get(url, stream=True)
    with open(os.getcwd()+"/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename

def main():
    url = argv[1]
    r = requests.get(url, params={'__a': 1})
    if (
        (r.headers['content-type'] != 'application/json') or
        (not 'graphql' in r.json())
    ):
        raise Exception('Wrong link')

    media = r.json()['graphql']['shortcode_media']
    if media['is_video']:
        print('Saved as ' + download(media['video_url'],
                                     media['shortcode'] + '.mp4') + '!')
    else:
        if media.get('edge_sidecar_to_children',None):
            print('Downloading mutiple images of this post')
            for child_node in media['edge_sidecar_to_children']['edges']:
                print('Saved as ' + download(child_node['node']['display_url'],
                                             child_node['node']['shortcode'] + '.jpg') + '!')
        else:
            print('Saved as ' + download(media['display_url'],
                                         media['shortcode'] + '.jpg') + '!')

if __name__ == '__main__':
    if len(argv) == 2:
        main()
    else:
        print('Usage: instagram-downloader.py link_to_photo')

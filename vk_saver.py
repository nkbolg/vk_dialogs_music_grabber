import os
from pathlib import Path
import vk_api
import requests
import argparse

MAX_COUNT = 200


def do_job(login, password, uid, odir):
    if not Path(odir).is_dir():
        os.mkdir(odir)
    vk_sess = vk_api.VkApi(login, password)
    try:
        vk_sess.auth(token_only=True)
    except vk_api.AuthError as error_msg:
            print(error_msg)
            return
    vk = vk_sess.get_api()
    start_from = ''
    while True:
        resp = vk.messages.getHistoryAttachments(peer_id=uid, media_type='audio', count=MAX_COUNT, offset=start_from)
        count = len(resp['items'])
        for elem in resp['items']:
            artist = elem['attachment']['audio']['artist']
            title = elem['attachment']['audio']['title']
            filename = os.path.join(odir, f'{artist} - {title}.mp3'.replace('/', ' '))
            p = Path(filename)
            print('Downloading', filename, '...', end='', flush=True)
            if p.is_file() and p.stat().st_size != 0:
                print('file already exist, skipping')
                continue

            url = elem['attachment']['audio']['url']
            if not url:
                print('no url, skipping')
                continue
            data = requests.get(url)
            with open(filename, 'wb') as fd:
                fd.write(data.content)
            print('success!')
        if count != MAX_COUNT:
            break
        start_from = resp['next_from']


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description="A tool for downloading all music from conversation at vk",
        usage="run vk_saver with the following parameters:"
              " login"
              " password"
              " conversation_id"
    )

    args_parser.add_argument("login", help="Email or phone number")
    args_parser.add_argument("password", help="Password")
    args_parser.add_argument("conversation_id", help="ID of the conversation, you want to download music from")
    args_parser.add_argument("--output_dir", help="Destination directory")
    args = args_parser.parse_args()
    do_job(args.login, args.password, args.conversation_id, args.output_dir)

import argparse
import os
from pathlib import Path

import requests
import vk_api

MAX_COUNT = 200


def process_items(resp, output_dir):
    for elem in resp["items"]:
        artist = elem["attachment"]["audio"]["artist"]
        title = elem["attachment"]["audio"]["title"]
        filename = os.path.join(output_dir, f"{artist} - {title}.mp3".replace("/", " "))
        print("Downloading", filename, "...", end="", flush=True)
        path = Path(filename)
        if path.is_file() and path.stat().st_size != 0:
            print("file already exist, skipping")
            continue

        url = elem["attachment"]["audio"]["url"]
        if not url:
            print("no url, skipping")
            continue
        data = requests.get(url)
        with open(filename, "wb") as datafile:
            datafile.write(data.content)
        print("success!")


def do_job(login, password, uid, output_dir):
    if not Path(output_dir).is_dir():
        os.mkdir(output_dir)
    vk_sess = vk_api.VkApi(login, password)
    try:
        vk_sess.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_session_api = vk_sess.get_api()
    start_from = ""
    while True:
        resp = vk_session_api.messages.getHistoryAttachments(
            peer_id=uid, media_type="audio", count=MAX_COUNT, offset=start_from
        )
        count = len(resp["items"])
        process_items(resp, output_dir)
        if count != MAX_COUNT:
            break
        start_from = resp["next_from"]


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        description="A tool for downloading all music from conversation at vk",
        usage="run vk_saver with the following parameters:"
        " login"
        " password"
        " conversation_id",
    )

    args_parser.add_argument("login", help="Email or phone number")
    args_parser.add_argument("password", help="Password")
    args_parser.add_argument(
        "conversation_id",
        help="ID of the conversation, you want to download music from",
    )
    args_parser.add_argument("--output_dir", help="Destination directory")
    args = args_parser.parse_args()
    do_job(args.login, args.password, args.conversation_id, args.output_dir)

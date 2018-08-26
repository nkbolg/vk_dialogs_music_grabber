# vk_dialogs_music_grabber

Simple script written in Python3 for dowloading music from vk.com conversations.

Installation:
Install packages for your environment using 
```pip install -r requirements.txt```

Usage:
```python vk_saver.py login password conversation_id```

positional arguments:
  login                 Email or phone number
  password              Password
  conversation_id       ID of the conversation, you want to download music
                        from

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Destination directory

import os
import json
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env
load_dotenv()

# Telegram API credentials from .env
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start the client and authenticate

    await client.start(phone=phone)
    print("Client connected!")

    # Replace 'friend_username' with your friend's Telegram username (e.g., '@username')
    friend = await client.get_entity('friend_username')

    # Fetch all messages (no limit)
    messages_data = []
    async for message in client.iter_messages(friend, limit=None):
        msg_dict = {
            'date': message.date.isoformat(),
            'sender_id': message.sender_id,
            'text': message.text or '',
            'has_link': False,
            'has_image': False,
            'has_video': False,
            'has_document': False,
            'has_music': False,
            'has_other_media': False,
            'links': []  # Store actual URLs if present
        }

        # Check for links in the text
        if message.text and message.entities:
            for entity in message.entities:
                if hasattr(entity, 'url'):
                    msg_dict['has_link'] = True
                    msg_dict['links'].append(entity.url)

        # Check for media types without downloading
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                msg_dict['has_image'] = True
            elif isinstance(message.media, MessageMediaDocument):
                doc = message.media.document
                if doc is not None:
                    mime_type = doc.mime_type
                    if 'video' in mime_type:
                        msg_dict['has_video'] = True
                    elif 'audio' in mime_type:
                        msg_dict['has_music'] = True
                    elif 'image' in mime_type:
                        msg_dict['has_image'] = True
                    else:
                        msg_dict['has_document'] = True
                else:
                    msg_dict['has_other_media'] = True
            elif isinstance(message.media, MessageMediaWebPage):
                msg_dict['has_link'] = True
            else:
                msg_dict['has_other_media'] = True

        messages_data.append(msg_dict)

    # Save to JSON file
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted {len(messages_data)} messages. Saved to chat_history.json")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())

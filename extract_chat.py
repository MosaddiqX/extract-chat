import os
import json
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
from datetime import datetime

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
    friend = await client.get_entity('@username')

    # Create a folder for media
    media_folder = 'chat_media'
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    # Fetch all messages (no limit)
    messages_data = []
    async for message in client.iter_messages(friend, limit=None):
        msg_dict = {
            'date': message.date.isoformat(),
            'sender_id': message.sender_id,
            'text': message.text or '',
            'media': None,
            'links': []
        }

        # Extract links from text
        if message.text:
            for entity in message.entities or []:
                if hasattr(entity, 'url'):
                    msg_dict['links'].append(entity.url)

        # Handle media (images, videos, etc.)
        if message.media:
            media_path = await message.download_media(file=media_folder)
            if media_path:
                msg_dict['media'] = media_path

        messages_data.append(msg_dict)

    # Save to JSON file
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted {len(messages_data)} messages. Saved to chat_history.json and media to {media_folder}")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())

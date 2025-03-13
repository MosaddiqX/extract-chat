import os
import json
import re
import argparse
from datetime import datetime
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

# Regular expression for emoji detection (covers common emojis)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
    "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
    "\U0001F700-\U0001F77F"  # Alchemical Symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE
)

def parse_args():
    """Parse command-line arguments for date filtering and keywords."""
    parser = argparse.ArgumentParser(description="Extract Telegram chat history with advanced features.")
    parser.add_argument('--start-date', type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument('--end-date', type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument('--keywords', type=str, default=None, help="Comma-separated keywords to search for")
    parser.add_argument('--username', type=str, required=True, help="Telegram username of the friend (e.g., @username)")
    return parser.parse_args()

async def main():
    args = parse_args()

    # Convert date strings to datetime objects if provided
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d') if args.start_date else None
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d') if args.end_date else None
    keywords = [kw.strip().lower() for kw in args.keywords.split(',')] if args.keywords else []

    # Start the client and authenticate
    await client.start(phone=phone)
    print("Client connected!")

    # Get the friend's entity
    friend = await client.get_entity(args.username)

    # Fetch messages with optional date filtering
    messages_data = []
    async for message in client.iter_messages(friend, limit=None):
        msg_date = message.date

        # Apply date filtering if specified
        if start_date and msg_date < start_date:
            continue
        if end_date and msg_date > end_date:
            continue

        msg_dict = {
            'date': msg_date.isoformat(),
            'sender_id': message.sender_id,
            'text': message.text or '',
            'has_link': False,
            'has_image': False,
            'has_video': False,
            'has_document': False,
            'has_music': False,
            'has_other_media': False,
            'links': [],
            'emojis': [],
            'is_question': False,
            'is_exclamation': False,
            'keywords_found': []  # New field for matched keywords
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

        # Extract emojis and check message type
        if message.text:
            # Emoji extraction
            emojis = EMOJI_PATTERN.findall(message.text)
            if emojis:
                msg_dict['emojis'] = emojis

            # Message type categorization
            if message.text.endswith('?'):
                msg_dict['is_question'] = True
            elif message.text.endswith('!'):
                msg_dict['is_exclamation'] = True

            # Keyword highlighting
            if keywords:
                text_lower = message.text.lower()
                matched_keywords = [kw for kw in keywords if kw in text_lower]
                if matched_keywords:
                    msg_dict['keywords_found'] = matched_keywords

        messages_data.append(msg_dict)

    # Save to JSON file
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted {len(messages_data)} messages. Saved to chat_history.json")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())

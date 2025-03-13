# Extract Chat

A sleek Python script to extract Telegram chat messages using the [Telethon](https://docs.telethon.dev/) library, with support for date and keyword filtering.

---

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Output](#output)
- [Notes](#notes)
- [Version 2 Updates](#version-2-updates)
- [Command-Line Arguments](#command-line-arguments)
- [Example](#example)
- [Telethon](#telethon)
- [Virtual Environment](#virtual-environment)

---

## Requirements

- **Python 3.11+**
- **Telethon**: `pip install telethon`
- **Environment Variables**: `API_ID`, `API_HASH`, `PHONE` in a `.env` file

---

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Create a `.env` file with your Telegram API credentials:
   ```makefile
   API_ID=your_api_id
   API_HASH=your_api_hash
   PHONE=your_phone_number
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the script with a Telegram username:
```bash
python extract_chat_v2.py --username @friend_username
```

Filter messages with optional arguments:
- `--start-date YYYY-MM-DD`
- `--end-date YYYY-MM-DD`
- `--keywords keyword1,keyword2`

The script connects to Telegram, authenticates, and retrieves messages from the specified chat.

---

## Output

A list of message dictionaries with these keys:

- `date`: Timestamp of the message (e.g., `"2023-01-15T10:00:00+00:00"`)
- `sender_id`: ID of the sender
- `text`: Message content
- `has_link`: `true` if a link is present
- `has_image`: `true` if an image is attached
- `has_video`: `true` if a video is attached
- `has_document`: `true` if a document is attached
- `has_music`: `true` if music is attached
- `has_other_media`: `true` if other media is present
- `links`: List of URLs in the message

---

## Notes

- Use a valid Telegram username for `--username`.
- Be cautious with large chats to avoid performance issues.

---

## Version 2 Updates

- **Date Filtering**: Limit messages with `--start-date` and `--end-date`.
- **Keyword Filtering**: Search with `--keywords`.
- **Enhanced Stability**: Better error handling and logging.

---

## Command-Line Arguments

| Argument       | Description                            | Format                  | Required |
|----------------|----------------------------------------|-------------------------|----------|
| `--username`   | Target Telegram username              | `@username`             | Yes      |
| `--start-date` | Start date for filtering              | `YYYY-MM-DD`            | No       |
| `--end-date`   | End date for filtering                | `YYYY-MM-DD`            | No       |
| `--keywords`   | Keywords to filter messages           | `keyword1,keyword2`     | No       |

---

## Example

Extract messages from `@friend_username` between Jan 1–31, 2023, with keywords "hello" or "world":
```bash
python extract_chat_v2.py --username @friend_username --start-date 2023-01-01 --end-date 2023-01-31 --keywords hello,world
```

**Sample Output**:
```json
[
  {
    "date": "2023-01-10T14:22:33+00:00",
    "sender_id": 987654321,
    "text": "Hello there!",
    "has_link": false,
    "has_image": false,
    "has_video": false,
    "has_document": false,
    "has_music": false,
    "has_other_media": false,
    "links": []
  }
]
```

---

## Telethon

Powered by [Telethon](https://docs.telethon.dev/), a Python library for seamless Telegram API interaction.

---

## Virtual Environment

Dependencies are managed in a `venv` directory for an isolated, reproducible setup.

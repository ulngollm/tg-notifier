from telethon import TelegramClient, events, functions
from pynotifier import Notification
from dotenv import load_dotenv

import asyncio
import os

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION')
selected_chats = os.getenv('CHATS').split(',') if os.getenv('CHATS') else None

client = TelegramClient(
    session_name,
    api_id,
    api_hash,
    connection_retries=2,
    request_retries=1
)


async def main():
    await client.start()
    await check_unread()

    @client.on(events.NewMessage(chats=selected_chats))
    async def my_event_handler(event):
        Notification(
            title=f"New messages in {event.chat.title}"
                  f"{' from' if event.message.sender.title != event.chat.title else ''}",
            description=f"{event.message.text}",
            urgency='normal',
        ).send()


async def check_unread():
    result = await client(functions.messages.GetPeerDialogsRequest(
        peers=selected_chats
    ))
    unread_messages = [dialog.unread_count for dialog in result.dialogs]
    Notification(
        title='Unread messages',
        description=f"You have {sum(unread_messages)} unread messages in chats {selected_chats}",
        urgency='normal'
    ).send()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

# pip install matrix-nio
# export MATRIX_PASSWORD=your-password


import os
from nio import AsyncClient, RoomMessageText, LoginResponse
import asyncio
import subprocess

async def send_matrix_message(homeserver, username, password, room_id, message):
    client = AsyncClient(homeserver, username)

    response = await client.login(password)

    if isinstance(response, LoginResponse):
        response = await client.room_send(
            room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )

        if not isinstance(response, RoomMessageText):
            print(f"Failed to send message: {response}")
        
        await client.close()
    else:
        print(f"Failed to log in: {response}")

rsync_command = "rsync -avz --progress source_directory destination_directory"

try:
    subprocess.check_call(rsync_command, shell=True)
except subprocess.CalledProcessError:
    matrix_password = os.getenv('MATRIX_PASSWORD')
    if not matrix_password:
        print("Matrix password not set in environment variable MATRIX_PASSWORD")
    else:
        asyncio.run(send_matrix_message("https://your-homeserver.com", "your-username", matrix_password, "!your-room-id:your-homeserver.com", "Rsync transfer failed!"))

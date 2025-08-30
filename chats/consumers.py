# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the current user from the scope
        self.user = self.scope['user']
        
        print(f"[Connect] Attempting to connect user: {self.user}")

        # Reject connection if user is not authenticated
        if not self.user.is_authenticated:
            print("[Connect] Connection REJECTED: User is not authenticated.")
            await self.close()
            return

        try:
            # Get the username of the other user from the URL
            other_username = self.scope['url_route']['kwargs']['username']
            self.other_user = await sync_to_async(User.objects.get)(username=other_username)

            # Prevent users from connecting to a chat with themselves
            if self.user == self.other_user:
                print(f"[Connect] Connection REJECTED: User {self.user} tried to connect with themselves.")
                await self.close()
                return

        except User.DoesNotExist:
            print(f"[Connect] Connection REJECTED: User '{other_username}' does not exist.")
            await self.close()
            return
        except Exception as e:
            print(f"[Connect] Connection REJECTED: An unexpected error occurred: {e}")
            await self.close()
            return

        # Create a unique and consistent room name by sorting the usernames
        sorted_usernames = sorted([self.user.username, self.other_user.username])
        self.room_group_name = f'chats_{sorted_usernames[0]}_{sorted_usernames[1]}'

        # Join the room group (the private chat channel)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"[Connect] Connection ACCEPTED for user {self.user.username} to room {self.room_group_name}")


    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"[Disconnect] User disconnected from room {self.room_group_name}")


    # This method is called when the server receives a message from the WebSocket
    async def receive(self, text_data):
        print(f"[Receive] Full message data: {text_data}")
        
        # --- Start of new robust error handling ---
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json['message']

            # Ignore empty messages
            if not message_content.strip():
                print("[Receive] Ignored empty message.")
                return
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Receive] ERROR: Received malformed message. Details: {e}")
            return
        # --- End of new robust error handling ---


        # Save the message to the database
        print("[Receive] Attempting to save message to database...")
        await self.save_message(message_content)
        print("[Receive] Message saved successfully.")

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # This calls the chat_message method below
                'message': message_content,
                'username': self.user.username
            }
        )

    # This method is called when a message is received from the room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send the message down to the client's WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, message_content):
        print(f"[DB] Saving message from {self.user.username} to {self.other_user.username}")
        # Create a new message object in the database
        Message.objects.create(
            sender=self.user,
            receiver=self.other_user,
            content=message_content,
            is_read=False
        )


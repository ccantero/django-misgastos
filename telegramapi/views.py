from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import os
import json

# Create your views here.


TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = os.getenv("TUTORIAL_BOT_TOKEN", "error_token")


def listener(request):

	if TUTORIAL_BOT_TOKEN == 'error_token':
		return HttpResponse("There is not TUTORIAL_BOT_TOKEN")

	if request.method == 'GET':
		return HttpResponse("You are listening!")

	if request.method == 'POST':
		t_data = json.loads(request.body)
		t_message = t_data["message"]
		t_chat = t_message["chat"]

		myTelegramMessage = TelegramMessage()
		myTelegramMessage.message = t_message
		myTelegramMessage.chat_id = t_chat
		myTelegramMessage.save()
		
		return JsonResponse({"ok": "POST request processed"}) 


def send_message(message, chat_id):
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(
        f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
    )	


# def post(self, request, *args, **kwargs):
#         t_data = json.loads(request.body)
#         t_message = t_data["message"]
#         t_chat = t_message["chat"]

#         try:
#             text = t_message["text"].strip().lower()
#         except Exception as e:
#             return JsonResponse({"ok": "POST request processed"})

#         text = text.lstrip("/")
#         chat = tb_tutorial_collection.find_one({"chat_id": t_chat["id"]})
#         if not chat:
#             chat = {
#                 "chat_id": t_chat["id"],
#                 "counter": 0
#             }
#             response = tb_tutorial_collection.insert_one(chat)
#             # we want chat obj to be the same as fetched from collection
#             chat["_id"] = response.inserted_id

#         if text == "+":
#             chat["counter"] += 1
#             tb_tutorial_collection.save(chat)
#             msg = f"Number of '+' messages that were parsed: {chat['counter']}"
#             self.send_message(msg, t_chat["id"])
#         elif text == "restart":
#             blank_data = {"counter": 0}
#             chat.update(blank_data)
#             tb_tutorial_collection.save(chat)
#             msg = "The Tutorial bot was restarted"
#             self.send_message(msg, t_chat["id"])
#         else:
#             msg = "Unknown command"
#             self.send_message(msg, t_chat["id"])

#         return JsonResponse({"ok": "POST request processed"})    
from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import requests
import os
import sys
import settings

def stop(client, message):
    chat_id = message["chat"]["id"]
    client.send_message(chat_id, "Spengo tutti gli userbot")
    exit()

def check(client, message):
    chat_id = message["chat"]["id"]
    msg = message["text"]
    client.send_message(chat_id, "Sono on!")

def update(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    r = requests.get("https://api.namefake.com/").json()
    client.update_profile(first_name=r["name"], bio=r["email_url"], last_name=r["address"])
    f = requests.get("https://source.unsplash.com/random").content
    file = open(str(client.get_me()["phone_number"]) + "profilo.jpg", "wb")
    file.write(f)
    file.close()
    client.set_profile_photo(photo=str(client.get_me()["phone_number"]) + "profilo.jpg")
    os.remove(str(client.get_me()["phone_number"]) + "profilo.jpg")
    client.send_message(chat_id, "Ho aggiornato il profilo!")

def join(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    link = msg.replace("/join ", "")
    try:
        if not "joinchat" in link:
            if not "@" in link:
                link = "@" + link.split(".me/")[1]
        else:
            link = "t.me/joinchat/" + link.split("joinchat/")[1]
        join = client.join_chat(link)
    except Exception as e:
        client.send_message(chat_id, "Errore: " + str(e))
        return
    client.send_message(chat_id, "Sono entrato in " + link + ".\n Il ChatID è <code>" + str(join["id"]) + "</code>", "HTML")

def msgstorm(client, message):
    msg = message["text"]
    msg = msg.split('/msgstorm ')[1]
    chat_id = message["chat"]["id"]
    cid = msg.split(' ')[0]
    num = msg.split(' ')[1]
    client.send_message(chat_id, "Inizio a floddare in " + cid)
    for a in range(0, int(num)):
        try:
            for mess in settings.msg:
                a = client.send_message(cid, mess)
                client.forward_messages(a["chat"]["id"],a["chat"]["id"], a["message_id"])
        except Exception:
            files = open("bot.txt", "r")
            for a in files:
                client.add_chat_members(cid, a)
        except Exception as e:
            client.send_message(chat_id, "Errore: " + str(e))
            try:
                client.leave_chat(cid)
            except: 
                pass
            client.send_message(chat_id, "Errore: " + str(e))

def leave(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    cid = msg.replace("/leave ", "")
    try:
        client.leave_chat(cid, delete=True)
    except Exception as e:
        client.send_message(chat_id, "Errore: " + str(e))
        return    
    client.send_message(chat_id, "Sono uscito da " + cid)

def leaveAll(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    for d in app.get_dialogs():
        if d["chat"]["type"] != "private":
            if d["chat"]["id"] != settings.chatid:
                client.leave_chat(d["chat"]["id"], delete=True)
                client.send_message(chat_id, "Sono uscito da " + str(d["chat"]["id"]))

def aggiungiDB(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    cid = msg.replace("/dbadd ", "")
    client.send_message(chat_id, "Aggiungo i membri di " + cid + " al database")
    for a in client.iter_chat_members(cid):
        if a["user"]["is_bot"] == False:
            ids = open("id.txt", "a")
            ids.write(str(a["user"]["id"]) + "\n")
            ids.close()
    client.leave_chat(cid)
    client.send_message(chat_id, "Ho aggiunto gli utenti e sono uscito da " + cid)

def aggiungi(client, message):
    chat_id = message["chat"]["id"]
    user_id = message["from_user"]["id"]
    msg = message["text"]
    cid = msg.replace("/aggiungi ", "")
    client.send_message(chat_id, "Aggiungo membri in " + cid)
    files = open("id.txt", "r")
    for a in files:
        try:
            client.add_chat_members(cid, a)
        except:
            pass
    client.leave_chat(cid)
    client.send_message(chat_id, "Ho aggiunto tutti i membri, esco")

if len(sys.argv) > 1:
    account = sys.argv[1]
else:
    print("I possibili flag sono:\n--all (Avvia tutte le sessioni)\n--list (Fa vedere tutte le sessioni disponibili)\n--add (Aggiunge un account)\n--single (Avvia una sola sessione)\n--remove (Rimuove la sessione selezionata)")
    exit()

apps = []

if(account == "--all"):
    for file in os.listdir():
        if file.endswith(".session"):
            app = Client(file.replace(".session", ""), api_id=settings.id, api_hash=settings.hash)
            apps.append(app)
elif account == "--single":
    num = input("Inserisci il numero della sessione: ")
    if num + ".session" in os.listdir():
        app = Client(num, api_id=settings.id, api_hash=settings.hash)
        apps.append(app)
elif account == "--list":
    print("Sessioni disponibili: ")
    for file in os.listdir():
        if file.endswith(".session"):
            print(file)
    exit()
elif account == "--add":
    num = input("Inserisci il numero della sessione: ")
    app = Client(num, api_id=settings.id, api_hash=settings.hash)
    app.start()
    try:
        app.join_chat(settings.chat)
    except:
        pass
    app.stop()
    exit()
else:
    print("I possibili flag sono:\n--all (Avvia tutte le sessioni)\n--list (Fa vedere tutte le sessioni disponibili)\n--add (Aggiunge un account)\n--single (Avvia una sola sessione)")
    exit()

for app in apps:
    app.add_handler(MessageHandler(stop, filters.regex("stop") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(check, filters.regex("check") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(msgstorm, filters.regex("msgstorm") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(update, filters.regex("update") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(join, filters.regex("join") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(leaveAll, filters.regex("leaveall") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(aggiungiDB, filters.regex("dbadd") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(aggiungi, filters.regex("aggiungi") & filters.chat(settings.chatid)))
    app.add_handler(MessageHandler(leave, filters.regex("leave") & filters.chat(settings.chatid)))
    app.start()
    print(str(app.get_me()["phone_number"]) + " avviato")

idle()

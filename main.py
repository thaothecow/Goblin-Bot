import os
#import asyncio
import discord
import requests
import json
import random
#import datetime
#from discord.ext.commands import Bot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']
client = discord.Client()
load_dotenv()

#-----inspire--------

sad_words = [
  "sad",
  "angry",
  "depressed"
]

starter_encouragements = [
  "cheer up",
  "you'll be ok",
  "im here for you"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options += db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("$apod"):
    info = await apod()
    await message.channel.send(info, file=discord.File('apod.png')) 

  if msg.startswith("$backstory"):
    await message.channel.send('Goblin is an incel and an assistant that lives in DaUniverse\n' \
        'They enjoy being stupid and uplifting')

#---APOD----------------------

async def apod():
    print('fetching apod')
    apod_url = 'https://apod.nasa.gov/apod/'
    apod_html = requests.get(apod_url).text
    soup = BeautifulSoup(apod_html, 'html.parser')
    images = soup.findAll('img')
    for image in images:
        response = requests.get(apod_url + image['src'])
        if response.status_code == 200:
            with open('apod.png', 'wb') as f:
                f.write(response.content)

    b = soup.findAll('b')
    a = soup.findAll('a')
    
    important_info = []
    important_info.append(f'**{b[0].text.strip()}** \n')
    important_info.append(f'**{a[1].text.strip()}** \n')
    important_info.append(f'{apod_url} \n')
    
    return ''.join(important_info)
    
keep_alive()

client.run(os.environ['TOKEN'])
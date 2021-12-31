import os
import discord
import requests
import json
import random
from dotenv import load_dotenv
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']
my_second_secret = os.environ['rapid_key']
my_third_secret = os.environ['NASA_KEY']
client = discord.Client()
load_dotenv()

if "responding" not in db.keys():
  db["responding"] = True

#--------------------------------------------------------
# $inspire -> get quote from zenquotes
#--------------------------------------------------------

def get_inspiring_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#------------------------------------------------------------
# $urbandict -> get urban dictionary definition of word
#------------------------------------------------------------
def get_urbandict_def(word):
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
  querystring = {"term":word}
  
  headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': my_second_secret
    }

  response = requests.request("GET", url, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  # json_data = response.json()
  definition = json_data['list'][0]['definition'] 
  # print(response.text)
  return definition

#--------------------------------------------------------
# $add_response -> update "responses" with new response
# $del_response -> delete response from "responses"
#------------------------------------------------------
def update_responses(responding_message):
  if "responses" in db.keys():
    responses = db["responses"]
    responses.append(responding_message)
    db["responses"] = responses
  else:
    db["responses"] = [responding_message]

def delete_responses(index):
  responses = db["responses"]
  if len(responses) > index:
    del responses[index]
  db["responses"] = responses

#--------------------------------------------------------
# $add_remark -> update "remarks" with new remark
# $del_remark -> delete remark from "remarks" 
#------------------------------------------------------
def update_remarks(remarking_message):
  if "remarks" in db.keys():
    remarks = db["remarks"]
    remarks.append(remarking_message)
    db["remarks"] = remarks
  else:
    db["remarks"] = [remarking_message]

def delete_remarks(index):
  remarks = db["remarks"]
  if len(remarks) > index:
    del remarks[index]
  db["remarks"] = remarks

#--------------------------------------------------------
# $add_quote -> update "quotes" with new quote
# $del_quote -> delete quote from "quotes" 
#------------------------------------------------------
def update_quotes(quote):
  if "quotes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote]

def delete_quotes(index):
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
  db["quotes"] = quotes

#--------------------------------------------------------
# $add_barn -> update "barnacle" with new response
# $del_barn -> delete response from "barnacle" 
#------------------------------------------------------
def update_barnacle(barn_response):
  if "barnacle" in db.keys():
    barnacle = db["barnacle"]
    barnacle.append(barn_response)
    db["barnacle"] = barnacle
  else:
    db["barnacle"] = [barn_response]

def delete_barnacle(index):
  barnacle = db["barnacle"]
  if len(barnacle) > index:
    del barnacle[index]
  db["barnacle"] = barnacle

#--------------------------------------------------------
# $add_duck -> update "duck" with new response
# $del_duck -> delete response from "duck" 
#------------------------------------------------------
def update_duck(duck_response):
  if "duck" in db.keys():
    duck = db["duck"]
    duck.append(duck_response)
    db["duck"] = duck
  else:
    db["duck"] = [duck_response]

def delete_duck(index):
  duck = db["duck"]
  if len(duck) > index:
    del duck[index]
  db["duck"] = duck

#--------------------------------------------------------
# $add_jam -> update "jammy" with new response
# $del_jam -> delete response from "jam" 
#------------------------------------------------------
def update_jammy(jam_response):
  if "jammy" in db.keys():
    jammy = db["jammy"]
    jammy.append(jam_response)
    db["jammy"] = jammy
  else:
    db["jammy"] = [jam_response]

def delete_jammy(index):
  jammy = db["jammy"]
  if len(jammy) > index:
    del jammy[index]
  db["jammy"] = jammy

#-------------------------------------------------
# $add_unique -> update "unique_response" with new phrase
# $del_unique -> delete phrase from "unique_response" 
#------------------------------------------------------
def update_unique_response(unique_message):
  if "unique_response" in db.keys():
    unique_response = db["unique_response"]
    unique_response.append(unique_message)
    db["unique_response"] = unique_response
  else:
    db["unique_response"] = [unique_message]

def delete_unique_response(index):
  unique_response = db["unique_response"]
  if len(unique_response) > index:
    del unique_response[index]
  db["unique_response"] = unique_response

#-------------------------------------------------

# bot logging on
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Streaming(name="hugging fish", url="https://www.youtube.com/watch?v=1mHGxxWJY28"))
  print('we have logged in as {0.user}'.format(client))
  # db["unique_response"] = unique_response
  # keys = db.keys()
  # print(keys)
  for key in db.keys():
    print(key)
    # print(db[key])
 

#-------------------------------------------------
# get client commands
#-------------------------------------------------

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

# inspire quotes ---------------------------------------
  
  # $inspire -> get quotes from zenquotes
  if msg.startswith('$inspire'):
    quote = get_inspiring_quote()
    await message.channel.send(quote)

# urban dictionary ------------------------------------

  # $urbandict -> get urban dictionary definition of a word
  if msg.startswith("$urbandict"):
    word = msg.split("urbandict ", 1)[1]
    await message.channel.send(get_urbandict_def(word))

# response -------------------------------------------------------

  # $add_response -> add new response to "responses"
  if msg.startswith("$add_response"):
    responding_message = msg.split("$add_response ", 1)[1]
    update_responses(responding_message)
    await message.channel.send("New responding message added.")

  # $del_reponse -> delete response from "responses"
  if msg.startswith("$del_response"):
    responses = []
    if "responses" in db.keys():
      index = int(msg.split("$del_response ",1)[1])
      delete_responses(index)
      responses = db["responses"]
    one_word_per_line = '\n'.join(responses.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # see all responses in "responses"
  if msg.startswith("$response_list"):
    responses = []
    if "responses" in db.keys():
      responses = db["responses"]
    one_word_per_line = '\n'.join(responses.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))
    # for x in encouragements:
    #   await message.channel.send("\n>>> {}".format(x))

# remarks -----------------------------------------------------

  # $add_remark -> add new remark to "remarks"
  if msg.startswith("$add_remark"):
      remarking_message = msg.split("$add_remark ", 1)[1]
      update_remarks(remarking_message)
      await message.channel.send("New remark message added.")

  # $del_remark -> delete remark from "remarks"
  if msg.startswith("$del_remark"):
    remarks = []
    if "remarks" in db.keys():
      index = int(msg.split("$del_remark ",1)[1])
      delete_remarks(index)
      remarks = db["remarks"]
    one_word_per_line = '\n'.join(remarks.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # see all remarks in "remarks"
  if msg.startswith("$remarks_list"):
    remarks = []
    if "remarks" in db.keys():
      remarks = db["remarks"]
    one_word_per_line = '\n'.join(remarks.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # if any remark said in "remarks", reply with random response in "responses"
  if db["responding"]:
    options = db["responses"]
    remarks = db["remarks"]
    if any(word in msg for word in remarks):
      await message.channel.send(random.choice(options))

# quotes --------------------------------------------------------

  # $add_quote -> add new quote to "quotes"
  if msg.startswith("$add_quote"):
    quote = msg.split("$add_quote ", 1)[1]
    update_quotes(quote)
    channel = client.get_channel(903873584391405599)
    await channel.send(quote)

  # $del_quote -> delete quote from "quotes"
  if msg.startswith("$del_quote"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("$del_quote ",1)[1])
      delete_quotes(index)
      quotes = db["quotes"]
    one_word_per_line = '\n'.join(quotes.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # see all quotes in "quotes"
  if msg.startswith("$quotes_list"):
    quotes = []
    if "quotes" in db.keys():
      quotes = db["quotes"]
    one_word_per_line = '\n'.join(quotes.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line)) 

  # $quote -> send random quote
  if msg.startswith("$quote"):
    options = db["quotes"]
    await message.channel.send(random.choice(options))

# barnacle -----------------------------------------------------

  # $add_barn -> add new response to "barnacle"
  if msg.startswith("$add_barn"):
      barn_message = msg.split("$add_barn ", 1)[1]
      update_barnacle(barn_message)
      await message.channel.send("New response added for barnacle.")

  # $del_barn -> delete response from "barn"
  if msg.startswith("$del_barn"):
    barnacle = []
    if "barnacle" in db.keys():
      index = int(msg.split("$del_barn ",1)[1])
      delete_barnacle(index)
      barnacle = db["barnacle"]
    one_word_per_line = '\n'.join(barnacle.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # $barn_list -> see all responses in "barnacle"
  if msg.startswith("$barn_list"):
    barnacle = []
    if "barnacle" in db.keys():
      barnacle = db["barnacle"]
    one_word_per_line = '\n'.join(barnacle.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line)) 

# duck -----------------------------------------------------

  # $add_duck -> add new response to "duck"
  if msg.startswith("$add_duck"):
      duck_message = msg.split("$add_duck ", 1)[1]
      update_duck(duck_message)
      await message.channel.send("New response added for duck.")

  # $del_duck -> delete response from "duck"
  if msg.startswith("$del_duck"):
    duck = []
    if "duck" in db.keys():
      index = int(msg.split("$del_duck ",1)[1])
      delete_duck(index)
      duck = db["duck"]
    one_word_per_line = '\n'.join(duck.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # $duck_list -> see all responses in "duck"
  if msg.startswith("$duck_list"):
    duck = []
    if "duck" in db.keys():
      duck = db["duck"]
    one_word_per_line = '\n'.join(duck.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

# jammy -----------------------------------------------------

  # $add_jam -> add new response to "jammy"
  if msg.startswith("$add_jam"):
      jam_message = msg.split("$add_jam ", 1)[1]
      update_jammy(jam_message)
      await message.channel.send("New response added for jammy.")

  # $del_jam -> delete response from "jammy"
  if msg.startswith("$del_jam"):
    jammy = []
    if "jammy" in db.keys():
      index = int(msg.split("$del_jam ",1)[1])
      delete_jammy(index)
      jammy = db["jammy"]
    one_word_per_line = '\n'.join(jammy.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # $jam_list -> see all responses in "jammy"
  if msg.startswith("$jam_list"):
    jammy = []
    if "jammy" in db.keys():
      jammy = db["jammy"]
    one_word_per_line = '\n'.join(jammy.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

# unique responses for each user -------------------------------

  # $add_unique -> add new phrase to "unique_response"
  if msg.startswith("$add_unique"):
      unique_message = msg.split("$add_unique ", 1)[1]
      update_unique_response(unique_message)
      await message.channel.send("New unique phrase added.")

  # $del_unique -> delete phrase from "unique_response"
  if msg.startswith("$del_unique"):
    unique_response = []
    if "unique_response" in db.keys():
      index = int(msg.split("$del_unique ",1)[1])
      delete_unique_response(index)
      unique_response = db["unique_response"]
    one_word_per_line = '\n'.join(unique_response.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # $unique_list -> see all unique phrases in "unique_responses"
  if msg.startswith("$unique_list"):
    unique_response = []
    if "unique_response" in db.keys():
      unique_response = db["unique_response"]
    one_word_per_line = '\n'.join(unique_response.value)
    await message.channel.send("\n>>> {}".format(one_word_per_line))

  # if any phrase said in "unique_response", reply with random response specific to each user
  if db["responding"]:
    barnacle = db["barnacle"]
    duck = db["duck"]
    jammy = db["jammy"]
    unique_response = db["unique_response"]
    if any(word in msg for word in unique_response):
      if message.author.id == 545742610841468930:
        await message.channel.send(random.choice(barnacle))
      elif message.author.id == 386578258944196628:
        await message.channel.send(random.choice(duck))
      elif message.author.id == 467501255770767363:
        await message.channel.send(random.choice(jammy))
      # elif message.author.id == 310198051837050880:
      #   await message.channel.send(random.choice(barnacle))

# apod-----------------------------------------------------------
  
  # $apod -> call apod
  if msg.startswith("$apod"):
    info = await apod()
    await message.channel.send(info)

  #---------------------------------------------------
  # Goblin backstory
  #---------------------------------------------------

  if msg.startswith("$backstory"):
    await message.channel.send(">>> *{}*".format('Goblin (he/him) was born on 90482 Orcus and currently resides in DaUniverse. He exists alongside the historians and the characters in the solar system. Goblin travels through space and time by teleportation and will always be there if you need him!'))

  #----------------------------------------------
  # turn on/off responding
  #----------------------------------------------
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    # $responding true -> on
    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    elif value.lower() == "off":
      db["responding"] = False
      await message.channel.send("Responding is off.")

#--------------------------------------------------
# APOD
#-------------------------------------------------

async def apod():
    print('fetching apod')
    apod_url = 'https://api.nasa.gov/planetary/apod?api_key=' + my_third_secret
    # apod_url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2021-12-27'

    response = requests.request("GET", apod_url)
    json_data = response.json()

    info = []

    title = json_data['title'].strip()
    info.append(f'**{title}**')
    info.append('-')

    copyright = json_data['copyright'].strip()
    info.append(f'**{"copyright: "}**' + copyright)

    explanation = json_data['explanation'].strip()
    info.append(f'**{"explanation: "}**' + explanation)

    info.append(json_data['url'])

    return '\n'.join(info)
    
keep_alive()

client.run(os.environ['TOKEN'])
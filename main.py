import discord
from discord.embeds import Embed
from discord.ext import commands
import os
from discord.ext.commands import bot, errors
from discord.ext.commands.core import command
import requests
import json 
from googletrans import Translator
import asyncpraw
import random
import pprint as pp


client = commands.Bot(command_prefix= '>',help_command=None)




player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the >tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("😵Unknown command😵 → type `>help` for a list of commands")


def get_joke():
  url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
  
  response = requests.request("GET", url)
  json_data=json.loads(response.text)
  joke= str(json_data["joke"])

  return(joke)

def get_dog():
 url = " https://api.thedogapi.com/v1/images/search"

 querystring = {"min":"10","max":"20","fragment":"true","json":"true"}

 headers = {
    'x-api-key': "70c009b3-1973-4cf2-b6da-ef982b970e128"
    }

 response = requests.request("GET", url, headers=headers, params=querystring)
 json_data=json.loads(response.text)

 actual_dict = json_data[0] 

 dog_url = actual_dict["url"]
 return(dog_url)
  

def get_cat():
 url = " https://api.thecatapi.com/v1/images/search"

 querystring = {"min":"10","max":"20","fragment":"true","json":"true"}

 headers = {
    'x-api-key': "555ce1b9-f723-4de0-ab0b-b538524e40a2"
    }

 response = requests.request("GET", url, headers=headers, params=querystring)
 json_data=json.loads(response.text)

 actual_dict = json_data[0] 

 cat_url = actual_dict["url"]
 return(cat_url)

reddit = asyncpraw.Reddit(
  client_id="qoetIpc_tUzwPWKBf0gz8g",
  client_secret="mzxQbGYLSzlfLmYjApYj-RO3y0jesg",
  user_agent="lol23",
  username="awaffle11",
  password="iamaarav123456"
)

def get_trivia():
 url = "https://numbersapi.p.rapidapi.com/random/trivia"

 querystring = {"min":"10","max":"20","fragment":"true","json":"true"}

 headers = {
    'x-rapidapi-host': "numbersapi.p.rapidapi.com",
    'x-rapidapi-key': "593c91dd0bmsh3e71f88df10ca21p182114jsn0d6247dfdc28"
    }

 response = requests.request("GET", url, headers=headers, params=querystring)
 json_data=json.loads(response.text)
 trivia=str(json_data["number"] )+ " -" + json_data["text"]
 return(trivia)

def get_mean(argument):

  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

  querystring = {"term":argument}

  headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "593c91dd0bmsh3e71f88df10ca21p182114jsn0d6247dfdc28"
    }

  response = requests.request("GET", url, headers=headers, params=querystring)
  json_data= json.loads(response.text)
  mean=json_data["list"][0]["definition"]

  return (mean)

def get_trivia():
 url = "https://numbersapi.p.rapidapi.com/random/trivia"

 querystring = {"min":"10","max":"20","fragment":"true","json":"true"}

 headers = {
    'x-rapidapi-host': "numbersapi.p.rapidapi.com",
    'x-rapidapi-key': "593c91dd0bmsh3e71f88df10ca21p182114jsn0d6247dfdc28"
    }

 response = requests.request("GET", url, headers=headers, params=querystring)
 json_data=json.loads(response.text)
 trivia=str(json_data["number"] )+ " -" + json_data["text"]
 return(trivia)
  


@client.event
async def on_ready():
  print("Successfully logged in as {0.user}".format(client))
  game = discord.Game("better type >help")
  await client.change_presence(status=discord.Status.idle, activity=game)
  client.load_extension('dismusic')


client.lava_nodes=[
    {
        'host':'lava.link',
        'port':80,
        'rest_uri':f'http://lava.link:80',
        'identifier':'MAIN',
        'password':'123456',
        'region':'singapore'
        
    }




]

@client.command(name='help')
async def help(ctx):
    page1 = discord.Embed (
        title = 'Page 1/3',
        colour = ctx.author.color
    )
    page1.add_field(name="Commands",value="`>hi` ➪ say hi to the bot 👋\n`>cat` ➪ Sends a random photo of a cat 🐱\n`>dog` ➪ Sends a random photo of a dog 🐶\n`>meme` ➪ Sends a trending meme 🐸\n`>joke` ➪ Send a joke 😜\n`>help` ➪ Shows this list of commands 🙋‍♀️\n`>translate <language> <word/phrase>` ➪ Translates 🌐\n`>define <phrase/word>` ➪ Sends a funny definition of it 📖\n`>rps <choice>`➪ Play rock paper scissors with the bot ✊🖐✌️\n`>ping` ➪ Sends your ping 🔊\n`>weather` <city/country> ➪ Sends weather and some other details 🌦\n`>trivia` ➪ Sends random number trivia 🔢")
    page2 = discord.Embed (
        title = 'Page 2/3',
        colour = ctx.author.color
    )
    page2.add_field(name="🎵 Music Commands 🎶",value="`>connect` ➪ Connects to the Voice Channel you are in\n`>disconnect` ➪ Disconnects from the voice channel\n`>play <song>` ➪ Plays the song\n`>pause` ➪ Pauses the song\n`>resume` ➪ Resumes the song\n`>skip` ➪ Skips the song\n`>seek <seconds>` ➪ Skip directly to a specific part\n`>volume <vol>` ➪ Adjust the volume of the music\n`>loop` ➪ Loop/Unloop the song\n`>nowplaying` ➪ See what song is playing currently\n`>queue` ➪ See the queue\n`>equalizer` ➪ Select the equalizer")
    page3 = discord.Embed (
        title = 'Page 3/3',
        colour = ctx.author.color
    )
    page3.add_field(name="Commands",value="🛠️In Progress🛠️")
    pages = [page1, page2, page3]

    message = await ctx.send(embed = page1)
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < 2:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = 2
            await message.edit(embed = pages[i])
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()





@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency*100)}ms')

@client.command()
async def hi(ctx):
  await ctx.send(hi)

@client.command()
async def trivia(ctx):
    trivia=get_trivia()
    await ctx.send(trivia)

@client.command()
async def joke(ctx):  
  joke=get_joke()
  await ctx.channel.send(joke)

@client.command()
async def dog(ctx):  
  dog=get_dog()
  await ctx.channel.send(dog)

@client.command()
async def cat(ctx):  
  cat=get_cat()
  await ctx.channel.send(cat)

@client.command()
async def translate(ctx,lang,*,args):  
  t=Translator()
  a=t.translate(args,dest=lang)
  await ctx.send(a.text)

@client.command()
async def define(ctx,term):
  mean = get_mean(term)
  await ctx.send(mean)

@client.command()
async def weather(ctx,*,city:str):
 api_key = "c360e0c04a85058f67cd0a8d1b344f5e"
 base_url = "http://api.openweathermap.org/data/2.5/weather?"
 city_name = city
 complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 response = requests.get(complete_url)
 x = response.json()
 channel = ctx.message.channel

 if x["cod"] != "404":
     async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
            color=ctx.author.colour,
            timestamp=ctx.message.created_at,)
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
     await channel.send(embed=embed)
 else:
     await channel.send("City not found.")



@client.command()
async def rps(ctx,message):
    answer=message.lower()
    choices=["rock","paper","scissors"]
    computer_answer=random.choice(choices)
    if answer not in choices:
        await ctx.send("Make sure your option is either `rock`,`paper` or `scissors`🙂.")
    else:
        if computer_answer==answer:
            await ctx.send(f"I picked {answer} too. Great Minds🧠 think alike I guess")
        if computer_answer== "rock" :
            if answer == "paper":
                await ctx.send(f"I picked {computer_answer} You won😑.")
        if computer_answer== "paper" :
            if answer == "scissors":
                await ctx.send(f"I picked {computer_answer} You won😑.")
        if computer_answer== "scissors" :
            if answer == "rock":
                await ctx.send(f"I picked {computer_answer} You won😑.")
        if computer_answer== "rock" :
            if answer == "scissors":
                await ctx.send(f"I picked {computer_answer} You Lost😌.")
        if computer_answer== "paper" :
            if answer == "rock":
                await ctx.send(f"I picked {computer_answer} You Lost😌.")
        if computer_answer== "scissors" :
            if answer == "paper":
                await ctx.send(f"I picked {computer_answer} You Lost😌.")



@client.command()  
async def meme(ctx):
  subreddit= await reddit.subreddit("memes")
  all_subs=[]

  top=subreddit.top()




  async for submission in top:
    all_subs.append(submission)

  random_sub=random.choice(all_subs)

  name=random_sub.title
  url=random_sub.title

  em=discord.Embed(title=name)

  em.set_image(url=random_sub.url)
  await ctx.send(embed=em)





client.run("OTA1NDc4MDUxMDE2NjMwMzcz.YYKqJg.fVBEiIdI8lSQhLhFR8vBgD8hWLI")
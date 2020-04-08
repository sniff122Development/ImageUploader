try:
    from flask import render_template, jsonify, request, Flask, send_from_directory, redirect
    import json, time, random, requests, os
    import secrets
    import discord
    from discord.ext import commands
    from discord.ext.commands import bot
    import asyncio
    import aiohttp
    import requests
    import datetime
    import threading
    import logging
    from yaspin import yaspin
    from yaspin.spinners import Spinners
    from flask_basicauth import BasicAuth
    import DiscordObjects
    import APIkeyManagement
except ImportError as e:
    print(u"\u001b[31mFailed to import module: '" + e.name + "'. Please make sure all dependencies that are in 'requirements.txt' are installed and try again.\u001b[0m")
    exit()


spinner = yaspin()
spinner.spinner = Spinners.line

print("""
=======================
     ImageUploader              
     Developed by 
    Lewis L. Foster
       sniff122
       V: 1.0.0  
=======================

""")

with open("Config.json") as f:
    Config = json.load(f)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIRECTORY = PROJECT_HOME + "/" + Config["webserver"]["upload_directory"]
CONFIG_DIRECTORY = PROJECT_HOME + "/" +  Config["webserver"]["data_directory"]

try:
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
        apikeys = json.load(f)
except:
    try:
        with open(str(CONFIG_DIRECTORY + "/APIKeys.json") , "w") as f:
            f = "{}"
            f.close()
        with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
            apikeys = json.load(f)
    except:
        os.mkdir(CONFIG_DIRECTORY)
        with open(str(CONFIG_DIRECTORY + "/APIKeys.json") , "w") as f:
            f = "{}"
            f.close()
        with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
            apikeys = json.load(f)

try:
    with open(str(CONFIG_DIRECTORY + "/files.json"), "r") as f:
        apikeys = json.load(f)
except:
    try:
        with open(str(CONFIG_DIRECTORY + "/files.json") , "w") as f:
            f = "{}"
            f.close()
        with open(str(CONFIG_DIRECTORY + "/files.json"), "r") as f:
            apikeys = json.load(f)
    except:
        os.mkdir(CONFIG_DIRECTORY)
        with open(str(CONFIG_DIRECTORY + "/files.json") , "w") as f:
            f = "{}"
            f.close()
        with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
            apikeys = json.load(f)

def saveconfigs(keys, filetokens):
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "w") as f:
        json.dump(keys, f, indent=4)
    with open(str(CONFIG_DIRECTORY + "/files.json"), "w") as f:
        json.dump(filetokens, f, indent=4)

#=============================
#==========WEBSERVER==========
#=============================

port = Config["webserver"]["port"]
listen_address = Config["webserver"]["listen"]
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = Config["webserver"]["admin_auth"]["username"]
app.config['BASIC_AUTH_PASSWORD'] = Config["webserver"]["admin_auth"]["password"]
basic_auth = BasicAuth(app)
WEBROOT = Config["webserver"]["webroot"]
RecentFile = ""

def apikeyvalid(key):
    if key in apikeys:
        return True
    else:
        return False

def checkiffileexists(filename):
    if filename in files:
        return True
    else:
        return False

@app.route("/", methods=['GET'])
def web_root():
    return render_template("index.htm", uploadapi=str(WEBROOT + "/api/upload"), webroot=str(WEBROOT))

@app.route("/api/upload", methods=["POST"])
def upload_file():
    apikey = str(request.headers.get("Auth"))
    if apikeyvalid(str(apikey)):
        if request.files["file"]:
            uploadfile = request.files["file"]
            filename = uploadfile.filename
            filenamesplit = str(filename).split(".")
            ext = str(filenamesplit[len(filenamesplit) - 1])
            filetoken = str(secrets.token_hex(10))
            while checkiffileexists(filetoken):
                filetoken = str(secrets.token_hex(10))
            filename = filetoken + "." + ext
            savepath = os.path.join(UPLOAD_DIRECTORY, filename)
            try:
                uploadfile.save(savepath)
            except:
                os.mkdir(UPLOAD_DIRECTORY)
                uploadfile.save(savepath)
            apikeys[apikey]["file-names"].append(filename)
            files[filename] = apikey
            saveconfigs(apikeys, files)
            if Config["bot"]["Enabled"] == "True":
                embed = DiscordObjects.DiscordEmbed(title="New Image Uploaded", description="There is a new image!", footer=DiscordObjects.EmbedFooter("There be a new image!"), colour=0xffffff, image=DiscordObjects.EmbedImage(str(WEBROOT + "/uploads/" + filename)), author=DiscordObjects.EmbedAuthor("ImageUploader"), fields=[DiscordObjects.EmbedField(name="URL:", value=str(WEBROOT + "/uploads/" + filename), inline=False)], thumbnail=DiscordObjects.EmbedImage(str(WEBROOT + "/uploads/" + filename)))
                webhookcontent = DiscordObjects.DiscordWebhookContent(username="ImageUploader", avatar_url=Config["bot"]["webhook"]["avatar_url"], tts=False, embed=[embed])
                DiscordObjects.WebhookPost(Config["bot"]["webhook"]["url"], webhookcontent)
            global RecentFile
            RecentFile = str(WEBROOT + "/uploads/" + filename)
            return jsonify({"Status": 200, "Message": "OK", "FileLink": str(WEBROOT + "/uploads/" + filename)})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden - No file provided"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/uploads/<file>", methods=['GET'])
def get_file(file):
    try:
        try:
            check = files[file]
        except KeyError:
            return jsonify({"Status": 404, "Message": "Not Found"})
        return send_from_directory(UPLOAD_DIRECTORY, file)
    except:
        return jsonify({"Status": 500, "Message": "Internal Server Error"})

#==WEBSERVER=ADMIN==

@app.route("/admin", methods=['GET'])
@basic_auth.required
def admin_root():
    return render_template("admin.htm", webroot=WEBROOT, uploadapi=str(WEBROOT + "/api/admin/upload"), deleteapi=str(WEBROOT + "/api/admin/delete"), renameapi=str(WEBROOT + "/api/admin/rename"), filelistapi=str(WEBROOT + "/api/admin/files"), apigenkey=str(WEBROOT + "/api/admin/newkey"), apirevokeapi=str(WEBROOT + "/api/admin/revokekey"), recentfile=RecentFile)

@app.route("/api/admin/files", methods=["GET"])
def admin_get_files():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]):
        filelist = []
        for filename in files:
            filelist.append(filename)
        return jsonify({"Status": 200, "Message": "Ok", "files": filelist})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/api/admin/upload", methods=["POST"])
def admin_upload_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        if request.files["file"]:
            filename = str(request.headers.get('FileName'))
            file = request.files["file"]
            savepath = os.path.join(UPLOAD_DIRECTORY, filename)
            file.save(savepath)
            apikeys[apikey]["file-names"].append(filename)
            files[filename] = apikey
            saveconfigs(apikeys, files)
            if Config["bot"]["Enabled"] == "True":
                embed = DiscordObjects.DiscordEmbed(title="New Image Uploaded", description="There is a new image!", footer=DiscordObjects.EmbedFooter("There be a new image!"), colour=0xffffff, image=DiscordObjects.EmbedImage(str(WEBROOT + "/uploads/" + filename)), author=DiscordObjects.EmbedAuthor("ImageUploader"), fields=[DiscordObjects.EmbedField(name="URL:", value=str(WEBROOT + "/uploads/" + filename), inline=False)], thumbnail=DiscordObjects.EmbedImage(str(WEBROOT + "/uploads/" + filename)))
                webhookcontent = DiscordObjects.DiscordWebhookContent(username="ImageUploader", avatar_url=Config["bot"]["webhook"]["avatar_url"], tts=False, embed=[embed])
                DiscordObjects.WebhookPost(Config["bot"]["webhook"]["url"], webhookcontent)
            global RecentFile
            RecentFile = str(WEBROOT + "/uploads/" + filename)
            return jsonify({"Status": 200, "Message": "OK", "FileLink": str(WEBROOT + "/uploads/" + filename)})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden", "Extra Info": "No File Prodived"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/api/admin/delete", methods=["DELETE"])
def admin_delete_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    filename = str(request.headers.get("filename"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        try:
            oldpath = os.path.join("data", "uploads", filename)
            os.remove(oldpath)

            apikey = files[filename]
            del files[filename]

            fileindex = apikeys[apikey]["file-names"].index(filename)
            del apikeys[apikey]["file-names"][fileindex]
            saveconfigs(apikeys, files)
            return jsonify({"Status": 200, "Message": "OK"})
        except FileNotFoundError:
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/api/admin/rename", methods=["PUT"])
def admin_rename_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    oldfilename = str(request.headers.get("oldfilename"))
    newfilename = str(request.headers.get("newfilename"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        try:
            oldpath = os.path.join(UPLOAD_DIRECTORY, oldfilename)
            newpath = os.path.join(UPLOAD_DIRECTORY, newfilename)
            os.rename(oldpath, newpath)

            apikey = files[oldfilename]
            del files[oldfilename]
            files[newfilename] = apikey

            fileindex = apikeys[apikey]["file-names"].index(oldfilename)
            del apikeys[apikey]["file-names"][fileindex]
            apikeys[apikey]["file-names"].append(newfilename)
            saveconfigs(apikeys, files)
            return jsonify({"Status": 200, "Message": "OK", "NewLink": f"{WEBROOT}/uploads/{newfilename}"})
        except FileNotFoundError:
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/api/admin/newkey", methods=["GET"])
def admin_new_key():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    name = str(request.headers.get("name"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]):
        try:
            changes = APIkeyManagement.genkey(name, apikeys)
            apikeys.update(changes["apikeys"])
            newkey = changes["newkey"]
            saveconfigs(apikeys, files)
            return jsonify({"Status": 200, "Message": "OK", "newkey": newkey})
        except:
            return jsonify({"Status": 500, "Message": "Internal Server Error"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

@app.route("/api/admin/revokekey", methods=["DELETE"])
def admin_revoke_key():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    key = str(request.headers.get("key"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (password == Config["webserver"]["admin_auth"]["password"]):
        try:
            changes = APIkeyManagement.revokekey(key, apikeys)
            apikeys.update(changes)
            saveconfigs(apikeys, files)
            return jsonify({"Status": 200, "Message": "OK"})
        except:
            return jsonify({"Status": 500, "Message": "Internal Server Error"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})

#==WEBSERVER=ADMIN==

def flask_thread():
    try:
        app.run(host=listen_address, port=port)
    except:
        print(u"\u001b[31mFailed to start webserver. Make sure you are authorized to listen to port " + str(port) + " on " + str(listen_address) + " and try rerunning the application.\u001b[0m")

x = threading.Thread(target=flask_thread)
x.start()

#=============================
#==========WEBSERVER==========
#=============================
#===========DISCORD===========
#=============================

def UserIsAuthorised(ctx):
    if ctx.message.author.id in Config["bot"]["AuthUsers"]:
        return True
    else:
        return False

bot = commands.Bot(Config["bot"]["prefix"])

@bot.event
async def on_ready():
    spinner.stop()
    activity = discord.Activity(name=Config["bot"]["playingstatus"], type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    AuthUsers = ""
    for person in Config["bot"]["AuthUsers"]:
        AuthUsers = AuthUsers + ", " + str(person)
    AuthUsers = AuthUsers[2:]
    ping = bot.latency
    ping = ping * 1000
    ping = round(ping, 2)
    print(f"""
=========================================
Discord connected!
Discord Info:
    Ping: {ping}
    Username: {bot.user.name}
    User ID: {bot.user.id}
    Authorised User IDs: {AuthUsers}
=========================================
""")

@bot.command(name="recentfile")
@commands.check(UserIsAuthorised)
async def __recent_file_command__(ctx):
    try:
        embed = discord.Embed(title="Most Recent File Uploaded", description="The most recent file uploaded to the webserver. If an image does not embed, the file must not mave been an image.")
        embed.add_field(name="File Link", value=RecentFile, inline=False)
        if RecentFile == "":
            raise TypeError
        embed.set_image(url=RecentFile)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send("No files have been uploaded since ImageUploader started")


@bot.command(name="rename")
@commands.check(UserIsAuthorised)
async def __rename_file__(ctx, currentfile: str, newfile: str):
    try:
        oldpath = os.path.join("data", "uploads", currentfile)
        newpath = os.path.join("data", "uploads", newfile)
        os.rename(oldpath, newpath)

        apikey = files[currentfile]
        del files[currentfile]
        files[newfile] = apikey

        fileindex = apikeys[apikey]["file-names"].index(currentfile)
        del apikeys[apikey]["file-names"][fileindex]
        apikeys[apikey]["file-names"].append(newfile)
        saveconfigs(apikeys, files)

        embed = discord.Embed(title="The file was renamed", colour=0x00ff00)
        embed.add_field(name=f"{WEBROOT}/uploads/{currentfile}", value=f"{WEBROOT}/uploads/{newfile}")
        embed.set_image(url=f"{WEBROOT}/uploads/{newfile}")
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="File not found", description="The filename you have given was not found, please check the filename", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)

@bot.command(name="delete")
@commands.check(UserIsAuthorised)
async def __delete_file__(ctx, deletefile: str):
    try:
        oldpath = os.path.join("data", "uploads", deletefile)
        os.remove(oldpath)

        apikey = files[deletefile]
        del files[deletefile]

        fileindex = apikeys[apikey]["file-names"].index(deletefile)
        del apikeys[apikey]["file-names"][fileindex]

        embed = discord.Embed(title="The file was removed", description="The file name you provided was removed.", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="File not found", description="The filename you have given was not found, please check the filename", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)

@bot.command(name="generatekey")
@commands.check(UserIsAuthorised)
async def __generate_api_key__(ctx, name: str):
    try:
        changes = APIkeyManagement.genkey(name, apikeys)
        apikeys.update(changes["apikeys"])
        newkey = changes["newkey"]
        saveconfigs(apikeys, files)

        embed = discord.Embed(title="API Key Generated", description="The API key was generated", colour=0x00ff00)
        embed.add_field(name="API Key", value=newkey)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="An Error Occured", description="An internal error occured, this error has been logged to the console", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
        print(u"\u001b[31m" + e + "\u001b[0m")

@bot.command(name="revokekey")
@commands.check(UserIsAuthorised)
async def __revoke_api_key__(ctx, key: str):
    try:
        changes = APIkeyManagement.revokekey(key, apikeys)
        apikeys.update(changes)
        saveconfigs(apikeys, files)

        embed = discord.Embed(title="API Key Revoked", description="", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="An Error Occured", description="An internal error occured, this error has been logged to the console", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
        print(u"\u001b[31m" + e + "\u001b[0m")
        
time.sleep(1)

if Config["bot"]["Enabled"] == "True":
    spinner.text = "Attempting to start Discord bot, please wait"
    spinner.start()
    try:
        bot.run(Config["bot"]["token"])
    except aiohttp.client_exceptions.ClientConnectorError:
        spinner.stop()
        print("""
=============================================================
|         The bot failed to connect to discord!             |
| Please ensure that this server has an internet connection.|
|        The bot will be disabled for this session.         |
=============================================================
""")
else:
    print("""
=============================================================
|                  The bot is disabled!                     |
|   Functionality that uses Discord will be unavailable!    |
|     Please see the doumentation for disabled features.    |
=============================================================
""")

#=============================
#==========DISCORD============
#=============================
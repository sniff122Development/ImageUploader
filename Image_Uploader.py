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
    import shutil
    import urllib
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
       V: 2.0.0  
=======================

""")

try:
    with open("Config.json") as f:
        Config = json.load(f)
except FileNotFoundError:
    print(u"\u001b[31mThe 'Config.json' file was not found, copying file from 'Config.example.json'\u001b[0m")
    try:
        shutil.copyfile(r"Config.example.json", r"Config.json")
    except:
        print(u"\u001b[31mThe 'Config.example.json' file was not found, downloading from GitHub\u001b[0m")
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/sniff122Development/ImageUploader/master/Config.example.json",
            "Config.json")
    print(
        u"\u001b[31mDone! Exiting application, please edit 'Config.json' and restart. If you need assistance, please see https://github.com/sniff122Development/ImageUploader/wiki\u001b[0m")
    exit()

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIRECTORY = PROJECT_HOME + "/" + Config["webserver"]["upload_directory"]
CONFIG_DIRECTORY = PROJECT_HOME + "/" + Config["webserver"]["data_directory"]

if not os.path.exists(str(CONFIG_DIRECTORY)):
    os.mkdir(CONFIG_DIRECTORY)

if os.path.exists(str(CONFIG_DIRECTORY + "/APIKeys.json")):
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
        apikeys = json.load(f)
else:
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "w") as f:
        f.write("{}")
        f.close()
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "r") as f:
        apikeys = json.load(f)

if os.path.exists(str(CONFIG_DIRECTORY + "/files.json")):
    with open(str(CONFIG_DIRECTORY + "/files.json"), "r") as f:
        files = json.load(f)
else:
    with open(str(CONFIG_DIRECTORY + "/files.json"), "w") as f:
        f.write("{}")
        f.close()
    with open(str(CONFIG_DIRECTORY + "/files.json"), "r") as f:
        files = json.load(f)

if os.path.exists(str(CONFIG_DIRECTORY + "/shortlinks.json")):
    with open(str(CONFIG_DIRECTORY + "/shortlinks.json"), "r") as f:
        shortlinks = json.load(f)
else:
    with open(str(CONFIG_DIRECTORY + "/shortlinks.json"), "w") as f:
        f.write("{}")
        f.close()
    with open(str(CONFIG_DIRECTORY + "/shortlinks.json"), "r") as f:
        shortlinks = json.load(f)


def saveconfigs(keys, filetokens, shortlinks):
    with open(str(CONFIG_DIRECTORY + "/APIKeys.json"), "w") as f:
        json.dump(keys, f, indent=4)
    with open(str(CONFIG_DIRECTORY + "/files.json"), "w") as f:
        json.dump(filetokens, f, indent=4)
    with open(str(CONFIG_DIRECTORY + "/shortlinks.json"), "w") as f:
        json.dump(shortlinks, f, indent=4)


# =============================
# ==========WEBSERVER==========
# =============================


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
    if filename in shortlinks:
        return True
    else:
        return False


@app.route("/", methods=['GET'])
def web_root():
    return render_template("index.htm", uploadapi=str(WEBROOT + "/api/upload"), linkshortapi=str(WEBROOT + "/api/url"), webroot=str(WEBROOT))


@app.route("/js/<jstype>", methods=["GET"])
def return_js(jstype):
    if jstype in ["admin_files.js", "admin_keys.js", "admin_links.js"]:
        return send_from_directory("JS", jstype)
    else:
        return jsonify({"Status": 404, "Message": "Not Found"})


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
            saveconfigs(apikeys, files, shortlinks)
            if Config["bot"]["Enabled"] == "True":
                embed = DiscordObjects.DiscordEmbed(title="New Image Uploaded", description="There is a new image!",
                                                    footer=DiscordObjects.EmbedFooter(""), colour=0xffffff,
                                                    image=DiscordObjects.EmbedImage(
                                                        str("https://" + request.headers['Host'] + "/uploads/" + filename)),
                                                    author=DiscordObjects.EmbedAuthor("ImageUploader"), fields=[
                        DiscordObjects.EmbedField(name="URL:", value=str("https://" + request.headers['Host'] + "/uploads/" + filename),
                                                  inline=False)], thumbnail=DiscordObjects.EmbedImage(
                        str("https://" + request.headers['Host'] + "/uploads/" + filename)))
                webhookcontent = DiscordObjects.DiscordWebhookContent(username="ImageUploader",
                                                                      avatar_url=Config["bot"]["webhook"]["avatar_url"],
                                                                      tts=False, embed=[embed])
                DiscordObjects.WebhookPost(Config["bot"]["webhook"]["url"], webhookcontent)
            global RecentFile
            RecentFile = str("https://" + request.headers['Host'] + "/uploads/" + filename)
            return jsonify({"Status": 200, "Message": "OK", "FileLink": str("https://" + request.headers['Host'] + "/uploads/" + filename)})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden - No file provided"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/url", methods=["POST"])
def shorten_link():
    apikey = str(request.headers.get("Auth"))
    if apikeyvalid(apikey):
        url = str(request.headers.get("url"))
        if url:
            exists = False
            for urlid in shortlinks:
                if url == shortlinks[urlid]:
                    exists = True
                    break
                else:
                    continue
            if not exists:
                urlid = str(secrets.token_hex(4))
                while urlid in shortlinks:
                    urlid = str(secrets.token_hex(4))
                try:
                    apikeys[apikey]["short-urls"].append(urlid)
                except:
                    apikeys[apikey]["short-urls"] = [urlid]
                shortlinks[urlid] = {"url": url, "key": apikey}
                saveconfigs(apikeys, files, shortlinks)
            return jsonify({"Status": 200, "Message": "OK", "shorturl": str("https://" + request.headers['Host'] + "/link/" + urlid)})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden - No url provided"})
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


@app.route("/link/<link>", methods=["GET"])
def get_link(link):
    try:
        if link in shortlinks:
            return redirect(shortlinks[link]["url"])
        else:
            return jsonify({"Status": 404, "Message": "Not Found"})
    except:
        return jsonify({"Status": 500, "Message": "Internal Server Error"})


# ==WEBSERVER=ADMIN==


@app.route("/admin", methods=['GET'])
@basic_auth.required
def admin_root():
    return render_template("admin.htm",
                           webroot=WEBROOT,
                           recentfile=RecentFile)


@app.route("/api/admin/listfiles", methods=["GET"])
def admin_get_files():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]):
        filelist = []
        for filename in files:
            filelist.append(filename)
        return jsonify({"Status": 200, "Message": "Ok", "files": filelist})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/listlinks", methods=["GET"])
def admin_get_links():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]):
        linklist = []
        for linkid in shortlinks:
            linklist.append(linkid)
        return jsonify({"Status": 200, "Message": "Ok", "links": linklist})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/uploadfile", methods=["POST"])
def admin_upload_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        if request.files["file"]:
            filename = str(request.headers.get('FileName'))
            file = request.files["file"]
            savepath = os.path.join(UPLOAD_DIRECTORY, filename)
            file.save(savepath)
            apikeys[apikey]["file-names"].append(filename)
            files[filename] = apikey
            saveconfigs(apikeys, files, shortlinks)
            if Config["bot"]["Enabled"] == "True":
                embed = DiscordObjects.DiscordEmbed(title="New Image Uploaded", description="There is a new image!",
                                                    footer=DiscordObjects.EmbedFooter("There be a new image!"),
                                                    colour=0xffffff, image=DiscordObjects.EmbedImage(
                        str("https://" + request.headers['Host'] + "/uploads/" + filename)), author=DiscordObjects.EmbedAuthor("ImageUploader"),
                                                    fields=[DiscordObjects.EmbedField(name="URL:", value=str(
                                                        "https://" + request.headers['Host'] + "/uploads/" + filename), inline=False)],
                                                    thumbnail=DiscordObjects.EmbedImage(
                                                        str("https://" + request.headers['Host'] + "/uploads/" + filename)))
                webhookcontent = DiscordObjects.DiscordWebhookContent(username="ImageUploader",
                                                                      avatar_url=Config["bot"]["webhook"]["avatar_url"],
                                                                      tts=False, embed=[embed])
                DiscordObjects.WebhookPost(Config["bot"]["webhook"]["url"], webhookcontent)
            global RecentFile
            RecentFile = str("https://" + request.headers['Host'] + "/uploads/" + filename)
            return jsonify({"Status": 200, "Message": "OK", "FileLink": str("https://" + request.headers['Host'] + "/uploads/" + filename)})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden", "Extra Info": "No File Prodived"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/url", methods=["POST"])
def admin_new_url():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        url = str(request.headers.get("url"))
        if url:
            try:
                index = apikeys[apikey]["short-urls"].index(request.headers.get("id"))
                return jsonify({"Status": 403, "Message": "Forbidden - Link ID already exists"})
            except:
                try:
                    apikeys[apikey]["short-urls"].append(request.headers.get("id"))
                except:
                    apikeys[apikey]["short-urls"] = [request.headers.get("id")]
                shortlinks[request.headers.get("id")] = {"url": url, "key": apikey}
                saveconfigs(apikeys, files, shortlinks)
                return jsonify(
                    {"Status": 200, "Message": "OK", "shorturl": str("https://" + request.headers['Host'] + "/link/" + request.headers.get("id"))})
        else:
            return jsonify({"Status": 403, "Message": "Forbidden - No url provided"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/deletefile", methods=["DELETE"])
def admin_delete_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    filename = str(request.headers.get("filename"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        try:
            oldpath = os.path.join("data", "uploads", filename)
            os.remove(oldpath)

            apikey = files[filename]
            del files[filename]

            fileindex = apikeys[apikey]["file-names"].index(filename)
            del apikeys[apikey]["file-names"][fileindex]
            saveconfigs(apikeys, files, shortlinks)
            return jsonify({"Status": 200, "Message": "OK"})
        except FileNotFoundError:
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/deletelink", methods=["DELETE"])
def admin_delete_link():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    lid = str(request.headers.get("id"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        try:

            apikey = shortlinks[lid]["key"]
            del shortlinks[lid]

            linkindex = apikeys[apikey]["short-urls"].index(lid)
            del apikeys[apikey]["short-urls"][linkindex]
            saveconfigs(apikeys, files, shortlinks)
            return jsonify({"Status": 200, "Message": "OK"})
        except KeyError:
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/renamefile", methods=["PUT"])
def admin_rename_file():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    oldfilename = str(request.headers.get("oldfilename"))
    newfilename = str(request.headers.get("newfilename"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
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
            saveconfigs(apikeys, files, shortlinks)
            return jsonify({"Status": 200, "Message": "OK", "NewLink": f"{WEBROOT}/uploads/{newfilename}"})
        except FileNotFoundError:
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/renamelink", methods=["PUT"])
def admin_rename_link():
    apikey = str(request.headers.get("Auth"))
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    oldid = str(request.headers.get("oldid"))
    newid = str(request.headers.get("newid"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]) and apikeyvalid(str(apikey)):
        try:
            oldobj = shortlinks[oldid]
            del shortlinks[oldid]
            shortlinks[newid] = oldobj

            fileindex = apikeys[apikey]["short-urls"].index(oldid)
            apikeys[apikey]["short-urls"].pop(fileindex)
            apikeys[apikey]["short-urls"].append(newid)
            saveconfigs(apikeys, shortlinks, shortlinks)
            return jsonify({"Status": 200, "Message": "OK", "NewLink": f"{WEBROOT}/uploads/{newid}"})
        except Exception as e:
            print(e)
            return jsonify({"Status": 404, "Message": "Not Found"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/newkey", methods=["GET"])
def admin_new_key():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    name = str(request.headers.get("name"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]):
        try:
            changes = APIkeyManagement.genkey(name, apikeys)
            apikeys.update(changes["apikeys"])
            newkey = changes["newkey"]
            saveconfigs(apikeys, shortlinks, shortlinks)
            return jsonify({"Status": 200, "Message": "OK", "newkey": newkey})
        except Exception as e:
            print(e)
            return jsonify({"Status": 500, "Message": "Internal Server Error"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


@app.route("/api/admin/revokekey", methods=["DELETE"])
def admin_revoke_key():
    username = str(request.headers.get("username"))
    password = str(request.headers.get("password"))
    key = str(request.headers.get("key"))
    if (username == Config["webserver"]["admin_auth"]["username"]) and (
            password == Config["webserver"]["admin_auth"]["password"]):
        try:
            changes = APIkeyManagement.revokekey(key, apikeys)
            apikeys.update(changes)
            saveconfigs(apikeys, shortlinks, shortlinks)
            return jsonify({"Status": 200, "Message": "OK"})
        except:
            return jsonify({"Status": 500, "Message": "Internal Server Error"})
    else:
        return jsonify({"Status": 401, "Message": "Unauthorized"})


# ==WEBSERVER=ADMIN==


def flask_thread():
    try:
        app.run(host=listen_address, port=port)
    except:
        print(u"\u001b[31mFailed to start webserver. Make sure you are authorized to listen to port " + str(
            port) + " on " + str(listen_address) + " and try rerunning the application.\u001b[0m")
        raise


x = threading.Thread(target=flask_thread)
x.start()


# =============================
# ==========WEBSERVER==========
# =============================
# ===========DISCORD===========
# =============================

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


@bot.group(name="files")
@commands.check(UserIsAuthorised)
async def __files_command_group__(ctx):
    if ctx.invoked_subcommand is __files_command_group__:
        embed = discord.Embed(title="Unknown or No Files Subcommand Passed",
                              description="You did not provide a known subcommand for the `files` command group, please use the help command for a list of subcommands.",
                              colour=0xff0000)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@__files_command_group__.command(name="recent")
@commands.check(UserIsAuthorised)
async def __recent_file_command__(ctx):
    try:
        embed = discord.Embed(title="Most Recent File Uploaded",
                              description="The most recent file uploaded to the webserver. If an image does not embed, the file must not mave been an image.")
        embed.add_field(name="File Link", value=RecentFile, inline=False)
        if RecentFile == "":
            raise TypeError
        embed.set_image(url=RecentFile)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send("No files have been uploaded since ImageUploader started")


@__files_command_group__.command(name="rename")
@commands.check(UserIsAuthorised)
async def __rename_file__(ctx, currentfile: str, newfile: str):
    try:
        oldpath = os.path.join("data", "uploads", currentfile)
        newpath = os.path.join("data", "uploads", newfile)
        os.rename(oldpath, newpath)

        apikey = shortlinks[currentfile]
        del shortlinks[currentfile]
        shortlinks[newfile] = apikey

        fileindex = apikeys[apikey]["file-names"].index(currentfile)
        del apikeys[apikey]["file-names"][fileindex]
        apikeys[apikey]["file-names"].append(newfile)
        saveconfigs(apikeys, shortlinks, shortlinks)

        embed = discord.Embed(title="The file was renamed", colour=0x00ff00)
        embed.add_field(name=f"{WEBROOT}/uploads/{currentfile}", value=f"{WEBROOT}/uploads/{newfile}")
        embed.set_image(url=f"{WEBROOT}/uploads/{newfile}")
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="File not found",
                              description="The filename you have given was not found, please check the filename",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@__files_command_group__.command(name="delete")
@commands.check(UserIsAuthorised)
async def __delete_file__(ctx, deletefile: str):
    try:
        oldpath = os.path.join("data", "uploads", deletefile)
        os.remove(oldpath)

        apikey = shortlinks[deletefile]
        del shortlinks[deletefile]

        fileindex = apikeys[apikey]["file-names"].index(deletefile)
        del apikeys[apikey]["file-names"][fileindex]

        embed = discord.Embed(title="The file was removed", description="The file name you provided was removed.",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="File not found",
                              description="The filename you have given was not found, please check the filename",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@bot.group(name="links")
@commands.check(UserIsAuthorised)
async def __links_command_group__(ctx):
    if ctx.invoked_subcommand is __files_command_group__:
        embed = discord.Embed(title="Unknown or No Links Subcommand Passed",
                              description="You did not provide a known subcommand for the `links` command group, please use the help command for a list of subcommands.",
                              colour=0xff0000)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@__links_command_group__.command(name="create")
@commands.check(UserIsAuthorised)
async def __create_link_command__(ctx):
    try:
        embed = discord.Embed(title="Most Recent File Uploaded",
                              description="The most recent file uploaded to the webserver. If an image does not embed, the file must not mave been an image.")
        embed.add_field(name="File Link", value=RecentFile, inline=False)
        if RecentFile == "":
            raise TypeError
        embed.set_image(url=RecentFile)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send("No files have been uploaded since ImageUploader started")


@__links_command_group__.command(name="rename")
@commands.check(UserIsAuthorised)
async def __rename_link__(ctx, currentfile: str, newfile: str):
    try:
        index = apikeys[apikey]["short-urls"].index(request.headers.get("id"))
        return jsonify({"Status": 403, "Message": "Forbidden - Link ID already exists"})
    except:
        try:
            apikeys[apikey]["short-urls"].append(request.headers.get("id"))
        except:
            apikeys[apikey]["short-urls"] = [request.headers.get("id")]
        shortlinks[request.headers.get("id")] = {"url": url, "key": apikey}
        saveconfigs(apikeys, files, shortlinks)
        return jsonify(
            {"Status": 200, "Message": "OK", "shorturl": str(WEBROOT + "/link/" + request.headers.get("id"))})


@__links_command_group__.command(name="delete")
@commands.check(UserIsAuthorised)
async def __delete_link__(ctx, deletefile: str):
    try:
        oldpath = os.path.join("data", "uploads", deletefile)
        os.remove(oldpath)

        apikey = shortlinks[deletefile]
        del shortlinks[deletefile]

        fileindex = apikeys[apikey]["file-names"].index(deletefile)
        del apikeys[apikey]["file-names"][fileindex]

        embed = discord.Embed(title="The file was removed", description="The file name you provided was removed.",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except FileNotFoundError:
        embed = discord.Embed(title="File not found",
                              description="The filename you have given was not found, please check the filename",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@bot.group(name="key")
@commands.check(UserIsAuthorised)
async def __apikey_command_group__(ctx):
    if ctx.invoked_subcommand is __files_command_group__:
        embed = discord.Embed(title="Unknown or No API Key Management Subcommand Passed",
                              description="You did not provide a known subcommand for the `key` command group, please use the help command for a list of subcommands.",
                              colour=0xff0000)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)


@__apikey_command_group__.command(name="generate")
@commands.check(UserIsAuthorised)
async def __generate_api_key__(ctx, name: str):
    try:
        changes = APIkeyManagement.genkey(name, apikeys)
        apikeys.update(changes["apikeys"])
        newkey = changes["newkey"]
        saveconfigs(apikeys, shortlinks, shortlinks)

        embed = discord.Embed(title="API Key Generated", description="The API key was generated", colour=0x00ff00)
        embed.add_field(name="API Key", value=newkey)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="An Error Occured",
                              description="An internal error occured, this error has been logged to the console",
                              colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
        print(u"\u001b[31m" + e + "\u001b[0m")


@__apikey_command_group__.command(name="revoke")
@commands.check(UserIsAuthorised)
async def __revoke_api_key__(ctx, key: str):
    try:
        changes = APIkeyManagement.revokekey(key, apikeys)
        apikeys.update(changes)
        saveconfigs(apikeys, shortlinks, shortlinks)

        embed = discord.Embed(title="API Key Revoked", description="", colour=0x00ff00)
        embed.set_footer(text="ImageUploader developed by sniff122/Lewis L. Foster")
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="An Error Occured",
                              description="An internal error occured, this error has been logged to the console",
                              colour=0x00ff00)
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

# =============================
# ==========DISCORD============
# =============================

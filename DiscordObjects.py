from requests import post

def EmbedField(name: str, value: str, inline: bool = False) -> dict:
    return {"name": name, "value": value, "inline": inline}

def EmbedFooter(text: str, icon_url: str = "") -> dict:
    return {"text": text, "icon_url": icon_url}

def EmbedImage(url: str) -> dict:
    return {"url": url}    

def EmbedAuthor(name: str, url: str = "", icon_url: str = "") -> dict:
    return {"url": url, "icon_url": icon_url, "name": name}

def DiscordEmbed(title: str, description: str, footer: EmbedFooter, colour: int, image: EmbedImage, author: EmbedAuthor, fields: list, thumbnail: EmbedImage):
    return {"title": title, "description": title, "footer": footer, "color": colour, "image": image, "author": author, "fields": fields}

def DiscordWebhookContent(embed: dict, username: str, avatar_url: str, tts: bool = False) -> dict:
    return {"embeds": embed, "tts": tts, "username": username, "avatar_url": avatar_url}

def WebhookPost(url, webhookcontent):
    try:
        post(url, json=webhookcontent).text
    except:
        pass
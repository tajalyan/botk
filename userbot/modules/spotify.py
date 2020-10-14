# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit

import spotify_token as st
from requests import get
from telethon.errors import AboutTooLongError
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_DC, SPOTIFY_KEY, bot)
from userbot.events import register

# =================== CONSTANT ===================
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("spotify")

# ████████████████████████████████ #

SPO_BIO_ENABLED = LANG['BIO_ENABLED']
SPO_BIO_DISABLED = LANG['BIO_DISABLED']
SPO_BIO_RUNNING = LANG['BIO_RUNNING']
ERROR_MSG = LANG['ERROR']

USERNAME = SPOTIFY_DC
PASSWORD = SPOTIFY_KEY

ARTIST = 0
SONG = 0

BIOPREFIX = BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False


# ================================================
async def get_spotify_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global ARTIST
    global SONG
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    oldartist = ""
    oldsong = ""
    while SPOTIFYCHECK:
        try:
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            song = data['item']['name']
            OLDEXCEPT = False
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = song
                spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                try:
                    await bot(UpdateProfileRequest(about=spobio))
                except AboutTooLongError:
                    short_bio = "🎧: " + song
                    await bot(UpdateProfileRequest(about=short_bio))
                environ["errorcheck"] = "0"
        except KeyError:
            print(2)

            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                SPOTIFYCHECK = False
                await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                print(ERROR_MSG)
                if BOTLOG:
                    await bot.send_message(BOTLOG_CHATID, ERROR_MSG)
        except JSONDecodeError:
            print(3)
            OLDEXCEPT = True
            await sleep(6)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        except TypeError:
            print(4)
            await dirtyfix()
        except Exception as e:
            print(e)
        SPOTIFYCHECK = False
        await sleep(2)
        await dirtyfix()
    RUNNING = False


async def update_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(4)
    await update_spotify_info()


@register(outgoing=True, pattern="^.spotify aç$")
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.spotify kapa$")
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)


CMD_HELP.update({"spotify": ['Spotify',
    " - `.enablespotify`: Enable Spotify bio updating.\n"
    " - `.disablespotify`: Disable Spotify bio updating.\n"]
})
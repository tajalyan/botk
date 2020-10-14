# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

""" UserBot yardım komutu """

from userbot import CMD_HELP
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__asena")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.asena(?: |$)(.*)")
async def asena(event):
    """ .asena komutu için """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        await event.edit(LANG["NEED_MODULE"])
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)

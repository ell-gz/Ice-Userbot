# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Kalo mau ngecopas, jangan hapus credit ya goblok

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, owner, DEVS, call_py
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply, ice_cmd


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@ice_cmd(pattern="startvc$")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cstartvc(?: |$)(.*)")
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await edit_or_reply(c, "`Vcg Dimulai...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@ice_cmd(pattern="stopvc$")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cstopvc(?: |$)(.*)")
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await edit_or_reply(c, "`Vcg Dihentikan...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@ice_cmd(pattern="vcinvite")
async def _(c):
    xxnx = await edit_or_reply(c, "`Mengundang orang ke Vcg...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botice = list(user_list(users, 6))
    for p in botice:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await xxnx.edit(f"`{z}` **Manusia Berhasil diundang ke VCG**")


@ice_cmd(pattern="vctitle(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cvctitle(?: |$)(.*)")
async def change_title(e):
    title = e.pattern_match.group(1)
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edit_delete(e, "**Silahkan Masukan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await edit_delete(e, f"**Maaf {owner} Bukan Admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await edit_or_reply(e, f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edit_delete(e, f"**ERROR:** `{ex}`")

@ice_cmd(pattern="joinvc(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.joinvcs(?: |$)(.*)")
async def _(event):
    Ice = await edit_or_reply(event, "`Memproses...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await Ice.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    file = "./userbot/resources/audio-ice.mp3"
    if chat_id:
        try:
            await call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await Ice.edit(
                f"❏ **Berhasil Join Ke OS**\n└ **Chat ID:** `{chat_id}`"
            )
        except AlreadyJoinedError:
            await call_py.leave_group_call(chat_id)
            await edit_delete(
                Ice,
                "**ERROR:** `Karena akun lagi di obrolan suara`\n\n• Silahkan coba `.joinvc` lagi",
                45,
            )
        except Exception as e:
            await Ice.edit(f"**INFO:** `{e}`")


@ice_cmd(pattern="leavevc(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.leavevcs(?: |$)(.*)")
async def vc_end(event):
    Ice = await edit_or_reply(event, "`Memproses...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await Ice.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    if chat_id:
        try:
            await call_py.leave_group_call(chat_id)
            await edit_delete(
                Ice,
                f"❏ **Berhasil Turun dari OS**\n└ **Chat ID:** `{chat_id}`",
            )
        except Exception as e:
            await Ice.edit(f"**INFO:** `{e}`")

CMD_HELP.update(
    {
        "vcg": f"**Plugin : **`vcg`\
        \n\n  •  **Syntax :** `{cmd}startvc`\
        \n  •  **Function : **Buat Mulai voice chat group\
        \n\n  •  **Syntax :** `{cmd}stopvc`\
        \n  •  **Function : **Buat Berhentiin voice chat group\
        \n\n  •  **Syntax :** `{cmd}joinvc` atau `{cmd}joinvc` <chatid/username gc>\
        \n  •  **Function : **Buat Gabung ke voice chat group\
        \n\n  •  **Syntax :** `{cmd}leavevc` atau `{cmd}leavevc` <chatid/username gc>\
        \n  •  **Function : **Buat Turun dari voice chat group\
        \n\n  •  **Syntax :** `{cmd}vctitle` <title vcg>\
        \n  •  **Function : **Buat Mengubah title/judul voice chat group\
        \n\n  •  **Syntax :** `{cmd}vcinvite`\
        \n  •  **Function : **Ngundang Member group ke voice chat group\
    "
    }
)

       
       
        

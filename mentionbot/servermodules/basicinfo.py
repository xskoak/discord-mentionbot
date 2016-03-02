import asyncio

import discord

import utils
import errors
from servermodule import ServerModule
import cmd

class BasicInfo(ServerModule):

   MODULE_NAME = "Basic Information"
   MODULE_SHORT_DESCRIPTION = "Retrieves basic information about the server, users, etc."
   RECOMMENDED_CMD_NAMES = ["basicinfo"]
   
   _SECRET_TOKEN = utils.SecretToken()
   _cmd_dict = {}

   _HELP_SUMMARY = """
PLACEHOLDER FOR {mod}
   """.strip()

   # TODO: Add this to help detail in the future...
   # *Note: Dates are presented in ISO 8601 format.*

   async def _initialize(self, resources):
      self._client = resources.client
      return

   async def msg_preprocessor(self, content, msg, default_cmd_prefix):
      str_avatar = default_cmd_prefix + "avatar"
      str_whois = default_cmd_prefix + "whois"
      str_thisserver = default_cmd_prefix + "thisserver"
      str_servericon = default_cmd_prefix + "servericon"
      if content.startswith(str_avatar):
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      elif content.startswith(str_whois):
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      elif content.startswith(str_thisserver):
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      elif content.startswith(str_servericon):
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      return content

   @cmd.add(_cmd_dict, "avatar", "dp", "avatarurl")
   async def _cmdf_avatar(self, substr, msg, privilege_level):
      """`{p}avatar [user]` - Get a user's avatar."""
      substr = substr.strip()
      user = None
      if len(substr) == 0:
         user = msg.author
      else:
         user = self._client.search_for_user(substr, enablenamesearch=True, serverrestriction=msg.server)
         if user is None:
            return await self._client.send_msg(msg, substr + " doesn't even exist m8")

      # Guaranteed to have a user.
      avatar = user.avatar_url
      if avatar == "":
         return await self._client.send_msg(msg, substr + " m8 get an avatar")
      else:
         return await self._client.send_msg(msg, avatar)

   @cmd.add(_cmd_dict, "user", "whois", "who")
   async def _cmdf_user(self, substr, msg, privilege_level):
      """`{p}whois [user]` - Get user info."""
      # Get user. Copied from _cmd_avatar()...
      substr = substr.strip()
      user = None
      if len(substr) == 0:
         user = msg.author
      else:
         user = self._client.search_for_user(substr, enablenamesearch=True, serverrestriction=msg.server)
         if user is None:
            return await self._client.send_msg(msg, substr + " doesn't even exist m8")
      
      # Guaranteed to have a user.
      buf = "```"
      buf += "\nID: " + user.id
      buf += "\nName: " + user.name
      buf += "\nAvatar hash: "
      if user.avatar is None:
         buf += "[no avatar]"
      else:
         buf += str(user.avatar)
      buf += "\nJoin date: " + user.joined_at.isoformat() + " UTC"
      buf += "\nServer Deafened: " + str(user.deaf)
      buf += "\nServer Mute: " + str(user.mute)
      buf += "\nServer Roles:"
      for role in user.roles:
         buf += "\n   {0} (ID: {1})".format(role.name.replace("@","@ "), role.id)
      buf += "\n```"
      return await self._client.send_msg(msg, buf)

   @cmd.add(_cmd_dict, "server", "thisserver")
   async def _cmdf_server(self, substr, msg, privilege_level):
      """`{p}thisserver` - Get some simple server info and statistics."""
      s = msg.server
      # Count voice and text channels
      text_ch_total = 0
      voice_ch_total = 0
      for channel in s.channels:
         if channel.type == discord.ChannelType.text:
            text_ch_total += 1
         else:
            voice_ch_total += 1

      buf = "```"
      buf += "\nID: " + s.id
      buf += "\nName: " + s.name
      buf += "\nIcon hash: "
      if s.icon is None:
         buf += "[no icon]"
      else:
         buf += str(s.icon)
      buf += "\nRegion: " + str(s.region)
      buf += "\nOwner: {0} (ID: {1})".format(s.owner.name, s.owner.id)
      buf += "\nNumber of roles: " + str(len(s.roles))
      buf += "\nNumber of members: " + str(len(s.members))
      buf += "\nNumber of text channels: " + str(text_ch_total)
      buf += "\nNumber of voice channels: " + str(voice_ch_total)
      buf += "\n```"
      return await self._client.send_msg(msg, buf)

   @cmd.add(_cmd_dict, "servericon")
   async def _cmdf_servericon(self, substr, msg, privilege_level):
      """`{p}servericon` - Get server icon."""
      if msg.server.icon_url == "":
         return await self._client.send_msg(msg, "This server has no icon.")
      else:
         return await self._client.send_msg(msg, str(msg.server.icon_url))

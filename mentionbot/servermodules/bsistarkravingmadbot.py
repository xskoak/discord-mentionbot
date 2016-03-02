import asyncio
import random

import discord

import utils
import errors
from servermodule import ServerModule
import cmd

class BsiStarkRavingMadBot(ServerModule):

   MODULE_NAME = "BSI StarkRavingMadBot"
   MODULE_SHORT_DESCRIPTION = "Allows this bot to stand-in for the bot *StarkRavingMadBot*."
   RECOMMENDED_CMD_NAMES = ["bsistarkravingmadbot", "stark"]
   
   _SECRET_TOKEN = utils.SecretToken()
   _cmd_dict = {}

   _HELP_SUMMARY = """
PLACEHOLDER FOR {mod}
   """.strip()

   # STARK_PF = "$" # TODO: Consider implementing this.

   STARK_HELP = """
**I'm acting as a stand-in for StarkRavingMadBot.**
**I have the following commands implemented:**
- $avatar
~~- $blame~~
- $choose
~~- $color~~
~~- $doot~~
- $flip
- $git
- $help
~~- $intensify~~
~~- $invite~~
~~- $pengu~~
~~- $reddit~~
- $rip
- $roll
- $say
- $serverstats
- $sleep
~~- $spooderman~~
~~- $subreddit~~
~~- $swole~~
~~- $truth~~
~~- $ud~~
- $whois

*Reference commit: 89c88d92c98e7ccdf4b45092b6a139982d01acec, 6/2/16*
*Disclaimer: Behaviour may not match up 1:1.*
For reference, I require the following modules to be installed:
`Basic Information`
`Random`
   """.strip()

   STARKRAVINGMADBOT_DEFAULTID = "121281613660160000"

   async def _initialize(self, resources):
      self._client = resources.client
      self._server = resources.server

      # pf = self._client.get_server_bot_instance(self._server).cmd_prefix
      pf = "/"
      this = pf + self._cmd_names[0]
      cmdnotimplemented = this + " cmdnotimplemented"

      self._stark = self._client.search_for_user(self.STARKRAVINGMADBOT_DEFAULTID, enablenamesearch=False, serverrestriction=self._server)
      self._preprocessor_replace = { # Maps commands to their exact substitute.
         "$avatar": pf + "basicinfo avatar",
         "$blame": cmdnotimplemented,
         "$choose": pf + "random choose",
         "$color": cmdnotimplemented,
         "$doot": cmdnotimplemented,
         "$flip": pf + "random coin",
         "$git": this + " git",
         "$help": this + " help",
         "$intensify": cmdnotimplemented,
         "$invite": cmdnotimplemented,
         "$pengu": cmdnotimplemented,
         "$reddit": cmdnotimplemented,
         "$rip": this + " rip",
         "$roll": pf + "random dice",
         "$say": this + " say",
         "$serverstats": pf + "basicinfo server",
         "$sleep": this + " sleep",
         "$spooderman": cmdnotimplemented,
         "$subreddit": cmdnotimplemented,
         "$swole": cmdnotimplemented,
         "$truth": cmdnotimplemented,
         "$ud": cmdnotimplemented,
         "$whois": pf + "basicinfo user",
      }

      self._sleep_choices = [
         "Go to sleep",
         "Git to bed",
         "(ﾉಠ_ಠ)ﾉ*:・ﾟ✧\ngit to sleep"
      ]

      self._c = self._cmd_names[0] # A shorter name. This will be used a LOT.
      return

   async def msg_preprocessor(self, content, msg, default_cmd_prefix):
      if self.dont_run_module():
         return content # Short-circuit if stark is not offline.
      
      # IMPORTANT: This might be a problem if the message implementation of
      #            StarkRavingMadBot changes. e.g. if messages are
      #            invoked with a prefix that has a space.
      (left, right) = utils.separate_left_word(content)
      try:
         left = self._preprocessor_replace[left.lower()]
      except KeyError:
         return content

      if right == "":
         return left
      else:
         return left + " " + right

   @cmd.add(_cmd_dict, "cmdnotimplemented")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}` - (Please don't use this command.)"""
      buf = "Sorry, I haven't implemented my own version of that command yet."
      await self._client.send_msg(msg, buf)
      return

   @cmd.add(_cmd_dict, "help")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}` - Get a stand-in version of Stark's help message."""
      await self._client.send_msg(msg, self.STARK_HELP)
      return

   @cmd.add(_cmd_dict, "git")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}` - Get a stand-in version of Stark's source command."""
      buf = "*Now, I'm not StarkRavingMadBot, but here's a copy-paste of what it would've said:*"
      buf += "\n\"You can find my source at https://github.com/josh951623/StarkRavingMadBot/tree/master. If you'd like to suggest a feature, go ahead and join me in my dev server: https://discord.gg/0ktzcmJwmeWuQtiM.\""
      await self._client.send_msg(msg, buf)
      return

   @cmd.add(_cmd_dict, "say")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}`"""
      await self._client.send_msg(msg, "m8")
      return

   @cmd.add(_cmd_dict, "sleep")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}`"""
      await self._client.send_msg(msg, random.choice(self._sleep_choices))
      return

   @cmd.add(_cmd_dict, "rip")
   async def _cmdf_cmdnotimplemented(self, substr, msg, privilege_level):
      """`{cmd}`"""
      await self._client.send_msg(msg, "doesnt even deserve a funeral")
      return

   def dont_run_module(self):
      try:
         return not utils.member_is_offline(self._stark)
      except AttributeError:
         return False


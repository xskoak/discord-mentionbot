import asyncio
import random

import discord

import utils
import errors
from enums import PrivilegeLevel
from servermodule import ServerModule

class JCFDiscord(ServerModule):
   
   _SECRET_TOKEN = utils.SecretToken()

   RECOMMENDED_CMD_NAMES = ["jcfdiscord"]

   MODULE_NAME = "JCFDiscord"
   MODULE_SHORT_DESCRIPTION = "Functions built specifically for the JCFDiscord community."

   _HELP_SUMMARY_LINES = """
`{pf}functions [types]` - Get a list of MBTI function stacks.
`{pf}choosetruth` - Randomly choose a truth player in the channel.
   """.strip().splitlines()

   _HELP_DETAIL_LINES = """
`{pf}functions [types]` - Get a list of MBTI function stacks.
`{pf}choosetruth` - Randomly choose a truth player in the channel.
   """.strip().splitlines()

   _FUNCTION_STACKS = {
      "INTJ": "Ni - Te - Fi - Se",
      "INTP": "Ti - Ne - Si - Fe",
      "ENTJ": "Te - Ni - Se - Fi",
      "ENTP": "Ne - Ti - Fe - Si",
      "INFJ": "Ni - Fe - Ti - Se",
      "INFP": "Fi - Ne - Si - Te",
      "ENFJ": "Fe - Ni - Se - Ti",
      "ENFP": "Ne - Fi - Te - Si",
      "ISTJ": "Si - Te - Fi - Ne",
      "ISFJ": "Si - Fe - Ti - Ne",
      "ESTJ": "Te - Si - Ne - Fi",
      "ESFJ": "Fe - Si - Ne - Ti",
      "ISTP": "Ti - Se - Ni - Fe",
      "ISFP": "Fi - Se - Ni - Te",
      "ESTP": "Se - Ti - Fe - Ni",
      "ESFP": "Se - Fi - Te - Ni",
   }

   _MBTI_TYPES = [
      "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
      "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP",
   ]

   @classmethod
   async def get_instance(cls, cmd_names, resources):
      inst = cls(cls._SECRET_TOKEN)
      inst._res = resources
      inst._client = inst._res.client
      inst._cmd_names = cmd_names
      return inst

   def __init__(self, token):
      if not token is self._SECRET_TOKEN:
         raise RuntimeError("Not allowed to instantiate directly. Please use get_instance().")
      return

   @property
   def cmd_names(self):
      return self._cmd_names

   async def msg_preprocessor(self, content, msg, default_cmd_prefix):
      str_functions = default_cmd_prefix + "functions"
      str_choosetruth = default_cmd_prefix + "choosetruth"
      if content.startswith(str_functions + " ") or (content == str_functions): # TODO: IMPORTANT! FIX THE INCONSISTENCY.
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      elif content == str_choosetruth:
         content = utils.add_base_cmd(content, default_cmd_prefix, self._cmd_names[0])
      return content

   def get_help_summary(self, cmd_prefix, privilegelevel=0):
      return utils.prepare_help_content(self._HELP_SUMMARY_LINES, cmd_prefix, privilegelevel)

   def get_help_detail(self, substr, cmd_prefix, privilegelevel=0):
      return utils.prepare_help_content(self._HELP_DETAIL_LINES, cmd_prefix, privilegelevel)

   async def process_cmd(self, substr, msg, privilegelevel=0):
      
      # Process the command itself
      (left, right) = utils.separate_left_word(substr)
      if (left == "functions") or (left == "fn") or (left == "stack"):
         args = right.split()
         types = []
         for arg in args:
            arg = arg.upper()
            if arg in self._MBTI_TYPES:
               types.append(arg)
         if len(types) == 0:
            types = self._MBTI_TYPES
         buf = "```\n"
         for mbti_type in types:
            buf += mbti_type + " = " + self._FUNCTION_STACKS[mbti_type] + "\n"
         buf += "```"
         await self._client.send_msg(msg, buf)

      elif left == "choosetruth":
         topic = msg.channel.topic
         if topic is None:
            await self._client.send_msg(msg, "There doesn't appear to be a truth game in here.")
            raise errors.OperationAborted
         
         mentions = utils.get_all_mentions(topic)
         if len(mentions) == 0:
            await self._client.send_msg(msg, "There doesn't appear to be a truth game in here.")
            raise errors.OperationAborted
         
         try:
            mentions.remove(msg.author.id)
            if len(mentions) == 0:
               await self._client.send_msg(msg, "<@{}>".format(msg.author.id))
               raise errors.OperationAborted
         except ValueError:
            pass
         
         choice = random.choice(mentions)
         buf = "<@{}>\n".format(choice)
         buf += "My choices were: "
         for mention in mentions:
            user = self._client.search_for_user(mention, enablenamesearch=False, serverrestriction=self._res.server)
            if user is None:
               buf += "<@{}>, ".format(mention)
            else:
               buf += "{}, ".format(user.name)
         buf = buf[:-2]
         await self._client.send_msg(msg, buf)

      else:
         raise errors.InvalidCommandArgumentsError

      return


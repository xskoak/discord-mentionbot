# Modules
from servermodules.mentions.mentions import Mentions
from servermodules.random import Random

class ServerModuleFactory:

   # Please hard-code every module class into this list.
   _MODULE_LIST = [
      Mentions,
      Random
   ]

   def __init__(self, client):
      self._client = client
      self._modules = {}

      for module in self._MODULE_LIST:
         self._modules[module.MODULE_NAME] = module
      return

   # Generator for iterating through all modules.
   def module_list_gen(self):
      for (name, module) in self._modules:
         yield (name, module.MODULE_SHORT_DESCRIPTION)

   def module_exists(self, module_name):
      try:
         self._modules[module_name]
         return True
      except KeyError:
         return False

   # PRECONDITION: self.module_exists(module_name) == True
   def new_module_instance(self, module_name):
      module = self._modules[module_name]
      return module.get_instance(module.RECOMMENDED_CMD_NAMES, self._client)







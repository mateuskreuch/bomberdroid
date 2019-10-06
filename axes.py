class Axis:
   def __init__(self):
      self.value = 0

      self._values = [0, 0]
      self._keys   = {}
      
   def assign_keys(self, *args):
      for key, sign in args:
         self._keys[key] = sign

   def react_to_key(self, key, state):
      if key in self._keys:
         if self._keys[key] == 1:
            self._values[0] += state
         
         else:
            self._values[1] += state

         if self._values[0] != 0 and self._values[1] == 0:
            self.value = 1

         elif self._values[0] == 0 and self._values[1] != 0:
            self.value = -1
         
         else:
            self.value = 0
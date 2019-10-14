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

         if   self._values[0] != 0 and self._values[1] == 0: self.value = 1
         elif self._values[0] == 0 and self._values[1] != 0: self.value = -1
         else:                                               self.value = 0

class Vector:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __mul__(self, othr):
      try:    return Vector(self.x * othr.x, self.y * othr.y)
      except: return Vector(self.x * othr, self.y * othr)

   def __str__(self):
      return "(%s, %s)" % (self.x, self.y)
   
   def totuple(self):
      return (self.x, self.y)

class Matrix:
   def __init__(self, w, h):
      self.cols = w
      self.rows = h
      
      self._elms = [None] * (w * h)
   
   def get(self, x, y):
      return self._elms[y * self.cols + x]

   def set(self, x, y, value = None):
      self._elms[y * self.cols + x] = value

   def __iter__(self):
      x = 0
      y = 0

      while y < self.rows:
         yield x, y, self._elms[y * self.cols + x]

         x += 1

         if x >= self.cols:
            x = 0
            y += 1
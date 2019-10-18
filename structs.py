# this file contains general data structures
# they simply assist and facilitate overall game development

class Vector:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __mul__(self, othr):
      try:    return Vector(self.x * othr.x, self.y * othr.y)
      except: return Vector(self.x * othr  , self.y * othr  )

   def __str__(self):
      return "(%s, %s)" % (self.x, self.y)
   
   def unpack(self):
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

   def move(self, x0, y0, x1, y1):
      self._elms[y1 * self.cols + x1] = self._elms[y0 * self.cols + x0]
      self._elms[y0 * self.cols + x0] = None

   def is_inside(self, x, y):
      return x >= 0 and y >= 0 and x < self.cols and y < self.rows

   def __iter__(self):
      x = y = 0

      while y < self.rows:
         yield x, y, self._elms[y * self.cols + x]

         x += 1

         if x >= self.cols:
            x = 0
            y += 1

class Tensor:
   def __init__(self, w, h, z):
      self.cols = w
      self.rows = h
      self.lyrs = z

      self._elms = [None] * (w * h * z)
   
   def get(self, x, y, z):
      return self._elms[z * self.rows * self.cols + y * self.cols + x]
   
   def set(self, x, y, z, value = None):
      self._elms[z * self.rows * self.cols + y * self.cols + x] = value

   def move(self, x0, y0, z0, x1, y1, z1):
      self._elms[z1 * self.rows * self.cols + y1 * self.cols + x1] = self._elms[z0 * self.rows * self.cols + y0 * self.cols + x0]
      self._elms[z0 * self.rows * self.cols + y0 * self.cols + x0] = None
   
   def is_inside(self, x, y, z = 0):
      return x >= 0 and y >= 0 and z >= 0 and x < self.cols and y < self.rows and z < self.lyrs
   
   def __iter__(self):
      x = y = z = 0

      while z < self.lyrs:
         yield x, y, z, self._elms[z * self.rows * self.cols + y * self.cols + x]

         x += 1

         if x >= self.cols:
            x = 0
            y += 1

            if y >= self.rows:
               y = 0
               z += 1

class Axis:
   def __init__(self, *keys):
      self.value = 0

      self._counter = [0, 0]
      self._keys    = {key: sign for key, sign in keys}

   def react_to_key(self, key, state):
      if key in self._keys:
         if   self._keys[key] > 0: self._counter[0] += state
         elif self._keys[key] < 0: self._counter[1] += state

         if   self._counter[0] and not self._counter[1]: self.value = 1
         elif self._counter[1] and not self._counter[0]: self.value = -1
         else:                                           self.value = 0
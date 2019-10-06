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
from pygame.sprite import RenderClear
from subpixelsurface import *

# This class keeps an ordered list of sprites in addition to the dict,
# so we can draw in the order the sprites were added.
class OrderedRenderUpdates(RenderClear):
  def __init__(self, group = ()):
    self.spritelist = []
    RenderClear.__init__(self, group)

  # Some quick benchmarks show that [:] is the fastest way to get a
  # shallow copy of a list.
  def sprites(self):
    return self.spritelist[:]

  # This is kind of a wart -- the actual RenderUpdates class doesn't
  # use add_internal in its add method, so just overriding
  # add_internal won't work.
  def add(self, sprite):
    if hasattr(sprite, '_spritegroup'):
      for sprite in sprite.sprites():
        if sprite not in self.spritedict:
          self.add_internal(sprite)
          sprite.add_internal(self) 
    else:
      try: len(sprite)
      except (TypeError, AttributeError):
        if sprite not in self.spritedict:
          self.add_internal(sprite)
          sprite.add_internal(self) 
      else:
        for sprite in sprite:
          if sprite not in self.spritedict:
            self.add_internal(sprite)
            sprite.add_internal(self) 

  def add_internal(self, sprite):
    RenderClear.add_internal(self, sprite)
    self.spritelist.append(sprite)

  def remove_internal(self, sprite):
    RenderClear.remove_internal(self, sprite)
    self.spritelist.remove(sprite)

  def draw(self, surface):
    spritelist = self.spritelist
    spritedict = self.spritedict
    surface_blit = surface.blit
    dirty = self.lostsprites
    self.lostsprites = []
    dirty_append = dirty.append
    for s in spritelist:
      r = spritedict[s]
      newrect = surface_blit(s.image, s.rect)
      #newrect = surfaceblit(s.image_subpixel.at(s.rect.center), (s.rect.center))
      if r is 0:
        dirty_append(newrect)
      else:
        if newrect.colliderect(r):
          dirty_append(newrect.union(r))
        else:
          dirty_append(newrect)
      spritedict[s] = newrect
    return dirty

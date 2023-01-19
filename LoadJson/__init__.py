if __name__ == "__main__":
      from .. import main

import json
import pygame

class Textures():
  def __init__(self,screen):
    self.screen = screen
    self.jsonitems = {}
    self.classes = [
      "Square", # 1 
      "Image", # 1
      "Text", # 0
      "Circle", # 0
      "Background", # 1
      "Button"
    ]
  def LoadFunc(self, func):
        self.func = func
  def jsoncon(self,js):
    loads = json.load(js)
    for l in loads:
      if l != "Comments":
        for o in loads[l]:
          try:
            item = loads[l][o]["Class"]
          except KeyError:
            print("KeyError when getting class. Did you add a class you your element")
          try:
            if loads[l][o]["Class"] == "Square":
              self.jsonitems[str(loads[l][o]["id"])] = Square(
                self.screen,
                loads[l][o]["pos"],
                loads[l][o]["size"],
                loads[l][o]["color"],
              )
            elif loads[l][o]["Class"] == "Image":
              self.jsonitems[str(loads[l][o]["id"])] = Image(
                loads[l][o]["path"],
                loads[l][o]["pos"],
                self.screen
                )
              if "flip" in loads[l][o]:
                if loads[l][o]["flip"] == "true":
                  print("Fliping Image\nId:"+str(loads[l][o]["id"])+"\nPath:"+loads[l][o]["path"])
                  self.jsonitems[str(loads[l][o]["id"])].flip()
            elif loads[l][o]["Class"] == "Background":
              self.screen.fill(loads[l][o]["color"])
            elif loads[l][o]["Class"] == "Text":
              self.jsonitems[str(loads[l][o]["id"])] = Text(
                loads[l][o]["fontSize"],
                loads[l][o]["text"],
                loads[l][o]["font"],
                loads[l][o]["color"],
                loads[l][o]["pos"],
                self.screen
                )
            elif loads[l][o]["Class"] == "Circle":
              self.jsonitems[str(loads[l][o]["id"])] = Circle(
                loads[l][o]["radius"],
                loads[l][o]["color"],
                loads[l][o]["pos"],
                self.screen
              )
            elif loads[l][o]["Class"] == "Button":
              if "repeat" not in loads[l][o]:
                loads[l][o]["repeat"] = False
              self.jsonitems[str(loads[l][o]["id"])] = Button(
                loads[l][o]["size"],
                loads[l][o]["pos"],
                self.screen,
                self.func[loads[l][o]["callback"]],
                loads[l][o]["args"],
                loads[l][o]["repeat"]
              )
          except KeyError as i:
            print(f"Error while loading {js.name}: {i} Not found in {item}. Did you forget to add it")
    return(self.screen)
  def update(self):
    for i in self.jsonitems:
      self.screen.blit(self.jsonitems[i].update(),(0,0))
    return(self.screen)
  def getjson(self,id):
    try:
      return(self.jsonitems[str(id)])
    except KeyError as err:
      print("Key Error: " + str(err) + "\n Id is probably out of range")



#Square class

class Square():
    def __init__(self,surface,pos,size,color):
        self.lenth = 1
        self.screen = surface
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.pos,self.size)
    def move(self,pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos,self.size)
    def set_color(self,color):
        self.color = color
    def update(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        return(self.screen)



# Image class

class Image():
  def __init__(self, path, pos, screen):
    self.path = path
    self.pos = pos
    self.screen = screen
    self.image = pygame.image.load(path)
  def move(self,pos): 
    self.pos = pos
  def flip(self):
      self.image = pygame.transform.flip(self.image,True,False)
  def update(self):
      self.screen.blit(self.image,self.pos)
      return(self.screen)

class Text():
    def __init__(self, fontSize, text, font, color, pos, screen):
      self.text = text
      self.pos = pos
      self.screen = screen
      self.color=color
      self.size = fontSize
      self.font = font
    def move(self,pos):
      self.pos = pos
    def changeText(self,text):
      self.text=text
    def changeFont(self,font):
      self.font=font
    def changeColor(self,color):
          self.color = color
    def update(self):
      myfont = pygame.font.SysFont(self.font, self.size)
      textsurface = myfont.render(self.text, False, self.color)
      self.screen.blit(textsurface,self.pos)
      return(self.screen)

class Circle():
  def __init__(self,radius,color,pos,screen):
    self.radius=radius
    self.color=color
    self.pos=pos
    self.screen=screen
  def move(self,pos):
    self.pos=pos
  def changeColor(self,color):
    self.color=color
  def changeRadius(self,radius):
    self.radius=radius
  def update(self):
    pygame.draw.circle(self.screen,self.color,(self.pos[0]-self.radius,self.pos[1]-self.radius),self.radius)
    return(self.screen)

def error(**args):
  print("No callback for button")

class Button():
  def __init__(self,size,pos,screen,callback=error,args=[], repeat=False):
    self.size=size
    self.pos=pos
    self.screen=screen
    self.func = [callback,args]
    self.pressed = False
    self.repeat = repeat
  def changeArgs(self,args):
    self.func[1] = args
  def move(self,pos):
    self.pos=pos
  def update(self):
    # Register Click
    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] > self.pos[0] and pygame.mouse.get_pos()[1] > self.pos[1] and pygame.mouse.get_pos()[0] < (self.pos[0]+self.size[0]) and pygame.mouse.get_pos()[1] < (self.pos[1]+self.size[1]):
      if self.pressed != True or self.repeat:
        self.func[0](*self.func[1])
      self.pressed = True
    else:
      self.pressed = False
    return(self.screen)
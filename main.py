import pygame
import LoadJson as utils
import time
pygame.init()


json_data = open("level.json")

screen = pygame.display.set_mode([480, 480])
def func(text="error"):
    print(__name__, text)

Texts = utils.Textures(screen)

Texts.LoadFunc({"func": func})

screen.blit(Texts.jsoncon(json_data),(0,0))
Text = Texts.getjson("3")
running = True

i=0

while running:
    i+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(Texts.update(), (0,0))
    
    Text.changeText(str(i))
    pygame.display.flip()
    time.sleep(1/60)
pygame.quit()

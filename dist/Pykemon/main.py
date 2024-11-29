import pygame
from ggoBugi.pokemonsurvival import pokemonsurvival
from jammanbo.jammanbo import  jammanbo
from pikachuValleyball.pikachuValleyball import pikacjuValleyball

pygame.init()

size_x = 500
size_y = 500
running = True  

screen = pygame.display.set_mode((size_x,size_y))
pygame.display.set_caption("pykemon")

fontPath = "Pykemon/assets/neodgm.ttf"

menuFont = pygame.font.Font(fontPath, 50)
subMenuFont = pygame.font.Font(fontPath, 20)

menuText = menuFont.render("잠만보 먹방", True, (255, 255, 255))
subMenuText = subMenuFont.render("엔터키 눌러서 시작하기!", True, (255, 255, 255))

selectIndex = 0

def menuTextChange():
    global menuText
    if selectIndex == 0:
        menuText = menuFont.render("잠만보 먹방", True, (255, 255, 255))
    elif selectIndex == 1:
        menuText = menuFont.render("피카츄 배구", True, (255, 255, 255))
    elif selectIndex == 2:
        menuText = menuFont.render("꼬부기 살아남기", True, (255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if selectIndex > 0:
                    selectIndex -= 1
                    menuTextChange()

            elif event.key == pygame.K_RIGHT:
                if selectIndex < 2:
                    selectIndex += 1
                    menuTextChange()

            elif event.key == pygame.K_RETURN:
                if selectIndex == 0:
                    jammanbo()
                elif selectIndex == 1:
                    pikacjuValleyball()
                elif selectIndex == 2:
                    pokemonsurvival()

        elif event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  

    menuTextRect = menuText.get_rect(center=(size_x // 2, size_y // 2))
    subMenuTextRect = subMenuText.get_rect(center=(size_x // 2, size_y // 2 + 36))

    screen.blit(menuText, menuTextRect.topleft)  
    screen.blit(subMenuText, subMenuTextRect.topleft)  
    
    pygame.display.update()
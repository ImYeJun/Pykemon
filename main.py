import pygame
from ggoBugi.pokemonsurvival import pokemonsurvival
from jammanbo.jammanbo import  jammanbo
from pikachuValleyball.pikachuValleyball import pikacjuValleyball

pygame.init()

size_x = 600
size_y = 500
running = True  


screen = pygame.display.set_mode((size_x,size_y))
pygame.display.set_caption("pykemon")

fontPath = "Pykemon/assets/neodgm.ttf"

jammanbo_background = pygame.image.load("Pykemon/jammanbo/img/background.png")
jammanbo_background = pygame.transform.scale(jammanbo_background,(size_x,size_y))
pikachuValleyball_background = pygame.image.load("Pykemon/pikachuValleyball/background.png")
pikachuValleyball_background = pygame.transform.scale(pikachuValleyball_background,(size_x,size_y))
ggobugi_background = pygame.image.load("Pykemon/ggoBugi/pokesurv_image/background.png")
ggobugi_background = pygame.transform.scale(ggobugi_background,(size_x,size_y))

menuFont = pygame.font.Font(fontPath, 50)
subMenuFont = pygame.font.Font(fontPath, 20)
gameInfoFont = pygame.font.Font(fontPath, 15)
backgound = jammanbo_background

menuText = menuFont.render("잠만보 먹방", True, (0,0,0))
subMenuText = subMenuFont.render("엔터키 눌러서 시작하기!", True, (0,0,0))
explainText = subMenuFont.render("(좌우 방향키로 게임 선택)", True, (0,0,0))
gameInfoText = gameInfoFont.render("좌우 방향 키로 이동하면서 폭탄을 피해 과일을 먹으면 점수를 얻음",True,(0,0,0))

selectIndex = 0

def menuTextChange():
    global menuText
    if selectIndex == 0:
        menuText = menuFont.render("잠만보 먹방", True, (0,0,0))
    elif selectIndex == 1:
        menuText = menuFont.render("피카츄 배구", True, (0,0,0))
    elif selectIndex == 2:
        menuText = menuFont.render("꼬부기 살아남기", True, (0,0,0))

def backgroundChange():
    global backgound
    if selectIndex == 0:
        backgound = jammanbo_background
    elif selectIndex == 1:
        backgound = pikachuValleyball_background
    elif selectIndex == 2:
        backgound = ggobugi_background

def gameInfoChange():
    global gameInfoText
    if selectIndex == 0:
        gameInfoText = gameInfoFont.render("좌우 방향 키로 이동하면서 폭탄을 피해 과일을 먹으면 점수를 얻음",True,(0,0,0))
    elif selectIndex == 1:
        gameInfoText = gameInfoFont.render("두 명의 플레이어가 피카츄 배구를 진행함(player1 : wasd, player2 : 방향키)",True,(0,0,0))
    elif selectIndex == 2:
        gameInfoText = gameInfoFont.render("방향키로 꼬부기를 이동시키고, 스페이스 키로 물방울을 발사해 적을 처치함",True,(0,0,0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if selectIndex > 0:
                    selectIndex -= 1
                    menuTextChange()
                    backgroundChange()
                    gameInfoChange()

            elif event.key == pygame.K_RIGHT:
                if selectIndex < 2:
                    selectIndex += 1
                    menuTextChange()
                    backgroundChange()
                    gameInfoChange()

            elif event.key == pygame.K_RETURN:
                if selectIndex == 0:
                    jammanbo()
                elif selectIndex == 1:
                    pikacjuValleyball()
                elif selectIndex == 2:
                    pokemonsurvival  ()

        elif event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  

    menuTextRect = menuText.get_rect(center=(size_x // 2, size_y // 2))
    subMenuTextRect = subMenuText.get_rect(center=(size_x // 2, size_y // 2 + 36))
    explainTextRect = explainText.get_rect(center=(size_x // 2, size_y // 2 + 60))
    gameInfoTextRect = gameInfoText.get_rect(center=(size_x // 2, size_y // 2 + 80))

    screen.blit(backgound, backgound.get_rect().topleft)
    screen.blit(menuText, menuTextRect.topleft)  
    screen.blit(subMenuText, subMenuTextRect.topleft)  
    screen.blit(explainText, explainTextRect.topleft)  
    screen.blit(gameInfoText, gameInfoTextRect.topleft)

    pygame.display.update()
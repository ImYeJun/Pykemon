def jammanbo():
    import pygame
    import random
    import sys

    # 초기 설정
    pygame.init()

    # 화면 크기
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("잠만보의 과일 먹기")

    # FPS 설정
    clock = pygame.time.Clock()
    FPS = 60

    # 폰트 설정
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)

    # 색상
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # 배경음악 및 효과음
    path = "Pykemon\jammanbo\img/"
    pygame.mixer.music.load(path + "background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    eat_sound = pygame.mixer.Sound(path + "eat_sound.wav.mp3")
    eat_sound.set_volume(0.7)

    bomb_sound = pygame.mixer.Sound(path + "bomb_sound.wav.mp3")
    bomb_sound.set_volume(0.7)

    game_over_sound = pygame.mixer.Sound(path + "game_over_sound.wav")
    game_over_sound.set_volume(0.7)

    # 플레이어 속성
    player_width, player_height = 120, 120
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 20
    player_speed = 7

    # 배경 이미지
    background_image = pygame.image.load(path + "background.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # 잠만보 이미지
    snorlax_closed = pygame.image.load(path + "snorlax_closed.png")
    snorlax_open = pygame.image.load(path + "snorlax_open.png")
    snorlax_closed = pygame.transform.scale(snorlax_closed, (player_width, player_height))
    snorlax_open = pygame.transform.scale(snorlax_open, (player_width, player_height))
    snorlax_image = snorlax_closed

    # 과일 이미지
    fruit_images = [
        pygame.image.load(path + "banana.png"),
        pygame.image.load(path + "grape.png"),
        pygame.image.load(path + "tomato.png"),
        pygame.image.load(path + "lime.png"),
        pygame.image.load(path + "peach.png"),
    ]
    fruit_images = [pygame.transform.scale(img, (40, 40)) for img in fruit_images]

    # 폭탄 이미지 (두리안)
    bomb_image = pygame.image.load(path + "bomb.png")
    bomb_image = pygame.transform.scale(bomb_image, (40, 40))

    # 게임 변수
    fruits = []
    bombs = []
    score = 0
    time_limit = 30  # 30초 제한 시간
    start_time = pygame.time.get_ticks()  # 게임 시작 시간
    game_over = False
    sound_played = False  # 게임 종료 효과음 재생 여부 확인 변수

    # 타이머 변수
    fruit_spawn_timer = 0  # 과일 생성 타이머 초기화
    bomb_spawn_timer = 0   # 폭탄 생성 타이머 초기화

    # 먹는 상태 타이머
    eat_timer = 0

    def reset_game():
        """게임 상태 초기화"""
        global player_x, fruits, bombs, score, game_over, snorlax_image, start_time, sound_played
        player_x = WIDTH // 2 - player_width // 2
        fruits = []
        bombs = []
        score = 0
        game_over = False
        sound_played = False
        snorlax_image = snorlax_closed
        start_time = pygame.time.get_ticks()
        pygame.mixer.music.unpause()  # 배경음악 재개

    def draw_game_over():
        """게임 종료 화면 표시"""
        pygame.mixer.music.pause()
        global sound_played  # Declare global

        # 게임 종료 효과음 한 번만 재생
        # if not sound_played:
        #     game_over_sound.play()
        #     sound_played = True

        result_text = font.render(f"Your Score: {score}", True, BLACK)
        # restart_text = small_font.render("Click to Restart", True, BLUE)

        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))
        # screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

        # 버튼 표시
        # restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        # pygame.draw.rect(screen, BLUE, restart_button)
        # button_text = small_font.render("Restart", True, WHITE)
        # screen.blit(button_text, (restart_button.x + 50, restart_button.y + 10))
        # return restart_button

    def draw_time_bar(elapsed_time):
        """시간 막대기 그리기"""
        remaining_time = max(0, time_limit - elapsed_time)
        bar_width = int((remaining_time / time_limit) * WIDTH)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 20, bar_width, 20))

    # 게임 루프
    running = True
    while running:
        current_time = (pygame.time.get_ticks() - start_time) // 1000  # 경과 시간

        if game_over:
            restart_button = draw_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        reset_game()
            continue

        screen.blit(background_image, (0, 0))  # 배경 표시

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 제한 시간 초과 처리
        if current_time >= time_limit:
            game_over = True
            continue

        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # 과일 생성 (0.5초마다)
        fruit_spawn_timer += 1
        if fruit_spawn_timer > 30:
            fruit_x = random.randint(0, WIDTH - 40)
            fruit_type = random.choice(fruit_images)
            fruits.append({"x": fruit_x, "y": 0, "image": fruit_type})
            fruit_spawn_timer = 0

        # 폭탄 생성 (2초마다)
        bomb_spawn_timer += 1
        if bomb_spawn_timer > 120:
            bomb_x = random.randint(0, WIDTH - 40)
            bombs.append({"x": bomb_x, "y": 0})
            bomb_spawn_timer = 0

        # 과일 이동
        for fruit in fruits[:]:
            fruit["y"] += 5
            if fruit["y"] > HEIGHT:
                fruits.remove(fruit)

        # 폭탄 이동
        for bomb in bombs[:]:
            bomb["y"] += 5
            if bomb["y"] > HEIGHT:
                bombs.remove(bomb)

        # 충돌 감지 (과일)
        for fruit in fruits[:]:
            if (
                player_x < fruit["x"] < player_x + player_width
                or player_x < fruit["x"] + 40 < player_x + player_width
            ) and player_y < fruit["y"] + 40:
                score += 1
                snorlax_image = snorlax_open  # 입 벌리는 애니메이션
                eat_timer = 10
                fruits.remove(fruit)
                eat_sound.play()

        # 충돌 감지 (폭탄)
        for bomb in bombs[:]:
            if (
                player_x < bomb["x"] < player_x + player_width
                or player_x < bomb["x"] + 40 < player_x + player_width
            ) and player_y < bomb["y"] + 40:
                bomb_sound.play()
                pygame.mixer.music.pause()  # 배경음악 중지
                game_over = True

        # 먹는 상태 타이머
        if eat_timer > 0:
            eat_timer -= 1
        else:
            snorlax_image = snorlax_closed

        # 화면 그리기
        screen.blit(snorlax_image, (player_x, player_y))

        # 과일 그리기
        for fruit in fruits:
            screen.blit(fruit["image"], (fruit["x"], fruit["y"]))

        # 폭탄 그리기
        for bomb in bombs:
            screen.blit(bomb_image, (bomb["x"], bomb["y"]))

        # 점수 표시
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 시간 막대 표시
        draw_time_bar(current_time)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

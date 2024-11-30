def pokemonsurvival():
    import pygame
    import random
    import sys

    # 초기화
    pygame.init()
    pygame.mixer.init()

    # 화면 크기 설정
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("POKEMON SURVIVAL")  # 제목 변경

    # 색상 정의
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # 플레이어 설정
    player_size = 40
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_speed = 5
    player_direction = [0, 1]  # 초기 방향 (아래쪽)
    player_health = 10
    last_dx, last_dy = 0, 1 #기본 방향 (아래쪽)

    # 적 설정
    enemy_size = 30
    enemies = []
    enemy_base_health = 3
    enemy_spawn_timer = 0  # 적 생성 타이머

    # 총알 설정
    bullet_size = 25
    bullets = []
    bullet_speed = 7
    bullet_damage = 1

    # 총알 발사 타이머 설정
    bullet_cooldown = 0.1  # 총알 발사 간격 (초)
    bullet_timer = 0

    # 게임 설정
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 36)

    # 점수 및 난이도
    score = 0

    #타이머
    timer = 30

    game_over = False

    # 게임 초기화 함수
    def reset_game():
        global player_pos, player_health, enemies, bullets, score, timer, enemy_base_health, game_over

        # 플레이어 상태 초기화
        player_pos = [WIDTH // 2, HEIGHT // 2]
        player_health = 10

        # 적 및 총알 초기화
        enemies = []
        bullets = []

        # 점수 및 게임 상태 초기화
        score = 0
        timer = 10
        enemy_base_health = 3
        game_over = False

        # 배경 음악 재생
        pygame.mixer.music.play(-1)

    path = "Pykemon\ggoBugi/"
    # 이미지 로드 (플레이어, 총알, 적)
    player_up = pygame.image.load(path+'pokesurv_image/player_up.png')
    player_down = pygame.image.load(path+'pokesurv_image/player_down.png')
    player_left = pygame.image.load(path+'pokesurv_image/player_left.png')
    player_right = pygame.image.load(path+'pokesurv_image/player_right.png')
    player_upleft = pygame.image.load(path+'pokesurv_image/player_upleft.png')
    player_upright = pygame.image.load(path+'pokesurv_image/player_upright.png')
    player_downleft = pygame.image.load(path+'pokesurv_image/player_downleft.png')
    player_downright = pygame.image.load(path+'pokesurv_image/player_downright.png')

    bullet_image = pygame.image.load(path+'pokesurv_image/bullet.png')
    enemy_image = pygame.image.load(path+'pokesurv_image/enemy.png')
    background_image = pygame.image.load(path+'pokesurv_image/background.png')

    # 기본 플레이어 이미지 설정 (초기 설정)
    player_image = player_down

    #사운드
    hit_sound = pygame.mixer.Sound(path+"pokesurv_sound/hitsound.MP3")
    clear_sound = pygame.mixer.Sound(path+"pokesurv_sound/clearsound.MP3")
    gameover_sound = pygame.mixer.Sound(path+"pokesurv_sound/gameoversound.MP3")
    clear_sound.set_volume(0.2)
    gameover_sound.set_volume(0.5)

    pygame.mixer.music.load(path+"pokesurv_sound/bgm.MP3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    # 게임 루프
    while running:
        # 배경
        screen.blit(background_image, (0, 0)) 

        # 시간 업데이트
        dt = clock.tick(30) / 1000  # 초 단위 delta time
        enemy_spawn_timer += dt

        # 플레이어 이동 및 방향 변경
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if timer > 0 and player_health > 0:
            if keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_RIGHT]:
                dx += 1
        else:
            if keys[pygame.K_ESCAPE]:
                running = False

        #마지막 방향 저장
        if dx != 0 or dy != 0:
            last_dx, last_dy = dx, dy

        # 대각선 방향 확인 및 이미지 변경
        if dx == -1 and dy == -1:  # 좌상
            player_image = player_upleft
        elif dx == 1 and dy == -1:  # 우상
            player_image = player_upright
        elif dx == -1 and dy == 1:  # 좌하
            player_image = player_downleft
        elif dx == 1 and dy == 1:  # 우하
            player_image = player_downright
        elif dx == 0 and dy == -1:  # 위
            player_image = player_up
        elif dx == 0 and dy == 1:  # 아래
            player_image = player_down
        elif dx == -1 and dy == 0:  # 왼쪽
            player_image = player_left
        elif dx == 1 and dy == 0:  # 오른쪽
            player_image = player_right

        # 이동 처리 (대각선 속도 조정)
        if dx != 0 and dy != 0:
            speed = player_speed / (2 ** 0.5)  # 대각선 속도 조정
        else:
            speed = player_speed

        player_pos[0] += dx * speed
        player_pos[1] += dy * speed

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if timer != 0 and player_health != 0: 
                    if event.key == pygame.K_SPACE:  # 스페이스바로 총알 발사
                        keys = pygame.key.get_pressed()
                        bullet_dx, bullet_dy = last_dx, last_dy

                        # 현재 입력된 방향키 확인
                        if keys[pygame.K_UP]:
                            bullet_dy = -1
                            bullet_dx = 0
                        if keys[pygame.K_DOWN]:
                            bullet_dy = 1
                            bullet_dx = 0
                        if keys[pygame.K_LEFT]:
                            bullet_dx = -1
                            bullet_dy = 0
                        if keys[pygame.K_RIGHT]:
                            bullet_dx = 1
                            bullet_dy = 0

                        # 대각선 방향 처리
                        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                            bullet_dx, bullet_dy = -1, -1
                        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                            bullet_dx, bullet_dy = 1, -1
                        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                            bullet_dx, bullet_dy = -1, 1
                        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                            bullet_dx, bullet_dy = 1, 1

                        # 방향 정상화
                        normalization_factor = (bullet_dx**2 + bullet_dy**2) ** 0.5
                        if normalization_factor > 0:
                            bullet_dx /= normalization_factor
                            bullet_dy /= normalization_factor

                        # 총알 생성
                        bullets.append([
                            player_pos[0] + player_size // 2,
                            player_pos[1] + player_size // 2,
                            bullet_dx,
                            bullet_dy,
                        ])
                        bullet_timer = 0  # 총알 타이머 초기화

        if timer > 0 and player_health > 0:
            timer -= dt
        elif timer > 0 and player_health == 0:
            timer = timer
        elif timer <= 0 and player_health > 0:
            timer = 0


            # 적 생성 (1초마다)
        if timer != 0:
            if player_health != 0:
                if enemy_spawn_timer >= 1.4:
                    enemy_spawn_timer = 0
                    enemies.append({
                        "pos": [random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size)],
                        "health": enemy_base_health,
                        "speed": random.uniform(1.0, 2.0),
                    })

                # 적 이동 (플레이어 추적)
                for enemy in enemies:
                    enemy_dx = player_pos[0] - enemy["pos"][0]
                    enemy_dy = player_pos[1] - enemy["pos"][1]
                    distance = (enemy_dx ** 2 + enemy_dy ** 2) ** 0.5

                    if distance > 0:    
                        enemy["pos"][0] += (enemy_dx / distance) * enemy["speed"]
                        enemy["pos"][1] += (enemy_dy / distance) * enemy["speed"]

                # 총알 이동
                for bullet in bullets:
                    bullet[0] += bullet[2] * bullet_speed
                    bullet[1] += bullet[3] * bullet_speed
                bullets = [bullet for bullet in bullets if 0 < bullet[0] < WIDTH and 0 < bullet[1] < HEIGHT]

                # 충돌 체크: 총알과 적
                for bullet in bullets[:]:
                    for enemy in enemies[:]:
                        if (
                            enemy["pos"][0] < bullet[0] < enemy["pos"][0] + enemy_size
                            and enemy["pos"][1] < bullet[1] < enemy["pos"][1] + enemy_size
                        ):
                            bullets.remove(bullet)
                            enemy["health"] -= bullet_damage
                            if enemy["health"] <= 0:
                                enemies.remove(enemy)
                                score += 1

                                # 난이도 증가
                                if score % 15 == 0:
                                    enemy_base_health += 1
                            break

                # 충돌 체크: 플레이어와 적
                for enemy in enemies[:]:
                    if (
                        player_pos[0] < enemy["pos"][0] + enemy_size
                        and player_pos[0] + player_size > enemy["pos"][0]
                        and player_pos[1] < enemy["pos"][1] + enemy_size
                        and player_pos[1] + player_size > enemy["pos"][1]
                    ):
                        player_health -= 1
                        enemies.remove(enemy)
                        hit_sound.play()

        # 플레이어 그리기
        screen.blit(player_image, (player_pos[0], player_pos[1]))  # 방향에 맞는 이미지 표시

        # 적 그리기
        for enemy in enemies:
            screen.blit(enemy_image, (*enemy["pos"], enemy_size, enemy_size))  # 적 이미지 표시
                # 체력 막대 표시
            health_bar_width = enemy_size
            health_bar_height = 5
            health_ratio = enemy["health"] / enemy_base_health  # 현재 체력 비율
            health_bar_color = GREEN if health_ratio > 0.5 else RED  # 체력 비율에 따라 색상 변경
        
            # 체력 막대 배경 (회색)
            pygame.draw.rect(screen, WHITE, (enemy["pos"][0], enemy["pos"][1] - health_bar_height - 2, health_bar_width, health_bar_height))
            # 체력 막대
            pygame.draw.rect(screen, health_bar_color, (enemy["pos"][0], enemy["pos"][1] - health_bar_height - 2, health_bar_width * health_ratio, health_bar_height))

        # 총알 그리기
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))  # 총알 이미지 표시

        # 점수 및 체력 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        timer_text = font.render(f"Timer: {int(timer)}", True, WHITE)
        screen.blit(timer_text, (650, 10))

        # 플레이어 체력 바 그리기
        player_health_ratio = player_health / 10  # 최대 체력을 10으로 설정
        player_health_bar_width = 200  # 플레이어 체력 바의 너비
        player_health_bar_height = 20  # 플레이어 체력 바의 높이

        # 체력 비율에 따라 색상 결정
        player_health_bar_color = GREEN if player_health_ratio > 0.3 else RED

        # 체력 바 배경 (회색)
        pygame.draw.rect(screen, WHITE, (10, 40, player_health_bar_width, player_health_bar_height))
        # 체력 바
        pygame.draw.rect(screen, player_health_bar_color, (10, 40, player_health_bar_width * player_health_ratio, player_health_bar_height))

        quit_text = font.render(f"Press esc to Quit", True, BLACK)
        quit_text_rect = quit_text.get_rect()
        quit_text_width = quit_text_rect.width
        endfont = pygame.font.Font(None, 100)
        can_play_sound = True

        if timer == 0:
            pygame.mixer.music.stop()
            clear_text = endfont.render(f"Game Clear!", True , GREEN)
            text_rect = clear_text.get_rect()
            text_width = text_rect.width
            text_height = text_rect.height
            screen.blit(clear_text, (400 - (text_width // 2), 300 - (text_height // 2)))
            screen.blit(quit_text, (400 - (quit_text_width // 2), 500))
            if not game_over:
                clear_sound.play()
                game_over = True


        if player_health == 0:
            pygame.mixer.music.stop()
            gameover_text = endfont.render(f"GAME OVER", True, RED)
            text_rect = gameover_text.get_rect()
            text_width = text_rect.width
            text_height = text_rect.height
            screen.blit(gameover_text, (400 - (text_width // 2), 300 - (text_height // 2)))
            screen.blit(quit_text, (400 - (quit_text_width // 2), 500))
            if not game_over:
                gameover_sound.play()
                game_over = True


        # 화면 업데이트
        pygame.display.flip()
    sys.exit()

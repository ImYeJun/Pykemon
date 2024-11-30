def pikacjuValleyball():
    import pygame
    import random
    import sys
    
    pygame.init()
    pygame.mixer.init()

    # 화면 크기
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))

    # 화면 타이틀
    pygame.display.set_caption("피카츄 배구게임")
    clock = pygame.time.Clock()
    FPS = 60

    path = "Pykemon\pikachuValleyball/"
    # 이미지 붙이기
    pikachu_image_a = pygame.image.load(path+"pikachu_a.png")
    pikachu_image_b = pygame.image.load(path+"pikachu_b.png")
    ball_image = pygame.image.load(path+"ball.png")
    background = pygame.image.load(path+"background.png")
    net_image = pygame.image.load(path+"net.png")

    # 공, 피카츄 속성
    ball_radius = 25
    ball_x, ball_y = screen_width // 2 , screen_height //4
    ball_speed_x, ball_speed_y = 5, 5

    player_width = 200
    player_height = 200
    player1_x, player1_y = 200, 400
    player2_x, player2_y = screen_width - 200, 400
    player_speed = 3

    # 네트 속성
    net_x = screen_width // 2
    net_width = 20
    net_height = screen_height // 2
    net_y = screen_height - net_height + 50

    #이미지 크기 조정
    ball_image = pygame.transform.scale(ball_image, (50, 50))
    background = pygame.transform.scale(background, (screen_width, screen_height))
    pikachu_image_a = pygame.transform.scale(pikachu_image_a, (player_width, player_height))
    pikachu_image_b = pygame.transform.scale(pikachu_image_b, (player_width, player_height))
    net_image = pygame.transform.scale(net_image, (net_width, net_height))

    # Rect 설정 (x,y,폭,높이) 순서
    player1_rect = pygame.Rect(player1_x, player1_y, player_width, player_height)
    player2_rect = pygame.Rect(player2_x, player2_y, player_width, player_height)
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius, ball_radius)
    net_rect = pygame.Rect(net_x - net_width // 2 - 5, net_y, net_width, net_height)

    # 중력 엔진
    player1_y_vel = 0
    player2_y_vel = 0
    jump_speed = 15  # 점프 초기 속도
    gravity = 0.5      # 중력 값
    is_jumping1 = False
    is_jumping2 = False
    ground_height = 600

    # 점수
    player1_score, player2_score = 0,0
    font = pygame.font.SysFont(path+"NanumGothic.ttf", 50)

    # 게임 타이머
    game_time = 30
    start_ticks = pygame.time.get_ticks()

    # 게임 종료 플래그 초기화
    time_up = False

    # 소리
    pygame.mixer.music.load(path+"game_sound.mp3") #게임 브금
    pygame.mixer.music.play(-1, 0.0)
    jump_sound = pygame.mixer.Sound(path+"jump_sound.mp3") #점프 효과음

    # 승자 결정 함수
    def show_winner(winner_text):
        # 화면 초기화 (배경 다시 그리기)
        screen.blit(background, (0, 0))  # 배경 이미지 다시 그리기
        
        # 승자 텍스트 렌더링
        winner_font = pygame.font.SysFont(path+"NanumGothic", 80)  # 승자 텍스트 폰트
        winner_message = winner_font.render(winner_text, True, (0, 0, 255))  # 파란색 텍스트
        screen.blit(winner_message, (screen_width // 2 - winner_message.get_width() // 2, screen_height // 2 - 50))
        
        # 화면 업데이트
        pygame.display.flip()
        
        # 3초 대기
        pygame.time.delay(3000)

    # 메인 이벤트
    running = True
    while running:
        
        # 게임 종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1_rect.left > 0:
            player1_rect.x -= player_speed
        if keys[pygame.K_d] and player1_rect.right < screen_width //2 :
            player1_rect.x += player_speed
        if keys[pygame.K_LEFT] and player2_rect.left > screen_width //2 :
            player2_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player2_rect.right < screen_width :
            player2_rect.x += player_speed

        # 플레이어 1 점프
        if keys[pygame.K_w] and not is_jumping1:  # W 키로 점프 시작
            is_jumping1 = True
            player1_y_vel = -jump_speed
            jump_sound.play()

        # 플레이어 2 점프
        if keys[pygame.K_UP] and not is_jumping2:  # ↑ 키로 점프 시작
            is_jumping2 = True
            player2_y_vel = -jump_speed
            jump_sound.play()

        # 중력 및 점프 처리 (플레이어 1)
        if is_jumping1:
            player1_rect.y += player1_y_vel  # 속도에 따라 Y축 이동
            player1_y_vel += gravity  # 중력 적용
            if player1_rect.bottom >= ground_height:  # 바닥에 도달
                player1_rect.bottom = ground_height
                is_jumping1 = False
                player1_y_vel = 0

        # 중력 및 점프 처리 (플레이어 2)
        if is_jumping2:
            player2_rect.y += player2_y_vel  # 속도에 따라 Y축 이동
            player2_y_vel += gravity  # 중력 적용
            if player2_rect.bottom >= ground_height:  # 바닥에 도달
                player2_rect.bottom = ground_height
                is_jumping2 = False
                player2_y_vel = 0

        # 공 이동
        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y

        # 벽 충돌
        if ball_rect.left <= 0 or ball_rect.right >= screen_width:
            ball_speed_x = -ball_speed_x
        if ball_rect.top <= 0:
            ball_speed_y = -ball_speed_y

        # 네트 충돌
        if ball_rect.colliderect(net_rect):
            if ball_rect.bottom >= net_rect.top and ball_rect.top <= net_rect.bottom:
                ball_speed_x = -ball_speed_x  # x축 반전
            # 공이 네트에 정확히 닿은 경우, 공이 겹치지 않도록 위치 조정
                if ball_rect.centerx < net_rect.centerx:
                    ball_rect.right = net_rect.left  # 왼쪽 네트의 오른쪽에 위치
                else:
                    ball_rect.left = net_rect.right

        # 바닥 충돌
        if ball_rect.bottom >= screen_height:
            if ball_rect.centerx < screen_width // 2:  # 왼쪽(플레이어 2의 득점)
                player2_score += 1
            else:  # 오른쪽(플레이어 1의 득점)
                player1_score += 1
            ball_rect.x = screen_width // 2 - ball_radius
            ball_rect.y = screen_height // 4 - ball_radius
            ball_speed_x = random.choice([5 , -5]) # 5, -5 중 랜덤으로 선택
            ball_speed_y = 4 #y축은 4 유지


        # 플레이어 충돌
        if ball_rect.colliderect(player1_rect):  # 공이 캐릭터와 충돌
            ball_speed_x = 7  # 공의 x축 속도 설정
        # 공의 위치에 따른 반응
            if ball_rect.centery <= player1_rect.bottom - 100:  # 발 위쪽에 충돌
                ball_speed_y = -7  # 위로 튕김
            else:  # 발에 충돌
                ball_speed_y = 5  # 아래로 떨어짐

        if ball_rect.colliderect(player2_rect):  # 공이 캐릭터와 충돌
            ball_speed_x = -7  # 공의 x축 속도 설정
        # 공의 위치에 따른 반응
            if ball_rect.centery <= player2_rect.bottom - 100:  # 발 위쪽에 충돌
                ball_speed_y = -7  # 위로 튕김
            else:  # 발에 충돌
                ball_speed_y = 5  # 아래로 떨어짐

        if ball_rect.colliderect(player1_rect):
            if is_jumping1 == True :
                ball_speed_x = 20  # 공의 x속도 증가
                ball_speed_y = 5

        if ball_rect.colliderect(player2_rect):
            if is_jumping2 == True :
                ball_speed_x = -20  # 공의 x속도 증가
                ball_speed_y = 5

        # 이미지 적용
        screen.blit(background, (0,0))
        screen.blit(pikachu_image_a, player1_rect)
        screen.blit(pikachu_image_b, player2_rect)
        screen.blit(ball_image, ball_rect)
        screen.blit(net_image, net_rect)

        # 타이머 계산
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, game_time - seconds)
        if time_left == 0:
            running = False
            time_up = True

        # 점수 및 타이머 텍스트 렌더링
        timer_text = font.render(f"Time Left: {time_left}s", True, (255, 0, 0))
        score1_text = font.render(f"Player 1: {player1_score}", True,(0, 0, 0))
        score2_text = font.render(f"Player 2: {player2_score}", True,(0, 0, 0))
        
        # 텍스트 화면에 출력
        screen.blit(timer_text, (screen_width // 2 -100 , 10))  # 화면 중앙 위쪽에 타이머
        screen.blit(score1_text, (150, 40))   # 화면 상단에 점수
        screen.blit(score2_text, (700, 40))

        # 화면 업데이트
        pygame.display.update()
        clock.tick(FPS)


    # 게임 종료 후 승자 표시
    if time_up:  # 시간이 끝난 경우에만 승자 표시
        if player1_score > player2_score:
            show_winner("Player 1 Wins!")
        elif player2_score > player1_score:
            show_winner("Player 2 Wins!")
        else:
            show_winner("Draw!")


    pygame.quit()
    sys.exit()


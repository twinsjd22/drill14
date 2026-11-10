import random

from pico2d import load_image, get_canvas_width

import game_framework

# bird_animation.png : 918 x 506, 5열 x 3행 격자, 총 14 프레임 (마지막 행은 4개)
SHEET_W, SHEET_H = 918, 506
FRAME_COLS = 5
FRAME_W, FRAME_H = 183, 168          # 918 / 5, 506 / 3
FRAME_COUNT = 14

# Bird Action Speed (날갯짓)
TIME_PER_ACTION = 0.5                       # 날갯짓 1회에 걸리는 시간(초)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION     # 초당 날갯짓 횟수 = 2회
FRAMES_PER_ACTION = FRAME_COUNT             # 날갯짓 1회 = 시트의 14 프레임

# Bird Fly Speed
PIXEL_PER_METER = (10.0 / 0.3)              # 10 pixel = 30 cm
FLY_SPEED_KMPH = 20.0                       # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)   # 약 185 pixel/s

# Bird Size (날개 편 길이 1.5 m 의 큰 새)
BIRD_WIDTH_M = 1.5
BIRD_W = int(BIRD_WIDTH_M * PIXEL_PER_METER)        # 50 pixel
BIRD_H = int(BIRD_W * FRAME_H / FRAME_W)            # 원본 비율 유지 -> 45 pixel


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        # 새떼가 한 몸처럼 움직이지 않도록 개체마다 값을 다르게 줌
        self.x = random.randint(BIRD_W, get_canvas_width() - BIRD_W)
        self.y = random.randint(300, 550)                  # 하늘 영역
        self.dir = random.choice([-1, 1])
        self.frame = random.uniform(0, FRAME_COUNT)         # 날갯짓 위상
        self.speed = FLY_SPEED_PPS * random.uniform(0.85, 1.15)
        # 빠른 새는 날갯짓도 빠르게: 속도 비율만큼 초당 프레임 수를 맞춤
        self.frames_per_second = (FRAMES_PER_ACTION * ACTION_PER_TIME
                                  * self.speed / FLY_SPEED_PPS)

    def update(self):
        self.x += self.dir * self.speed * game_framework.frame_time

        # 화면 끝에 닿으면 방향 반전 (몸 절반만큼 안쪽에서 반전해 화면 밖으로 안 나감)
        left_limit = BIRD_W // 2
        right_limit = get_canvas_width() - BIRD_W // 2
        if self.x > right_limit:
            self.x = right_limit
            self.dir = -1
        elif self.x < left_limit:
            self.x = left_limit
            self.dir = 1
        # 기준 초당 FRAMES_PER_ACTION * ACTION_PER_TIME (=28) 프레임, frame_time 으로 FPS 독립
        self.frame = (self.frame + self.frames_per_second
                      * game_framework.frame_time) % FRAME_COUNT

    def draw(self):
        f = int(self.frame)
        col, row = f % FRAME_COLS, f // FRAME_COLS
        # pico2d 는 좌하단 원점 -> 시트 위쪽 행일수록 bottom 이 커진다
        left = col * FRAME_W
        bottom = SHEET_H - (row + 1) * FRAME_H
        if self.dir == 1:   # 원본 그림은 오른쪽을 바라봄
            Bird.image.clip_draw(left, bottom, FRAME_W, FRAME_H,
                                 self.x, self.y, BIRD_W, BIRD_H)
        else:               # 왼쪽으로 날 때는 좌우 반전
            Bird.image.clip_composite_draw(left, bottom, FRAME_W, FRAME_H,
                                           0, 'h', self.x, self.y, BIRD_W, BIRD_H)

from pico2d import load_image

# bird_animation.png : 918 x 506, 5열 x 3행 격자, 총 14 프레임 (마지막 행은 4개)
SHEET_W, SHEET_H = 918, 506
FRAME_COLS = 5
FRAME_W, FRAME_H = 183, 168          # 918 / 5, 506 / 3
FRAME_COUNT = 14


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % FRAME_COUNT

    def draw(self):
        f = int(self.frame)
        col, row = f % FRAME_COLS, f // FRAME_COLS
        # pico2d 는 좌하단 원점 -> 시트 위쪽 행일수록 bottom 이 커진다
        left = col * FRAME_W
        bottom = SHEET_H - (row + 1) * FRAME_H
        Bird.image.clip_draw(left, bottom, FRAME_W, FRAME_H, self.x, self.y)

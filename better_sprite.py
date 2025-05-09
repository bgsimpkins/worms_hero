import pygame as pg


class BetterSprite(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)  # call super constructor

        # image and rect are Required by Group to wrap rendering
        # self.image = pg.transform.scale_by(self.image, (.5, .5))

        self.image: pg.Surface = image
        self.orig = self.image
        self.rect: pg.Rect = self.image.get_rect()
        self.angle = 0

    def rotate(self, degrees):
        self.angle += degrees
        self.image = pg.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_rotate(self, degrees):
        self.angle = degrees
        self.image = pg.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def flip_x(self):
        self.image = pg.transform.flip(self.image, 1, 0)

    def flip_y(self):
        self.image = pg.transform.flip(self.image, 0, 1)

    # def update(self):
    #     self.angle += 2
    #     self.image = pg.transform.rotate(self.orig, self.angle)
    #     self.rect = self.image.get_rect(center=self.rect.center)
    #     # self.image = pg.transform.flip(self.image)
    #     self.rect = self.rect.move(1, 1)

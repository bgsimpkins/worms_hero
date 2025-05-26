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

    def set_position(self,x, y, center=True):
        if center:
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.rect.x = x
            self.rect.y = y

    def get_position(self, center=True):
        if center:
            return{"x":self.rect.centerx, "y":self.rect.centery}
        else:
            return{"x":self.rect.x, "y":self.rect.y}

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def flip_x(self):
        self.image = pg.transform.flip(self.image, 1, 0)

    def flip_y(self):
        self.image = pg.transform.flip(self.image, 0, 1)

    def x(self, center=True):
        return self.rect.centerx if center else self.rect.x

    def y(self, center=True):
        return self.rect.centery if center else self.rect.y

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    # def update(self):
    #     self.angle += 2
    #     self.image = pg.transform.rotate(self.orig, self.angle)
    #     self.rect = self.image.get_rect(center=self.rect.center)
    #     # self.image = pg.transform.flip(self.image)
    #     self.rect = self.rect.move(1, 1)

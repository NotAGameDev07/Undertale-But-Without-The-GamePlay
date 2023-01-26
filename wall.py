from enemy import Enemy


class Wall(Enemy):
    scale_height = False
    scale_full = True
    def __init__(self, screen, px, py, imagepath, waittime=1, velocity=0, delay=0, angle=0, spx=None, spy=None):
        if self.scale_height == True and self.scale_full == False:
            super().__init__(screen, px, py, imagepath, waittime, velocity, delay, angle, spx, screen.get_size()[1])
        elif self.scale_full == True and self.scale_height == False:
            super().__init__(screen, px, py, imagepath, waittime, velocity, delay, angle, screen.get_size()[1] / spy * spx, screen.get_size()[1])
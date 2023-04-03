from random import random, randint
import pygame, simple_draw as D
import entities.snowflake as S


class EventMouseMove:
    __moves_count = 0

    @staticmethod
    def check_moves_reached_number(number) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                EventMouseMove.__moves_count += 1
                break
        
        if EventMouseMove.__moves_count >= number:
            return True
        
        return False


class Engine:
    def __init__(self, cfg) -> None:
        self.__cfg = cfg

        self.__resolution_width = 0
        self.__resolution_height = 0

        self.__choose_resolution()

        self.__snowflakes_number = self.__cfg['ent_snowflakesNumber']
        self.__snowflakes = [
            self.make_snowflake() for _ in range(self.__snowflakes_number)
        ]

        D.resolution = (self.__resolution_width, self.__resolution_height)
        D.background_color = D.COLOR_BLACK

        pygame.init()
        pygame.mouse.set_visible(False)
    
    def __choose_resolution(self) -> None:
        if self.__cfg['r_fullscreenMode']:
            self.__resolution_width = self.__cfg['r_fullscreenResolutionWidth']
            self.__resolution_height = self.__cfg['r_fullscreenResolutionHeight']
        else:
            self.__resolution_width = self.__cfg['r_windowResolutionWidth']
            self.__resolution_height = self.__cfg['r_windowResolutionHeight']

    def run(self) -> None:
        while True:
            for i in range(self.__snowflakes_number):
                self.__snowflakes[i].draw_trail()
                self.__snowflakes[i].move()
                self.__snowflakes[i].draw()
                if self.__snowflakes[i].y < -170:
                    self.__snowflakes[i] = self.make_snowflake()

            if EventMouseMove.check_moves_reached_number(4):
                pygame.quit()
                break
            
            D.sleep(0.005)
    
    def make_snowflake(self) -> S.Snowflake:
        x = randint(-120, self.__resolution_width*0.75)
        y = randint(self.__resolution_height + 170, self.__resolution_height + 720)
        speed_x = self.__cfg['ent_snowflakeSpeedX']
        speed_y = self.__cfg['ent_snowflakeSpeedYMin'] + self.__cfg['ent_snowflakeSpeedYMax']*random()
        accel_x = self.__cfg['ent_snowflakeAccelXMin'] + self.__cfg['ent_snowflakeAccelXMax']*random()
        size = randint(self.__cfg['ent_snowflakeSizeMin'], self.__cfg['ent_snowflakeSizeMax'])
        sub_color = randint(230, 250)
        color = (sub_color, sub_color, sub_color)
        trail_color = D.COLOR_BLACK
        factor_a = random()
        factor_b = random()
        factor_c = 1 + 179*random()

        return S.Snowflake(x=x, y=y, speed_x=speed_x,
                           speed_y=speed_y, accel_x=accel_x, size=size,
                           color=color, trail_color=trail_color, factor_a=factor_a,
                           factor_b=factor_b, factor_c=factor_c)
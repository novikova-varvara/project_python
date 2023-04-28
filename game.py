import pygame
from pygame.locals import *
from global_variables import *
import time
import random
class Game(object):
    '''
    Класс игры.
    ...
    Атрибуты
    --------
    width : int
        ширина экрана
    height : int
        высота экрана
    wrong_signs : int
         неправильно введённые знаки
    sighs : int
        число введённых знаков
    time_start : int
        время начала ввода
    time_end : int
        время окончания ввода
    spm : int
        знаки в минуту
    lsentence : str
        правильно введённые символы
    ls_size : int
        размер lsentence
    rsentence : str
        символы, которые нужно ввести
    rs_size : int
        размер rsentence
    help_sentence : str
        предложение, чтобы обновлять rsentence
    results : str
        результаты
    game_exit : bool
        состояние игры
    actine : bool
        состояние сеанса игры
    Методы
    ------
    choose_sentence() :
        Функция для рандомного выбора предложения из базы предложений.
    update_sentences() :
        Функция для обновления lsentence и rsentence.
    update_input_field() :
        Функция для обновления поля ввода: заливки белым цветом, прорисовки контура, прозрачной заливки.
    write_text(txt, coord_x, coord_y, size, color) :
        Функция для написания текста.
    draw_rect_alpha(color, rect) :
        Функция для рисования прозрачного прямоугольника.
    get_results() :
        Функция для получения результатов и вывод их на экран
    reset() :
        Функция для сброса данных, а также обновления полей ввода и результатов.
    run(self):
        Основная функция, отвечающая за ход игры.
    '''
    def __init__(self):
        '''
        Инициализация атрибутов класса, создания экрана и заливка его белым цветом.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        self.width = WIDTH
        self.height = HEIGHT
        self.wrong_signs = 0
        self.signs = -1
        self.time_start = 0
        self.time_end = 0
        self.spm = 0
        self.lsentence = str()
        self.ls_size = 0
        self.rsentence = str()
        self.rs_size = 0
        self.help_sentence = str()
        self.results = 'Время:0  Ошибки:0  Знаков в минуту:0'
        self.game_exit = False
        self.active = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(WHITE)
        pygame.display.set_caption("Клавиатурный тренажёр")
    def choose_sentence(self):
        '''
        Функция для рандомного выбора предложения из базы предложений.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        with open('sentences.txt', 'r', encoding='UTF8') as f:
            sentences = f.readlines()
            sentence = random.choice(sentences)
            self.help_sentence = str(sentence)
    def update_sentences(self):
        '''
        Функция для обновления lsentence и rsentence.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        if self.rs_size == 0:
            self.choose_sentence()
            self.rs_size = len(self.help_sentence) - 1
            self.rsentence = self.help_sentence[:self.rs_size]
        else:
            if self.rs_size < SZ:
                self.choose_sentence()
                self.rs_size += len(self.help_sentence)
                self.rsentence += ' ' + self.help_sentence[:len(self.help_sentence) - 1]
            self.lsentence += self.rsentence[0]
            self.ls_size += 1
            if self.ls_size > SZ:
                self.lsentence = self.lsentence[1:]
                self.ls_size = SZ
            self.rsentence = self.rsentence[1:]
            self.rs_size -= 1
    def update_input_field(self):
        '''
        Функция для обновления поля ввода: заливки белым цветом, прорисовки контура, прозрачной заливки.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        self.screen.fill(WHITE, INPUT_FIELD)
        self.draw_rect_alpha(ALPHA_GRAY, ALPHA_RECT)
        pygame.draw.rect(self.screen, BLACK, INPUT_FIELD, CONTOUR)
    def write_text(self, txt, coord_x, coord_y, size, color):
        '''
        Функция для написания текста.
        Параметры
        ---------
        txt : str
            текст
        coord_x : int
            координата x текста
        coord_y : int
            координата y текста
        size : int
            размер шрифта
        color : tuple
            цвет шрифта
        Возвращаемое значние
        --------------------
        None
        '''
        font = pygame.font.SysFont("Courier New", size)
        txt = font.render(txt, True, color)
        txtRect = txt.get_rect()
        txtRect.center = (coord_x, coord_y)
        self.screen.blit(txt, txtRect)
        pygame.display.update()
    def draw_rect_alpha(self, color, rect):
        '''
        Функция для рисования прозрачного прямоугольника; на вход получает цвет и координаты прямоугольника.
        Параметры
        ---------
        color : tuple
            цвет прямоугольника
        rect : tuple
            координаты прямоугольника
        Возвращаемое значние
        --------------------
        None
        '''
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self.screen.blit(shape_surf, rect)
        pygame.display.update()
    def get_results(self):
        '''
        Функция для получения результатов и вывод их на экран.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        self.time_end = time.time()
        if self.time_start == 0:
            total_time = 0
            self.spm = 0
        else:
            total_time = max(self.time_end - self.time_start, 0)
            self.spm = max(round((self.signs - self.wrong_signs) / total_time * 60), 0)
        self.results = 'Время:' + str(round(total_time)) + ' секунд  Ошибки:' + str(self.wrong_signs) + '  З/м:' + str(self.spm)
        self.screen.fill(WHITE, RES_FIELD)
        self.write_text(self.results, COORD_X_RES, COORD_Y_RES, FONT_SIZE_2, RED)
        pygame.display.update()
    def  reset(self):
        '''
        Функция для сброса данных, а также обновления полей ввода и результатов.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        self.get_results()

        self.height = HEIGHT
        self.wrong_signs = 0
        self.signs = -1
        self.time_start = 0
        self.time_end = 0
        self.spm = 0
        self.lsentence = str()
        self.ls_size = 0
        self.rsentence = str()
        self.rs_size = 0
        self.help_sentence = str()
        self.game_exit = False
        self.active = False

        self.update_input_field()
        self.write_text('Пробел - СТАРТ', COORD_X_IF_LH, COORD_Y_IF, FONT_SIZE_1, GRAY)
        self.write_text('Return - ВЫХОД', COORD_X_IF_RH, COORD_Y_IF, FONT_SIZE_1, BLACK)
        pygame.display.update()
    def run(self):
        '''
        Основная функция, отвечающая за ход игры.
        Параметры
        ---------
        None
        Возвращаемое значние
        --------------------
        None
        '''
        self.reset()
        while not self.game_exit:
            if self.active:
                self.get_results() # постоянное обновление статистики во время игры
            for event in pygame.event.get():
                if event.type == QUIT: # закртыие игры при нажатии на крестик
                    self.game_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.signs += 1
                        if self.signs == 0: # пробел служит запсуком игры: обновление поял ввода, предложений и вывод предложения для ввода
                            self.time_start = time.time()
                            self.active = True
                            self.update_input_field()
                            self.update_sentences()
                            self.write_text(self.rsentence[:SZ], COORD_X_RSENT, COORD_Y_SENT, FONT_SIZE_1, BLACK)
                        else: # если пробел часть предлложения
                            if self.rs_size > 0 and self.rsentence[0] != ' ': # если символ введён неправильно
                                self.wrong_signs += 1
                            elif self.rs_size > 0 and self.rsentence[0] == ' ': # если символ введён правильно
                                self.update_input_field()
                                self.update_sentences()
                                self.write_text(self.lsentence, COORD_X_LSENT - self.ls_size * DELTA, COORD_Y_SENT, FONT_SIZE_1, GRAY)
                                self.write_text(self.rsentence[:SZ], COORD_X_RSENT, COORD_Y_SENT, FONT_SIZE_1, BLACK)
                    elif event.key == pygame.K_RETURN: # если нажата кнопка завершения игры
                        self.reset()
                    else: # обработка остальных нажатых клавиш
                        self.signs += 1
                        if self.rs_size > 0 and self.rsentence[0] != event.unicode: # если символ введён неправильно
                            self.wrong_signs += 1
                        elif self.rs_size > 0 and self.rsentence[0] == event.unicode: # если символ введён правильно
                            self.update_input_field()
                            self.update_sentences()
                            self.write_text(self.lsentence, COORD_X_LSENT - self.ls_size * DELTA, COORD_Y_SENT, FONT_SIZE_1, GRAY)
                            self.write_text(self.rsentence[:SZ], COORD_X_RSENT, COORD_Y_SENT, FONT_SIZE_1, BLACK)
                pygame.display.update()
import pygame, win32gui, sys, time
from pywinauto.findwindows import find_window
from datetime import datetime
import win32com.client


class Stopwatch:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("stopwatch")

        #Internet is amazing, I must say ↓
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(find_window(title = "stopwatch"))
        
        self.start = False
        self.time = "0.00"
        self.position = (self.screen_width / 2, self.screen_height / 2)
        self.pressing_keys = False
        
        self.font = pygame.font.SysFont('Times New Roman', 200)
        self.text_color = (0, 0, 255)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.time = "0.00"
                        self.start = False
                    elif event.key == pygame.K_SPACE:
                        if self.start == True:
                            self.start = False
                        else:
                            self.start_time = self.get_time()
                            self.time_when_start = self.time
                            self.start = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.start == True:
                self.stopwatch()
            self.screen.fill((190, 190, 190))
            self.print_text()

    def run_one_time(self, inspection, competition):
        self.corresponding_keys = {pygame.K_s: "s", pygame.K_d: "d", pygame.K_f: "f",
                                   pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l"}
        self.competition = competition
        self.green= False
        if inspection:
            self.time = "16.00"
        else:
            self.time = "0.00"
        self.keys = {"s": False, "d": False, "f": False, "j": False, "k": False, "l": False}
        self.trues = 0
        self.time_between_keys = 0
        self.raised_keys = False
        self.running = True
        self.timer_repeat_time = 1500
        self.start_time = self.get_time()
        #pygame is quite stupid in that it can't handle 8 KeyDown simultaneously, so I was forced to use
        #only 6.
        while self.running and self.timer_repeat_time != 0:
            if self.competition:
                if self.trues == 0:
                    for i in self.keys.values():
                        if i:
                            self.trues += 1
                    if self.trues == 6:
                        self.pressing_keys = True
                        if self.start == False and self.time_between_keys == 0:
                            self.time_before_keys = self.get_time()
                    else:
                        self.trues = 0

                elif self.trues == 6:
                    for i in self.keys.values():
                        if not i:
                            self.trues -= 1
                    if self.trues != 6:
                        self.pressing_keys = False
                        if self.get_time() - self.time_before_keys > 1:
                            self.green = False
                            self.start_time = self.get_time()
                            self.time_when_start = self.time
                            self.start = True
                            self.raised_keys = True
                            self.text_color = (0, 0, 255)
                        self.trues = 0
                    
            try:
                if self.start == False and self.get_time() - self.time_before_keys > 1 and self.pressing_keys:
                    self.green = True
                    self.text_color = (100, 255, 50)
            except AttributeError:
                pass

            if inspection:
                self.sixteen_s_timer()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.check_keys_down(event)
                    if self.start == True and self.raised_keys == True:
                        self.running = False
                        
                elif event.type == pygame.KEYUP:
                    self.check_keys_up(event)
                    
                elif event.type == pygame.QUIT:
                    return False
            if self.start == True:
                self.stopwatch()
            self.screen.fill((190, 190, 190))
            self.print_text()
        if self.timer_repeat_time == 0:
            return 38226
        return self.time

    def stopwatch(self):
        #calibrate against the clock
        self.difference = float(self.c(self.time)) - float(self.c(self.time_when_start))  + 0.01
        while abs(self.get_time() - self.start_time) < self.difference:
            time.sleep(0.001)

        #0.09 -> 0.1; 59.99 -> 60.00
        if ":" not in self.time:
            self.time = str(round(float(self.time) + 0.01, 2))
        else:
            self.time = self.time.split(":")[0] + ":" + str(round(float(self.time.split(":")[1]) + 0.01, 2))
            
        self.formating(True)

    def sixteen_s_timer(self):        
        if (not self.green) and (not self.start) and self.timer_repeat_time != 0:
            self.difference = 16 - float(self.time) + 0.01
            while abs(self.get_time() - self.start_time) < self.difference:
                time.sleep(0.001)
            self.time = str(round(float(self.time) - 0.01, 2))
            self.formating(False)
            self.timer_repeat_time -= 1
            
        elif self.green and self.time != "0.00":
            self.time = "0.00"

    def formating(self, stopwatch):
        #0.1 -> 0.10
        if len(self.time.split(".")[1]) == 1:
            self.time += "0"

        #60.00 -> 1:0.00; 1:60.00 -> 2:0.00
        if stopwatch:
            if int(self.time.split(":")[-1].split(".")[0]) == 60:
                if ":" not in self.time:
                    self.time = "1:" + str((int(self.time.split(".")[0]) - 60)) + "." + self.time.split(".")[1]
                else:
                    self.time = self.time.split(":")[0] + ":" + str(int(self.time.split(":")[1].split(".")[0]) - 60) + "." + self.time.split(".")[1]

        #1:0.00 -> 1:00.00
        if stopwatch:
            if ":" in self.time:
                if len(self.time.split(".")[0].split(":")[1]) == 1:
                    self.time = self.time.split(".")[0].split(":")[0] + ":0" + self.time.split(".")[0].split(":")[1] + "." + self.time.split(".")[1]
    
    def print_text(self):
        self.text = self.font.render(self.time, True, self.text_color, (190, 190, 190))
        self.screen.blit(self.text, self.get_pos())
        pygame.display.flip()

    def get_pos(self):
        self.rect = self.text.get_rect()
        self.rect_position = (self.rect.w, self.rect.h)
        self.x = self.position[0] - (self.rect_position[0] / 2)
        self.y = self.position[1] - (self.rect_position[1] / 2)
        #need topleft coordinates
        self.pos = (self.x, self.y)
        return self.pos

    def get_time(self):
        return int(datetime.now().strftime("%M")) * 60 + float(datetime.now().strftime("%S.%f")[:-2])

    def c(self, string):
        if ":" in string:
            return float(string.split(":")[0]) * 60 + float(string.split(":")[1])
        else:
            return float(string)

    def check_keys_down(self, event):
        if self.competition:
            if event.unicode.lower() in self.keys.keys():
                self.keys[event.unicode.lower()] = True
            elif event.key in self.corresponding_keys.keys():
               self.keys[self.corresponding_keys[event.key]] = True
        else:
            if event.key == pygame.K_SPACE:
                self.pressing_keys = True
                if self.start == False and self.time_between_keys == 0:
                    self.time_before_keys = self.get_time()

    def check_keys_up(self, event):
        if self.competition:
            if event.unicode.lower() in self.keys.keys():
                self.keys[event.unicode.lower()] = False
            elif event.key in self.corresponding_keys.keys():
               self.keys[self.corresponding_keys[event.key]] = False
        else:
            if event.key == pygame.K_SPACE:
                self.pressing_keys = False
                if self.get_time() - self.time_before_keys > 1:
                    self.green = False
                    self.start_time = self.get_time()
                    self.time_when_start = self.time
                    self.start = True
                    self.raised_keys = True
                    self.text_color = (0, 0, 255)
        
def begin(go_on, inspection = False, competition = True):
##    global stpwtch
    stpwtch = Stopwatch()
    if go_on:
        stpwtch.run()
    else:
        status = stpwtch.run_one_time(inspection, competition)
        pygame.quit()
        if not status:
            return None
        elif status == 38226:
            return False
        else:
            return status

##stpwtch = Stopwatch()
##begin(False)


from pydoc import text
from utils import *
import pygame

error_text = ""


class ErrorScreen:
    def __init__(self):
        global error_text
        self.msg = "Unspecified error!!!"
        self.active = False
        error_text = self.msg
    def draw(self, screen: pygame.Surface):
        
        if not self.active:
            return
        global error_text
        if not error_text == self.msg:
            error_text = self.msg
            finalErrorText = ""
            for txt in error_text.split("."):
                finalErrorText += txt + ".\n"
            if error_text == finalErrorText:
                print(error_text)
            error_text = finalErrorText
        error_msg_surface = get_font(18).render(error_text, True, (255, 0, 0))  # TODO: cache the error text
        press_esc_to_exit = get_font(24).render("Press escape to go back", True, get_colors()["hallway"])
        screen.blit(error_msg_surface, error_msg_surface.get_rect(center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT / 3)))
        screen.blit(press_esc_to_exit, press_esc_to_exit.get_rect(center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT * (2 / 3))))

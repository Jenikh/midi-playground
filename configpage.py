from config import set_default_config
from utils import *
import pygame
import pygame_gui as pgui
from io import StringIO
from os import listdir
import webbrowser


class ConfigPage:
    @property
    def made_with_pgui_rect(self):
        return self.made_with_pgui_surf.get_rect(bottomleft=(30, Config.SCREEN_HEIGHT - 30))

    def __init__(self):
        self.active = False
        self.made_with_pgui_surf = get_font(12).render(
            "Config page made with pygame_gui library", True, (255, 255, 255))

        pgui_theme = "{}"
        if lang_key("do-custom-pgui-font"):
            pgui_theme = f"""
            {{
                "label":
                {{
                    "font":
                    {{
                        "name": "hanyisongjian",
                        "regular_path": "./assets/fonts/{lang_key('font')}"
                    }}
                }}
            }}
            """

        # pygame_gui stuff
        self.ui_manager = pgui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), StringIO(pgui_theme))
        self.back_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH - 120, 30, 90, 30)),
            text="Back",
            manager=self.ui_manager
        )
        self.off_on_dropdown = [lang_key('off'), lang_key('on')]
        # all attributes matching /s_.+/ are "s"ettings
        self.t_camera_mode_dropdown = lang_key('camera-mode-dropdown')
        if not type(self.t_camera_mode_dropdown) == list:
            self.t_camera_mode_dropdown = ["Warning! Dont use this setting!","This translation is invalid!"]
        try:
            self.t_camera_mode_dropdown[Config.camera_mode]
        except:
            while True:
                if len(self.t_camera_mode_dropdown) == Config.camera_mode + 2:
                    break
                self.t_camera_mode_dropdown.append("Warning! Dont use this setting!")
        self.s_camera_mode = pgui.elements.UIDropDownMenu(
            self.t_camera_mode_dropdown,
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT // 10, 300, 30)),
            starting_option=self.t_camera_mode_dropdown[Config.camera_mode],
            manager=self.ui_manager
        )
        self.s_camera_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT // 10 - 30, 240, 30)),
            text=lang_key('camera-mode') + ":",
            manager=self.ui_manager
        )
        self.t_seed_placeholder = lang_key('rng-seed-placeholder')
        self.s_seed = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 2 // 10, 300, 30)),
            placeholder_text=self.t_seed_placeholder,
            manager=self.ui_manager
        )
        self.s_seed.set_allowed_characters('numbers')
        self.s_seed.set_text(str(Config.seed if Config.seed is not None else ''))
        self.s_seed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 2 // 10 - 30, 240, 30)),
            text=lang_key('rng-seed') + ":",
            manager=self.ui_manager
        )

        self.s_start_playing_delay = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 3 // 10, 300, 30)),
            start_value=Config.start_playing_delay,
            value_range=(1000, 5000),
            manager=self.ui_manager
        )
        self.s_start_playing_delay_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 3 // 10 - 30, 240, 30)),
            text=lang_key('starting-time-delay') + f" ({self.s_start_playing_delay.get_current_value()}ms):",
            manager=self.ui_manager
        )
        self.t_max_notes_placeholder = lang_key('max-notes-to-generate-placeholder')
        self.s_max_notes = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 4 // 10, 300, 30)),
            placeholder_text=str(self.t_max_notes_placeholder),
            manager=self.ui_manager
        )
        self.s_max_notes.set_allowed_characters('numbers')
        self.s_max_notes.set_text(str(Config.max_notes if Config.max_notes is not None else ''))
        self.s_max_notes_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 4 // 10 - 30, 240, 30)),
            text=lang_key('max-notes-to-generate') + ":",
            manager=self.ui_manager
        )

        self.s_bounce_min_spacing = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 5 // 10, 300, 30)),
            start_value=Config.bounce_min_spacing,
            value_range=(5, 50),
            manager=self.ui_manager
        )
        self.s_bounce_min_spacing_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 5 // 10 - 30, 240, 30)),
            text=f"{lang_key('bounce-min-spacing')} ({Config.bounce_min_spacing}ms):",
            manager=self.ui_manager
        )

        self.s_square_speed = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 6 // 10, 300, 30)),
            start_value=Config.square_speed,
            value_range=(100, 2000),
            manager=self.ui_manager
        )
        self.s_square_speed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 6 // 10 - 30, 240, 30)),
            text=f"{lang_key('square-speed')} ({Config.square_speed} pixels/s):",
            manager=self.ui_manager
        )

        self.s_music_offset = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 7 // 10, 300, 30)),
            start_value=Config.music_offset,
            value_range=(-500, 500),
            manager=self.ui_manager
        )
        self.s_music_offset_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 7 // 10 - 30, 240, 30)),
            text=f"{lang_key('music-offset')} ({Config.music_offset}ms):",
            manager=self.ui_manager
        )

        self.s_direction_change_chance = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 8 // 10, 300, 30)),
            start_value=Config.direction_change_chance,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_direction_change_chance_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 8 // 10 - 30, 240, 30)),
            text=f"{lang_key('change-dir-chance')} ({Config.direction_change_chance}%):",
            manager=self.ui_manager
        )

        self.s_hp_drain_rate = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 9 // 10, 300, 30)),
            start_value=Config.hp_drain_rate,
            value_range=(3, 20),
            manager=self.ui_manager
        )
        self.s_hp_drain_rate_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 9 // 10 - 30, 240, 30)),
            text=f"{lang_key('hp-drain-rate')} ({Config.hp_drain_rate}/s):",
            manager=self.ui_manager
        )

        # audio and general settings

        self.s_game_volume = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT // 10, 300, 30)),
            start_value=Config.volume,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_game_volume_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT // 10 - 30, 240, 30)),
            text=f"{lang_key('music-volume')} ({Config.volume}%):",
            manager=self.ui_manager
        )

        self.s_color_theme = pgui.elements.UIDropDownMenu(
            [theme for theme in Config.color_themes],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 2 // 10, 300, 30)),
            starting_option=Config.theme,
            manager=self.ui_manager
        )
        self.s_color_theme_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 2 // 10 - 30, 240, 30)),
            text=f"{lang_key('color-theme')}:",
            manager=self.ui_manager
        )

        self.s_theatre_mode = pgui.elements.UIDropDownMenu(
            self.off_on_dropdown,
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 3 // 10, 300, 30)),
            starting_option=self.off_on_dropdown[int(Config.theatre_mode)],
            manager=self.ui_manager
        )
        self.s_theatre_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 3 // 10 - 30, 240, 30)),
            text=f"{lang_key('theatre-mode')}:",
            manager=self.ui_manager
        )

        self.s_particle_trail = pgui.elements.UIDropDownMenu(
            self.off_on_dropdown,
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 4 // 10, 300, 30)),
            starting_option=self.off_on_dropdown[int(Config.particle_trail)],
            manager=self.ui_manager
        )
        self.s_particle_trail_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 4 // 10 - 30, 240, 30)),
            text=f"{lang_key('particle-trail')}:",
            manager=self.ui_manager
        )

        self.s_shader = pgui.elements.UIDropDownMenu(
            [_ for _ in listdir("./assets/shaders/") if _.endswith(".glsl")],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 5 // 10, 300, 30)),
            starting_option=Config.shader_file_name,
            manager=self.ui_manager
        )
        self.s_shader_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect(Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 5 // 10 - 30, 240, 30),
            text=f"{lang_key('shader')} ({lang_key('restart-required')}):",
            manager=self.ui_manager
        )

        self.s_do_bounce_color_pegs = pgui.elements.UIDropDownMenu(
            self.off_on_dropdown,
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 6 // 10, 300, 30)),
            starting_option=self.off_on_dropdown[int(Config.do_color_bounce_pegs)],
            manager=self.ui_manager
        )
        self.s_do_bounce_color_pegs_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 6 // 10 - 30, 240, 30)),
            text=f"{lang_key('color-pegs-on-bounce')}:",
            manager=self.ui_manager
        )

        self.s_do_particles_on_bounce = pgui.elements.UIDropDownMenu(
            self.off_on_dropdown,
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 7 // 10, 300, 30)),
            starting_option=self.off_on_dropdown[int(Config.do_color_bounce_pegs)],
            manager=self.ui_manager
        )
        self.s_do_particles_on_bounce_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 7 // 10 - 30, 240, 30)),
            text=f"{lang_key('particles-on-bounce')}:",
            manager=self.ui_manager
        )
        self.s_resolution = pgui.elements.UIDropDownMenu(
            [str(Config.rSCREEN_WIDTH) + "x" + str(Config.rSCREEN_HEIGHT), "800x600", "1024x768", "1280x720",
             "1920x1080"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 8 // 10, 300, 30)),
            starting_option=str(Config.SCREEN_WIDTH) + "x" + str(Config.SCREEN_HEIGHT),
            manager=self.ui_manager
        )
        self.s_resolution_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 8 // 10 - 30, 240, 30)),
            text=f"{lang_key('resolution')} ({lang_key('restart-required')}):",
            manager=self.ui_manager
        )

        # reset button
        self.t_reset_button_placeholder = lang_key('reset-button-placeholder')
        self.s_reset_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH - 330, Config.SCREEN_HEIGHT - 60, 300, 30)),
            text=self.t_reset_button_placeholder,
            manager=self.ui_manager
        )
        self.can_write_to_config = True

    def handle_event(self, event: pygame.event.Event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.made_with_pgui_rect.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open("https://github.com/MyreMylar/pygame_gui")

        if event.type == pgui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                play_sound("wood.wav")
                return True
            
            if event.ui_element == self.s_reset_button:
                # TODO: rework this
                # TODO: this does not work with translation stuffs
                set_default_config()
                play_sound("wood.wav")
                self.active = False
                self.__init__()
                return True
        if not self.can_write_to_config:
            return
        if event.type == pgui.UI_DROP_DOWN_MENU_CHANGED:
            play_sound("wood.wav")
            try:
                if event.ui_element == self.s_camera_mode:
                    Config.camera_mode = "CLSP".index(event.text[0])  # awful way of doing this lol
                if event.ui_element == self.s_color_theme:
                    Config.theme = event.text
                if event.ui_element == self.s_theatre_mode:
                    Config.theatre_mode = bool(self.off_on_dropdown.index(event.text))
                if event.ui_element == self.s_particle_trail:
                    Config.particle_trail = bool(self.off_on_dropdown.index(event.text))
                if event.ui_element == self.s_shader:
                    Config.shader_file_name = event.text
                if event.ui_element == self.s_do_bounce_color_pegs:
                    Config.do_color_bounce_pegs = bool(self.off_on_dropdown.index(event.text))
                if event.ui_element == self.s_do_particles_on_bounce:
                    Config.do_particles_on_bounce = bool(self.off_on_dropdown.index(event.text))
                if event.ui_element == self.s_resolution:
                    event.text = event.text.split("x")
                    Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT = int(event.text[0]), int(event.text[1])

                if event.type == pgui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == self.s_seed:
                        text: str = event.text
                        if text.isnumeric() and len(text):
                            Config.seed = int(text)
                        else:
                            Config.seed = None
                    if event.ui_element == self.s_max_notes:
                        text: str = event.text
                        if text.isnumeric() and len(text):
                            Config.max_notes = int(text)
                        else:
                            Config.max_notes = None

                if event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.s_start_playing_delay:
                        self.s_start_playing_delay_label.set_text(f"{lang_key('starting-time-delay')} ({event.value}ms):")
                        Config.start_playing_delay = event.value
                    if event.ui_element == self.s_bounce_min_spacing:
                        self.s_bounce_min_spacing_label.set_text(f"{lang_key('bounce-min-spacing')} ({event.value}ms):")
                        Config.bounce_min_spacing = event.value
                    if event.ui_element == self.s_square_speed:
                        rounded = round(event.value, -2)
                        self.s_square_speed_label.set_text(f"{lang_key('square-speed')} ({rounded} pixels/s):")
                        Config.square_speed = rounded
                    if event.ui_element == self.s_game_volume:
                        self.s_game_volume_label.set_text(f"{lang_key('music-volume')} ({event.value}%):")
                        Config.volume = event.value
                        pygame.mixer.music.set_volume(event.value / 100)
                    if event.ui_element == self.s_music_offset:
                        self.s_music_offset_label.set_text(f"{lang_key('music-offset')} ({event.value}ms):")
                        Config.music_offset = event.value
                    if event.ui_element == self.s_direction_change_chance:
                        self.s_direction_change_chance_label.set_text(f"{lang_key('change-dir-chance')} ({event.value}%):")
                        Config.direction_change_chance = event.value
                    if event.ui_element == self.s_hp_drain_rate:
                        self.s_hp_drain_rate_label.set_text(f"{lang_key('hp-drain-rate')} ({event.value}/s):")
                        Config.hp_drain_rate = event.value
            except (AttributeError, ValueError):
                print("Translation is invalid!")
                print("Going back...")
                self.can_write_to_config = False
                play_sound("wood.wav")
                return True
        self.ui_manager.process_events(event)

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        self.ui_manager.update(1 / FRAMERATE)  # supposed to use dt but whatever
        self.ui_manager.draw_ui(screen)

        screen.blit(self.made_with_pgui_surf, self.made_with_pgui_rect)

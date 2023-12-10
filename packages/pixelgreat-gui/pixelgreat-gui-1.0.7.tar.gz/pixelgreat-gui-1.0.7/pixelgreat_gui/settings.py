import pixelgreat as pg

from . import constants


class PixelgreatSettings:
    def __init__(self):
        # Set default screen type
        self.screen_type = constants.DEFAULTS["screen_type"]

        # Fill out default settings for each screen type
        self.settings_dict = dict()
        self.set_to_defaults()

    def set_to_defaults(self):
        for screen_type in ["LCD", "CRT_TV", "CRT_MONITOR"]:
            screen_type_settings = dict()

            for setting_name in ["pixel_padding", "direction", "washout", "blur", "rounding", "scanline_strength"]:
                screen_type_settings[setting_name] = constants.DEFAULTS[setting_name][screen_type]

            for setting_name in ["brighten", "bloom_size", "pixel_aspect", "scanline_spacing", "scanline_size",
                                 "scanline_blur", "bloom_strength", "grid_strength", "pixelate", "output_scale",
                                 "pixel_size"]:
                screen_type_settings[setting_name] = constants.DEFAULTS[setting_name]

            self.settings_dict[screen_type] = screen_type_settings
        self.set_screen_type(constants.DEFAULTS["screen_type"])

    def get_screen_type(self):
        return self.screen_type

    def set_screen_type(self, screen_type):
        self.screen_type = screen_type

    def get_setting(self, setting):
        return self.settings_dict[self.screen_type.value][setting]

    def set_setting(self, setting, value):
        self.settings_dict[self.screen_type.value][setting] = value

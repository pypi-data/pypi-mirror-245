import pixelgreat as pg


DEFAULTS = {
    "screen_type": pg.ScreenType.LCD,
    "pixel_size": 20,
    "pixel_padding": {
        "LCD": 0.25,
        "CRT_TV": 0.25,
        "CRT_MONITOR": 0.1
    },
    "direction": {
        "LCD": pg.Direction.VERTICAL,
        "CRT_TV": pg.Direction.VERTICAL,
        "CRT_MONITOR": pg.Direction.HORIZONTAL
    },
    "washout": {
        "LCD": 0.1,
        "CRT_TV": 0.5,
        "CRT_MONITOR": 0.5
    },
    "brighten": 1.0,
    "blur": {
        "LCD": 0,
        "CRT_TV": 0.5,
        "CRT_MONITOR": 0.75
    },
    "bloom_size": 0.5,
    "pixel_aspect": 1.0,
    "rounding": {
        "LCD": 0,
        "CRT_TV": 0.5,
        "CRT_MONITOR": 0
    },
    "scanline_spacing": 0.79,
    "scanline_size": 0.75,
    "scanline_blur": 0.25,
    "scanline_strength": {
        "LCD": 0,
        "CRT_TV": 1,
        "CRT_MONITOR": 0.5
    },
    "bloom_strength": 1.0,
    "grid_strength": 1.0,
    "pixelate": True,
    "output_scale": 1.0
}

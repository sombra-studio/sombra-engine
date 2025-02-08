import pyglet

def create_color_tex(color: tuple[int, int, int, int]) -> pyglet.image.Texture:
    color_pattern = pyglet.image.SolidColorImagePattern(color)
    img = color_pattern.create_image(16, 16)
    return img.get_texture()

def create_black_tex() -> pyglet.image.Texture:
    return create_color_tex((0, 0, 0, 255))

def create_white_tex() -> pyglet.image.Texture:
    return create_color_tex((255, 255, 255, 255))

def create_gray_tex() -> pyglet.image.Texture:
    return create_color_tex((123, 123, 123, 255))

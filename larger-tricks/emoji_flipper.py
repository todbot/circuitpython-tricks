# emoji_flipper.py - show a bunch of emojis from a sprite sheet
# 23 Jun 2022 - @todbot / Tod Kurt
import time
import board
import displayio
import adafruit_imageload

sprite_fname = "emoji_spritesheet_27x7_28x28.bmp"
sprite_cnt = 27*7
sprite_w,sprite_h = 28,28

sprite_sheet,sprite_palette = adafruit_imageload.load(sprite_fname)
#sprite_sheet = displayio.OnDiskBitmap(open(sprite_fname, "rb"))
#sprite_palette = sprite_sheet.pixel_shader
sprite_palette.make_transparent(0)  # make background color transparent
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=sprite_palette,
                            width = 1, height = 1,
                            tile_width = sprite_w, tile_height = sprite_h)
display = board.DISPLAY  # our board has built-in display

maingroup = displayio.Group(scale=4) # make 4x big
maingroup.append(sprite)
display..root_group = maingroup

sprite_index = 0 # where in the sprite sheet we currently are
while True:
    sprite[0] = sprite_index
    sprite_index = (sprite_index + 1) % sprite_cnt
    time.sleep(0.1)

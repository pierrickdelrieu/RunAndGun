# pygame_functions

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs at https://github.com/StevePaget/Pygame_Functions/issues


import os
import pygame
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
sprite_group = pygame.sprite.OrderedUpdates()
textbox_group = pygame.sprite.OrderedUpdates()
game_clock = pygame.time.Clock()
music_paused = False
hidden_sprites = pygame.sprite.OrderedUpdates()
screen_refresh = True
background = None

key_dict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "return": pygame.K_RETURN,
            "a": pygame.K_a,
            "b": pygame.K_b,
            "c": pygame.K_c,
            "d": pygame.K_d,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "i": pygame.K_i,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "m": pygame.K_m,
            "n": pygame.K_n,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "q": pygame.K_q,
            "r": pygame.K_r,
            "s": pygame.K_s,
            "t": pygame.K_t,
            "u": pygame.K_u,
            "v": pygame.K_v,
            "w": pygame.K_w,
            "x": pygame.K_x,
            "y": pygame.K_y,
            "z": pygame.K_z,
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3,
            "4": pygame.K_4,
            "5": pygame.K_5,
            "6": pygame.K_6,
            "7": pygame.K_7,
            "8": pygame.K_8,
            "9": pygame.K_9,
            "0": pygame.K_0}

screen: pygame.SurfaceType


class Background:
    tiles: list
    stage_pos_x: int
    stage_pos_y: int
    tile_width: int
    tile_height: int
    surface: str

    def __init__(self):
        self.colour = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stage_pos_x = 0
        self.stage_pos_y = 0
        self.tile_width = self.tiles[0][0].get_width()
        self.tile_height = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stage_pos_x -= x
        self.stage_pos_y -= y
        col = (self.stage_pos_x % (self.tile_width * len(self.tiles[0]))) // self.tile_width
        x_off = (0 - self.stage_pos_x % self.tile_width)
        row = (self.stage_pos_y % (self.tile_height * len(self.tiles))) // self.tile_height
        y_off = (0 - self.stage_pos_y % self.tile_height)

        col2 = ((self.stage_pos_x + self.tile_width) % (self.tile_width * len(self.tiles[0]))) // self.tile_width
        row2 = ((self.stage_pos_y + self.tile_height) % (self.tile_height * len(self.tiles))) // self.tile_height
        screen.blit(self.tiles[row][col], [x_off, y_off])
        screen.blit(self.tiles[row][col2], [x_off + self.tile_width, y_off])
        screen.blit(self.tiles[row2][col], [x_off, y_off + self.tile_height])
        screen.blit(self.tiles[row2][col2], [x_off + self.tile_width, y_off + self.tile_height])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()


class NewSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)

        self.original_width = img.get_width() // frames
        self.original_height = img.get_height()
        x = 0

        for frameNo in range(frames):
            frame_surf = pygame.Surface((self.original_width, self.original_height), pygame.SRCALPHA, 32)
            frame_surf.blit(img, (x, 0))
            self.images.append(frame_surf.copy())
            x -= self.original_width
        self.image = img.copy()

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, x_pos, y_pos, centre=False):
        if centre:
            self.rect.center = [x_pos, y_pos]
        else:
            self.rect.topleft = [x_pos, y_pos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        original_rect = self.images[self.currentImage].get_rect()
        self.original_width = original_rect.width
        self.original_height = original_rect.height
        self.rect.center = old_center
        self.mask = pygame.mask.from_surface(self.image)
        if screen_refresh:
            updateDisplay()


class NewTextBox(pygame.sprite.Sprite):
    def __init__(self, text, x_pos, y_pos, width, case, max_length, font_size):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = max_length
        self.boxSize = int(font_size * 1.7)
        self.image = pygame.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1])
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColour = pygame.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, font_size)
        self.rect.topleft = [x_pos, y_pos]
        new_surface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(new_surface, [10, 5])

    def update(self, key_event):
        key = key_event.key
        unicode = key_event.unicode
        if 31 < key < 127 \
                and (self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if key_event.mod in (1, 2) \
                    and self.case == 1 \
                    and 97 <= key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif key_event.mod == 0 \
                    and self.case == 2 \
                    and 97 <= key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            next_time = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    this_time = pygame.time.get_ticks()
                    if this_time > next_time:
                        self.text = self.text[0:len(self.text) - 1]
                        self.clear(True)
                        next_time = this_time + 50
                        pygame.event.clear()
                else:
                    deleting = False

        self.clear()

    def move(self, x_pos, y_pos, centre=False):
        if centre:
            self.rect.topleft = [x_pos, y_pos]
        else:
            self.rect.center = [x_pos, y_pos]

    def clear(self, refresh=False):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1])
        new_surface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(new_surface, [10, 5])
        if screen_refresh or refresh:
            updateDisplay()


class NewLabel(pygame.sprite.Sprite):
    image: pygame.SurfaceType
    rect: pygame.Rect

    def __init__(self, text, font_size, font, font_colour, x_pos, y_pos, bg):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(font_colour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = font_size
        self.background = bg
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [x_pos, y_pos]

    def update(self, new_text, font_colour, bg):
        self.text = new_text
        if font_colour:
            self.fontColour = parseColour(font_colour)
        if bg:
            self.background = parseColour(bg)

        old_topleft = self.rect.topleft
        self.renderText()
        self.rect.topleft = old_topleft
        if screen_refresh:
            updateDisplay()

    def renderText(self):
        line_surfaces = []
        text_lines = self.text.split("<br>")
        max_width = 0
        max_height = 0
        for line in text_lines:
            line_surfaces.append(self.font.render(line, True, self.fontColour))
            this_rect = line_surfaces[-1].get_rect()
            if this_rect.width > max_width:
                max_width = this_rect.width
            if this_rect.height > max_height:
                max_height = this_rect.height

        self.image = pygame.Surface((max_width, (self.fontSize + 1) * len(text_lines) + 5), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha(self.image)
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        line_pos = 0
        for lineSurface in line_surfaces:
            self.image.blit(lineSurface, [0, line_pos])
            line_pos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(file_name):
    if os.path.isfile(file_name):
        return pygame.image.load(file_name).convert_alpha()
    else:
        raise Exception(f"Error loading image: {file_name} - Check filename and path?")


def screenSize(size_x, size_y, x_pos=None, y_pos=None, fullscreen=False):
    global screen
    global background
    if x_pos is not None and y_pos is not None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x_pos, y_pos + 50)
    else:
        window_info = pygame.display.Info()
        monitor_width = window_info.current_w
        monitor_height = window_info.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitor_width - size_x) / 2, (monitor_height - size_y) / 2)
    if fullscreen:
        screen = pygame.display.set_mode([size_x, size_y], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([size_x, size_y])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screen_refresh:
        updateDisplay()


def rotateSprite(sprite, angle):
    print("rotateSprite has been deprecated. Please use transformSprite")
    transformSprite(sprite, angle, 1)


def transformSprite(sprite, angle, scale, h_flip=False, v_flip=False):
    old_middle = sprite.rect.center
    if h_flip or v_flip:
        temp_image = pygame.transform.flip(sprite.images[sprite.currentImage], h_flip, v_flip)
    else:
        temp_image = sprite.images[sprite.currentImage]
    if angle != 0 or scale != 1:
        sprite.angle = angle
        sprite.scale = scale
        temp_image = pygame.transform.rotozoom(temp_image, -angle, scale)
    sprite.image = temp_image
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = old_middle
    sprite.mask = pygame.mask.from_surface(sprite.image)
    if screen_refresh:
        updateDisplay()


def killSprite(sprite):
    sprite.kill()
    if screen_refresh:
        updateDisplay()


def setBackgroundColour(colour):
    background.setColour(colour)
    if screen_refresh:
        updateDisplay()


def setBackgroundImage(img):
    global background
    background.setTiles(img)
    if screen_refresh:
        updateDisplay()


def hideSprite(sprite):
    hidden_sprites.add(sprite)
    sprite_group.remove(sprite)
    if screen_refresh:
        updateDisplay()


def hideAll():
    hidden_sprites.add(sprite_group.sprites())
    sprite_group.empty()
    if screen_refresh:
        updateDisplay()


def unhideAll():
    sprite_group.add(hidden_sprites.sprites())
    hidden_sprites.empty()
    if screen_refresh:
        updateDisplay()


def showSprite(sprite):
    sprite_group.add(sprite)
    if screen_refresh:
        updateDisplay()


def makeSprite(filename, frames=1):
    return NewSprite(filename, frames)


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def prevSpriteImage(sprite):
    sprite.currentImage -= 1
    if sprite.currentImage < 0:
        sprite.currentImage = len(sprite.images) - 1
    sprite.changeImage(sprite.currentImage)


def makeImage(filename):
    return loadImage(filename)


def touching(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1, sprite2)
    return collided


def allTouching(sprite_name):
    if sprite_group.has(sprite_name):
        collisions = pygame.sprite.spritecollide(sprite_name, sprite_group, False, collided=pygame.sprite.collide_mask)
        collisions.remove(sprite_name)
        return collisions
    else:
        return []


def pause(milliseconds, allow_esc=True):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    wait_time = current_time + milliseconds
    updateDisplay()
    while not (current_time > wait_time or (keys[pygame.K_ESCAPE] and allow_esc)):
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and allow_esc:
            pygame.quit()
            sys.exit()
        current_time = pygame.time.get_ticks()


def drawRect(x_pos, y_pos, width, height, colour, stroke=0):
    colour = parseColour(colour)
    this_rect = pygame.draw.rect(screen, colour, [x_pos, y_pos, width, height], stroke)
    if screen_refresh:
        pygame.display.update(this_rect)


def drawLine(x1, y1, x2, y2, colour, line_width=1):
    colour = parseColour(colour)
    this_rect = pygame.draw.line(screen, colour, (x1, y1), (x2, y2), line_width)
    if screen_refresh:
        pygame.display.update(this_rect)


def drawPolygon(pointlist, colour):
    colour = parseColour(colour)
    this_rect = pygame.draw.polygon(screen, colour, pointlist)
    if screen_refresh:
        pygame.display.update(this_rect)


def drawEllipse(centre_x, centre_y, width, height, colour):
    global bg_surface
    colour = parseColour(colour)
    this_rect = pygame.Rect(centre_x - width / 2, centre_y - height / 2, width, height)
    pygame.draw.ellipse(screen, colour, this_rect)
    if screen_refresh:
        pygame.display.update(this_rect)


def drawTriangle(x1, y1, x2, y2, x3, y3, colour):
    colour = parseColour(colour)
    this_rect = pygame.draw.polygon(screen, colour, [(x1, y1), (x2, y2), (x3, y3)])
    if screen_refresh:
        pygame.display.update(this_rect)


def clearShapes():
    global background
    screen.blit(background.surface, [0, 0])
    if screen_refresh:
        updateDisplay()


def updateShapes():
    pygame.display.update()


def end():
    pygame.quit()


def makeSound(filename):
    pygame.mixer.init()
    return pygame.mixer.Sound(filename)


def playSound(sound, loops=0):
    sound.play(loops)


def stopSound(sound):
    sound.stop()


def playSoundAndWait(sound):
    sound.play()
    while pygame.mixer.get_busy():
        # pause
        pause(10)


def makeMusic(filename):
    pygame.mixer.music.load(filename)


def playMusic(loops=0):
    global music_paused
    if music_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(loops)
    music_paused = False


def stopMusic():
    pygame.mixer.music.stop()


def pauseMusic():
    global music_paused
    pygame.mixer.music.pause()
    music_paused = True


def rewindMusic():
    pygame.mixer.music.rewind()


def endWait():
    updateDisplay()
    print("Press ESC to quit")
    keys = pygame.key.get_pressed()
    wait_time = 0

    while not keys[pygame.K_ESCAPE]:
        current_time = pygame.time.get_ticks()
        if current_time > wait_time:
            pygame.event.clear()
            keys = pygame.key.get_pressed()
            wait_time += 20

    pygame.quit()


def keyPressed(key_check=""):
    global key_dict
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if key_check == "" or keys[key_dict[key_check.lower()]]:
            return True
    return False


def makeLabel(text, font_size, x_pos, y_pos, font_colour='black', font='Arial', bg="clear"):
    # make a text sprite
    this_text = NewLabel(text, font_size, font, font_colour, x_pos, y_pos, bg)
    return this_text


def moveLabel(sprite, x, y):
    sprite.rect.topleft = [x, y]
    if screen_refresh:
        updateDisplay()


def changeLabel(text_object, new_text, font_colour=None, bg=None):
    text_object.update(new_text, font_colour, bg)


def waitPress():
    pygame.event.clear()
    this_event = pygame.event.wait()

    while this_event.type != pygame.KEYDOWN:
        this_event = pygame.event.wait()

    return this_event.key


def makeTextBox(x_pos, y_pos, width, case=0, starting_text="Please type here", max_length=0, font_size=22):
    this_text_box = NewTextBox(starting_text, x_pos, y_pos, width, case, max_length, font_size)
    textbox_group.add(this_text_box)
    return this_text_box


def textBoxInput(textbox, callback=None, args=None):
    # starts grabbing key inputs, putting into textbox until enter pressed
    if args is None:
        args = []

    global key_dict
    textbox.text = ""
    return_val = None
    while True:
        updateDisplay()
        if callback:
            return_val = callback(*args)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    textbox.clear()
                    if return_val:
                        return textbox.text, return_val
                    else:
                        return textbox.text
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    textbox.update(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


def tick(fps):
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    game_clock.tick(fps)
    return game_clock.get_fps()


def showLabel(label_name):
    textbox_group.add(label_name)
    if screen_refresh:
        updateDisplay()


def hideLabel(label_name):
    textbox_group.remove(label_name)
    if screen_refresh:
        updateDisplay()


def showTextBox(text_box_name):
    textbox_group.add(text_box_name)
    if screen_refresh:
        updateDisplay()


def hideTextBox(text_box_name):
    textbox_group.remove(text_box_name)
    if screen_refresh:
        updateDisplay()


def updateDisplay():
    global background
    pygame.display.update()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    sprite_group.clear(screen, background.surface)
    textbox_group.clear(screen, background.surface)


def mousePressed():
    pygame.event.clear()
    mouse_state = pygame.mouse.get_pressed()
    if mouse_state[0]:
        return True
    else:
        return False


def spriteClicked(sprite):
    mouse_state = pygame.mouse.get_pressed()
    if not mouse_state[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parseColour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colour_rgb = pygame.Color("white")
        colour_rgb.r = colour[0]
        colour_rgb.g = colour[1]
        colour_rgb.b = colour[2]
        return colour_rgb


def mouseX():
    x = pygame.mouse.get_pos()
    return x[0]


def mouseY():
    y = pygame.mouse.get_pos()
    return y[1]


def scrollBackground(x, y):
    global background
    background.scroll(x, y)


def setAutoUpdate(val):
    global screen_refresh
    screen_refresh = val


if __name__ == "__main__":
    print(""""pygame_functions is not designed to be run directly.
    See the wiki at https://github.com/StevePaget/Pygame_Functions/wiki/Getting-Started for more information""")

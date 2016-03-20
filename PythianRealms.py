# according to PEP 8, it's better to waste a tonne of space like this??
import sys
import os
import time
import random
import math
import traceback
import webbrowser
import platform
import socket
import _thread as thread
import zipfile
import shutil
import easygui
import logging
import ftplib
import urllib.request
import pygame
from pygame.locals import *
from com.scratso.pr.variables import *
from com.scratso.pr.locales.en_UK import *
# from com.scratso.pr.locales.google import *

# -*- coding: utf-8 -*-

"""
    PythianRealms Singleplayer Construction Sandbox
    Copyright (C) 2016 Adonis Megalos <scratso@yahoo.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

version = "2016.168"

# Encompass the entire program in a try statement for the error reporter.
try:    
    online = False
    server = False  # set to true to enable mysql connections. DON'T!
    chat = None
    channel = "#PythianRealms"

    fullscreen = False

    messages = [
        "",
        chatwelcome,
        chatstaff
        ]

    staff = {"Scratso": staffowner,
             "Scratsy": staffowner,
             "SapphireCoyote": staffmod}

    ########################
    # SET UP POPUP WINDOWS #
    ########################

    def msgbox(title, mtext): # not sure if this is still used
        easygui.msgbox(mtext, title)


    class Settings(easygui.EgStore): # member details save/loading system
        def __init__(self, filename):  # filename is required
            # -------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            # -------------------------------------------------
            self.username = None
            self.password = None

            # -------------------------------------------------
            # For subclasses of EgStore, these must be
            # the last two statements in  __init__
            # -------------------------------------------------
            self.filename = filename  # this is required
            self.restore()  # restore values from the storage file if possible


    # # Initialise the logger #

    logger = logging.getLogger('DEBUGGER')

    file_log_handler = logging.FileHandler('data/debug.log')
    logger.addHandler(file_log_handler)

    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)

    logger.setLevel("DEBUG")

    # nice output format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    file_log_handler.setFormatter(formatter)
    stderr_log_handler.setFormatter(formatter)

    #######################
    # INITIALIZE SETTINGS #
    #######################

    settingsFile = "data\Settings.txt"
    settings = Settings(settingsFile)

    # print(settings.username)

    if settings.username is None:
        username = None
        settings.username = username
        settings.store()  # persist the settings

    opt = False
    premium = True  # set to false if you actually want people to pay for premium

    if online:
        logger.info("Is the user a PREMIUM player? " + str(premium))

    # Print the GNU GPL
    print("""
    """ + gameName + """  Copyright (C) 2016 Adonis Megalos
    This program comes with ABSOLUTELY NO WARRANTY; type 'show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type 'show c'.
    http://gnu.org/licenses/gpl.html for details.
    Otherwise, type 'run' to play.
    """)

    i = 1
    while i == 1:
        cmd = input("> ").lower()
        if cmd == "show w":
            print("""
    15. Disclaimer of Warranty.

    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE
    LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR
    OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND,
    EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
    ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.
    SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY
    SERVICING, REPAIR OR CORRECTION.
    """)
        elif cmd == "show c":
            print("""
    2. Basic Permissions.

    All rights granted under this License are granted for the term of copyright
    on the Program, and are irrevocable provided the stated conditions are met.
    This License explicitly affirms your unlimited permission to run the
    unmodified Program. The output from running a covered work is covered by
    this License only if the output, given its content, constitutes a covered
    work. This License acknowledges your rights of fair use or other equivalent,
    as provided by copyright law. You may make, run and propagate covered works
    that you do not convey, without conditions so long as your license otherwise
    remains in force. You may convey covered works to others for the sole purpose
    of having them make modifications exclusively for you, or provide you with
    facilities for running those works, provided that you comply with the terms
    of this License in conveying all material for which you do not control
    copyright. Those thus making or running the covered works for you must do
    so exclusively on your behalf, under your direction and control, on terms
    that prohibit them from making any copies of your copyrighted material outside
    their relationship with you. Conveying under any other circumstances is
    permitted solely under the conditions stated below. Sublicensing is not
    allowed; section 10 makes it unnecessary.
    """)
        elif cmd == "run":
            i = 0
        else:
            print("Unknown command.")


    #####################
    # OPERATING SYSTEMS #
    #####################

    # can't be bothered changing when it leaves alpha
    if "Alpha" in version:
        print("""
    Please be aware that this is alpha-level software, and some changes may
    severely affect the game's experience or break the game on your device.
    If this happens, please create an issue at
    https://github.com/Scratso/PythianRealms . Additionally, previous versions
    are available for download from there.
        Thank you.
    """)
    elif "Beta" in version:
        print("""
    Please be aware that this is beta-level software, and some changes may
    severely affect the game's experience or cause errors and problems. If this
    happens, please create an issue at https://github.com/Scratso/PythianRealms.
    Additionally, previous versions are available for download from there.
        Thank you.
    """)

    useros = sys.platform
    logger.info("Operating System Environment: " + useros + ".")
    logger.info("Operating System Architecture: " + platform.architecture()[0])
    logger.info("Operating System Version: " + platform.platform())
    logger.info("Operating System Name: " + platform.system())
    logger.info("Processor: " + platform.processor())
    logger.info("Game Version: " + version)
    logger.info("Game Quality: " + str(tilesizex))

    #################
    # SET UP PYGAME #
    #################

    # try to center the game window
    try:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    except Exception as e:
        logger.error("Unable to auto-center " + gameName + " Window. Error: %s" % e)

    # colours
    black = (0, 0, 0)
    brown = (139, 69, 19)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    gray = (80, 80, 80)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    purple = (204, 0, 102)

    texturezips = [os.path.splitext(f)[0] for f in os.listdir("graphics") if
                   os.path.isfile(os.path.join("graphics", f)) and ".zip" in f]
    texturepack = easygui.choicebox(
        texture1, texturehead, texturezips)
    try:
        os.mkdir("graphics/temp/")
    except:
        logger.info("Removing previous temporary texture files...")
        for the_file in os.listdir("graphics/temp/"):
            file_path = os.path.join("graphics", "temp", the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(e)
        os.rmdir("graphics/temp/")
        os.mkdir("graphics/temp/")
    logger.info("Extracting textures...")
    with zipfile.ZipFile("graphics/" + texturepack + ".zip", "r") as z:
        z.extractall("graphics/temp/")

    musicpack = "music"
    try:
        os.mkdir("music/temp/")
    except:
        logger.info("Removing previous temporary music files...")
        for the_file in os.listdir("music/temp/"):
            file_path = os.path.join("music", "temp", the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(e)
        os.rmdir("music/temp/")
        os.mkdir("music/temp/")
    logger.info("Extracting music...")
    with zipfile.ZipFile("music/" + musicpack + ".zip", "r") as z:
        z.extractall("music/temp/")

##    localfiles = [os.path.splitext(f)[0] for f in os.listdir(os.path.join("com", "scratso", "pr", "locales")) if
##                   os.path.isfile(os.path.join("com", "scratso", "pr", "locales", f)) and ".py" in f and
##                   f != "__init__.py"]
##
##    locale = easygui.choicebox(locale1, localehead, localfiles)

    # set up the displays
    pygame.init()
    display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey),
                                      HWSURFACE | DOUBLEBUF)  # |RESIZABLE later
    mapsurf = pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey))
    mapsurf.fill(brown)
    prevsurf = pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    prevplacesurf = pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    npcsurf = pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    activesurf = pygame.Surface((tilesizex + 10, tilesizey + 27), pygame.SRCALPHA, 32).convert_alpha()
    activesurf.fill((23, 100, 255, 50))
    activeblock = pygame.Surface((tilesizex, tilesizey))
    musicsurf = pygame.Surface((vmapwidth / 3 * tilesizex + 4, 40), pygame.SRCALPHA, 32).convert_alpha()
    musicsurf.fill((23, 100, 255, 50))
    musictrack = pygame.Surface((vmapwidth / 3 * tilesizex, 36), pygame.SRCALPHA, 32).convert_alpha()
    musictrack.fill(0)
    invsurf = pygame.Surface((620, 620), pygame.SRCALPHA, 32).convert_alpha()
    invsurf.fill((23, 100, 255, 50))
    shopsurf = pygame.Surface((620, 620), pygame.SRCALPHA, 32).convert_alpha()
    shopsurf.fill((23, 100, 255, 50))
    magicsurf = pygame.Surface((vmapwidth * tilesizex, vmapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    magicsurf.fill(0)
    watersurf = pygame.Surface((vmapwidth * tilesizex, vmapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    watersurf.fill((0, 0, 255, 75))

    layersurfs = []
    for layer in range(mapz):
        layersurfs.append(
            pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey), pygame.SRCALPHA, 32).convert_alpha())

    # fonts
    gamefont = pygame.font.Font("graphics/temp/misc/gameFont.ttf", 12)
    gamefontl = pygame.font.Font("graphics/temp/misc/gameFont.ttf", 18)
    magichead = pygame.font.Font("graphics/temp/misc/gameFont.ttf", 60)
    magicbody = pygame.font.Font("graphics/temp/misc/gameFont.ttf", 36)

    activetxt = gamefont.render("Active", True, white)
    activesurf.blit(activetxt, (5, 5))

    pygame.display.set_caption(gameName + " " + gameYear)
    # set the window icon
    pygame.display.set_icon(pygame.image.load("graphics/temp/misc/icon.ico"))

##    # set up scratso screen
##    display.fill((9,9,9))
##    loadtext = magicbody.render(presenting, True, white)
##    display.blit(loadtext, (
##                    vmapwidth * tilesizex / 2 - round((len(presenting) / 2) * 16),
##                    vmapheight * tilesizey / 3 * 2))
##    display.blit(pygame.image.load("graphics/temp/misc/scratso.png"), (vmapwidth * tilesizex / 2 - 351, 200))
##    pygame.display.update()
##    time.sleep(3)
    # allow movie to play sound
    pygame.mixer.quit()
    # play intro movie
    FPS = 60
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie('Scratso_games_intro.mpg')

    movie.set_display(display, (0, 0, tilesizex * vmapwidth, tilesizey * vmapheight))
    movie.play()

    start = time.time()

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        now = time.time()
        if now - start >= 10:
            movie.stop()
            playing = False

        pygame.display.update()
        clock.tick(FPS)
    # enable game sounds
    pygame.mixer.init()

    # set up loading screen
    display.fill(white)
    loadtext = gamefont.render(loadingmsg, True, black)
    display.blit(loadtext, (0, vmapheight * tilesizey - 12))
    display.blit(pygame.image.load("graphics/temp/misc/logo.png"), (vmapwidth * tilesizex - 1200, -50))
    pygame.display.update()

    # load the player sprite
    player = pygame.transform.scale(
        pygame.image.load("graphics/temp/player/player_right.png").convert_alpha(),
        (tilesizex, tilesizey))

    # load the hp bar
    #    hpbar = pygame.image.load("graphics/temp//blood_red_bar.png")

    # Constants for the resources
    DIRT = 0
    GRASS = 1
    WATER = 2
    COAL = 3
    LAVA = 4
    ROCK = 5
    DIAM = 6
    SAPP = 7
    RUBY = 8
    GOLD = 9
    AIR = 10
    WOOD = 11
    GLASS = 12
    BRICK = 13
    CARP = 14
    SNOW = 15
    SEL = 16
    GSWORD = 17
    DSTAFF = 18
    SAND = 19

    prices = {
        DIRT : 0,
        GRASS : 1,
        WATER : 3,
        COAL : 4,
        LAVA : 5,
        ROCK : 6,
        DIAM : 10,
        SAPP : 12,
        RUBY : 14,
        GOLD : 13,
        CARP : 9,
        SNOW : 7,
        WOOD : 7,
        GLASS : 8,
        BRICK : 9,
        GSWORD : 12,
        DSTAFF : 25,
        SAND : 2
        }

    physics = {
        DIRT : "solid",
        GRASS : "solid",
        WATER : "liquid",
        COAL : "solid",
        LAVA : "liquid",
        ROCK : "solid",
        DIAM : "solid",
        SAPP : "solid",
        RUBY : "solid",
        GOLD : "solid",
        AIR : "liquid",
        CARP : "solid",
        SNOW : "solid",
        WOOD : "solid",
        GLASS : "solid",
        BRICK : "solid",
        GSWORD : "weapon",
        DSTAFF : "weapon",
        SAND : "solid"
        }

    active = DIRT

    sel = ((vmapwidth * tilesizex) / 2 - 310 + 10, (vmapheight * tilesizey) / 2 - 310 + 20)
    sel2 = ((vmapwidth * tilesizex) / 2 - 310 + 10, (vmapheight * tilesizey) / 2 - 310 + 120)

    seamless = False

    # a list of resources
    resources = [DIRT, GRASS, WATER, COAL, LAVA, ROCK, DIAM, SAPP, RUBY, GOLD,
                 CARP, SNOW, WOOD, GLASS, BRICK, GSWORD, DSTAFF, SAND]

    ########
    # NPCS #
    ########

# Best way to describe this:
# link every npc to a number, and refer to that npc as a number. Then add sub-numbers depending on how many of each npc
# you want to exist.

    # 0 = Penguin, 1 = Poacher, 4 = (Custom) Tudor, 16 = (Custom) Amnesiac
    NPCs = [0, 1, 2, 3]
    npcDrop = {
        0: 0,
        1: 10,
        2: 0,
        3: 6
    }
    # NPC ID : { CHUNK : [LIST OF NPC NUMBERS IN CHUNK] },
    NPCcount = {
        0: [0, 1, 2, 3, 4],
        1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        2: [0],
        3: [0]
    }
    NPCrealm = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }
    NPCtype = {
        0: "Friendly",
        1: "Hostile",
        2: "Friendly",
        3: "Hostile",
    }
    NPCdamage = {
        0: 0,
        1: 6,
        2: 0,
        3: 8,
    }
    # NPC ID : {  NPC NUMBER : NPC NUMBER HP  }
    NPChealth = {
        0: {0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1},
        1: {0: 24,
            1: 24,
            2: 24,
            3: 24,
            4: 24,
            5: 24,
            6: 24,
            7: 24,
            8: 24,
            9: 24,
            10:24,
            11:24,
            12:24,
            12:24,
            13:24,
            14:24},
        2: {0: 1},
        3: {0: 48},
    }
    # for npc in NPCs:
    #    for chunk in range(25):
    #        if chunk in NPChealth[npc]:
    #            for curnpc in NPChealth[npc]:
    #                if os.path.isfile("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt")
    #  and os.access("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", os.R_OK):
    #                    file = open("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", "r")
    #                    integer = int(file.read())
    #                    NPChealth[npc][curnpc] = integer
    #                    file.close()
    NPCmaxHealth = {
        0: 1,
        1: 24,
        2: 1,
        3: 48,
    }
    # NPC ID : { NPC NUMBER : NPC NUMBER pos },
    npcPosX = {
        0: {0: random.randint(0, mapwidth - 1),
            1: random.randint(0, mapwidth - 1),
            2: random.randint(0, mapwidth - 1),
            3: random.randint(0, mapwidth - 1),
            4: random.randint(0, mapwidth - 1)},
        1: {0: random.randint(0, mapwidth - 1),
            1: random.randint(0, mapwidth - 1),
            2: random.randint(0, mapwidth - 1),
            3: random.randint(0, mapwidth - 1),
            4: random.randint(0, mapwidth - 1),
            5: random.randint(0, mapwidth - 1),
            6: random.randint(0, mapwidth - 1),
            7: random.randint(0, mapwidth - 1),
            8: random.randint(0, mapwidth - 1),
            9: random.randint(0, mapwidth - 1),
            10:random.randint(0, mapwidth - 1),
            11:random.randint(0, mapwidth - 1),
            12:random.randint(0, mapwidth - 1),
            13:random.randint(0, mapwidth - 1),
            14:random.randint(0, mapwidth - 1)},
        2: {0: random.randint(0, mapwidth - 1)},
        3: {0: random.randint(0, mapwidth - 1)},
    }
    npcPosY = {
        0: {0: random.randint(0, mapheight - 1),
            1: random.randint(0, mapheight - 1),
            2: random.randint(0, mapheight - 1),
            3: random.randint(0, mapheight - 1),
            4: random.randint(0, mapheight - 1)},
        1: {0: random.randint(0, mapheight - 1),
            1: random.randint(0, mapheight - 1),
            2: random.randint(0, mapheight - 1),
            3: random.randint(0, mapheight - 1),
            4: random.randint(0, mapheight - 1),
            5: random.randint(0, mapheight - 1),
            6: random.randint(0, mapheight - 1),
            7: random.randint(0, mapheight - 1),
            8: random.randint(0, mapheight - 1),
            9: random.randint(0, mapheight - 1),
            10:random.randint(0, mapheight - 1),
            11:random.randint(0, mapheight - 1),
            12:random.randint(0, mapheight - 1),
            13:random.randint(0, mapheight - 1),
            14:random.randint(0, mapheight - 1)},
        2: {0: random.randint(0, mapheight - 1)},
        3: {0: random.randint(0, mapheight - 1)},
    }
    npcPosZ = {
        0: 4,
        1: 4,
        2: 4,
        3: 4,
    }
    npcGraphic = {
        0: pygame.image.load('graphics/temp/npcs/penguin.png').convert_alpha(),
        1: pygame.image.load('graphics/temp/player-old/player_right.png').convert_alpha(),
        2: pygame.image.load('graphics/temp/npcs/void1.png').convert_alpha(),
        3: pygame.image.load('graphics/temp/npcs/smiler.png').convert_alpha(),
    }
    global npcName
    npcName = {
        0: "Penguin",
        1: "Poacher",
        2: "Tudor",
        3: "Amnesiac",
    }

    #    # Is the user 13 or older?
    #    if easygui.ynbox("""PythianRealms has an online chat system.
    # However, if you are below the age of 13, you must have parental consent to use such services.
    # Are you over the age of 13 or have parental consent?""", "Multiplayer Chat?"):
            # Open Multiplayer Chat System
    #        webbrowser.open("https://irc.editingarchive.com:8080/?channels=PythianRealms")

    # webbrowser.open("http://tmcore.co.uk:9090/?channels=PythianRealms")

    # use list comprehension to create the tilemap
    tilemap = [[[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz)]

    mapload = False

    # set the map's x and y offsets (positioning)
    xoffset, yoffset = 0, 0

    # a dictionary linking resources to textures
    textures = {
        DIRT: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/dirt.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        GRASS: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/grass.jpg').convert(),
                                      (tilesizex, tilesizey + round(tilesizey / 2))),
        WATER: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/water.jpg').convert(),
                                      (tilesizex, tilesizey + round(tilesizey / 2))),
        COAL: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/coal.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        LAVA: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/lava.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        ROCK: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/rock.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        DIAM: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/diamond.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        SAPP: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/sapphire.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        RUBY: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/ruby.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        GOLD: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/gold.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        AIR: pygame.transform.scale(pygame.image.load('graphics/temp/misc/air.png').convert_alpha(),
                                    (tilesizex, tilesizey + round(tilesizey / 2))),
        WOOD: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/wood.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        GLASS: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/glass.png').convert_alpha(),
                                      (tilesizex, tilesizey + round(tilesizey / 2))),
        BRICK: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/brick.jpg').convert(),
                                      (tilesizex, tilesizey + round(tilesizey / 2))),
        CARP: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/carpet/mid.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        SNOW: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/snow.jpg').convert(),
                                     (tilesizex, tilesizey + round(tilesizey / 2))),
        # NTS: Limited edition Item! To be removed on New Year's Day.
        SEL: pygame.transform.scale(pygame.image.load('graphics/temp/misc/sel.png').convert_alpha(),
                                    (tilesizex, tilesizey + round(tilesizey / 2))),
        GSWORD: pygame.transform.scale(pygame.image.load('graphics/temp/items/gsword.png').convert_alpha(),
                                       (tilesizex, tilesizey + round(tilesizey / 2))),
        DSTAFF: pygame.transform.scale(pygame.image.load('graphics/temp/items/DSTAFF.png').convert_alpha(),
                                       (tilesizex, tilesizey + round(tilesizey / 2))),
        SAND: pygame.transform.scale(pygame.image.load('graphics/temp/blocks/sand.jpg').convert(),
                                       (tilesizex, tilesizey + round(tilesizey / 2)))
    }

    elapsed = 0
    fps = 0
    cachedscreen = []

    # music vars - the music files start at 1, so the names and stuff must start at 1 too, hence buffer.
    tracks = ["Buffer",
              "Short But Sweet",
              "This is BLUESHIFT",
              "BLUESCREEN",
              "Keyboard Demo Attack!",
              "Are You Gunna Eat That",
              "Oh I Feel Just Fine... (Because I'm Making Macaroni)",
              "Magnetic Jellyfish Dance Party",
              "Four Color Hero",
              "BSOD'd",
              "BLUENOISE",
              "There's Always Next Week",
              "Nostalgia Breaks Hearts",
              "Analogue Dream Girl",
              "Grayscale",
              "This Broken Heart Has Too Many Pieces",
              "Hello World",
              "9am Skies",
              "Blueberry Jam",
              "Bitmap Blues",
              "Heat Death",
              "Her #0000ff Eyes",
              "Zero-G Lemonade"]
    albums = ["Buffer",
              "None (SoundCloud)",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESHIFT",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUESCREEN",
              "BLUENOISE",
              "BLUENOISE",
              "BLUENOISE",
              "BLUENOISE",
              "BLUENOISE",
              "BLUENOISE",
              "BLUENOISE"]
    authors = ["Buffer",
               "SmileBoy",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME",
               "PROTODOME"]
    covers = ["Buffer",
              "graphics/temp/misc/icon.ico",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/protodome200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluescreen200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif",
              "music/temp/bluenoise200.gif"]
    music = 0
    pygame.mixer.music.set_volume(0.75)


    def initMusic():
        global silence, music
        logger.info(
            "Initializing Music...")  # if this process fails and it starts in silent mode, you screwed something up...
                                      # or you don't have speakers, ofc.
        if music == 22:
            music = 1
        else:
            music += 1
        logger.info("Running music #" + str(music))
        pygame.mixer.music.set_endevent(USEREVENT)
        try:
            m = pygame.mixer.music.get_volume()
            pygame.mixer.music.load('music/temp/' + str(music) + '.ogg')
            pygame.mixer.music.set_volume(m)
            pygame.mixer.music.play()
        except Exception:
            logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)

    def msg(message=["A message wasn't found! Tell Scratso!"]):
        message.append("")
        message.append("Press E to continue")
        messageactive = True
        while messageactive:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        change = True
                        messageactive = False
            display.fill(gray)
            pygame.draw.rect(display, blue, (15, 15, vmapwidth * tilesizex - 30, vmapheight * tilesizey - 30))
            textoffset = 0
            for line in message:
                text = gamefont.render(line, True, white)
                display.blit(text, (17, 17 + textoffset))
                textoffset += 12
            pygame.display.update()


# Notice: the following error reporting function is designed based on the BSOD, as my computer was experiencing
# BSODs while programming this.

    def err(err="ERROR_NOT_PROVIDED", trace="NO TRACEBACK PROVIDED\nERR 0x01"):
        display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey), HWSURFACE | DOUBLEBUF)
        # Idea from BSOD chat with MS, ref: 1301341941
        message = [
            err1,
            "",
            err2,
            "",
            err3,
            "",
            err4,
            "",
            err5,
            "",
            "*** ERROR: " + err,
            "",
            "*** OS ENV: " + useros,
            "",
            "*** OS ARCHITECTURE: " + platform.architecture()[0],
            "",
            "*** OS VERSION: " + platform.platform(),
            "",
            "*** OS NAME: " + platform.system(),
            "",
            "*** PROCESSOR: " + platform.processor(),
            "",
            "*** VERSION: " + version,
            "",
            "*** TRACEBACK: "
        ]
        for line in trace.split("\n"):
            message.append(line)
        display.fill(gray)
        pygame.draw.rect(display, blue, (15, 15, vmapwidth * tilesizex - 30, vmapheight * tilesizey - 30))
        textoffset = 0
        for line in message:
            text = gamefont.render(line, True, white)
            display.blit(text, (17, 17 + textoffset))
            textoffset += 12
        pygame.display.update()
        while True:
            pygame.event.flush()
            time.sleep(1)


    def magic_out(): # pretty sure this isn't used, but it was an idea. nts: work on this at some point
        magicsurf.fill((0, 0, 0, 100))
        pygame.display.update()
        time.sleep(0.01)
        for i in range(255):
            magicsurf.fill((i, i, i, 100))
            display.blit(magicsurf, (0, 0))
            pygame.display.update()
            time.sleep(0.01)


    def magicmsg(head="Oops", message=["A message wasn't found! Tell Scratso!"], fade=True, append=True):
        if append:
            message.append("")
            message.append(presse)
        messageactive = True
        while messageactive:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        change = True
                        messageactive = False
            display.fill(black)
            text = magichead.render(head, True, purple)
            display.blit(text, (vmapwidth * tilesizex / 2 - round((len(head) / 2) * 30), vmapheight * tilesizey / 3))
            textoffset = 70
            for line in message:
                text = magicbody.render(line, True, purple)
                display.blit(text, (
                    vmapwidth * tilesizex / 2 - round((len(line) / 2) * 16), vmapheight * tilesizey / 3 + textoffset))
                textoffset += 36
            pygame.display.update()
        if fade:
            magic_out()


    def loading():
        display.fill(white)
        loadtext = gamefontl.render(loadingmsg, True, black)
        if chat:
            display.blit(loadtext, (0, vmapheight * tilesizey + 32))
        else:
            display.blit(loadtext, (0, vmapheight * tilesizey - 18))
        display.blit(pygame.image.load("graphics/temp/misc/logo.png"), (vmapwidth * tilesizex - 1200, -50))
        pygame.display.update()


    def magic():
        magic_in()
        magic_out()


    def addchat(string):
        messages.append(string)

        # magicmsg("PythianRealms", ["Welcome back to the land of the living, my friend.",
        # "You've been asleep for a very long time."], False, False)
    
    menu = False
    # welcome screen
    messageactive = True
    while messageactive:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    change = True
                    messageactive = False
        display.fill(white)
        display.blit(pygame.image.load("graphics/temp/misc/logo.png"), (vmapwidth * tilesizex - 1200, -150))
        text = magichead.render(pressspace, True, black)
        display.blit(text, (
            vmapwidth * tilesizex / 2 - round((len(pressspace) / 2) * 27), vmapheight * tilesizey / 3 * 2))
        pygame.display.update()

    # Display all the startup things.
##    startupnotes = [welcome,
##                    welcome2 + version,
##                    welcomedev,
##                    welcomedonate,
##                    "",
##                    welcome3,
##                    "",
##                    welcome4,
##                    "",
##                    "",
##                    "KEYBINDINGS:",
##                    "============",
##                    "Arrow Keys: Move",
##                    "F3: Toggle debug information",
##                    "Q: Enable Build Mode",
##                    "A: Disable Build Mode",
##                    "R: Enable Pickup Mode",
##                    "F: Disable Pickup Mode",
##                    "T: Toggle RPG/Construction Realm",
##                    "C: Open " + gameName + " IRC Chat"] # nts: update keybindings
##    msg(startupnotes)

    changedz = list(range(mapz))  # 0,1,2,3 after you add the loading system. Until then, this'll do.

    oldNPCposX = None
    oldNPCposY = None

    initMusic()

    boost = 300  # 600 = 10 Minutes, 60 = 1 Minute, it's in seconds

    SECONDCOUNTDOWN = USEREVENT + 1
    pygame.time.set_timer(SECONDCOUNTDOWN, 1000)

    NPCMOVE = USEREVENT + 2
    pygame.time.set_timer(NPCMOVE, 1000)

    SAVE = USEREVENT + 3
    pygame.time.set_timer(SAVE, 30000)

    chatmsg = gamefont.render(clickchat, True, black)

    change = True

    while chat is None:
        global un
        if settings.username is None:
            un,pw = easygui.multpasswordbox("PythianRealms Account Informaton. This is for online chat. If you do not want online chat, please leave blank.", chathead, [enterun, enterpw])
        else:
            un,pw = settings.username,settings.password
        if (un is not None and un != "" and un != " " and un != False) and (pw is not None and pw != "" and pw != " " and pw != False):
            try:
                logger.info("Logging in as: "+un)
                check = str(urllib.request.urlopen('http://scratso.com/pythianrealms/acc/print.php?user='+un+"&password="+pw).read()).split("'")[1]
                if check == "Log in.":
                    global irc
                    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("connecting to irc.editingarchive.com...")
                    irc.connect(("irc.editingarchive.com", 6667))
                    irc.send(bytes("USER " + un + " " + un + " " + un + " :" + gameName + " Game Chat\n", "utf-8"))
                    irc.send(bytes("NICK " + un + "\n", "utf-8"))
                    text = str(irc.recv(2040))
                    unraw = text.split("\\r\\n")
                    for line in unraw:
                        print(line)
                        try:
                            nick = line.split(":")[1].split("!")[0]
                            text = line.split(":", 2)[2]
                        except:
                            nick = "Service"
                        if line.find("PING :") != -1:
                            irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
                    irc.send(bytes("JOIN " + channel + "\n", "utf-8"))
                    display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 50),
                                                      HWSURFACE | DOUBLEBUF)  # |RESIZABLE later
                    settings.username = un
                    settings.password = pw
                    settings.store()
                    chat = True
                else:
                    easygui.msgbox(check, "Unable to log in.")
                    logger.warn("Unable to log in: "+check)
            except Exception as e:
                logger.error(e)
                chat = False
        else:
            chat = False
    print(chat)
    if chat == False:
        display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 38),
                                                      HWSURFACE | DOUBLEBUF)  # |RESIZABLE later
        addchat("You are currently in offline mode, and so chat is disabled. Game notifications will still go here though!")


    def ircthread():
        if chat:
            con = 0
            last_ping = time.time()
            threshold = 7 * 60  # seven minutes, make this whatever you want
            while True:
                text = str(irc.recv(2040))
                unraw = text.split("\\r\\n")
                for line in unraw:
                    try:
                        nick = line.split(":")[1].split("!")[0]
                        try:
                            nick = "[" + staff[nick] + "] " + nick
                        except:
                            print(end="")
                        chan = line.split(" :")[0].split(" ")[2]
                        text = line.split(":", 2)[2]
                    except:
                        nick = "Service"
                    if "Serv" in nick or "irc.editingarchive.com" in nick:
                        nick = "Service"
                    print("<" + nick + "> " + text)
                    if line.find("PING :") != -1 and nick == "Service":
                        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
                        last_ping = time.time()
                    elif line.find("JOIN :") != -1:
                        irc.send(bytes("JOIN " + channel + "\n", "utf-8"))
                        if nick != un and nick != "Service":
                            addchat(nick + chatjoin)
                    elif line.find("KICK ") != -1:
                        if line.split("#PythianRealms ")[1].split(" :")[0] == un:
                            addchat(chatkicky + text + "\"")
                            addchat(chatlost)
                            break
                        else:
                            addchat(nick + chatkick1 + line.split("#PythianRealms ")[1].split(" :")[
                                0] + chatkick2 + text + "\"")
                    elif "\\x01" in text:
                        text = text.split("\\x01")[1].split("ACTION ")[1]
                        addchat("* " + line.split(":")[1].split("!")[0] + " " + text + " *")
                    elif line.find("NICK :") != -1:
                        addchat(line.split(":")[1].split("!")[0] + chatnick + line.split(":", 2)[2])
                    elif line.find("QUIT :") != -1:
                        addchat(line.split(":")[1].split("!")[0] + chatleave)
                    elif line.find("PART #PythianRealms") != -1:
                        addchat(line.split(":")[1].split("!")[0] + chatleave)
                    elif nick != "Service" and "MODE " not in line:
                        addchat(nick + ": " + text)
                    elif nick == "Service" and text == "You have not registered":
                        con += 1
                        if con >= 3:
                            addchat(chatlost)
                            break
                    elif nick == "Service" and text == "Nickname is already in use":
                        addchat(chatnicku)
                        addchat(chatlost)
                        break
                    elif line.find("353") != -1:
                        addchat("*** Players online: " + text)
                    if (time.time() - last_ping) > threshold:
                        addchat(chatlost)
                        break
                else:
                    continue
                break


    class Save(
        easygui.EgStore):  # Create a class named Settings inheriting from easygui.EgStore so that I can persist
        # TechnoMagic Account info.
        def __init__(self, filename):  # filename is required
            # -------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            # -------------------------------------------------
            self.map = [[[[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz)],
                        [[[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz)]]
            for row in range(mapheight):
                for col in range(mapwidth):
                    b = random.randint(1, 20)
                    if 1 <= b <= 8:
                        self.map[0][0][row][col] = ROCK
                    elif 9 <= b <= 10:
                        self.map[0][0][row][col] = COAL
                    elif 11 <= b <= 12:
                        self.map[0][0][row][col] = DIAM
                    elif 13 <= b <= 14:
                        self.map[0][0][row][col] = GOLD
                    elif 15 <= b <= 16:
                        self.map[0][0][row][col] = LAVA
                    elif 17 <= b <= 18:
                        self.map[0][0][row][col] = RUBY
                    elif 19 <= b <= 20:
                        self.map[0][0][row][col] = SAPP
            for row in range(mapheight):
                for col in range(mapwidth):
                    b = random.randint(1, 20)
                    if 1 <= b <= 10 or self.map[0][0][row][col] == LAVA:
                        self.map[0][1][row][col] = ROCK
                    elif 11 <= b <= 20:
                        self.map[0][1][row][col] = DIRT
            for row in range(mapheight):
                for col in range(mapwidth):
                    self.map[0][2][row][col] = WATER
            islands = random.randint(15, 20)
            logger.info("Number of islands: " + str(islands))
            for island in range(islands):
                size = random.randint(10, 20)
                pos = (random.randint(0, mapwidth - size), random.randint(0, mapheight - size))
                logger.info("Island #" + str(island) + " is " + str(size * size) + " blocks big at " + str(pos))
                for row in range(size):
                    for column in range(size):
                        self.map[0][2][pos[0] + row][pos[1] + column] = SAND
                for row in range(size-4):
                    for column in range(size-4):
                        self.map[0][3][pos[0] + 2 + row][pos[1] + 2 + column] = GRASS
            self.inventory = {
                DIRT: 0,
                GRASS: 0,
                WATER: 0,
                COAL: 0,
                LAVA: 0,
                ROCK: 0,
                DIAM: 0,
                SAPP: 0,
                RUBY: 0,
                GOLD: 0,
                CARP: 0,
                SNOW: 0,
                WOOD: 0,
                GLASS: 0,
                BRICK: 0,
                GSWORD: 0,
                DSTAFF: 0,
                SAND: 0,
            }
            self.realm = 0
            self.coins = 1000

            # -------------------------------------------------
            # For subclasses of EgStore, these must be
            # the last two statements in  __init__
            # -------------------------------------------------
            self.filename = filename  # this is required
            self.restore()  # restore values from the storage file if possible


    savefile = easygui.buttonbox(saveselect, saveselhead,
                                 savechoices)
    # savefile = easygui.choicebox("Please select a save file.", "Select a Save!", list(string.ascii_uppercase))
    data = Save("data/" + savefile + ".txt")

    realm = data.realm
    coins = data.coins
    inventory = data.inventory
    tilemap = data.map[realm]

    if chat:
        thread.start_new_thread(ircthread, ())

    # speed up evet handling
    pygame.event.set_allowed([SECONDCOUNTDOWN, USEREVENT, SAVE, QUIT, MOUSEBUTTONDOWN, KEYDOWN, NPCMOVE])

    while True:
        # msg(["Test"])
        now = time.time()
        display.fill(black)
        # display.fill(blue)
        # magic()
        if place or pickup:
            shownz = list(range(zaxis+1))
        else:
            shownz = list(range(mapz))
        musictrack.fill(0)

        if boost <= 0:
            coins += 1000
            boost = 300

        timeleft = boost

        mintile = [-xoffset / tilesizex, -yoffset / tilesizey]
        maxtile = [mintile[0] + (vmapwidth * tilesizex) / tilesizex, mintile[1] + (vmapheight * tilesizey) / tilesizey]
        if mintile[0] < 0:
            mintile[0] = 0
        elif mintile[1] < 0:
            mintile[1] = 0
        if maxtile[0] > 100:
            maxtile[0] = 100
        elif maxtile[1] > 100:
            maxtile[1] = 100

        if place or pickup or change:
            prevsurf.fill(0)

        if change:
            loading()

        mx, my = pygame.mouse.get_pos()
        playerTile = (round(((vmapwidth * tilesizex / 2 - 12) - xoffset) / tilesizex),
                      round(((vmapheight * tilesizey / 2 - 12) - yoffset) / tilesizey))
        playerRegion = (math.floor(playerTile[0] / 16), math.floor(playerTile[1] / 16))

        keys = pygame.key.get_pressed()
        # if the right arrow is pressed
        if keys[pygame.K_RIGHT]:  # and playerTile[0] < mapwidth - 1
            player = pygame.transform.scale(
                pygame.image.load("graphics/temp/player/player_right.png").convert_alpha(),
                (tilesizex, tilesizey))
            if playerTile[0] != 99:
                try:
                    if (physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and
                        physics[tilemap[playerz + 1][playerTile[1]][playerTile[0]]] == "solid"):
                        xoffset += tilesizex
                    else:
                        if physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and playerz < mapz-1:  # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if physics[tilemap[playerz - 1][playerTile[1]][playerTile[0]]] == "liquid" and playerz > 0:  # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    xoffset -= 2
                except:
                    pass
        if keys[pygame.K_LEFT]:
            player = pygame.transform.scale(
                pygame.image.load("graphics/temp/player/player_left.png").convert_alpha(),
                (tilesizex, tilesizey))
            if playerTile[0] != 0:
                try:
                    if (physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and
                        physics[tilemap[playerz + 1][playerTile[1]][playerTile[0]]] == "solid"):
                        xoffset -= tilesizex
                    else:
                        if physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and playerz < mapz-1:  # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if physics[tilemap[playerz - 1][playerTile[1]][playerTile[0]]] == "liquid" and playerz > 0:  # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    xoffset += 2
                except:
                    pass
        if keys[pygame.K_UP]:
            if playerTile[1] != 0:
                try:
                    if (physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and
                        physics[tilemap[playerz + 1][playerTile[1]][playerTile[0]]] == "solid"):
                        yoffset -= tilesizey
                    else:
                        if physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and playerz < mapz-1:  # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if physics[tilemap[playerz - 1][playerTile[1]][playerTile[0]]] == "liquid" and playerz > 0:  # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    yoffset += 2
                except:
                    pass
        if keys[pygame.K_DOWN]:
            if playerTile[1] != 99:
                try:
                    if (physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and
                        physics[tilemap[playerz + 1][playerTile[1]][playerTile[0]]] == "solid"):
                        yoffset += tilesizey
                    else:
                        if physics[tilemap[playerz][playerTile[1]][playerTile[0]]] == "solid" and playerz < mapz-1:  # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if physics[tilemap[playerz - 1][playerTile[1]][playerTile[0]]] == "liquid" and playerz > 0:  # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    yoffset -= 2
                except:
                    pass

        for event in pygame.event.get():
            if event.type == SECONDCOUNTDOWN:
                boost -= 1
                if playerHP < 100:
                    playerHP += 1
            elif event.type == USEREVENT:
                initMusic()
            elif event.type == SAVE:
                logger.info("Auto-saving...")
                data.realm = realm
                data.map[realm] = tilemap
                data.inventory = inventory
                data.coins = coins
                data.store()
                logger.info("Save complete.")
            elif event.type == QUIT:
                if chat:
                    irc.send(bytes("QUIT :Client exited.\n", "utf-8"))
                    irc.close()
                if easygui.ynbox(savequery):
                    logger.info("Saving game...")
                    data.realm = realm
                    data.map[realm] = tilemap
                    data.inventory = inventory
                    data.coins = coins
                    data.store()
                    logger.info("Game saved.")
                pygame.quit()
                try:
                    logger.info("Removing previous temporary music files...")
                    for the_file in os.listdir("music/temp/"):
                        file_path = os.path.join("music", "temp", the_file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            logger.error(e)
                    os.rmdir("music/temp/")
                except Exception as e:
                    logger.error(e)
                try:
                    logger.info("Removing previous temporary texture files...")
                    for the_file in os.listdir("graphics/temp/"):
                        file_path = os.path.join("graphics", "temp", the_file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            logger.error(e)
                    os.rmdir("graphics/temp/")
                except Exception as e:
                    logger.error(e)
                sys.exit("User has quit the application.")
            elif event.type == MOUSEBUTTONDOWN:
                if place:
                    x = math.floor(mx / tilesizex - xoffset / tilesizex)
                    y = math.floor(my / tilesizey - yoffset / tilesizey)
                    if inventory[active] > 0:
                        inventory[active] -= 1
                        tilemap[zaxis][y][x] = active
                        if zaxis not in changedz:
                            changedz.append(zaxis)
                        prevplacesurf.blit(textures[active], (x * tilesizex, y * tilesizey - zaxis * 16))
                        # print(tilemap[0][y][x])
                    else:
                        magicmsg(noblocks, [noblocksmsg],
                                 False)
                if pickup:
                    x = math.floor(mx / tilesizex - xoffset / tilesizex)
                    y = math.floor((my - (zaxis * 8)) / tilesizey - yoffset / tilesizey)
                    if tilemap[zaxis][y][x] != AIR:
                        inventory[tilemap[zaxis][y][x]] += 1
                        tilemap[zaxis][y][x] = AIR
                        if zaxis not in changedz:
                            changedz.append(zaxis)
                            # change = True
                            # print(tilemap[0][y][x])
                lowerx = 10
                upperx = 50
                lowery = 20
                uppery = 60
                index = 1
                for item in resources:
                    if (mx >= (vmapwidth * tilesizex) / 2 - 310 + lowerx and
                        mx <= (vmapwidth * tilesizex) / 2 - 310 + upperx and
                        my >= (vmapheight * tilesizey) / 2 - 310 + lowery and
                        my <= (vmapheight * tilesizey) / 2 - 310 + uppery):
                            if invshow:
                                if physics[item] != "weapon":
                                    active = item
                                    sel = ((vmapwidth * tilesizex) / 2 - 310 + lowerx, (vmapheight * tilesizey) / 2 - 310 + lowery)
                            elif shopshow:
                                if event.button == 1:
                                    if coins >= prices[item]:
                                        coins -= prices[item]
                                        inventory[item] += 1
                                    else:
                                        addchat(buycoin1 + str(prices[item]) + buyonecoin2)
                                elif event.button == 3:
                                    if coins >= (prices[item] * 10):
                                        coins -= (prices[item] * 10)
                                        inventory[item] += 10
                                    else:
                                        addchat(buycoin1 + str(prices[item] * 10) + buytencoin2)
                    if index % 12 != 0:
                        lowerx += 50
                        upperx += 50
                    else:
                        lowerx = 10
                        upperx = 50
                        lowery += 50
                        uppery += 50
                    index += 1

                if mx >= 50 and mx <= 60 and my >= 15 and my <= 25 and opt:
                    if silence:
                        initMusic()
                    elif not silence:
                        silence = True
                        pygame.mixer.music.stop()
                elif mx >= 50 and mx <= 60 and my >= 55 and my <= 65 and opt:
                    if activeoverlay:
                        activeoverlay = False
                    elif not activeoverlay:
                        activeoverlay = True
                elif (50 <= mx <= 60) and (75 <= my <= 85) and opt:
                    if seamless:
                        seamless = False
                    else:
                        seamless = True
                elif mx >= 50 and mx <= 60 and my >= 95 and my <= 105 and opt:
                    if smoothwalk:
                        smoothwalk = False
                    else:
                        smoothwalk = True

                elif mx >= 0 and mx <= vmapwidth * tilesizex and my >= vmapheight * tilesizey + 38 and \
                        (my <= vmapheight * tilesizey + 50):
                    if chat:
                        msgn = easygui.enterbox(chatentermsg, chathead)
                        if msgn is not None:
                            if msgn == "/who":
                                irc.send(bytes("NAMES :" + channel + "\n", "utf-8"))
                            elif msgn == "/help":
                                addchat("*** " + gameName + " "+version.split(".")[0]+" revision "+version.split(".")[1]+".")
                                webbrowser.open("http://scratso.com/pythianrealms/help.php", 2, True)
                            elif msgn.split(" ")[0] == "/nsid":
                                addchat("*** Submitted password to NickServ.")
                                irc.send(bytes("PRIVMSG NickServ :IDENTIFY "+msgn.split(" ",1)[1]+"\n", "utf-8"))
                            else:
                                irc.send(bytes("PRIVMSG " + channel + " :" + msgn + "\n", "utf-8"))
                                addchat(chaty + msgn)

                x = math.floor(mx / tilesizex - xoffset / tilesizex)
                y = math.floor(my / tilesizey - yoffset / tilesizey)
                for npc in NPCs:
                    for npcd in NPCcount[npc]:
                        if npcPosX[npc][npcd] == x and npcPosY[npc][npcd] == y:
                            if selectednpc is None or (selectednpc[0] != npc and selectednpc[1] != npcd):
                                selectednpc = (npc, npcd)
                            else:
                                selectednpc = None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = True
                elif event.key == K_F1:
                    webbrowser.open("http://scratso.com/pythianrealms/help.php", 2, True)
                elif event.key == K_F2:
                    if fullscreen:
                        if chat == False:
                            display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 38),
                                                      HWSURFACE | DOUBLEBUF)
                        else:
                            display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 50),
                                                      HWSURFACE | DOUBLEBUF)
                    else:
                        if chat == False:
                            display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 38),
                                                      HWSURFACE | DOUBLEBUF |
                                                              FULLSCREEN)
                        else:
                            display = pygame.display.set_mode((vmapwidth * tilesizex, vmapheight * tilesizey + 50),
                                                      HWSURFACE | DOUBLEBUF |
                                                              FULLSCREEN)
                elif event.key == K_F3:
                    debug = not debug
                elif event.key == K_INSERT:
                    # PythianRealms Debug Console Command System
                    cmd = easygui.enterbox("""This is a console input box. This
should be used for debug purposes only. Some commands may damage the game /
cause issues. Use this at your own risk. (This terminal is English only.)""")
                    if cmd is not None:
                        if " " in cmd:
                            command = cmd.split(" ")[0]
                            dat = cmd.split(" ")[1]
                            try:
                                num = int(cmd.split(" ")[2])
                            except:
                                num = None
                            if command == "additem":
                                dat = int(dat)
                                try:
                                    inventory[dat] += num
                                    addchat("Console: Added "+str(num)+" "+str(dat)+" to inventory.")
                                except:
                                    try:
                                        inventory[data] += 1
                                        addchat("Console: Added 1 "+str(dat)+" to inventory.")
                                    except:
                                        addchat("Error: "+str(dat)+" is not a valid inventory item.")
                            elif command == "setactive":
                                dat = int(dat)
                                active = dat
                            else:
                                addchat("Error: Command '"+cmd+"' not recognised.")
                        else:
                            addchat("Error: Unknown syntax for console command.")
                elif event.key == K_MINUS:
                    if zaxis >= 1:
                        zaxis -= 1
                elif event.key == K_EQUALS:
                    if zaxis <= mapz-2: # z limit - 2
                        zaxis += 1
                elif event.key == K_q:
                    if realm == 2 or premium:
                        changedz = []
                        pickup = True
                        addchat(pickupmodenotice)
                elif event.key == K_r:
                    if realm == 2 or premium:
                        changedz = []
                        place = True
                elif event.key == K_i:
                    invshow = not invshow
                elif event.key == K_h:
                    shopshow = not shopshow
                elif event.key == K_m:
                    if inventory[DSTAFF] > 0:
                        if selectednpc is not None:
                            if NPCtype[selectednpc[0]] == "Hostile":
                                magicmsg(darkness, darkdesc, True)
                                NPChealth[selectednpc[0]][selectednpc[1]] -= 25
                        else:
                            addchat(targetselect)
                            addchat(targetinstruct)
                    else:
                        if premium:
                            msg(["Hey, premium member!",
                                 "Did you know that you can buy a Staff of Darkness in the shop (H) for just 25 coins?",
                                 "Why not go do that, and then try this key again!"])
                elif event.key == K_SPACE:
                    if selectednpc is not None:
                        if NPCtype[selectednpc[0]] == "Hostile":
                            if (npcPosX[selectednpc[0]][selectednpc[1]] == playerTile[0] and npcPosY[selectednpc[0]][
                                selectednpc[1]] == playerTile[1]) or (
                                                -5 < playerTile[0] - npcPosX[selectednpc[0]][
                                                    selectednpc[1]] < 5 and -5 <
                                                        playerTile[1] - npcPosY[selectednpc[0]][selectednpc[1]] < 5):
                                if inventory[GSWORD] >= 1:
                                    NPChealth[selectednpc[0]][selectednpc[1]] -= 12
                                else:
                                    NPChealth[selectednpc[0]][selectednpc[1]] -= 6
                                selectednpc = None
                            else:
                                addchat("You're too far away to attack! You must be within 5 blocks of the enemy.")
                elif event.key == K_t:
                    logger.info("Saving Realm " + str(realm) + "...")
                    data.map[realm] = tilemap
                    data.store()
                    logger.info("Saved Realm " + str(realm) + ".")
                    if realm == 0:
                        realm = 1
                        data.realm = 1
                        #msg(["THE CONSTRUCTION REALM",
                        #     "======================",
                        #     """The construction realm contains monsters and NPCs to teach you how to build, destroy,
                        #     and use the Construction realm, but it does NOT have a storyline.""",
                        #     """The construction realm provides a home for all your construction talent to come together
                        #      to create a wondrous, magnificent building for you to share with your friends.""",
                        #     """The Construction realm, by all defaults, is a barren wasteland - that is, until you
                        #     build in it. The construction realm serves to satisfy the construction aspect of
                        #     PythianRealms.""",
                        #     """Have fun, and remember - T to toggle between realms... If you wish to return to the RPG
                        #     realm, of course. ;)"""])
                    elif realm == 1:
                        realm = 0
                        data.realm = 0
                        # msg(["THE RPG REALM",
                        #      "=============",
                        #      """The RPG realm is the home of the PythianRealms storyline. Riddled with people, monsters
                        #      and stories, the RPG realm is built by Scratso (the developer) and distributed with all
                        #      copies of PythianRealms.""",
                        #      """Construction within the RPG realm is usually forbidden, however Premium Users may
                        #      happily change the RPG realm to suit themselves. This allows premium users to improve on
                        #      existing buildings, if they wish.""",
                        #      """Have fun, and remember - T to toggle between realms... If you wish to return to the
                        #      Construction realm, of course. ;)"""])
                    change = True

                    tilemap = data.map[realm]
            elif event.type == NPCMOVE:
                for npc in NPCs:
                    for npcd in NPCcount[npc]:
                        if False: # NPCtype[npc] == "Hostile" and (playerTile[0] - npcPosX[npc][npcd] == 0 or npcPosX[npc][npcd] - playerTile[0] == 0 or playerTile[1] - npcPosY[npc][npcd] == 0 or npcPosY[npc][npcd] - playerTile[1] == 0):
                            playerHP -= 1
                        else:
                            if 0 < npcPosX[npc][npcd] < mapwidth - 1 and 0 < npcPosY[npc][npcd] < mapheight - 1:
                                if NPCtype[npc] == "Hostile" and (-1 <= playerTile[0] - npcPosX[npc][npcd] <= 1) and \
                                        (-1 <= playerTile[1] - npcPosY[npc][npcd] <= 1):
                                    # go right
                                    logger.info(str(npc) + " attacks you.")
                                    playerHP -= NPCdamage[npc]
                                if NPCtype[npc] == "Hostile" and -5 <= playerTile[0] - npcPosX[npc][npcd] <= 5 and -5 <= playerTile[
                                    0] - npcPosX[npc][npcd] <= 5:
                                    # go right
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd]][npcPosX[npc][npcd] + 1]
                                    if movementTile == AIR:
                                        # change the player's x position
                                        npcPosX[npc][npcd] += 1
                                elif NPCtype[npc] == "Hostile" and -5 <= npcPosX[npc][npcd] - playerTile[0] <= 5 and \
                                                        -5 <= npcPosX[npc][npcd] - playerTile[0] <= 5:
                                    # go left
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd]][npcPosX[npc][npcd] - 1]
                                    if movementTile == AIR:
                                        # change the player's x position
                                        npcPosX[npc][npcd] -= 1
                                elif NPCtype[npc] == "Hostile" and -5 <= playerTile[1] - npcPosY[npc][npcd] <= 5 and \
                                                        -5 <= playerTile[1] - npcPosY[npc][npcd] <= 5:
                                    # go down
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd] + 1][npcPosX[npc][npcd]]
                                    if movementTile == AIR:
                                        # change the player's x position
                                        npcPosY[npc][npcd] += 1
                                elif NPCtype[npc] == "Hostile" and -5 <= npcPosY[npc][npcd] - playerTile[1] <= 5 and \
                                                        -5 <= npcPosY[npc][npcd] - playerTile[1] <= 5:
                                    # go up
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd] - 1][npcPosX[npc][npcd]]
                                    if movementTile == AIR:
                                        # change the player's x position
                                        npcPosY[npc][npcd] -= 1
                                move = random.randint(1, 5)
                                if move == 2:
                                    # up
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd] - 1][npcPosX[npc][npcd]]
                                    if movementTile == AIR:
                                        npcPosY[npc][npcd] -= 1
                                elif move == 3:
                                    # down
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd] + 1][npcPosX[npc][npcd]]
                                    if movementTile == AIR:
                                        npcPosY[npc][npcd] += 1
                                elif move == 4:
                                    # left
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd]][npcPosX[npc][npcd] - 1]
                                    if movementTile == AIR:
                                        npcPosX[npc][npcd] -= 1
                                elif move == 5:
                                    # right
                                    movementTile = tilemap[npcPosZ[npc]][npcPosY[npc][npcd]][npcPosX[npc][npcd] + 1]
                                    if movementTile == AIR:
                                        npcPosX[npc][npcd] += 1
                realm = data.realm
                npcsurf.fill(0)
                # for each NPC
                for item in NPCs:
                    # determine the NPC's name here. This name **only** affects the text shown above the NPC.
                    # if chunk == NPCchunk[item] and realm == NPCrealm[item]:
                    npcPosZ[item] = 1
                    for curnpc in NPCcount[item]:
                        if (npcPosX[item][curnpc] >= mintile[0] and npcPosX[item][curnpc] <= maxtile[0]) and (
                                        npcPosY[item][curnpc] >= mintile[1] and npcPosY[item][curnpc] <= maxtile[1]):
                            # display the npc at the correct position
                            npcsurf.blit(pygame.transform.scale(npcGraphic[item], (tilesizex, tilesizey)),
                                         (npcPosX[item][curnpc] * tilesizex, npcPosY[item][curnpc] * tilesizey))
                            if NPCtype[item] == "Hostile":
                                # display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, red)
                                npcsurf.blit(NPCname, (
                                    npcPosX[item][curnpc] * tilesizex, npcPosY[item][curnpc] * tilesizey - 15))
                                percent = NPChealth[item][curnpc] / NPCmaxHealth[item] * 100
                                if percent <= 0:
                                    npcPosX[item][curnpc] = random.randint(0,mapwidth-1)
                                    npcPosY[item][curnpc] = random.randint(0,mapheight-1)
                                    coins += npcDrop[item]
                                    NPChealth[item][curnpc] = NPCmaxHealth[item]
                                    percent = 100
                                NHP = gamefont.render(str(round(percent)) + "%", True, red)                                    
                                npcsurf.blit(NHP, (
                                    npcPosX[item][curnpc] * tilesizex, npcPosY[item][curnpc] * tilesizey - 27))
                                if selectednpc is not None:
                                    if selectednpc[0] == item and selectednpc[1] == curnpc:
                                        npcselimg = pygame.transform.scale(
                                            pygame.image.load("graphics/temp/misc/selnpc.png").convert_alpha(),
                                            (tilesizex * 3, tilesizey + round(tilesizey / 2)))
                                        npcsurf.blit(npcselimg, (npcPosX[item][curnpc] * tilesizex - tilesizex,
                                                                 npcPosY[item][curnpc] * tilesizey))
                            elif NPCtype[item] == "Friendly":
                                # display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, green)
                                npcsurf.blit(NPCname, (
                                    npcPosX[item][curnpc] * tilesizex, npcPosY[item][curnpc] * tilesizey - 15))
                            else:
                                # display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, black)
                                npcsurf.blit(NPCname, (
                                    npcPosX[item][curnpc] * tilesizex, npcPosY[item][curnpc] * tilesizey - 15))
                                #                    else:
                                #                        npcPosZ[item] = 2
        pygame.event.pump()
        if playerz == 0:
            if tilemap[playerz + 1][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0]
            elif tilemap[playerz + 2][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0, 1]
            elif tilemap[playerz + 3][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0, 1, 2]
        elif playerz == 1:
            if tilemap[playerz + 1][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0, 1]
            elif tilemap[playerz + 2][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0, 1, 2]
        elif playerz == 2:
            if tilemap[playerz + 1][playerTile[1]][playerTile[0]] != AIR:
                shownz = [0, 1, 2]

        if change:
            loading()
            logger.info("Changing the following layers: " + str(changedz))
            change = False
            # mapsurf.fill(brown)
            prevplacesurf.fill(0)
            # loop through each layer
            for layer in changedz:  # mapz
                layersurfs[layer].fill(0)
                # loop through each row
                for row in range(mapheight):
                    # loop through each column in the row
                    for column in range(mapwidth):
                        # draw an image for the resource, in the correct position
                        layersurfs[layer].blit(textures[tilemap[layer][row][column]],
                                               (column * tilesizex, row * tilesizey)) #  - layer * 16
            changedz = []
            pass
        if place:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            # the below was lagging waay too much.
            prevsurf.blit(textures[active], (x * tilesizex, y * tilesizey - zaxis * 16))
            if pygame.key.get_pressed()[K_f]:
                place = False
                change = True
        if pickup:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            prevsurf.blit(textures[SEL], (x * tilesizex, y * tilesizey - zaxis * 16))
            if pygame.key.get_pressed()[K_a]:
                pickup = False
                change = True

        display.blit(mapsurf, (xoffset, yoffset))
        z = 0
        for layersurf in layersurfs:
            if layersurfs.index(layersurf) in shownz:
                display.blit(layersurfs[layersurfs.index(layersurf)], (xoffset, yoffset-(z+1)*16))
            z += 1
        display.blit(npcsurf, (xoffset, yoffset))
        display.blit(prevsurf, (xoffset, yoffset))
        display.blit(prevplacesurf, (xoffset, yoffset))
        display.blit(player, (
            vmapwidth * tilesizex / 2 - (tilesizex / 2), vmapheight * tilesizey / 2 - (tilesizey / 2) - playerz * 16))
        display.blit(activesurf, (vmapwidth * tilesizex - tilesizex - 10, 0))
        activeblock.blit(textures[active], (0, 0))
        display.blit(activeblock, (vmapwidth * tilesizex - tilesizex - 5, 22))
        display.blit(musicsurf,
                     ((vmapwidth * tilesizex) - (vmapwidth / 3 * tilesizex + 4), vmapheight * tilesizex - 40))
        track = gamefont.render(musicplaying + tracks[music], True, white)
        album = gamefont.render(musicalbum + albums[music], True, white)
        author = gamefont.render(musicauthor + authors[music], True, white)
        musictrack.blit(track, (36, 0))
        musictrack.blit(album, (40, 12))
        musictrack.blit(author, (44, 24))
        musictrack.blit(pygame.transform.scale(pygame.image.load(covers[music]).convert(), (32, 32)), (2, 2))
        display.blit(musictrack,
                     ((vmapwidth * tilesizex) - (vmapwidth / 3 * tilesizex + 2), vmapheight * tilesizex - 38))

        ztext = gamefont.render(zaxisname + str(zaxis), True, white)
        display.blit(ztext, (0, 0))

        ctext = gamefont.render(coins1 + format(coins, ",d") + coins2, True, white)
        display.blit(ctext, (0, 12))

        ttext = gamefont.render(coinsb1 + str(timeleft) + coinsb2, True, white)
        display.blit(ttext, (0, 24))

        hptext = gamefont.render(healthname + str(playerHP) + " / 100", True, white)
        display.blit(hptext, (0, 36))

        if debug:
            ptext = gamefont.render(tilename + str(playerTile), True, white)
            display.blit(ptext, (0, 48))

            rtext = gamefont.render(regionname + str(playerRegion), True, white)
            display.blit(rtext, (0, 60))

            etext = gamefont.render(fpsname + str(fps), True, white)
            display.blit(etext, (0, 72))

            qtext = gamefont.render(imagename1 + str(tilesizex) + imagename2, True,
                                    white)
            display.blit(qtext, (0, 84))

            pztext = gamefont.render(playerzname + str(playerz), True, white)
            display.blit(pztext, (0, 96))

            pptext = gamefont.render(mapoffname1 + str(xoffset) + mapoffname2 + str(yoffset) + mapoffname3, True, white)
            display.blit(pptext, (0, 108))

            rtext = gamefont.render(realmname + str(realm), True, white)
            display.blit(rtext, (0, 120))

        if tilemap[playerz][playerTile[1]][playerTile[0]] == WATER:
            display.blit(watersurf, (0, 0))

        if shopshow:
            shopsurf.fill((23, 100, 255, 50))
            text = gamefont.render(shoptitle, True, white)
            shopsurf.blit(text, (1, 1))
            # display the inventory, starting 10 pixels in
            placePosition = 10
            yoff = 20
            newrow = 12
            curitem = 1
            for item in resources:
                # add the image
                if item == AIR:
                    continue
                if curitem <= newrow:
                    shopsurf.blit(textures[item], (placePosition, yoff))
                    placePosition += 0
                    # add the text showing the amount in the inventory:
                    textObj = gamefont.render(str(inventory[item]), True, white)
                    shopsurf.blit(textObj, (placePosition, yoff + 35))
                    textObj = gamefont.render(str(prices[item])+"c", True, white)
                    shopsurf.blit(textObj, (placePosition, yoff))
                    placePosition += 50
                    if curitem == newrow:
                        curitem = 1
                        yoff += 50
                        placePosition = 10
                    else:
                        curitem += 1
            display.blit(shopsurf, ((vmapwidth * tilesizex) / 2 - 310, (vmapheight * tilesizey) / 2 - 310))

        if invshow:
            invsurf.fill((23, 100, 255, 50))
            text = gamefont.render(invtitle, True, white)
            invsurf.blit(text, (1, 1))
            # display the inventory, starting 10 pixels in
            placePosition = 10
            yoff = 20
            newrow = 12
            curitem = 1
            for item in resources:
                #      ANIMATION CODE - ADAPT FOR ANIMATED BLOCKS :)
                #        if item == WATER:
                #            if wateranim == 1:
                #                textures[WATER] = pygame.image.load("graphics/temp/water_2.jpg")
                #                wateranim = 2
                #            elif wateranim == 2:
                #                textures[WATER] = pygame.image.load("graphics/temp/water_1.jpg")
                #                wateranim = 1
                # add the image
                if item == AIR:
                    continue
                if curitem <= newrow:
                    invsurf.blit(textures[item], (placePosition, yoff))
                    placePosition += 0
                    # add the text showing the amount in the inventory:
                    textObj = gamefont.render(str(inventory[item]), True, white)
                    invsurf.blit(textObj, (placePosition, yoff + 35))
                    placePosition += 50
                    if curitem == newrow:
                        curitem = 1
                        yoff += 50
                        placePosition = 10
                    else:
                        curitem += 1
            display.blit(invsurf, ((vmapwidth * tilesizex) / 2 - 310, (vmapheight * tilesizey) / 2 - 310))
            if activeoverlay:
                display.blit(textures[SEL], sel)

        if playerHP <= 0:
            playerHP = 100
            coins = int(coins / 2)
            xoffset = 0
            yoffset = 0
            realm = 0

        if place:
            placetext = gamefont.render(buildmode, True, green)
            display.blit(placetext, (0, vmapheight * tilesizey - 12))
        if pickup:
            pickuptext = gamefont.render(pickupmode, True, red)
            display.blit(pickuptext, (0, vmapheight * tilesizey - 12))

        if menu:
            savecol = black
            sharecol = black
            screencol = black
            dlcol = black
            credcol = black
            impcol = black
            irccol = black
            quitcol = black
            screensurf = pygame.Surface((mapwidth * tilesizex, mapheight * tilesizey))
            screensurf.blit(mapsurf, (0, 0))
            for l in layersurfs:
                screensurf.blit(l, (0, 0))
            game = pygame.image.tostring(screensurf, "RGBA")
            game = pygame.image.fromstring(game, (mapwidth * tilesizex, mapheight * tilesizey), "RGBA")
        while menu:
            mx, my = pygame.mouse.get_pos()
            display.fill(gray)
            pygame.draw.rect(display, white, (15, 15, vmapwidth * tilesizex - 30, vmapheight * tilesizey - 30))
            pygame.draw.rect(display, black, (30, vmapheight * tilesizey - 130, vmapwidth * tilesizex - 60, 100))
            display.blit(pygame.transform.scale(pygame.image.load(covers[music]).convert(), (96, 96)),
                         (32, vmapheight * tilesizey - 128))
            track = gamefontl.render(musicplaying + tracks[music], True, white)
            album = gamefontl.render(musicalbum + albums[music], True, white)
            author = gamefontl.render(musicauthor + authors[music], True, white)
            playtime = gamefontl.render(
               musictime + str(math.floor(pygame.mixer.music.get_pos() / 1000 / 60)) + ":" + str(
                    math.floor(pygame.mixer.music.get_pos() / 1000)), True, white)
            volume = gamefontl.render(musicvolume + str(math.floor(pygame.mixer.music.get_volume() * 100)) + "%", True,
                                      white)
            display.blit(track, (130, vmapheight * tilesizey - 128))
            display.blit(album, (134, vmapheight * tilesizey - 110))
            display.blit(author, (138, vmapheight * tilesizey - 92))
            display.blit(playtime, (142, vmapheight * tilesizey - 76))
            display.blit(volume, (146, vmapheight * tilesizey - 58))
            display.blit(pygame.image.load("graphics/temp/music/minus.png").convert_alpha(), (269, vmapheight * tilesizey - 56))
            display.blit(pygame.image.load("graphics/temp/music/plus.png").convert_alpha(), (289, vmapheight * tilesizey - 56))
            display.blit(pygame.image.load("graphics/temp/music/prev.png").convert_alpha(), (560, vmapheight * tilesizey - 98))
            display.blit(pygame.image.load("graphics/temp/music/pause.png").convert_alpha(), (600, vmapheight * tilesizey - 98))
            display.blit(pygame.image.load("graphics/temp/music/play.png").convert_alpha(), (640, vmapheight * tilesizey - 98))
            display.blit(pygame.image.load("graphics/temp/music/skip.png").convert_alpha(), (680, vmapheight * tilesizey - 98))
            pygame.draw.rect(display, savecol, ((vmapwidth * tilesizex) / 2 + 5, 285, 200, 40))
            display.blit(magicbody.render(menusave, True, white), ((vmapwidth * tilesizex) / 2 + 15, 287))
            pygame.draw.rect(display, sharecol, ((vmapwidth * tilesizex) / 2 - 205, 285, 200, 40))
            display.blit(magicbody.render(menushare, True, white), ((vmapwidth * tilesizex) / 2 - 190, 287))
            pygame.draw.rect(display, screencol, ((vmapwidth * tilesizex) / 2 + 5, 330, 200, 40))
            display.blit(magicbody.render(menuscreenshot, True, white), ((vmapwidth * tilesizex) / 2 + 15, 332))
            pygame.draw.rect(display, dlcol, ((vmapwidth * tilesizex) / 2 - 205, 330, 200, 40))
            display.blit(magicbody.render(menudownload, True, white), ((vmapwidth * tilesizex) / 2 - 190, 332))
            pygame.draw.rect(display, credcol, ((vmapwidth * tilesizex) / 2 + 5, 375, 200, 40))
            display.blit(magicbody.render(menucredits, True, white), ((vmapwidth * tilesizex) / 2 + 15, 377))
            pygame.draw.rect(display, impcol, ((vmapwidth * tilesizex) / 2 - 205, 375, 200, 40))
            display.blit(magicbody.render(menuimport, True, white), ((vmapwidth * tilesizex) / 2 - 200, 377))
            pygame.draw.rect(display, irccol, ((vmapwidth * tilesizex) / 2 + 5, 420, 200, 40))
            display.blit(magicbody.render(menuirc, True, white), ((vmapwidth * tilesizex) / 2 + 15, 422))
            pygame.draw.rect(display, quitcol, ((vmapwidth * tilesizex) / 2 - 205, 420, 200, 40))
            display.blit(magicbody.render(menuquit, True, white), ((vmapwidth * tilesizex) / 2 - 190, 422))
            display.blit(pygame.image.load("graphics/temp/misc/logo2016.png"), ((vmapwidth * tilesizex - 30) / 2 - 360, 60))
            display.blit(gamefont.render(versiontag + version, True, blue), (15, (vmapheight * tilesizey) - 27))
            for event in pygame.event.get():
                if event.type == SECONDCOUNTDOWN:
                    boost -= 1
                elif event.type == USEREVENT:
                    initMusic()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu = False
                elif event.type == QUIT:
                    if chat:
                        irc.send(bytes("QUIT :Client exited.\n", "utf-8"))
                        irc.close()
                    if easygui.ynbox(savequery):
                        logger.info("Saving game...")
                        data.realm = realm
                        data.map[realm] = tilemap
                        data.inventory = inventory
                        data.coins = coins
                        data.store()
                        logger.info("Game saved.")
                    pygame.quit()
                    try:
                        logger.info("Removing previous temporary music files...")
                        for the_file in os.listdir("music/temp/"):
                            file_path = os.path.join("music", "temp", the_file)
                            try:
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                logger.error(e)
                        os.rmdir("music/temp/")
                    except Exception as e:
                        logger.error(e)
                    try:
                        logger.info("Removing previous temporary texture files...")
                        for the_file in os.listdir("graphics/temp/"):
                            file_path = os.path.join("graphics", "temp", the_file)
                            try:
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                logger.error(e)
                        os.rmdir("graphics/temp/")
                    except Exception as e:
                        logger.error(e)
                    sys.exit("User has quit the application.")
                elif event.type == MOUSEMOTION:
                    if ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    285 <= my <= 325):
                        savecol = green
                    else:
                        savecol = black
                    if ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    285 <= my <= 325):
                        sharecol = green
                    else:
                        sharecol = black
                    if ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    330 <= my <= 370):
                        screencol = green
                    else:
                        screencol = black
                    if ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    330 <= my <= 370):
                        dlcol = green
                    else:
                        dlcol = black
                    if ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    375 <= my <= 415):
                        credcol = green
                    else:
                        credcol = black
                    if ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    375 <= my <= 415):
                        impcol = green
                    else:
                        impcol = black
                    if ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    420 <= my <= 460):
                        irccol = green
                    else:
                        irccol = black
                    if ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    420 <= my <= 460):
                        quitcol = red
                    else:
                        quitcol = black
                elif event.type == MOUSEBUTTONDOWN:
                    if ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    285 <= my <= 325):
                        logger.info("Saving game...")
                        data.realm = realm
                        data.map[realm] = tilemap
                        data.inventory = inventory
                        data.coins = coins
                        data.store()
                        logger.info("Game saved.")
                        easygui.msgbox(savean, saveanhead)
                    elif ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    285 <= my <= 325):
                        f = open("tempmap.txt", "a")
                        # loop through each layer
                        for layer in range(mapz):  # changedz
                            # loop through each row
                            for row in range(mapheight):
                                # loop through each column in the row
                                for column in range(mapwidth):
                                    f.write(str(tilemap[layer][row][column])+"|")
                        f.close()
                        file = "tempmap"
                        pygame.image.save(game, file + ".png")
                        ftp = ftplib.FTP("ftp.scratso.com", "prmaps@scratso.com", "prshare")
                        mapsock = urllib.request.urlopen("http://scratso.com/pythianrealms/mapgen.php")
                        mapnum = str(mapsock.read()).split("'")[1]
                        mapsock.close()
                        f = open("tempmap.txt", "rb")
                        ftp.storbinary("STOR "+mapnum+".prm", f)
                        f.close()
                        f = open("tempmap.png", "rb")
                        ftp.storbinary("STOR "+mapnum+".png", f)
                        f.close()
                        os.remove("tempmap.txt")
                        os.remove("tempmap.png")
                        easygui.msgbox("Uploaded map to http://scratso.com/datastore/pythianrealms/\
                                           maps#"+mapnum)
                        logger.info("Uploaded map to http://scratso.com/datastore/pythianrealms/\
                                           maps#"+mapnum)
                    elif vmapheight * tilesizey - 56 <= my <= vmapheight * tilesizey - 38:
                        if 269 <= mx <= 287:
                            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
                        elif 289 <= mx <= 307:
                            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
                    elif vmapheight * tilesizey - 98 <= my <= vmapheight * tilesizey - 64:
                        if 560 <= mx <= 594:
                            if music != 1:
                                music -= 2
                                initMusic()
                        elif 600 <= mx <= 634:
                            pygame.mixer.music.pause()
                        elif 640 <= mx <= 674:
                            pygame.mixer.music.unpause()
                        elif 680 <= mx <= 714:
                            initMusic()
                    elif ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    330 <= my <= 370):
                        file = easygui.filesavebox(filetypes=["*.png"])
                        time.sleep(10)
                        pygame.image.save(game, file)
                        easygui.msgbox(screenshotsaved + file)
                        logger.info("Saved screenshot.")
                    elif ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    330 <= my <= 370):
                        webbrowser.open("http://www.scratso.com/datastore/pythianrealms/maps")
                    elif ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    375 <= my <= 415):
                        f = open("Docs/CREDITS.md", "r")
                        r = f.readlines()
                        f.close()
                        # noinspection PyTypeChecker
                        easygui.textbox(credstextnote, credstexty, r)
                    elif ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    375 <= my <= 415):
                        if easygui.ynbox("Importing a map will replace your current map. Are you sure?", "Warning"):
                            file = easygui.fileopenbox(filetypes=["*.prm"])
                            time.sleep(10)
                            change = True
                            read = open(file, 'r')
                            read2 = read.read()
                            read3 = read2.split("|")
                            file = 0
                            for ly in range(mapz):
                                for rw in range(mapheight):
                                    for cl in range(mapwidth):
                                        read4 = int(read3[file])
                                        tilemap[ly][rw][cl] = read4
                                        file = file + 1
                            read.close()
                    elif ((vmapwidth * tilesizex) / 2 + 5 <= mx <= (vmapwidth * tilesizex) / 2 + 205) and (
                                    420 <= my <= 460):
                        # Open Multiplayer Chat System
                        webbrowser.open("https://irc.editingarchive.com:8080/?channels=PlatSwag")
                        logger.info("IRC Opened.")
                    elif ((vmapwidth * tilesizex) / 2 - 205 <= mx <= (vmapwidth * tilesizex) / 2 - 5) and (
                                    420 <= my <= 460):
                        if chat:
                            irc.send(bytes("QUIT :Client exited.\n", "utf-8"))
                            irc.close()
                        if easygui.ynbox(savequery):
                            logger.info("Saving game...")
                            data.realm = realm
                            data.map[realm] = tilemap
                            data.inventory = inventory
                            data.coins = coins
                            data.store()
                            logger.info("Game saved.")
                        pygame.quit()
                        try:
                            logger.info("Removing previous temporary music files...")
                            for the_file in os.listdir("music/temp/"):
                                file_path = os.path.join("music", "temp", the_file)
                                try:
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    logger.error(e)
                            os.rmdir("music/temp/")
                        except Exception as e:
                            logger.error(e)
                        try:
                            logger.info("Removing previous temporary texture files...")
                            for the_file in os.listdir("graphics/temp/"):
                                file_path = os.path.join("graphics", "temp", the_file)
                                try:
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    logger.error(e)
                            os.rmdir("graphics/temp/")
                        except Exception as e:
                            logger.error(e)
                        sys.exit("User has quit the application.")

                        #            for line in message:
                        #                text = gamefont.render(line, True, white)
                        #                display.blit(text, (17,17+textoffset))
                        #                textoffset += 12
            pygame.display.update()

        if chat:
            pygame.draw.rect(display, black, (0, vmapheight * tilesizey, vmapwidth * tilesizex, 50))
            pygame.draw.rect(display, white, (0, vmapheight * tilesizey + 38, vmapwidth * tilesizex, 12))
            display.blit(chatmsg, (2, vmapheight * tilesizey + 38))
            display.blit(gamefont.render(messages[-3], True, white), (0, vmapheight * tilesizey))
            display.blit(gamefont.render(messages[-2], True, white), (0, vmapheight * tilesizey + 12))
            display.blit(gamefont.render(messages[-1], True, white), (0, vmapheight * tilesizey + 24))
        else:
            pygame.draw.rect(display, black, (0, vmapheight * tilesizey, vmapwidth * tilesizex, 38))
            display.blit(gamefont.render(messages[-3], True, white), (0, vmapheight * tilesizey))
            display.blit(gamefont.render(messages[-2], True, white), (0, vmapheight * tilesizey + 12))
            display.blit(gamefont.render(messages[-1], True, white), (0, vmapheight * tilesizey + 24))

        pygame.display.update((0, 0, vmapwidth * tilesizex, vmapheight * tilesizey + 50))

        elapsed = time.time() - now
        try:
            fps = round(1 / elapsed)
        except:
            pass

except Exception as e:
    if type(e) is IOError:
        print("This issue may be a permissions problem. Running " + gameName + """ as an administrator should fix the problem. You could force
it to run in admin mode by using the following steps:
1. Right click the application (shortcut).
2. Click "Properties".
3. Go to the "Compatibility" tab.
4. Check "Run this program as an administrator, in the settings section.
5. Press OK.

""")
    try:
        logger.error(str(e) + "\n" + traceback.format_exc())
        err(str(e), traceback.format_exc())
    except:
        try:
            logger.error(str(e) + "\n" + traceback.format_exc())
            while True:
                time.sleep(1)
        except:
            print(str(e) + "\n" + traceback.format_exc())
            while True:
                time.sleep(1)
            # easygui.exceptionbox("""Oops! Something went wrong. But don't worry! Because I'm so amazingly kind,
            # you need only send me this error report below and I'll get right on it.""", "An Error Ocurred!")

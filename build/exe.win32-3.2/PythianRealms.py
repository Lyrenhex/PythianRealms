# -*- coding: utf-8 -*-

# Copyright (c) 2015 Damian Heaton and TechnoMagic Enterprises. ALL RIGHTS RESERVED.

version = "0.0.0.5"

import sys, os, time, random, math, traceback, webbrowser, datetime as dt

# Error Reporting note: %0D%0A is the Newline Character for the Mailto: command. Since the Error Reporter uses Mailto:,
# use %0D%0A instead of \n.

# Encompass the entire program in a try statement for the error reporter.
try:

    #######################
    # SET UP POUP WINDOWS #
    #######################

    import easygui  # I really feel sorry for Linux users. So many depndencies :'(
    def msgbox(title, text):
        #ctypes.windll.user32.MessageBoxA(None, str(text), str(title), 0)
        easygui.msgbox(text, title) 
    #msgbox('Your title', 'Your text', 1)

    class Settings(easygui.EgStore): # Create a class named Settings inheriting from easygui.EgStore so that I can persist TechnoMagic Account info.
        def __init__(self, filename):  # filename is required
            #-------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            #-------------------------------------------------
            self.username = None
            self.password = None
            self.storyintro = False
            self.realm = 0

            #-------------------------------------------------
            # For subclasses of EgStore, these must be
            # the last two statements in  __init__
            #-------------------------------------------------
            self.filename = filename  # this is required
            self.restore()            # restore values from the storage file if possible
    
    #########################
    # Initialise the logger #
    #########################
    import logging
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

    ######################
    # CHECK FOR INTERNET #
    ######################

    import urllib.request as urllib2
    try:
        response=urllib2.urlopen('http://92.234.196.233',timeout=10)
        online = True
    except:
        online = False
        pass
    logger.info("Can we connect to the server? "+str(online))
    if not online:
        logger.warn("Cannot connect to the Auth Server! Any online data will not be available and any purchased items will also not be available!")
        msgbox("Warning!", "PythianRealms cannot connect to the Auth Server! Any data saved online will not be available until PythianRealms can connect to the authorisation server. After a connection is available, please restart PythianRealms to reconnect. PythianRealms will run in Offline Mode.")

    #######################
    # INITIALIZE SETTINGS #
    #######################

    settingsFile = "data\Settings.txt"
    settings = Settings(settingsFile)

    #print(settings.username)

    if settings.username == None:
        username = None
        password = None
        settings.username = username
        settings.password = password
        settings.store()    # persist the settings

        # run code that gets a new value for userId, and persist the settings
        username = None
        settings.username = username
        settings.store()

    #######################
    # CONNECT TO DATABASE #
    #######################

    if online:
        if settings.username == None:
            if easygui.ynbox("Do you have a TechnoMagic Account? (An account at http://www.tmcore.co.uk)", "Login"):
                username = easygui.enterbox("TechnoMagic Account Username", "Login")
                password = easygui.passwordbox("TechnoMagic Account Password", "Login")
                try:
                    import mysql.connector as dbc
                    db = dbc.connect(user='PYTH_'+username, password=password,
                                                                  host='92.234.196.233',
                                                                  database='tchnm_15865510_acc')
                    db.autocommit = True
                    dba = db.cursor()
                    query = ("SELECT * FROM `PYTH_"+username+"`")
                    dba.execute(query)
                    dbd = []
                    for columns in dba:
                        for column in columns:
                            dbd.append(column)
                    logger.info("Authorisation Server returned: "+str(dbd))
##                    if dbd[3] != password:
##                        msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: Wrong password.")
##                        online = False
##                        username = "Offline User"
                    settings.username = username
                    settings.password = password
                    settings.store()
                    logger.info("Successfully logged in to account!")
                except Exception as e:
                    msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: %s" % e)
                    online = False
                    username = "Offline User"
            else:
                webbrowser.open("http://www.tmcore.co.uk/accounts/register.php")
                username = easygui.enterbox("TechnoMagic Account Username", "Login")
        else:
            username = settings.username
            password = settings.password
            try:
                import mysql.connector as dbc
                db = dbc.connect(user='PYTH_'+username, password=password,
                                                              host='92.234.196.233',
                                                              database='tchnm_15865510_acc')
                db.autocommit = True
                dba = db.cursor()
                query = ("SELECT * FROM `PYTH_"+username+"`")
                dba.execute(query)
                dbd = []
                for columns in dba:
                    for column in columns:
                        dbd.append(column)
                logger.info("Authorisation Server returned: "+str(dbd))
##                    if dbd[3] != password:
##                        msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: Wrong password.")
##                        online = False
##                        username = "Offline User"
                logger.info("Successfully logged in to account!")
            except Exception as e:
                msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: %s" % e)
                online = False
                username = "Offline User"
    else:
        username = "Offline User"

    if online:
        logintime = dt.datetime.now().strftime("%I:%M %p on %B %d, %Y")
        logger.info ("Logged in on "+str(logintime))

    if online:
        if dbd[2] == 1:
            premium = True
        else:
            premium = False
    else:
        premium = False

    logger.info("Is the user a PREMIUM player? "+str(premium))

    #####################
    # OPERATING SYSTEMS #
    #####################

    useros = sys.platform
    logger.info("Operating System Environment: "+useros+".")
    if useros == "linux" or useros == "linux2" or useros == "linux3" or useros == "linux4":
        useros = "linux"
        logger.error("""*** Please note that PythianRealms may be very buggy on Linux as it is not natively programmed in it. Please report any bugs you find. Thanks. :) ***""")

    #####################
    # VARIABLE DECLARES #
    #####################

    tilesizex = 32
    tilesizey = 32
    mapwidth = 100
    mapheight = 100
    mapz = 4

    realms = 2
    realm = settings.realm

    playerz = 0

    oldtiles = []

    zaxis = 0
    place = False
    pickup = False
    changedz = []

    change = False
    debug = False

    invshow = False
    shopshow = False

    activeoverlay = True

    coins = 1000 # 1000 coins to start, and per boost

    if online:
        coins = dbd[1]
    elif os.path.isfile("data/Coins.txt") and os.access("data/Coins.txt", os.R_OK):
        read = open("data/Coins.txt", "r")
        coins = int(read.read())
        read.close()

    # visible map sizes. There is always hidden map.
    vmapwidth = round(75/(tilesizex/16))
    vmapheight = round(40/(tilesizey/16))

    #################
    # SET UP PYGAME #
    #################

    import pygame
    from pygame.locals import *

    try:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    except Exception as e:
        logger.error("Unable to auto-center PythianRealms Window. Error: %s" % e)

    # colours
    black = (0,0,0)
    brown = (139,69,19)
    green = (0,255,0)
    blue = (0,0,255)
    red = (255,0,0)
    gray = (80,80,80)
    white = (255,255,255)
    yellow = (255,255,0)

    # set up the displays
    pygame.init()
    display = pygame.display.set_mode((vmapwidth*tilesizex, vmapheight*tilesizey), HWSURFACE|DOUBLEBUF) #|RESIZABLE later
    mapsurf = pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey))
    mapsurf.fill(brown)
    prevsurf = pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    npcsurf = pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey), pygame.SRCALPHA, 32).convert_alpha()
    activesurf = pygame.Surface((tilesizex+10, tilesizey+27), pygame.SRCALPHA, 32).convert_alpha()
    activesurf.fill((23, 100, 255, 50))
    activeblock = pygame.Surface((tilesizex, tilesizey))
    invsurf = pygame.Surface((310, 310), pygame.SRCALPHA, 32).convert_alpha()
    invsurf.fill((23, 100, 255, 50))
    shopsurf = pygame.Surface((310, 310), pygame.SRCALPHA, 32).convert_alpha()
    shopsurf.fill((23, 100, 255, 50))

    layersurfs = []
    for layer in range(mapz):
        layersurfs.append(pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey), pygame.SRCALPHA, 32).convert_alpha())

    # fonts
    gamefont = pygame.font.Font("graphics/gameFont.ttf", 12)

    activetxt = gamefont.render("Active", True, white)
    activesurf.blit(activetxt, (5,5))

    # set up loading screen
    display.fill(white)
    loadtext = gamefont.render("Loading PythianRealms...", True, black)
    display.blit(loadtext, (0,vmapheight*tilesizey-12))
    display.blit(pygame.image.load("graphics/logo.png"), (vmapwidth*tilesizex/2-360,0))
    pygame.display.update()

    # set the window title
    if premium:
        premtext = "PREMIUM ACCOUNT"
    else:
        premtext = "STANDARD ACCOUNT"
    pygame.display.set_caption("PythianRealms Game | Version "+version+" | Online: "+str(online)+" | "+premtext) # , "graphics/logo-small.png"
    # set the window icon
    pygame.display.set_icon(pygame.image.load("graphics/logo-small.png").convert_alpha())

    # load the player sprite
    player = pygame.transform.scale(pygame.image.load("graphics/"+str(premium)+"/player_right.png").convert_alpha(), (tilesizex,tilesizey))

    # load the hp bar
    hpbar = pygame.image.load("graphics/blood_red_bar.png")

    # Constants for the resources
    DIRT  = 0
    GRASS = 1
    WATER = 2
    COAL  = 3
    LAVA  = 4
    ROCK  = 5
    DIAM  = 6
    SAPP  = 7
    RUBY  = 8
    GOLD  = 9
    AIR   = 10
    WOOD  = 11
    GLASS = 12
    BRICK = 13
    CARP  = 14
    SNOW  = 15
    SEL   = 16
    GSWORD= 17
    FPORT = 18
    BPORT = 19
    ORB   = 20

    active = DIRT

    sel = ((vmapwidth*tilesizex)/2-155+10,(vmapheight*tilesizey)/2-155+20)
    sel2 = ((vmapwidth*tilesizex)/2-155+10,(vmapheight*tilesizey)/2-155+120)

    seamless = False

    #a list of resources
    resources = [DIRT,GRASS,WATER,COAL,LAVA,ROCK,DIAM,SAPP,RUBY,GOLD,CARP,SNOW,WOOD,GLASS,BRICK,GSWORD,ORB]

    # set the inventory
    inventory =   {
                            DIRT   : 0,
                            GRASS  : 0,
                            WATER  : 0,
                            COAL   : 0,
                            LAVA   : 0,
                            ROCK   : 0,
                            DIAM   : 0,
                            SAPP   : 0,
                            RUBY   : 0,
                            GOLD   : 0,
                            CARP   : 0,
                            SNOW   : 0,
                            WOOD   : 0,
                            GLASS  : 0,
                            BRICK  : 0,
                            GSWORD : 0,
                            ORB    : 0,
                            FPORT  : 1,
                            BPORT  : 1,
                        }

    if online:
        inventory[DIRT] = dbd[3]
        inventory[GRASS] = dbd[4]
        inventory[WATER] = dbd[5]
        inventory[COAL] = dbd[6]
        inventory[LAVA] = dbd[7]
        inventory[ROCK] = dbd[8]
        inventory[DIAM] = dbd[9]
        inventory[SAPP] = dbd[10]
        inventory[RUBY] = dbd[11]
        inventory[GOLD] = dbd[12]
        inventory[CARP] = dbd[13]
        inventory[SNOW] = dbd[14]
        inventory[WOOD] = dbd[15]
        inventory[GLASS] = dbd[16]
        inventory[BRICK] = dbd[17]
        inventory[GSWORD] = dbd[18]
        inventory[ORB] = dbd[19]
    elif os.path.isfile("data/Inventory.txt") and os.access("data/Inventory.txt", os.R_OK):
        file = 0
        read = open("data/Inventory.txt", 'r')
        read2 = read.read()
        read3 = read2.split("\n")
        for item in inventory:
            inventory[item] = int(read3[file])
            file = file + 1
        read.close()

    ########
    # NPCS #
    ########

    # 0 = Mr. Smiler, 1 = Werewolf, 2 = Sssnake, 3 = Void Chunk A, 4 = (Custom) Tudor, 5 = Old Man, 6 = Jared's Wife, 7 = Calem, 8 = Bjorvik, 9 = Stephan,
    # 10 = King Rhask, 11  = Rakjoke, 12 = Rakjoke's Friend, 13 = Homeless Man, 14 = Stranger, 15 = Blood Hound, 16 = (Custom) Amnesiac
    NPCs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    npcDrop = {
                    0 : 0,
                    1 : 2,
                    2 : 0,
                    3 : 4,
                    4 : 0,
                    5 : 0,
                    6 : 0,
                    7 : 0,
                    8 : 0,
                    9 : 0,
                    10: 0,
                    11: 0,
                    12: 0,
                    13: 0,
                    14: 0,
                    15: 3,
                    16: 1,
                }
    # NPC ID : { CHUNK : [LIST OF NPC NUMBERS IN CHUNK] },
    NPCcount = {
                0 : [0] ,
                1 : [0,1,2,3,4,5],
                2 : [0] ,
                3 : [0],
                4 : [0],
                5 : [0],
                6 : [0],
                7 : [0],
                8 : [0] ,
                9 : [0],
                10: [0] ,
                11: [0] ,
                12: [0] ,
                13: [0] ,
                14: [0] ,
                15: [0,1] ,
                16: [0] ,
               }
    NPCrealm = {
                0 : 0,
                1 : 0,
                2 : 1,
                3 : 0,
                4 : 0,
                5 : 0,
                6 : 0,
                7 : 0,
                8 : 0,
                9 : 0,
                10: 0,
                11: 0,
                12: 0,
                13: 0,
                14: 0,
                15: 0,
                16: 0,
               }
    NPCtype = {
                0 : "Friendly",
                1 : "Hostile",
                2 : "Hostile",
                3 : "Hostile",
                4 : "Friendly",
                5 : "Friendly",
                6 : "Friendly",
                7 : "Friendly",
                8 : "Friendly",
                9 : "Friendly",
                10: "Friendly",
                11: "Friendly",
                12: "Friendly",
                13: "Friendly",
                14: "Friendly",
                15: "Hostile",
                16: "Hostile",
              }
    NPCdamage = {
                    0 : 0,
                    1 : 4,
                    2 : 20,
                    3 : 20,
                    4 : 0,
                    5 : 0,
                    6 : 0,
                    7 : 0,
                    8 : 0,
                    9 : 0,
                    10: 0,
                    11: 0,
                    12: 0,
                    13: 0,
                    14: 0,
                    15: 15,
                    16: 8,
                }
    #NPC ID : {  NPC NUMBER : NPC NUMBER HP  }
    NPChealth = {
                    0 : { 0 : 1 },
                    1 : { 0 : 8,
                          1 : 8,
                          2 : 8,
                          3 : 8,
                          4 : 8,
                          5 : 8 },
                    2 : { 0 : 190 },
                    3 : { 0 : 16 },
                    4 : { 0 : 1 },
                    5 : { 0 : 1 },
                    6 : { 0 : 1 },
                    7 : { 0 : 1 },
                    8 : { 0 : 1 },
                    9 : { 0 : 1 },
                    10: { 0 : 1 },
                    11: { 0 : 1 },
                    12: { 0 : 1 },
                    13: { 0 : 1 },
                    14: { 0 : 1 },
                    15: { 0 : 10,
                          1 : 10 },
                    16: { 0 : 16 },
                }
    #for npc in NPCs:
    #    for chunk in range(25):
    #        if chunk in NPChealth[npc]:
    #            for curnpc in NPChealth[npc]:
    #                if os.path.isfile("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt") and os.access("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", os.R_OK):
    #                    file = open("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", "r")
    #                    integer = int(file.read())
    #                    NPChealth[npc][curnpc] = integer
    #                    file.close()
    NPCmaxHealth = {
        0 : 1,
        1 : 8,
        2 : 190,
        3 : 16,
        4 : 1,
        5 : 1,
        6 : 1,
        7 : 1,
        8 : 1,
        9 : 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 10,
        16: 16,
        }
                #NPC ID : { NPC NUMBER : NPC NUMBER pos },
    npcPosX = {
                0 : { 0 : 5 },
                1 : { 0 : random.randint(0,mapwidth-1),
                            1 : random.randint(0,mapwidth-1),
                            2 : random.randint(0,mapwidth-1),
                            3 : random.randint(0,mapwidth-1),
                            4 : random.randint(0,mapwidth-1),
                            5 : random.randint(0,mapwidth-1) },
                2 : { 0 : random.randint(0,mapwidth-1) },
                3 : { 0 : random.randint(0,mapwidth-1) },
                4 : { 0 : random.randint(0,mapwidth-1) },
                5 : { 0 : random.randint(0,mapwidth-1) },
                6 : { 0 : random.randint(0,mapwidth-1) },
                7 : { 0 : random.randint(0,mapwidth-1) },
                8 : { 0 : random.randint(0,mapwidth-1) },
                9 : { 0 : random.randint(0,mapwidth-1) },
                10: { 0 : random.randint(0,mapwidth-1) },
                11: { 0 : random.randint(0,mapwidth-1) },
                12: { 0 : random.randint(0,mapwidth-1) },
                13: { 0 : random.randint(0,mapwidth-1) },
                14: { 0 : random.randint(0,mapwidth-1) },
                15: { 0 : random.randint(0,mapwidth-1),
                            1 : random.randint(0,mapwidth-1) },
                16: { 0 : random.randint(0,mapwidth-1) },
              }
    npcPosY = {
                0 : { 0 : 5 },
                1 : { 0 : random.randint(0,mapheight-1),
                            1 : random.randint(0,mapheight-1),
                            2 : random.randint(0,mapheight-1),
                            3 : random.randint(0,mapheight-1),
                            4 : random.randint(0,mapheight-1),
                            5 : random.randint(0,mapheight-1) },
                2 : { 0 : random.randint(0,mapheight-1) },
                3 : { 0 : random.randint(0,mapheight-1) },
                4 : { 0 : random.randint(0,mapheight-1) },
                5 : { 0 : random.randint(0,mapheight-1) },
                6 : { 0 : random.randint(0,mapheight-1) },
                7 : { 0 : random.randint(0,mapheight-1) },
                8 : { 0 : random.randint(0,mapheight-1) },
                9 : { 0 : random.randint(0,mapheight-1) },
                10: { 0 : random.randint(0,mapheight-1) },
                11: { 0 : random.randint(0,mapheight-1) },
                12: { 0 : random.randint(0,mapheight-1) },
                13: { 0 : random.randint(0,mapheight-1) },
                14: { 0 : random.randint(0,mapheight-1) },
                15: { 0 : random.randint(0,mapheight-1),
                            1 : random.randint(0,mapheight-1) },
                16: { 0 : random.randint(0,mapheight-1) },
              }
    npcPosZ = {
                0 : 1,
                1 : 1,
                2 : 1,
                3 : 1,
                4 : 1,
                5 : 1,
                6 : 1,
                7 : 1,
                8 : 1,
                9 : 1,
                10: 1,
                11: 1,
                12: 1,
                13: 1,
                14: 1,
                15: 1,
                16: 1,
              }
    npcGraphic = {
        0 : pygame.image.load('graphics/smiler.png'), # I DON'T KNOW why I need to convert alpha; PyGame simply REFUSED to work otherwise. SOMEONE TELL ME!
        1 : pygame.image.load('graphics/smiler.png'),
        2 : pygame.image.load('graphics/smiler.png'),
        3 : pygame.image.load('graphics/void1.png'),
        4 : pygame.image.load('graphics/smiler.png'),
        5 : pygame.image.load('graphics/smiler.png'),
        6 : pygame.image.load('graphics/smiler.png'),
        7 : pygame.image.load('graphics/smiler.png'),
        8 : pygame.image.load('graphics/smiler.png'),
        9 : pygame.image.load('graphics/smiler.png'),
        10: pygame.image.load('graphics/smiler.png'),
        11: pygame.image.load('graphics/smiler.png'),
        12: pygame.image.load('graphics/smiler.png'),
        13: pygame.image.load('graphics/smiler.png'),
        14: pygame.image.load('graphics/smiler.png'),
        15: pygame.image.load('graphics/smiler.png'),
        16: pygame.image.load('graphics/smiler.png'),
    }
    global npcName
    npcName = {
        0 : "Mr. Smiler",
        1 : "Werewolf",
        2 : "Ssssnake",
        3 : "Void Chunk A",
        4 : "Tudor",
        5 : "Old Man",
        6 : "Jared's Wife",
        7 : "Calem",
        8 : "Bjorvik",
        9 : "Stephan",
        10: "King Rhask",
        11: "Rakjoke",
        12: "Rakjoke's F.",
        13: "Homeless Man",
        14: "Stranger",
        15: "Blood Hound",
        16: "(C) Amnesiac",
        }

    ## Is the user 13 or older?
    #if easygui.ynbox("PythianRealms has an online chat system. However, if you are below the age of 13, you must have parental consent to use such services. Are you over the age of 13 or have parental consent?", "Multiplayer Chat?"):
    #    # Open Multiplayer Chat System
    #    webbrowser.open("https://irc.editingarchive.com:8080/?channels=PythianRealms")

    #webbrowser.open("http://tmcore.co.uk:9090/?channels=PythianRealms")

    #use list comprehension to create the tilemap
    tilemap = [ [[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz) ]

    mapload = False

    if os.path.isfile("data/Map"+str(realm)+".txt") and os.access("data/Map"+str(realm)+".txt", os.R_OK):
        mapload = True
        file = 0
        read = open("data/Map"+str(realm)+".txt", 'r')
        read2 = read.read()
        read3 = read2.split("|")
        for ly in range(mapz):
            for rw in range(mapheight):
                for cl in range(mapwidth):
                    read4 = int(read3[file])
                    tilemap[ly][rw][cl] = read4
                    file = file + 1
        read.close()

    # set the map's x and y offsets (positioning)
    xoffset,yoffset = 0,0

    #a dictionary linking resources to textures
    textures =   {
                    DIRT  : pygame.transform.scale(pygame.image.load('graphics/dirt.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GRASS : pygame.transform.scale(pygame.image.load('graphics/grass.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    WATER : pygame.transform.scale(pygame.image.load('graphics/water.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    COAL  : pygame.transform.scale(pygame.image.load('graphics/coal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    LAVA  : pygame.transform.scale(pygame.image.load('graphics/lava.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    ROCK  : pygame.transform.scale(pygame.image.load('graphics/rock.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    DIAM  : pygame.transform.scale(pygame.image.load('graphics/diamond.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    SAPP  : pygame.transform.scale(pygame.image.load('graphics/sapphire.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    RUBY  : pygame.transform.scale(pygame.image.load('graphics/ruby.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GOLD  : pygame.transform.scale(pygame.image.load('graphics/gold.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    AIR   : pygame.transform.scale(pygame.image.load('graphics/air.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    WOOD  : pygame.transform.scale(pygame.image.load('graphics/wood.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GLASS : pygame.transform.scale(pygame.image.load('graphics/glass.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    BRICK : pygame.transform.scale(pygame.image.load('graphics/brick.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    CARP  : pygame.transform.scale(pygame.image.load('graphics/carpet/mid.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    SNOW  : pygame.transform.scale(pygame.image.load('graphics/snow.jpg'), (tilesizex,tilesizey+round(tilesizey/2))), # NTS: Limited edition Item! To be removed on New Year's Day.
                    SEL   : pygame.transform.scale(pygame.image.load('graphics/sel.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GSWORD: pygame.transform.scale(pygame.image.load('graphics/gsword.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    FPORT : pygame.transform.scale(pygame.image.load('graphics/forportal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    BPORT : pygame.transform.scale(pygame.image.load('graphics/backportal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    ORB   : pygame.transform.scale(pygame.image.load('graphics/orb.png'), (tilesizex,tilesizey+round(tilesizey/2)))
                }

    elapsed = 0
    fps = 0
    cachedscreen = []

    def initMusic():
        global silence
        logger.info("Initializing Music...") # if this process fails and it starts in silent mode, you screwed something up... or you don't have speakers, ofc.
        music = random.randint(1,7)
        logger.info("Running music #"+str(music))
        pygame.mixer.music.set_endevent(USEREVENT)
        try:
            pygame.mixer.music.load('music/'+str(music)+'.mp3')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
        except Exception:
            try:
                pygame.mixer.music.load('music/'+str(music)+'.mid')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
            except Exception as e:
                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
                silence = True
##        if realm == 1:
##            try:
##                if OS == "windows":
##                    pygame.mixer.music.load('music/No-Survivors.mid')
##                    pygame.mixer.music.play(-1)
##                    silence = False
##                elif OS == "linux":
##                    print("Due to issues with MIDIs on Linux, trying alternative. *This may impact on game feel.*")
##                    pygame.mixer.music.load('music/Bustling-Ancient-City.mp3')
##                    pygame.mixer.music.play(-1)
##                    silence = False
##            except Exception as e:
##                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
##                silence = True
##        elif realm == 2:
##            try:
##                pygame.mixer.music.load('music/Running Freedom.mp3')
##                pygame.mixer.music.play(-1)
##                silence = False
##            except Exception as e:
##                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
##                silence = True
##        elif realm == 3:
##            try:
##                pygame.mixer.music.load('music/Bustling-Ancient-City.mp3')
##                pygame.mixer.music.play(-1)
##                silence = False
##            except Exception as e:
##                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
##                silence = True
##        elif realm == 4:
##            try:
##                pygame.mixer.music.load('music/Across-the-Moat.mp3')
##                pygame.mixer.music.play(-1)
##                silence = False
##            except Exception as e:
##                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
##                silence = True
##        elif realm == 5:
##            try:
##                pygame.mixer.music.load('music/History-Piano.mp3')
##                pygame.mixer.music.play(-1)
##                silence = False
##            except Exception as e:
##                logger.error("Music failed to Initialize. Game will run in silence instead. Error: %s" % e)
##                silence = True

    def msg(message = ["A message wasn't found! Tell Scratso!"]):
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
            pygame.draw.rect(display, blue, (15,15,vmapwidth*tilesizex-30,vmapheight*tilesizey-30))
            textoffset = 0
            for line in message:
                text = gamefont.render(line, True, white)
                display.blit(text, (17,17+textoffset))
                textoffset += 12
            pygame.display.update()

    # Display all the startup things.
    startupnotes = ["Welcome to PythianRealms!",
                     "You are running version "+version,
                     "This is a Public Alpha Development version of PythianRealms. All feedback is appreciated. Want to help give feedback? Simply email me at scratso@tmcore.co.uk!",
                     "PythianRealms cannot thrive without donations. Why not help us out by donating? You can donate over at http://www.tmcore.co.uk/PythianRealms.php",
                     "",
                     "Please make sure that you have fun, and spread the word!",
                     "",
                     "PROTIP: You can find a load of helpful guides by typing (without quotes) \"%APPDATA%\PythianRealms\\Game\\Docs\" into run (Windows key + R).",
                    "",
                    "",
                    "KEYBINDINGS:",
                    "============",
                    "Arrow Keys: Move",
                    "F3: Toggle debug information",
                    "Q: Enable Build Mode",
                    "A: Disable Build Mode",
                    "R: Enable Pickup Mode",
                    "F: Disable Pickup Mode",
                    "T: Toggle RPG/Construction Realm",
                    "C: Open PythianRealms IRC Chat"]
    if online:
        startupnotes[0] = "Hey, "+str(username)+", welcome back to PythianRealms! You last logged in at "+str(dbd[0])+"."
        if premium:
            startupnotes.append("")
            startupnotes.append("You are a premium PythianRealms Player.")
    msg(startupnotes)

##    poem2 = [
##        "\"Aha, you're new, so let's lay down the ground rules:",
##        "First we'll send you off to nurseries and schools,",
##        "Where we'll hijack your will and bring you to heel,",
##        "And if you resist we'll break you on the wheel.",
##        "Once we've purged your flaws, when heart and mind are clean,",
##        "We'll offer you up to the banking machine.",
##        "",
##        "Get out of your heart, and get into your head,",
##        "So you won't want to play, but solve problems instead.",
##        "You're way too soft and you need to be tougher,",
##        "Or the important ones will make you suffer.",
##        "It's not taking part, winning's all that matters.",
##        "Be ruthless and quick, leave the rest in tatters.",
##        "",
##        "Acknowledge that greed is good and might is right.",
##        "Discard compassion, it never wins the fight.",
##        "Despise weak people, they'll only drag you down,",
##        "And instead of Ray-Bans, you'll wear a frown.",
##        "So leave needy people on the bottom shelf,",
##        "And seek friends who can multiply your wealth.",
##        "",
##        "Ignore the guilty feelings that may arise,",
##        "Those are just echoes of weakness' demise.",
##        "So cheat, bend the rules, do whatever you must,",
##        "And don't be swayed by their envious disgust.",
##        "They're just jealous and wish they were like you,",
##        "Losers are too weak and do what they need to.",
##        "",
##        "You'll need to bend the truth, but never say you lied.",
##        "You deserve to win so all is justified.",
##        "In a perfect world that ran on peace and love,",
##        "You wouldn't even need any of the above.",
##        "Dishonesty would be a rare last resort,",
##        "But make no mistake son, this is bloodsport.",
##        "",
##        "(More on next page.)"
##        "Now we've purged your flaws, we'll send you on your way.",
##        "Use all you've learned here to win the games you play.",
##        "All will marvel at your great house, wife and car.",
##        "Likewise teach your kids, so they too can go far.",
##        "And at the final curtain, you can take heart,",
##        "That in our little play, you had a big part.",
##        "",
##        "...",
##        "",
##        "Aha you're new, and it says you have depression.",
##        "Christ - your life story reads like a confession!",
##        "Well, I don't need to be that well qualified,",
##        "To spot where the roots of your problems reside.",
##        "Tell me - how does one who started out just fine,",
##        "End up so comprehensively asinine?",
##        "",
##        "You need to abide by your heart, not by your head.",
##        "You ought to play more, and put mind games to bed.",
##        "You act way too tough, and need to soften up.",
##        "Good people have suffered to overfill your cup.",
##        "Winning is nothing, it's all in how you play,",
##        "When the game ends, and the board is put away.\"",
##        "",
##        "- A poem by Armanax, reflecting the greed and cruelty of the world we live. The greed and cruelty that this game also reflects."]
##    msg(poem2)
    
    changedz = [0,1,2,3] #0,1,2,3 after you add the loading system. Until then, this'll do.
    
    if settings.storyintro == False:
        # show the story intro (somehow make a video show here).
        settings.storyintro = True
        settings.store()

    oldNPCposX = None
    oldNPCposY = None

    initMusic()

    boost = 300 # 600 = 10 Minutes, 60 = 1 Minute, it's in seconds

    SECONDCOUNTDOWN = USEREVENT+1
    pygame.time.set_timer(SECONDCOUNTDOWN, 1000)

    NPCMOVE = USEREVENT+2
    pygame.time.set_timer(NPCMOVE, 2000)

    realm = settings.realm

    if mapload:
        change = True
    
    while True:
        # msg(["Test"])
        now = time.time()
        display.fill(black)
        shownz = [0,1,2,3]

        if boost == 0:
            if premium:
                coins += 1000
            else:
                coins += 100
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

        if place or change:
            prevsurf.fill(0)

        if change:
            changetext = gamefont.render("RENDERING ENGINE IS BUSY... PLEASE WAIT!", True, yellow, red)
            display.blit(changetext, (0,0))
            pygame.display.update()

        mx,my = pygame.mouse.get_pos()
        playerTile = (round(((vmapwidth*tilesizex/2-12)-xoffset)/tilesizex),round(((vmapheight*tilesizey/2-12)-yoffset)/tilesizey))
        
        #get all the user events - SO, SO, SO, SO SORRY ABOUT THE SAVING METHODS. PLEASE FORGIVE ME!
        keys = pygame.key.get_pressed()
        #if the right arrow is pressed
        if keys[pygame.K_RIGHT]: # and playerPos[0] < mapwidth - 1
            player = pygame.transform.scale(pygame.image.load("graphics/"+str(premium)+"/player_right.png").convert_alpha(), (tilesizex,tilesizey))
            if playerTile[0] != 99:
                try:
                    if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and tilemap[playerz+1][playerTile[1]][playerTile[0]] != AIR:
                        xoffset += tilesizex
                    else:
                        if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and playerz < 3: # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if tilemap[playerz-1][playerTile[1]][playerTile[0]] == AIR and playerz > 0: # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    xoffset -= 2
                except:
                    pass
        if keys[pygame.K_LEFT]:
            player = pygame.transform.scale(pygame.image.load("graphics/"+str(premium)+"/player_left.png").convert_alpha(), (tilesizex,tilesizey))
            if playerTile[0] != 0:
                try:
                    if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and tilemap[playerz+1][playerTile[1]][playerTile[0]] != AIR:
                        xoffset -= tilesizex
                    else:
                        if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and playerz < 3: # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if tilemap[playerz-1][playerTile[1]][playerTile[0]] == AIR and playerz > 0: # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    xoffset += 2
                except:
                    pass
        if keys[pygame.K_UP]:
            if playerTile[1] != 0:
                try:
                    if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and tilemap[playerz+1][playerTile[1]][playerTile[0]] != AIR:
                        yoffset -= tilesizey
                    else:
                        if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and playerz < 3: # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if tilemap[playerz-1][playerTile[1]][playerTile[0]] == AIR and playerz > 0: # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    yoffset += 2
                except:
                    pass
        if keys[pygame.K_DOWN]:
            if playerTile[1] != 99:
                try:
                    if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and tilemap[playerz+1][playerTile[1]][playerTile[0]] != AIR:
                        yoffset += tilesizey
                    else:
                        if tilemap[playerz][playerTile[1]][playerTile[0]] != AIR and playerz < 3: # tilemap[z][y][x]
                            playerz += 1
                        try:
                            if tilemap[playerz-1][playerTile[1]][playerTile[0]] == AIR and playerz > 0: # tilemap[z][y][x]
                                playerz -= 1
                        except:
                            pass
                    yoffset -= 2
                except:
                    pass

        if playerz < 3:
            if tilemap[playerz+1][playerTile[1]][playerTile[0]] != AIR and tilemap[playerz][playerTile[1]][playerTile[0]] == AIR:
                try:
                    for shownlayer in range(mapz):
                        if shownlayer > playerz:
                            shownz.pop(shownlayer)
                except:
                    pass

        for event in pygame.event.get():
            if event.type == SECONDCOUNTDOWN:
                boost -= 1
            if event.type == USEREVENT:
                initMusic()
            if event.type == QUIT:
                if(easygui.ynbox("Are you sure you want to quit? Your game WILL be saved!")):
                    if online:
                        logger.info("Saving coins and inventory to server...")
                        dba.execute("UPDATE PYTH_"+username+" SET `LastLogin` = '"+str(logintime)+"', `Coins` = "+str(coins)+", `Dirt` = "+str(inventory[DIRT])+", `Grass` = "+str(inventory[GRASS])+", `Water` = "+str(inventory[WATER])+", `Coal` = "+str(inventory[COAL])+", `Lava` = "+str(inventory[LAVA])+", `Rock` = "+str(inventory[ROCK])+", `Diam` = "+str(inventory[DIAM])+", `Sapp` = "+str(inventory[SAPP])+", `Ruby` = "+str(inventory[RUBY])+", `Gold` = "+str(inventory[GOLD])+", `Carp` = "+str(inventory[CARP])+", `Snow` = "+str(inventory[SNOW])+", `Wood` = "+str(inventory[WOOD])+", `Glass` = "+str(inventory[GLASS])+", `Brick` = "+str(inventory[BRICK])+", `GSword` = "+str(inventory[GSWORD])+", `Orb` = "+str(inventory[ORB]))
                        db.close()
                        logger.info("Inventory saved to server.")
                    settings.realm = realm
                    logger.info("Saving Realm "+str(realm)+"...")
                    if os.path.isfile("data/Map"+str(realm)+".txt") and os.access("data/Map"+str(realm)+".txt", os.R_OK):
                        os.remove("data/Map"+str(realm)+".txt")
                    time.sleep(0.1)
                    write = open("data/Map"+str(realm)+".txt", 'a')
                    for ly in range(mapz):
                        for rw in range(mapheight):
                            for cl in range(mapwidth):
                                write.write(str(tilemap[ly][rw][cl])+"|")
                    write.close()
                    logger.info("Saved Realm "+str(realm)+".")
                    if not online:
                        logger.info("Saving inventory offline...")
                        if os.path.isfile("data/Inventory.txt") and os.access("data/Inventory.txt", os.R_OK):
                            os.remove("data/Inventory.txt")
                        time.sleep(0.1)
                        write = open("data/Inventory.txt", 'a')
                        for item in inventory:
                            write.write(str(inventory[item])+"\n")
                        write.close()
                        logger.info("Inventory saved to computer.")
                        logger.info("Saving coins to computer...")
                        write = open("data/Coins.txt", "w")
                        write.write(str(coins))
                        write.close()
                        logger.info("Coins saved to computer.")
                    sys.exit("User has quit the application.")
            if event.type == MOUSEBUTTONDOWN:
                if place:
                    x = math.floor(mx / tilesizex - xoffset / tilesizex)
                    y = math.floor(my / tilesizey - yoffset / tilesizey)
                    if inventory[active] > 0:
                        inventory[active] -= 1
                        tilemap[zaxis][y][x] = active
                        if zaxis not in changedz:
                            changedz.append(zaxis)
                        mapsurf.blit(textures[active], (x*tilesizex,y*tilesizey-zaxis*16))
                        #print(tilemap[0][y][x])
                if pickup:
                    x = math.floor(mx / tilesizex - xoffset / tilesizex)
                    y = math.floor(my / tilesizey - yoffset / tilesizey)
                    if tilemap[zaxis][y][x] != AIR:
                        inventory[tilemap[zaxis][y][x]] += 1
                        tilemap[zaxis][y][x] = AIR
                        if zaxis not in changedz:
                            changedz.append(zaxis)
                        #change = True
                        #print(tilemap[0][y][x])
                #row 1
                if mx >= (vmapwidth*tilesizex)/2-155+10 and mx <= (vmapwidth*tilesizex)/2-155+50 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = DIRT
                        sel = ((vmapwidth*tilesizex)/2-155+10,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        inventory[DIRT] += 1
                elif mx >= (vmapwidth*tilesizex)/2-155+60 and mx <= (vmapwidth*tilesizex)/2-155+100 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = GRASS
                        sel = ((vmapwidth*tilesizex)/2-155+60,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        if coins >= 1:
                            coins -= 1
                            inventory[GRASS] += 1
                        else:
                            msg(["You need 1 Credit to buy the Grass that is being Monitored.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+110 and mx <= (vmapwidth*tilesizex)/2-155+150 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = WATER
                        sel = ((vmapwidth*tilesizex)/2-155+110,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        if coins >= 3:
                            coins -= 3
                            inventory[WATER] += 1
                        else:
                            msg(["You need 3 Credits to buy Water.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+160 and mx <= (vmapwidth*tilesizex)/2-155+200 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = COAL
                        sel = ((vmapwidth*tilesizex)/2-155+160,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        if coins >= 4:
                            coins -= 4
                            inventory[COAL] += 1
                        else:
                            msg(["You need 4 Credits to buy Coal.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+210 and mx <= (vmapwidth*tilesizex)/2-155+250 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = LAVA
                        sel = ((vmapwidth*tilesizex)/2-155+210,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        if coins >= 5:
                            coins -= 5
                            inventory[LAVA] += 1
                        else:
                            msg(["You need 5 Credits to buy Lava. A wise man once told me, 'Chicks dig lava moats'.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                             
                elif mx >= (vmapwidth*tilesizex)/2-155+260 and mx <= (vmapwidth*tilesizex)/2-155+300 and my >= (vmapheight*tilesizey)/2-155+20 and my <= (vmapheight*tilesizey)/2-155+60:
                    if invshow:
                        active = ROCK
                        sel = ((vmapwidth*tilesizex)/2-155+260,(vmapheight*tilesizey)/2-155+20)
                    elif shopshow:
                        if coins >= 6:
                            coins -= 6
                            inventory[ROCK] += 1
                        else:
                            msg(["You need 6 Credits to buy Stone. Or is it cement? Who knows...",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                #row 2
                elif mx >= (vmapwidth*tilesizex)/2-155+10 and mx <= (vmapwidth*tilesizex)/2-155+50 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = DIAM
                        sel = ((vmapwidth*tilesizex)/2-155+10,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 10:
                            coins -= 10
                            inventory[DIAM] += 1
                        else:
                            msg(["You need 10 Credits to buy Diamond.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+60 and mx <= (vmapwidth*tilesizex)/2-155+100 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = SAPP
                        sel = ((vmapwidth*tilesizex)/2-155+60,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 12:
                            coins -= 12
                            inventory[SAPP] += 1
                        else:
                            msg(["You need 12 Credits to buy Sapphire(Coyote).",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."]) # give the guys at 8BitMMO an Easter Egg. ;)
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+110 and mx <= (vmapwidth*tilesizex)/2-155+150 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = RUBY
                        sel = ((vmapwidth*tilesizex)/2-155+110,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 14:
                            coins -= 14
                            inventory[RUBY] += 1
                        else:
                            msg(["You need 14 Credits to buy Ruby. I would make a dog joke here, but doge.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+160 and mx <= (vmapwidth*tilesizex)/2-155+200 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = GOLD
                        sel = ((vmapwidth*tilesizex)/2-155+160,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 13:
                            coins -= 13
                            inventory[GOLD] += 1
                        else:
                            msg(["You need 13 Credits to buy Gold. 'Tis secretly 789 generic pikas squashed up.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+210 and mx <= (vmapwidth*tilesizex)/2-155+250 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = CARP
                        sel = ((vmapwidth*tilesizex)/2-155+210,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 9:
                            coins -= 9
                            inventory[CARP] += 1
                        else:
                            msg(["You need 9 Credits to buy Carpet. Or if you're a Meep, you'll buy this and stockpile them.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+260 and mx <= (vmapwidth*tilesizex)/2-155+300 and my >= (vmapheight*tilesizey)/2-155+70 and my <= (vmapheight*tilesizey)/2-155+110:
                    if invshow:
                        active = SNOW
                        sel = ((vmapwidth*tilesizex)/2-155+260,(vmapheight*tilesizey)/2-155+70)
                    elif shopshow:
                        if coins >= 7:
                            coins -= 7
                            inventory[SNOW] += 1
                        else:
                            msg(["You need 7 Credits to buy Snow. But beware! It could be Toxic.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                #row 3
                elif mx >= (vmapwidth*tilesizex)/2-155+10 and mx <= (vmapwidth*tilesizex)/2-155+50 and my >= (vmapheight*tilesizey)/2-155+120 and my <= (vmapheight*tilesizey)/2-155+160:
                    if invshow:
                        active = WOOD
                        sel = ((vmapwidth*tilesizex)/2-155+10,(vmapheight*tilesizey)/2-155+120)
                    elif shopshow:
                        if coins >= 7:
                            coins -= 7
                            inventory[WOOD] += 1
                        else:
                            msg(["You need 7 Credits to buy Wood.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+60 and mx <= (vmapwidth*tilesizex)/2-155+100 and my >= (vmapheight*tilesizey)/2-155+120 and my <= (vmapheight*tilesizey)/2-155+160:
                    if invshow:
                        active = GLASS
                        sel = ((vmapwidth*tilesizex)/2-155+60,(vmapheight*tilesizey)/2-155+120)
                    elif shopshow:
                        if coins >= 8:
                            coins -= 8
                            inventory[GLASS] += 1
                        else:
                            msg(["The Value of Glass is 8 Credits.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])
                            
                elif mx >= (vmapwidth*tilesizex)/2-155+110 and mx <= (vmapwidth*tilesizex)/2-155+150 and my >= (vmapheight*tilesizey)/2-155+120 and my <= (vmapheight*tilesizey)/2-155+160:
                    if invshow:
                        active = BRICK
                        sel = ((vmapwidth*tilesizex)/2-155+110,(vmapheight*tilesizey)/2-155+120)
                    elif shopshow:
                        if coins >= 9:
                            coins -= 9
                            inventory[BRICK] += 1
                        else:
                            msg(["You need 9 Credits to buy Brick.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])

                elif mx >= (vmapwidth*tilesizex)/2-155+160 and mx <= (vmapwidth*tilesizex)/2-155+200 and my >= (vmapheight*tilesizey)/2-155+120 and my <= (vmapheight*tilesizey)/2-155+160:
                    if shopshow:
                        if coins >= 12:
                            coins -= 12
                            inventory[GSWORD] += 1
                        else:
                            msg(["You need 12 Credits to buy Gold Sword.",
                                 "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                 "You can also earn coins by slaying evil monsters, or by completing quests."])

                elif mx >= (vmapwidth*tilesizex)/2-155+210 and mx <= (vmapwidth*tilesizex)/2-155+260 and my >= (vmapheight*tilesizey)/2-155+120 and my <= (vmapheight*tilesizey)/2-155+160:
                    if shopshow:
                        if premium:
                            if coins >= 25:
                                coins -= 25
                                inventory[ORB] += 1
                            else:
                                msg(["You need 25 Credits to buy an Orb.",
                                     "100 gold boosts are given every 5 minutes, however you may be interested in purchasing coins at http://www.tmcore.co.uk/games/pr-coinpur.php",
                                     "You can also earn coins by slaying evil monsters, or by completing quests."])
                        else:
                            msg(["ORB",
                                 "===",
                                 "This item is a PREMIUM content item. Premium access to PythianRealms is available for just £5.",
                                 "By purchasing premium access, you support the developer to keep working on and improving PythianRealms, and help him to use your premium fee to hire graphics artists and musicians to improve the game feel.",
                                 "Premium access is a one-time fee, and will allow you unlimited access to all Premium content items, such as this one.",
                                 "If you are interested in obtaining Premium PythianRealms access, please purchase \"PremiumPythian Game Access\" from the following URL:",
                                 "http://www.tmcore.co.uk/accounts/spendcr.php (also accessible by going to www.tmcore.co.uk, going to 'My Account' and clicking 'Spend Credits')",
                                 "Thank you.",
                                 "",
                                 "Note: Premium access is only valid when PythianRealms is running in online mode. If your account has PythianRealms Premium enabled, please ensure that you have a connection to the internet. Thank you."])

    
                if mx >= 50 and mx <= 60 and my >= 15 and my <= 25 and opt == True:
                    if silence == True:
                        initMusic()
                    elif silence == False:
                        silence = True
                        pygame.mixer.music.stop()
                if mx >= 50 and mx <= 60 and my >= 55 and my <= 65 and opt == True:
                    if activeoverlay == True:
                        activeoverlay = False
                    elif activeoverlay == False:
                        activeoverlay = True
                if mx >= 50 and mx <= 60 and my >= 75 and my <= 85 and opt:
                    if seamless:
                        seamless = False
                    else:
                        seamless = True
                if mx >= 50 and mx <= 60 and my >= 95 and my <= 105 and opt:
                    if smoothwalk:
                        smoothwalk = False
                    else:
                        smoothwalk = True
            if event.type == KEYDOWN:
                if event.key == K_F3:
                    debug = not debug
                if event.key == K_MINUS:
                    if zaxis >= 1:
                        zaxis -= 1
                if event.key == K_EQUALS:
                    if zaxis <= 2:
                        zaxis += 1
                if event.key == K_q:
                    if realm == 2 or premium:
                        changedz = []
                        place = True
                    else:
                        msg(["RPG REALM CONSTRUCTION",
                             "======================",
                             "We're super sorry to have to say this, but Construction within the RPG realm is restricted to Premium users. Why?",
                             "Well, we need to earn money to keep working on and producing content for PythianRealms. Premiumship shows your dedication to the game,",
                             "and gives you sweet perks - such as being able to shape the RPG world to make it how you imagine it.",
                             "",
                             "If you wish to build without Premium access, simply go over to the Construction realm, by pressing T.",
                             "",
                             "If you're interested in becoming a Premium user, please feel free to buy premiumship at http://www.tmcore.co.uk - more info available there.",
                             "",
                             "Thank you."])
                if event.key == K_r:
                    if realm == 2 or premium:
                        changedz = []
                        pickup = True
                        msg(["Pickup mode changes will not immediately take effect, and will be shown after pressing F to exit pickup mode."])
                    else:
                        msg(["RPG REALM CONSTRUCTION",
                             "======================",
                             "We're super sorry to have to say this, but Construction within the RPG realm is restricted to Premium users. Why?",
                             "Well, we need to earn money to keep working on and producing content for PythianRealms. Premiumship shows your dedication to the game,",
                             "and gives you sweet perks - such as being able to shape the RPG world to make it how you imagine it.",
                             "",
                             "If you wish to build without Premium access, simply go over to the Construction realm, by pressing T.",
                             "",
                             "If you're interested in becoming a Premium user, please feel free to buy premiumship at http://www.tmcore.co.uk - more info available there.",
                             "",
                             "Thank you."])
                if event.key == K_i:
                    invshow = not invshow
                if event.key == K_h:
                    shopshow = not shopshow
                if event.key == K_c:
                    webbrowser.open("https://irc.editingarchive.com:8080/?channels=PythianRealms", 2)
                if event.key == K_t:
                    logger.info("Saving Realm "+str(realm)+"...")
                    if os.path.isfile("data/Map"+str(realm)+".txt") and os.access("data/Map"+str(realm)+".txt", os.R_OK):
                        os.remove("data/Map"+str(realm)+".txt")
                    time.sleep(0.1)
                    write = open("data/Map"+str(realm)+".txt", 'a')
                    for ly in range(mapz):
                        for rw in range(mapheight):
                            for cl in range(mapwidth):
                                write.write(str(tilemap[ly][rw][cl])+"|")
                    write.close()
                    logger.info("Saved Realm "+str(realm)+".")
                    if realm == 0:
                        realm = 1
                        settings.realm = 1
                        msg(["THE CONSTRUCTION REALM",
                             "======================",
                             "The construction realm contains monsters and NPCs to teach you how to build, destroy, and use the Construction realm, but it does NOT have a storyline.",
                             "Thee construction realm provides a home for all your construction talent to come together to create a wondrous, magnificent building for you to share with your friends.",
                             "The Construction realm, by all defaults, is a barren wasteland - that is, until you build in it. The construction realm serves to satisfy the construction aspect of PythianRealms.",
                             "Have fun, and remember - T to toggle between realms... If you wish to return to the RPG realm, of course. ;)"])
                    elif realm == 1:
                        realm = 0
                        settings.realm = 0
                        msg(["THE RPG REALM",
                             "=============",
                             "The RPG realm is the home of the PythianRealms storyline. Riddled with people, monsters and stories, the RPG realm is built by Scratso (the developer) and distributed with all copies of PythianRealms.",
                             "Construction within the RPG realm is usually forbidden, however Premium Users may happily change the RPG realm to suit themselves. This allows premium users to improve on existing buildings, if they wish.",
                             "Have fun, and remember - T to toggle between realms... If you wish to return to the Construction realm, of course. ;)"])
                    change = True
                    tilemap = [ [[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz) ]

                    if os.path.isfile("data/Map"+str(realm)+".txt") and os.access("data/Map"+str(realm)+".txt", os.R_OK):
                        file = 0
                        read = open("data/Map"+str(realm)+".txt", 'r')
                        read2 = read.read()
                        read3 = read2.split("|")
                        for ly in range(mapz):
                            for rw in range(mapheight):
                                for cl in range(mapwidth):
                                    read4 = int(read3[file])
                                    tilemap[ly][rw][cl] = read4
                                    file = file + 1
                        read.close()
                if event.key == K_TAB:
                    if tilesizex == 64:
                        tilesizex, tilesizey = 16,16
                    else:
                        tilesizex, tilesizey = tilesizex+16,tilesizey+16
                    display = pygame.display.set_mode((vmapwidth*tilesizex, vmapheight*tilesizey), HWSURFACE|DOUBLEBUF) #|RESIZABLE later
                    textures =   {
                        DIRT  : pygame.transform.scale(pygame.image.load('graphics/0/dirt.jpg'), (tilesizex,tilesizey)),
                        GRASS : pygame.transform.scale(pygame.image.load('graphics/grass.jpg'), (tilesizex,tilesizey)),
                        WATER : pygame.transform.scale(pygame.image.load('graphics/water_1.jpg'), (tilesizex,tilesizey)),
                        COAL  : pygame.transform.scale(pygame.image.load('graphics/coal.jpg'), (tilesizex,tilesizey)),
                        LAVA  : pygame.transform.scale(pygame.image.load('graphics/lava.jpg'), (tilesizex,tilesizey)),
                        ROCK  : pygame.transform.scale(pygame.image.load('graphics/stone.jpg'), (tilesizex,tilesizey)),
                        DIAM  : pygame.transform.scale(pygame.image.load('graphics/diamond.jpg'), (tilesizex,tilesizey)),
                        SAPP  : pygame.transform.scale(pygame.image.load('graphics/sapphire.jpg'), (tilesizex,tilesizey)),
                        RUBY  : pygame.transform.scale(pygame.image.load('graphics/ruby.jpg'), (tilesizex,tilesizey)),
                        GOLD  : pygame.transform.scale(pygame.image.load('graphics/gold.jpg'), (tilesizex,tilesizey)),
                        AIR   : pygame.transform.scale(pygame.image.load('graphics/air.png'), (tilesizex,tilesizey)),
                        WOOD  : pygame.transform.scale(pygame.image.load('graphics/wood.jpg'), (tilesizex*2,tilesizey*2)),
                        GLASS : pygame.transform.scale(pygame.image.load('graphics/glass.png'), (tilesizex*2,tilesizey*2)),
                        BRICK : pygame.transform.scale(pygame.image.load('graphics/brick.jpg'), (tilesizex*2,tilesizey*2)),
                        CARP  : pygame.transform.scale(pygame.image.load('graphics/carpet.jpg'), (tilesizex,tilesizey)),
                        SNOW  : pygame.transform.scale(pygame.image.load('graphics/snow.jpg'), (tilesizex,tilesizey)), # NTS: Limited edition Item! To be removed on New Year's Day.
                        SEL   : pygame.transform.scale(pygame.image.load('graphics/grass.jpg'), (tilesizex,tilesizey)),
                        GSWORD: pygame.transform.scale(pygame.image.load('graphics/gsword.png'), (tilesizex,tilesizey)),
                        FPORT : pygame.transform.scale(pygame.image.load('graphics/forportal.jpg'), (tilesizex,tilesizey)),
                        BPORT : pygame.transform.scale(pygame.image.load('graphics/backportal.jpg'), (tilesizex,tilesizey)),
                        ORB   : pygame.transform.scale(pygame.image.load('graphics/orb.png'), (tilesizex,tilesizey))
                    }
                    player = pygame.transform.scale(pygame.image.load("graphics/"+str(premium)+"/player_right.png").convert_alpha(), (tilesizex,tilesizey))
                    change = True
                    for z in range(mapz):
                        changedz.append(z)
            if event.type == NPCMOVE:
                for npc in NPCs:
                    for npcd in NPCcount[npc]:
                        move = random.randint(1,5)
                        if move == 2:
                            #up
                            npcPosY[npc][npcd] -= 1
                        elif move == 3:
                            #down
                            npcPosY[npc][npcd] += 1
                        elif move == 4:
                            #left
                            npcPosX[npc][npcd] -= 1
                        elif move == 5:
                            #right
                            npcPosX[npc][npcd] += 1
                realm = settings.realm
                npcsurf.fill(0)
                #for each NPC
                for item in NPCs:
                    #determine the NPC's name here. This name **only** affects the text shown above the NPC.
                    #if chunk == NPCchunk[item] and realm == NPCrealm[item]:
                    npcPosZ[item] = 1
                    for curnpc in NPCcount[item]:
                        if (npcPosX[item][curnpc] >= mintile[0] and npcPosX[item][curnpc] <= maxtile[0]) and (npcPosY[item][curnpc] >= mintile[1] and npcPosY[item][curnpc] <= maxtile[1]):
                            #display the npc at the correct position
                            npcsurf.blit(npcGraphic[item],(npcPosX[item][curnpc]*tilesizex,npcPosY[item][curnpc]*tilesizey))
                            if NPCtype[item] == "Hostile":
                                #display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, red)
                                npcsurf.blit(NPCname, (npcPosX[item][curnpc]*tilesizex, npcPosY[item][curnpc]*tilesizey-15))
                                percent = NPChealth[item][curnpc]/NPCmaxHealth[item]
                                NHP = gamefont.render(str(round(percent*100))+"%", True, red)
                                npcsurf.blit(NHP, (npcPosX[item][curnpc]*tilesizex,npcPosY[item][curnpc]*tilesizey-27))
                            elif NPCtype[item] == "Friendly":
                                #display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, green)
                                npcsurf.blit(NPCname, (npcPosX[item][curnpc]*tilesizex, npcPosY[item][curnpc]*tilesizey-15))
                            else:
                                #display the NPC's name...?
                                NPCname = gamefont.render(str(npcName[item]), True, black)
                                npcsurf.blit(NPCname, (npcPosX[item][curnpc]*tilesizex, npcPosY[item][curnpc]*tilesizey-15))
##                    else:
##                        npcPosZ[item] = 2

        if change:
            display.fill(black)
            changetext = gamefont.render("RENDERING ENGINE IS BUSY... PLEASE WAIT!", True, yellow, red)
            display.blit(changetext, (0,0))
            pygame.display.update()
            logger.info("Changing the following layers: "+str(changedz))
            change = False
            mapsurf.fill(brown)
            #loop through each layer
            for layer in range(mapz): #changedz
                layersurfs[layer].fill(0)
                #loop through each row
                for row in range(mapheight):
                    #loop through each column in the row
                    for column in range(mapwidth):
                        #draw an image for the resource, in the correct position
                        layersurfs[layer].blit(textures[tilemap[layer][row][column]], (column*tilesizex,row*tilesizey-layer*16))
            changedz = []
            pass
        if place:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            # the below was lagging waay too much.
            prevsurf.blit(textures[active],(x*tilesizex,y*tilesizey-zaxis*16))
            if pygame.key.get_pressed()[K_a]:
                place = False
                change = True
        if pickup:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            if pygame.key.get_pressed()[K_f]:
                pickup = False
                change = True

        display.blit(mapsurf, (xoffset, yoffset))
        for layersurf in layersurfs:
            if layersurfs.index(layersurf) in shownz:
                display.blit(layersurfs[layersurfs.index(layersurf)], (xoffset,yoffset))
        display.blit(npcsurf, (xoffset, yoffset))
        display.blit(prevsurf, (xoffset, yoffset))
        display.blit(player, (vmapwidth*tilesizex/2-(tilesizex/2),vmapheight*tilesizey/2-(tilesizey/2)-playerz*16))
        display.blit(activesurf, (vmapwidth*tilesizex-tilesizex-10, 0))
        activeblock.blit(textures[active], (0,0))
        display.blit(activeblock, (vmapwidth*tilesizex-tilesizex-5, 22))

        ztext = gamefont.render("Z-Axis Lock: "+str(zaxis), True, white)
        display.blit(ztext, (0,0))

        ctext = gamefont.render("You have "+format(coins, ",d")+" coins.", True, white)
        display.blit(ctext, (0,12))

        ttext = gamefont.render("Next gold boost: "+str(timeleft)+" seconds.", True, white)
        display.blit(ttext, (0,24))

        if debug:
            ptext = gamefont.render("Player Tile: "+str(playerTile), True, white)
            display.blit(ptext, (0,36))

            etext = gamefont.render("FPS: "+str(fps), True, white)
            display.blit(etext, (0,48))

            qtext = gamefont.render("Image Quality: "+str(tilesizex)+"bit (Tab to cycle) (32bit recommended)", True, white)
            display.blit(qtext, (0,60))

            pztext = gamefont.render("Player Z Pos: "+str(playerz), True, white)
            display.blit(pztext, (0,72))

            pptext = gamefont.render("Map Offset: ("+str(xoffset)+", "+str(yoffset)+")", True, white)
            display.blit(pptext, (0,84))

            rtext = gamefont.render("Realm: "+str(realm), True, white)
            display.blit(rtext, (0,96))

        if shopshow:
            shopsurf.fill((23, 100, 255, 50))
            text = gamefont.render("Shop", True, white)
            shopsurf.blit(text, (1,1))
            #display the inventory, starting 10 pixels in
            placePosition = 10
            yoff = 20
            newrow = 6
            curitem = 1
            for item in resources:
                #add the image
                if item == AIR or item == BPORT or item == FPORT:
                    continue
                if curitem <= newrow:
                    shopsurf.blit(textures[item],(placePosition,yoff))
                    placePosition += 0
                    #add the text showing the amount in the inventory:
                    textObj = gamefont.render(str(inventory[item]), True, white)
                    shopsurf.blit(textObj,(placePosition,yoff+20))
                    placePosition += 50
                    if curitem == newrow:
                        curitem = 1
                        yoff += 50
                        placePosition = 10
                    else:
                        curitem += 1
            display.blit(shopsurf, ((vmapwidth*tilesizex)/2-155,(vmapheight*tilesizey)/2-155))
    
        if invshow:
            invsurf.fill((23, 100, 255, 50))
            text = gamefont.render("Inventory", True, black)
            invsurf.blit(text, (1,1))
            #display the inventory, starting 10 pixels in
            placePosition = 10
            yoff = 20
            newrow = 6
            curitem = 1
            for item in resources:
    ##      ANIMATION CODE - ADAPT FOR ANIMATED BLOCKS :)
    ##        if item == WATER:
    ##            if wateranim == 1:
    ##                textures[WATER] = pygame.image.load("graphics/water_2.jpg")
    ##                wateranim = 2
    ##            elif wateranim == 2:
    ##                textures[WATER] = pygame.image.load("graphics/water_1.jpg")
    ##                wateranim = 1
    ############################################################################################### THIS LINE IS WELL COMMENTED, ACCORDING TO PYTHON!
                #add the image
                if item == AIR or item == BPORT or item == FPORT:
                    continue
                if curitem <= newrow:
                    invsurf.blit(textures[item],(placePosition,yoff))
                    placePosition += 0
                    #add the text showing the amount in the inventory:
                    textObj = gamefont.render(str(inventory[item]), True, white)
                    invsurf.blit(textObj,(placePosition,yoff+20)) 
                    placePosition += 50
                    if curitem == newrow:
                        curitem = 1
                        yoff += 50
                        placePosition = 10
                    else:
                        curitem += 1
            display.blit(invsurf, ((vmapwidth*tilesizex)/2-155,(vmapheight*tilesizey)/2-155))
            if activeoverlay == True:
                display.blit(textures[SEL], sel)

        if place:
            placetext = gamefont.render("Build mode active", True, green)
            display.blit(placetext, (0, vmapheight*tilesizey-12))
        if pickup:
            pickuptext = gamefont.render("Pickup mode active", True, red)
            display.blit(pickuptext, (0, vmapheight*tilesizey-12))

        pygame.display.update((0,0,vmapwidth*tilesizex,vmapheight*tilesizey))

        elapsed = time.time() - now
        try:
            fps = round(1/elapsed)
        except:
            pass
    
except Exception as e:
    #reporterr.Mail.report(object, str(e)+"%0D%0A %0D%0A"+str(traceback.format_exc()))
    #print("Error reporter opened. Please send it, and possibly include any steps to reproduce the issue.")
    logger.error(traceback.format_exc())
    easygui.exceptionbox("Oops! Something went wrong. But don't worry! Because I'm so amazingly kind, you need only send me this error report below and I'll get right on it.", "An Error Ocurred!")

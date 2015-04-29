# -*- coding: utf-8 -*-

# Copyright (c) 2015 Damian Heaton and TechnoMagic Enterprises. ALL RIGHTS RESERVED.

version = "0.0.0.3"

import sys, os, time, random, math, traceback, webbrowser, datetime as dt

# Error Reporting note: %0D%0A is the Newline Character for the Mailto: command. Since the Error Reporter uses Mailto:,
# use %0D%0A instead of \n.

# Encompass the entire program in a try statement for the error reporter.
try:

    #######################
    # SET UP POUP WINDOWS #
    #######################

    import easygui  # An included library with Python install.
    def msgbox(title, text):
        #ctypes.windll.user32.MessageBoxA(None, str(text), str(title), 0)
        easygui.msgbox(text, title) 
    #msgbox('Your title', 'Your text', 1)

    class Settings(easygui.EgStore):
        def __init__(self, filename):  # filename is required
            #-------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            #-------------------------------------------------
            self.username = None
            self.password = None

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
        response=urllib2.urlopen('http://92.234.196.233',timeout=1)
        online = True
    except urllib2.URLError as err:
        online = False
        pass
    logger.info("Can we connect to the server? "+str(online))
    if not online:
        logger.warn("Cannot connect to the Auth Server! Any online data will not be available and any purchased items will also not be available!")
        msgbox("Warning!", "PythianRealms cannot connect to the Auth Server! Any data saved online will not be available until PythianRealms can connect to the authorisation server. After a connection is available, please restart PythianRealms to reconnect. PythianRealms will run in Offline Mode.")

    #######################
    # INITIALIZE SETTINGS #
    #######################

    settingsFile = "Settings.txt"
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
            if easygui.ynbox("Do you have a TechnoMagic Account? (An account at http://www.technomagic.net)", "Login"):
                username = easygui.enterbox("TechnoMagic Account Username", "Login")
                password = easygui.passwordbox("TechnoMagic Account Password", "Login")
                try:
                    import mysql.connector as dbc
                    db = dbc.connect(user='pythian', password='realmsian',
                                                  host='92.234.196.233',
                                                  database='tchnm_15865510_acc')
                    webbrowser.open("http://www.technomagic.net/accounts/securekey.php?userpw="+password)
                    password = easygui.enterbox("TechnoMagic Account SecureKey (Should be shown in browser.)", "Login")
                    dba = db.cursor()
                    query = ("SELECT * FROM users WHERE Username = '"+username+"' AND Password = '"+password+"'")
                    dba.execute(query)
                    dbd = []
                    for columns in dba:
                        for column in columns:
                            dbd.append(column)
                    logger.info("Authorisation Server returned: "+str(dbd))
                    if dbd[3] != password:
                        msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: Wrong password.")
                        online = False
                        username = "Offline User"
                    else:
                        settings.username = username
                        settings.password = password
                        settings.store()
                        logger.info("Successfully logged in to account!")
                except Exception as e:
                    msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: %s" % e)
                    online = False
                    username = "Offline User"
            else:
                webbrowser.open("http://www.technomagic.net/accounts/register.php")
                username = easygui.enterbox("TechnoMagic Account Username", "Login")
        else:
            username = settings.username
            password = settings.username
            try:
                import mysql.connector as dbc
                db = dbc.connect(user='pythian', password='realmsian',
                                              host='92.234.196.233',
                                              database='tchnm_15865510_acc')
                dba = db.cursor()
                query = ("SELECT * FROM users WHERE Username = '"+username+"' AND Password = '"+password+"'")
                dba.execute(query)
                dbd = []
                for columns in dba:
                    for column in columns:
                        dbd.append(column)
                logger.info("Authorisation Server returned: "+str(dbd))
                if dbd[3] != password:
                    msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: Wrong password.")
                    online = False
                    username = "Offline User"
                else:
                    logger.info("Successfully logged in to account!")
            except Exception as e:
                msgbox("Login Failed!", "Sorry, your login failed! Switching to offline mode. You can try log in again by restarting the game. Error: %s" % e)
                online = False
                username = "Offline User"
    else:
        username = "Offline User"

    if online:
        logintime = dt.datetime.today().strftime("%Y/%m/%d").split("/")
        logintime = dt.date(int(logintime[0]), int(logintime[1]), int(logintime[2]))
        logger.info ("Logged in on "+str(logintime))

    #####################
    # OPERATING SYSTEMS #
    #####################

    useros = sys.platform
    logger.info("Operating System Environment: "+useros+".")
    if useros == "linux" or useros == "linux2" or useros == "linux3" or useros == "linux4":
        useros = "linux"
        logger.error("""*** Please note that PythianRealms may be very buggy on Linux as it is not natively programmed in it. Please report any bugs you find. Thanks. :) ***""")

    #####################
    # mapsurf SIZES ETC #
    #####################

    tilesizex = 32
    tilesizey = 32
    mapwidth = 100
    mapheight = 100
    mapz = 4

    playerz = 0

    oldtiles = []

    zaxis = 0
    place = False
    pickup = False
    changedz = []

    change = True
    debug = False

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

    # set up the display
    pygame.init()
    display = pygame.display.set_mode((vmapwidth*tilesizex, vmapheight*tilesizey), HWSURFACE|DOUBLEBUF) #|RESIZABLE later
    mapsurf = pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey))
    mapsurf.fill(brown)
    prevsurf = pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey), pygame.SRCALPHA, 32).convert_alpha()

    layersurfs = []
    for layer in range(mapz):
        layersurfs.append(pygame.Surface((mapwidth*tilesizex, mapheight*tilesizey), pygame.SRCALPHA, 32).convert_alpha())

    # fonts
    gamefont = pygame.font.Font("graphics/gameFont.ttf", 12)

    # set up loading screen
    display.fill(white)
    loadtext = gamefont.render("Loading PythianRealms...", True, black)
    display.blit(loadtext, (0,vmapheight*tilesizey-12))
    display.blit(pygame.image.load("graphics/logo.png"), (vmapwidth*tilesizex/2-360,0))
    pygame.display.update()

    # set the window title
    pygame.display.set_caption("PythianRealms Game | Version "+version+" | Online: "+str(online)) # , "graphics/logo-small.png"
    # set the window icon
    pygame.display.set_icon(pygame.image.load("graphics/logo-small.png").convert_alpha())

    # load the player sprite
    player = pygame.transform.scale(pygame.image.load("graphics/player_right.png").convert_alpha(), (tilesizex,tilesizey))

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
                            CARP   : 450,
                            SNOW   : 1000,
                            WOOD   : 900,
                            GLASS  : 900,
                            BRICK  : 900,
                            GSWORD : 0,
                            ORB    : 0,
                            FPORT  : 1,
                            BPORT  : 1,
                        }

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
                0 : 1,
                1 : 1,
                2 : 2,
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
    #            for curnpc in NPChealth[npc][chunk]:
    #                if os.path.isfile("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt") and os.access("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", os.R_OK):
    #                    file = open("data/"+str(npc)+"/"+str(chunk)+"/"+str(curnpc)+".txt", "r")
    #                    integer = int(file.read())
    #                    NPChealth[npc][chunk][curnpc] = integer
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
                0 : { 0 : random.randint(0,mapwidth-1) },
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
                0 : { 0 : random.randint(0,mapheight-1) },
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

    #webbrowser.open("http://technomagic.net:9090/?channels=PythianRealms")

    #use list comprehension to create the tilemap
    tilemap = [ [[AIR for w in range(mapwidth)] for h in range(mapheight)] for z in range(mapz) ]

    # set the map's x and y offsets (positioning)
    xoffset,yoffset = 0,0

    #a dictionary linking resources to textures
    textures =   {
                    DIRT  : pygame.transform.scale(pygame.image.load('graphics/0/dirt.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GRASS : pygame.transform.scale(pygame.image.load('graphics/grass.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    WATER : pygame.transform.scale(pygame.image.load('graphics/water_1.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    COAL  : pygame.transform.scale(pygame.image.load('graphics/coal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    LAVA  : pygame.transform.scale(pygame.image.load('graphics/lava.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    ROCK  : pygame.transform.scale(pygame.image.load('graphics/stone.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    DIAM  : pygame.transform.scale(pygame.image.load('graphics/diamond.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    SAPP  : pygame.transform.scale(pygame.image.load('graphics/sapphire.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    RUBY  : pygame.transform.scale(pygame.image.load('graphics/ruby.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GOLD  : pygame.transform.scale(pygame.image.load('graphics/gold.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    AIR   : pygame.transform.scale(pygame.image.load('graphics/air.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    WOOD  : pygame.transform.scale(pygame.image.load('graphics/wood.jpg'), (tilesizex*2,tilesizey*2+round(tilesizey/2))),
                    GLASS : pygame.transform.scale(pygame.image.load('graphics/glass.png'), (tilesizex*2,tilesizey*2+round(tilesizey/2))),
                    BRICK : pygame.transform.scale(pygame.image.load('graphics/brick.jpg'), (tilesizex*2,tilesizey*2+round(tilesizey/2))),
                    CARP  : pygame.transform.scale(pygame.image.load('graphics/carpet.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    SNOW  : pygame.transform.scale(pygame.image.load('graphics/snow.jpg'), (tilesizex,tilesizey+round(tilesizey/2))), # NTS: Limited edition Item! To be removed on New Year's Day.
                    SEL   : pygame.transform.scale(pygame.image.load('graphics/grass.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    GSWORD: pygame.transform.scale(pygame.image.load('graphics/gsword.png'), (tilesizex,tilesizey+round(tilesizey/2))),
                    FPORT : pygame.transform.scale(pygame.image.load('graphics/forportal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    BPORT : pygame.transform.scale(pygame.image.load('graphics/backportal.jpg'), (tilesizex,tilesizey+round(tilesizey/2))),
                    ORB   : pygame.transform.scale(pygame.image.load('graphics/orb.png'), (tilesizex,tilesizey+round(tilesizey/2)))
                }

    elapsed = 0
    fps = 0
    cachedscreen = []

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
         "This is a Public Alpha Development version of PythianRealms. All feedback is appreciated. Want to help give feedback? Simply email me at scratso@technomagic.net!",
         "PythianRealms cannot thrive without donations. Why not help us out by donating? You can donate over at http://www.technomagic.net/PythianRealms.php",
         "",
         "Please make sure that you have fun, and spread the word!",
         "",
         "PROTIP: You can find a load of helpful guides by typing (without quotes) \"%APPDATA%\PythianRealms\" into run (Windows key + R), selecting the folder of the latest build, and going into the Docs folder."]
    if online:
        startupnotes[0] = "Hey, "+str(username)+", welcome back to PythianRealms! You last logged in on "+str(dbd[16])+"."
    msg(startupnotes)
    
    changedz = [] #0,1,2,3 after you add the loading system. Until then, this'll do.
    
    while True:
        # msg(["Test"])
        now = time.time()
        display.fill(black)
        shownz = [0,1,2,3]

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
            player = pygame.transform.scale(pygame.image.load("graphics/player_right.png").convert_alpha(), (tilesizex,tilesizey))
            if playerTile[0] != 100:
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
                    xoffset -= 1
                except:
                    pass
        if keys[pygame.K_LEFT]:
            player = pygame.transform.scale(pygame.image.load("graphics/player_left.png").convert_alpha(), (tilesizex,tilesizey))
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
                    xoffset += 1
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
                    yoffset += 1
                except:
                    pass
        if keys[pygame.K_DOWN]:
            if playerTile[1] != 100:
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
                    yoffset -= 1
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
            if event.type == QUIT:
                if(easygui.ynbox("Are you sure you want to quit? Your game WILL be saved!")):
                    if online:
                        dba.execute("UPDATE users SET `PythianRealms_Last-Login` = '"+str(logintime)+"' WHERE Username = '"+username+"' AND Password = '"+password+"'")
                    try:
                        db.close()
                    except:
                        pass
                    sys.exit("User has quit the application.")
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
                    changedz = []
                    place = True
                if event.key == K_r:
                    changedz = []
                    pickup = True
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
                    player = pygame.transform.scale(pygame.image.load("graphics/player_right.png").convert_alpha(), (tilesizex,tilesizey))
                    change = True
                    for z in range(mapz):
                        changedz.append(z)

        if change:
            logger.info("Changing the following layers: "+str(changedz))
            change = False
            mapsurf.fill(brown)
            #loop through each layer
            for layer in changedz: #range(mapz)
                layersurfs[layer].fill(0)
                #loop through each row
                for row in range(mapheight):
                    #loop through each column in the row
                    for column in range(mapwidth):
                        #draw an image for the resource, in the correct position
                        layersurfs[layer].blit(textures[tilemap[layer][row][column]], (column*tilesizex,row*tilesizey-layer*16))
            changedz = []
        if place:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            # the below was lagging waay too much.
            prevsurf.blit(textures[active],(x*tilesizex,y*tilesizey-zaxis*16))
            if pygame.mouse.get_pressed()[0] == True:
                tilemap[zaxis][y][x] = active
                if zaxis not in changedz:
                    changedz.append(zaxis)
                mapsurf.blit(textures[active], (x*tilesizex,y*tilesizey-zaxis*16))
                #print(tilemap[0][y][x])
            if pygame.key.get_pressed()[K_a]:
                place = False
                change = True
        if pickup:
            x = math.floor(mx / tilesizex - xoffset / tilesizex)
            y = math.floor(my / tilesizey - yoffset / tilesizey)
            if pygame.mouse.get_pressed()[0] == True:
                tilemap[zaxis][y][x] = AIR
                if zaxis not in changedz:
                    changedz.append(zaxis)
                change = True
                #print(tilemap[0][y][x])
            if pygame.key.get_pressed()[K_f]:
                pickup = False

        display.blit(mapsurf, (xoffset, yoffset))
        for layersurf in layersurfs:
            if layersurfs.index(layersurf) in shownz:
                display.blit(layersurfs[layersurfs.index(layersurf)], (xoffset,yoffset))
        display.blit(prevsurf, (xoffset, yoffset))
        display.blit(player, (vmapwidth*tilesizex/2-(tilesizex/2),vmapheight*tilesizey/2-(tilesizey/2)-playerz*16))

        ztext = gamefont.render("Z-Axis Lock: "+str(zaxis), True, white)
        display.blit(ztext, (0,0))

        if debug:
            ptext = gamefont.render("Player Tile: "+str(playerTile), True, white)
            display.blit(ptext, (0,12))

            etext = gamefont.render("FPS: "+str(fps), True, white)
            display.blit(etext, (0,24))

            qtext = gamefont.render("Image Quality: "+str(tilesizex)+"bit (Tab to cycle) (32bit recommended)", True, white)
            display.blit(qtext, (0,36))

            pztext = gamefont.render("Player Z Pos: "+str(playerz), True, white)
            display.blit(pztext, (0,48))

            pptext = gamefont.render("Map Offset: ("+str(xoffset)+", "+str(yoffset)+")", True, white)
            display.blit(pptext, (0,60))

        pygame.event.pump()

        pygame.display.update()

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

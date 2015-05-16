Changelog:

0.0.0.3 -> 0.0.0.4:
- Added inventory gui back. Background due to change from blue, since I'm adding translucency to make it look better.
- Added active block gui element at top-right corner of screen.
- Overhauled majority of block graphics to fit with the new rendering methods (all blocks have sides, and all sides are part of the block's graphics, so the blocks from the old PythianRealms render oddly now (stretched)).
- Added CREDITS.md file in Docs folder.
- Added shop back.
- Overhauled inventory and shop GUIs to be translucent.
- Added back coin system.
- Easter eggs in the shop are back. ;) And this time they're utilising the huge-screen message system. :D

0.0.0.2 -> 0.0.0.3:
- Game will now ask if you really want to quit. Just press "No" if you don't.
- Game will now attempt to connect to an "Auth Server" at startup.
- Actually now making use of easygui. Linux users will need to install it!!
- Linux users will now need to also install MySQL "Connector/Python" module.
- Integration with TechnoMagic Accounts. All users must have a TechnoMagic Account to save their data "cloudly" (saving not a feature, yet). Playing offline works, but saves locally (no saving yet!).
- If online, the game will now display your last login when you start up the game.
- Improved error handler.
- Added a .zip file containing all the required Python Modules if on Linux (requires Launcher redownload)... Now you just need Python 3.2.5! Yay! :D
- Added NPCs. They currently do nothing, but eh.
- TechnoMagic Accounts Login info now saves! Yaaay! :D
- Moved settings.txt file to the data folder.
- Optimized NPC rendering.
- Made Database more secure, by splitting PythianRealms' users' data off from all other database data. *** IF YOU ALREADY HAD A TECHNOMAGIC ACCOUNT, PLEASE CONTACT ME, AS THE NEW DATABASES ARE ONLY MADE DURING REGISTRATION ***
- The game now also reports the time that you last logged in.
- Linux users have a much easier play. I now distribute PythianRealms as a .exe and a .py, meaning that any version of Python (3.0 and above) will work. Launcher updated to fit, please redownload from http://scratso.itch.io/pythianrealms .
- === If anyone can donate, please do! Pushing for a graphics overhaul, but I need money for the graphics! Thank you! :) ===

0.0.0.1 -> 0.0.0.2:
- Created a framework for myself, so that I can easily make messages appear on the screen.
- Used aforementioned framework to add a startup message.
- Fixed map alignment with player.
- Added stair-style physics. Your player can go up and down half-blocks (dirt is a half-block, btw).

0.6.0.1 -> 0.0.0.1:
=== REWRITTEN ===

- Player will never actually move. The map moves instead. This allows us to load in a massive tileset, stick it in a surface and then move the surface.
- Different z-axis levels are easier to program. I could make it have however many z-axis levels I want, but I ave locked it at 4 because the more z-axis levels there are, the longer it takes to startup. May change in future.
- Revamped building. Please refer to Docs.
- Added different "Image Qualities". Refer to Docs.

0.6 -> 0.6.0.1:
- Fixed a bug that crashed the game.
- Ground layer construction is easier. It now involves graphics.
- Player now moves pixel by pixel.
=== REWRITE ===

0.5.9 -> 0.6:
- Server no longer tracks location, possibly just chat-based(?). Otherwise, may experiment with better techniques.
- When trying to move, you can now just hold down an arrow key rather than repeatedly spamming it. Much more graceful.
- Due to the above, movement is now high-priority in the code. As such, movement should be much faster and less laggy.
- Fixed ' dropping chat to a new line.
- Fixed the messages you were typing not showing up in Multiplayer.
- Fixed random empty messages (from users) in chat.
- Encrypted Inventory file. The file is en/decrypted by the game.
- Changed the game's font to Ubuntu Bold Italics. Preferred more by me, but you CAN use whatever font you want by simply sticking the .ttf file in the graphics folder and renaming it to FreeSansBold.ttf. I also kept the ACTUAL FreeSansBold in there, but renamed it to FreeSansBold-old.ttf.
- Added Magic Orbs. These Magic Orbs are *currently* useless, but will no longer be useless in future updates. Magic Orbs will cost when their use is added to the game, and are currently unobtainable. They are planned to be required to make Staffs, which will be part of a new magic attack option in the turn-based combat system. Their graphic is under work.

0.5.8 -> 0.5.9:
- Added coins.
- Hostile NPCs now drop a set amount of coins dependant on what NPC they are upon death, rather than a random amount of a random block.
- The Server no longer handled maps - they are client-side (for now, at least).
- The Server now tracks your current chunk.
- The Server now saves your chunk on every chunk update.
- Added Error Reporter. The Error Reporter will:
  - Open up an email, filled out with the necessary error details. Just hit send :)
  - Log the error down in debug.log as an error.
  - Close PythianRealms.
  This means that errors are now always available, unless PythianRealms can't access the Error Reporter.
- Added Shop system. Hidden inside the "you don't have enough credits!" messages for specific blocks, there are Easter eggs! See if you can find them all ;)
- Added Amnesiac Custom NPC for Brandon Fuller after he donated £10.

0.5.7 -> 0.5.8:
- Fixed bug in which, during a battle, it wouldn't show how much HP the enemy took from you.
- Added Crafting panel, accessible by pressing M.
- Fixed resizing and fullscreen window sizing. (Upon pressing esc, the window was too big - due to old inventory panel.)
- Removed Crafting bar.
- Resized game window so that the about button goes to the side of the window.
- Updated Bjorvik to represent the lack of crafting bar.
- Added a new button below the About button, named "Donate". This button takes you to the IndieGoGo campaign page.
- Added a new button below the Donate button, named "Forum". This button takes you to the IndieRising thread.
- Stopped distributing "inv" folder unneccessarily.

0.5.6 -> 0.5.7:
- Cleaned up Server shutdown message. When the server disconnects it now alerts the client.
- technomagic.net pings are no longer added to the connection list.
- The server no longer asks for a Port on startup - port is now set up in serv/config.txt.
- Changed a bit of music.
- Linux support added. (Still needs a decent amount of development)
- The Linux version will now attempt to dodge .mid files, as Linux doesn't natively have the codecs for them.
- Added Inventory panel, accessible by pressing I.
- Remapped Touch layout. It's now relative to the inventory panel.
- Removed inventory bar from the bottom of the screen.
- Pushed chat bar up so it located in the place the inventory bar was.
- Removed Linux "Not Supported" message and close.

0.5.5 -> 0.5.6:
- Fixed where the game would crash (not game-breaking) when you closed it, due to the NPC folders not always being there. It now generates the folders if they aren't found.
- Added Stephan, who Bjorvik now tells you to go and see.
- Added King Rhask.
- Added Rakjoke.
- Added Rakjoke's Friend.
- Added Homeless Man.
- Added Stranger.
- Added Blood Hound.
The purpose of adding these NPCs is to extend the storyline. The storyline for Realm 1 is complete, but I'm still looking for mappers and artists. Also, Special Offer with PythianRealms: If you join TechnoMagic Accounts within March 2015, and post a comment about PythianRealms in the account CP, you are likely to earn some free Credits. More information available at technomagic.net. :)

0.5.4 -> 0.5.5:
- When an NPC initiates a battle, the screen now flashes black 3 times and then shows the battle screen.
- When attacking an NPC, the NPC now has a chance of dodging the attack. (1 in 6 chance.)
- When an NPC attacks you, you now have a 1 in 6 chance of dodging the attack.
- Reworked a ton of NPC code so that I can now assign multiple NPCs to each chunk.
- Renamed TestNPC to Werewolf and assigned 6 to Map 3 and 4 to map 11. This is due to the storyline.
- Added Old Man NPC and assigned to Map 2. He teaches you how to build and furthers your journey.
- Modified Mr. Smiler chat and Welcome message.
- Added Jared's Wife and assigned to Map 6. She tells you Jared's missing and to go kill some werewolves.
- Modified Werewolves HP to now be 8. They may now be killed by hand. I've also modified their attack to 4, so that you don't die so often.
- Fixed a bunch of bugs with Combat.
- Added Calem and assigned to Map 11. He tells you to go see Bjorvik, because punching werewolves is detrimental to your health. ;)
- Should have fixed Windows saying that PythianRealms is "Not Responding" even when it was after around 15 minutes. I suspect the issue to be the PyGame Event Queue filling up, and so PythianRealms will now clear unused events.
- Added Bjorvik and assigned to Map 3. He teaches you how to craft. So far this is as far as the storyline goes, but expect a ton more updates expanding the Storyline!

0.5.3 -> 0.5.4:
- Completely rebuilt combat from the ground up. It used to be hack and slash combat, however I have instead chosen to replace it with a turn-based combat system. This new system allows me to then create actions, such as Attack and Escape. It then allows me to make potions, etc. work in combat, when I add them. It features a completely new fully thought-out UI, featuring explanations on what goes on and a 6x upscaled image of the enemy.
- Added accounts. Now, if a player who has never been on the server before connects, it will create a savefile for that player which will then be used to save their password and server rank.
- Added server ranks. You can now be either "NORM" or "MOD". A NORM user will be a normal player - they cannot kick people and do not have the abilities of moderation that I will be adding later. A MOD user currently has the ability to use the kick command.
- Added passwords. However, the server never sees your raw password - the password is encoded by the Client and then compared with the server's encoded password. If they match, you join the server. If not, you get "isolated" from the rest of the server, and then your client crashes since you don't get keepalive statements. :P
- Added kick command. It uses the format "kick!<name>", and requires the user to be a MOD to use it. Since hitting ! on your keyboard inputs | (since ! is a server separator statement so I had to find an alternative), you would have to hit INSERT to input a !. Don't use that, it's a pain on the server since it splits at them :P
- Added password section to the multiplayer login. NOTE: If a server owner finds out your password by decoding, I am not responsible. I have gone through all the neccessary security measures, but you should use a different password for everything. Thanks.

0.5.2 -> 0.5.3:
- Fixed glitch in which everyone was called the same thing.
- Improved disconnect message. It no longer shows an error upon a client disconnecting.
- Server now shows who is who... I hope I explained that well enough. :P
- Fixed the game calling walking and talking chunk modifications.
- Cut down on useless code hindering development.

0.5.1 -> 0.5.2:
- Fixed really bad server-client connection bugs. When a client disconnected, chat ceased - I've fixed it now.
- Fixed character disappearing when entering text.
- Fixed Player HP showing "20.99999999999%" (for example.)
- Added Graphical UI for connecting to a server. Note that you have to click the box you want to set (such as Address), enter the details by typing (they should be displayed as you type) and then hit enter to "set" the box. Not hitting enter will result in PythianRealms getting confused...
- Added username functionality. When you now enter connection details, it offers you the ability to set a username. NOTICE: usernames are for chat labels. Not entering a username will result in PythianRealms sending your local IP address to the server, as if it was a username... As such, your computer's local IP would be displayed to all whenever you chatted.
- The server now announces to all online players whenever a player joins or leaves.


0.5 -> 0.5.1:
- Inventory now uses one file named "inv.pr" in the data folder.
- Optimized Smooth Walking. Now has a super small impact on your frames per second rate when in use! :D
- Optimized Seamless Tiles. Smooth walking and Seamless tiles enabled at the same time now has less of an FPS impact that Seamless Tiles made on its own!
- Fixed crash when going into fullscreen.
- Fixed walking on top of layer 2&3 blocks.
- Beginnings of chat. Singleplayer *sort of* has chat if you press enter and type messages, then press enter again... But this is mainly for preparation of multiplayer.
- Talking to NPCs now uses the Left ALT button, rather than the enter key.
- NPCs now add messages to the "chat bar" at the bottom of the screen that was added previously.
- Added the beginnings of multiplayer! Chat...

0.4.9 -> 0.5:
- Game goes to Menu when you press the X button.
- Added smooth walking. Animated walking isn't quite in yet, but this is a base. Thus far, the character smoothly glides over to the next tile of the map.
- Fixed loading of player position. I had forgotten to fix the fact that I moved the location files to the data/ directory.
- Gold Sword now takes only 15 hp from the enemy, and fists only take 2 hp.
- PythianRealms will now log Operating System to log output for better debugging. This will later be enhanced for running OS-specific codes.
- Added option for Smooth Walking in the Options Menu.
- Smooth Walking and Seamless Tiles are automatically disabled if there is less than 1 GB of RAM allocated for PythianRealms' use.
- NPCs' health now saves and loads.

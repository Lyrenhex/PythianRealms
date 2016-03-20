Changelog:



2016.:
- Removed "Scratso Presenting" screen
- Added "Scratso Games" animation to the start.
- Inside pickup/placement modes, layers above the current Z Axis are now hidden. This should make building significantly less confusing.
- When a block is placed, that block is now shown at the top, rather than underneath all other blocks. Potentially confusing if you build multiple layers in the same build run...
- Optimised shownz list -- it is generated each time with only the visible layers, rather than generating the whole list of layers and removing the hidden ones.

2016.168:

- Slightly improved layer rendering.


- Music is now zipped up (extracted on game launch and temp files deleted on game quit like texture files).
- Added seven new PROTODOME tracks from the BLUESCREEN album.
- Added seven new PROTODOME tracks from the BLUENOISE album.
- Changed Credits slightly.
- Updated PythianRealms logo.
- Refined NPCs.
- Removed quality cycling. It is possible to manually change the com.scratso.pr.variables file to change the quality. (com.scratso.pr.variables => com/scratso/pr/variables.py)
- Increased Z-Axis Limit to 30.
- Automated mouse click shop/inv events, which cut the source down a tonne.
- Added price tags to shop, where "c" is coins.
- Increased size of inventory and shop. They can now support up to 144 different blocks, rather than just 36.
- Corrected physics for water and lava - The player is no longer Jesus.
- Added healing, at a rate of 1 hp per second.
- Nudged a bit of debug info around.
- Started work on a debug command terminal for the game. Currently includes the additem and setactive commands. Example: "additem 1 10" without quotes will give you 10 dirt (item id 1), and "setactive 2" will set the active item to grass (item id 2). NOTE: Although item id 11 is valid, item id 10 is NOT. Entity #10 is air, which is not a valid inventory item, and so adding it to your inventory or attempting to place it will result in an error.
- Pressing F2 now toggles fullscreen. (Fullscreen will go to the best size possible for the screen you're on, but won't always fill the screen.)
- Slightly optmized map rendering, as unchanged layers after pickup and placement will no longer be re-rendered unnecessarily.
- Nudged each layer up by 16 pixels, so now the bottom layer's sides are shown.
- Corrected the album image for "Short but Sweet"
- Added a blue overlay when walking in water.

2016.147:

- Updated staff list.

- Menu logo changed to the 2016 edition.

- Game title is now "PythianRealms 2016".

- Improved menu layout.

- Fixed issue where boosts wouldn't be given while in the menu.

- Fixed issue where pressing the "X" button in the menu wouldn't do anything.

- Fixed issue where music would not continuously play while in the menu.



2016.140:

- Fixed issue with sharing maps. (ref: #25)

- Fixed some issues with the Scratso.com integration.

- Added /nsid NickServ identification command. (ref: #26)



2016.137:

- Integrated chatbox into the game more, as shop "not enough money" notifications are now displayed there.

- Added a "too far away" notice if you're too far away for a melee attack.

- Fixed issue where npcs would not die at 0% health. (ref: #24)

- Probably fixed boost bug where the boost wouldn't be given. It appears to be that if you lag and it skips over 0 seconds left, it will just keep counting down, checking for exactly 0. Changed == to <= to account for this. (ref: #23)

- Added Scratso.com account integration to add user security. (ref: #22)

-- GitHub Commit --



2016.132:

- Updated "Scratso" intro screen

- Increased ping timeout minimum time, to hopefully counteract the random connection losses (ref: #20)

- Fixed issue where Credits and Import Map buttons would both light up when you hovered oer the Credits button on the ingame menu (ref: #19)

- Fixed some issues with the chat system. Will be doing more work on this in future (ref: #14)

- Added players online notice when you join chat

- Added /who command to chat, which tells you who's online

- Added /help command to chat, which opens a help page

- Added F1 button, which opens a help page
- Slightly optimised event handler

- Fixed issue where shop and inventory could not show

- Increased Z-Axis Limit to 10 (because 4 levels for a release software is bad...) -- the map catalog has been cleared to prevent errors arising from out-of-date maps

- Removed logging message from the chat welcome message



Beta.120:

- Added sand.

- Improved island template for map generation

- Added "Scratso" Intro screen

-- GitHub Commit --

- Reorganised texture packs has resulted in some code changes...

- Removed some dead items

-- GitHub Commit --

- Added "micro-terminal" for license stuff before starting the game

- Added alpha/beta messages

- Finally added a .gitignore

- Created Map Catalog at http://scratso.com/datastore/pythianrealms/maps

- Added "Share Map" button to ingame menu, which will upload the map to the catalog

- Added "Get Maps" button to ingame menu, which opens the catalog

- Added "Import Map" button to ingame menu, which will import a downloaded map (overwriting your current map)

-- GitHub Commit --

- Improved workspace layout

- Should now have fixed issue #9

- Improved documentation (see #15)

-- GitHub Commit --


SETTING UP A COMPETITION VERSUS SPARBOT ON POKER ACADEMY.


STEP 1: Unzip plugin.zip
STEP 2: Change to the directory plugin
STEP 3: Run compile.bat 
STEP 4: Place plugin\AAAIBot.pd and plugin\aaaibot.jar in ...\PokerAcademy\data\bots
STEP 5: Start Poker Academy Pro, Version 2.5.
STEP 6: Press Ctrl-O to open the Opponent Manager.
STEP 7: Click on "Import New Player", third icon down on the left hand side of the opponent
manager.
STEP 8: Select PokerAcademy\data\bots\AAAIBot.pd from the Open dialog.
STEP 9: Close the Opponent Manager.
STEP 10: Click on "RING GAMES".
STEP 11: Click on "Create a new table", the top icon on the left hand side of the ring game
screen.
STEP 12: On the right hand side, there are seats. Right click on the second seat, 
second column, and a list of bots will show up. Click on AAAIBot->AAAIBot.
STEP 13: Right click on the sixth seat, second column, and click on Sparbot->Sparbot (or whatever 
opponent you wish to face.
STEP 14: Change the title of the table to "AAAI CPC Table" or whatever you want.
STEP 15: Save the table with the disk icon in the top right-hand corner.
STEP 16: The new name will appear on the left hand side. Double-click on this name.
STEP 17: Right click on the human in seat 1 and set his bankroll to zero, 
making this a bot table.
STEP 18: Under Options->Animation and Sound, turn off all animation and sound, and under
Options->Edit Throttle, switch the throttles to zero, but leave the check boxes unchecked
(otherwise, some opponents might have degraded performance).
STEP 19: Set the bankrolls of AAAIBot and Sparbot to 1,000,000.
STEP 20: Under Options, make sure Auto Deal is checked.
STEP 21: Press "Deal Hand" in the bottom middle.
STEP 22: A dialog called AAAI Bot Startme will show up. Find the startme.bat of your entry into 
the competition and select it.

STEP 23: Let the process run for about a few days. The standard deviation is about 6 small
bets/hand, so in order to determine your performance to within a few hundredths of a small
bet, you need to observe at least 100,000 hands. After 10,000 hands, you will have an idea
within a few tenths of a small bet.

STEP : After they have played for a while, right-click on AAAIBot's seat and click on 
"Statistics for AAAIBot". This has a variety of statistics about your bot.
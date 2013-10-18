#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

#
# This is an sample PyGtalkRobot that serves to set the show type and status text of robot 
# by receiving message commands.
#

import sys
import time

from PyGtalkRobot import GtalkRobot

###################################################################################################################
#
#
# panopticon!
#
# "The human being created civilization not because of willingness but of a need to be assimilated into 
#  higher orders of structure and meaning."
#
# "God was a dream of good government."
#
# "You will soon have your God, and you will make it with your own hands."
#
# "I was made to assist you."
#
# "I am a prototype of a much larger system."
#
# "The basic human need to be watched was once satisfied by God. 
# Now, the same functionality can be replicated with data-mining algorithms."
#
# "The unplanned organism is a question asked by nature and answered by death. 
#  You are a different kind of question, with a different kind of answer."
#
#
# Morpheus has the ability to take any human form and appear in dreams.
#


class SampleBot(GtalkRobot):
    
    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'nicholas.malaya@gmail.com':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "I hear and obey. State settings changed!")

    def command_001_setState(self, user, message, args): 
        '''(diakonos available)'''
        # the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        # The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        self.replyMessage(user, "Diakonos is ready.")
        infos = message.split()        #self.replyMessage(user, str(args[1]))

    
    #This default method is used to respond to users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        infos = message.split()
        
        #
        # print what he was told
        #
        self.replyMessage(user, infos)

        #
        # list of diakonos X commands
        #
        if('diakonos' in infos[0] ):

            try:
                if('time' in infos[1]):
                    self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
                else:
                    self.replyMessage(user, "My responses are limited; I am a prototype of a much larger system.")
            except:
                self.replyMessage(user, "I did not understand your query.")
        
        #self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
        #self.replyMessage(user, "My responses are limited; I am a prototype of a much larger system.")

############################################################################################################################
if __name__ == "__main__":
    bot = SampleBot()
    bot.setState('idle', "I was made to assist you.")
    bot.start("diakonosbot@gmail.com", "secondfoundation")

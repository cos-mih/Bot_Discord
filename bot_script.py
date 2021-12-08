#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.



 #!./.venv/bin/python

import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random
import os
from discord.channel import VoiceChannel       # dumb random number generator

from discord.ext import commands    # Bot class and utils

################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################

# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}
def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }

    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }

    # get information about call site
    caller = inspect.stack()[1]

    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return

    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))

################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################

playlist = {
    'strut.mp3',
    'jumpinjacks.mp3', 
    'cowboylikeme.mp3' 
}

# bot instantiation
bot = commands.Bot(command_prefix='!')

# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')

# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    if msg.author == bot.user:
        return
    
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')

    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_commands(msg)
    #code.interact(local=dict(globals(), **locals())) 

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return 
    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')

    await ctx.send(random.randint(1, max_val))

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))

#command for joining voice channel
@bot.command(brief="Join voice channel")
async def join(ctx):
    await ctx.send('Okok')
    channel = ctx.author.voice.channel
    await channel.connect()
#disconnect command
@bot.command(brief="Disconnect from voice channel")
async def scram(ctx):
    await ctx.send("Ok bye then")
    await ctx.voice_client.disconnect()
#command for playing songs
@bot.command(brief='Plays songs')
async def play(ctx,song):
    if not ctx.message.author.voice:
        await ctx.send("Not yet on a voice channel I see".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.send("Your wish is my command!")
        await channel.connect()
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            if song in playlist:
                async with ctx.typing():
                    voice_channel.play(discord.FFmpegPCMAudio(song))
                await ctx.send('Jammin to ' + song)
            else :
                await ctx.send("Try something else")
        except :
            await ctx.send("Not much going on at the moment")
#listing songs
@bot.command(brief="Lists all songs that can be played")
async def list(ctx):
    await ctx.send("These songs are available:")
    for song in playlist:
        await ctx.send (song)
#command for stopping the music
@bot.command(brief="Stops current song")
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    voice.stop();       
       



############################################################################################################ PROGRAM ENTRY POINT ##############################
################################################################################

if __name__ == '__main__':
    # check that token exists in environment
    if 'BOT_TOKEN' not in os.environ:
        log_msg('save your token in the BOT_TOKEN env variable!', 'error')
        exit(-1)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--token", help="add bot token")
args = parser.parse_args()
if args.token:
        BOT_TOKEN=args.token
        bot.run(['BOT_TOKEN'])
else:
	bot.run(os.environ['BOT_TOKEN'])

    # launch bot (blocking operation)
	bot.run(os.environ['BOT_TOKEN'])
    


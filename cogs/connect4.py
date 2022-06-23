import asyncio
import discord
from game import Game, MoveError
from discord.ext import commands

class Connect4(commands.Cog):
    DIGITS = [str(i) + '\u20E3' for i in range(1, 8)]
    CROSS = '❌'
    TIMEOUT = 60
    PLAYERS = set()

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def play(self, ctx, player2: discord.Member=None):
        player1 = ctx.author
        if player2 is None:
            player2 = ctx.author
        
        if player1 in self.PLAYERS and player2 in self.PLAYERS:
            if player1 == player2:
                await ctx.send(f'{player1.display_name} is already in a game')
            else:
                await ctx.send(f'{player1.display_name} and {player2.display_name} are already in games')
            return
        if player1 in self.PLAYERS:
            await ctx.send(f'{player1.display_name} is already in a game')
            return
        if player2 in self.PLAYERS:
            await ctx.send(f'{player2.display_name} is already in a game')
            return
        
        self.PLAYERS.add(player1)
        self.PLAYERS.add(player2)

        game = Game()
        player = 0
        message = await ctx.send(str(game))
        
        for digit in self.DIGITS:
            await message.add_reaction(digit)
        await message.add_reaction(self.CROSS)

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=self.TIMEOUT, check=None)
                if user == self.client.user:
                    continue
            except asyncio.TimeoutError:
                await ctx.send('TIMEOUT, GAME STOPPED')
                break
                
            await asyncio.sleep(0.1)
            try:
                await message.remove_reaction(reaction, user)
            except Exception:
                pass
            
            if str(reaction) == self.CROSS and user in (player1, player2):
                await ctx.send('GAME STOPPED')
                break
            
            try:
                if user == (player1, player2)[player]:
                    game.make_move(column=self.DIGITS.index(str(reaction)), player=player)
                    player = 1 - player
            except (ValueError, MoveError):
                pass

            await message.edit(content=str(game))

            status = game.status()
            match status:
                case 'PLAYER1' | 'PLAYER2':
                    if player1 == player2:
                        await ctx.send(f'{status} WON!')
                    else:
                        await ctx.send(f'{player1.display_name if status == "PLAYER1" else player2.display_name} WON!')
                    break
                case 'TIE':
                    await ctx.send(f'TIE!')
                    break
                case 'CONTINUE':
                    pass
        try:
            self.PLAYERS.remove(player1)
            self.PLAYERS.remove(player2)
        except KeyError:
            pass
    
def setup(client):
    client.add_cog(Connect4(client))

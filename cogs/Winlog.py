import discord
from discord.ext import commands, tasks
import aiohttp

class WinLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None
        self.last_game = None

    @commands.group(invoke_without_command=True)
    async def winlog(self, ctx):
        await ctx.send("Usage: !winlog start | !winlog stop")

    @winlog.command()
    async def start(self, ctx):
        self.channel_id = ctx.channel.id

        if not self.check_logs.is_running():
            self.check_logs.start()

        await ctx.send("✅ Win log started.")

    @winlog.command()
    async def stop(self, ctx):
        if self.check_logs.is_running():
            self.check_logs.cancel()

        await ctx.send("🛑 Win log stopped.")

    @tasks.loop(seconds=1)
    async def check_logs(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://territorial.io/log/team-games"
                ) as resp:
                    text = await resp.text()

            newest = text.split("\n\n")[0]

            if newest == self.last_game:
                return

            self.last_game = newest

            if "Winning Clan:  [WAVE]" in newest:
                channel = self.bot.get_channel(self.channel_id)

                if channel:
                    await channel.send(
                        f"🏆 **WAVE WIN DETECTED!**\n```{newest}```"
                    )

        except Exception as e:
            print("WinLog Error:", e)

async def setup(bot):
    await bot.add_cog(WinLog(bot))

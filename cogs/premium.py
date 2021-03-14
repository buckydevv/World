import patreon
from discord.ext import commands
from os import environ

__import__("dotenv").load_dotenv()

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = environ["PREMIUM_SECRET"]
        self.creator_token = environ["CREATOR_TOKEN"]
        self.api_client = patreon.API(self.creator_token)
        self.campaign_response = self.api_client.fetch_campaign()
        self.campaign_id = self.campaign_response.data()[0].id()
        self.pledges = []
        self.cursor= None


    @commands.command()
    async def wow(self, ctx):
    	for result in self.api_client.fetch_page_of_pledges(self.campaign_id, 25, cursor=self.cursor, fields={'pledge': ['total_historical_amount_cents', 'declined_since']}):
    		await ctx.send(result)

def setup(bot):
    bot.add_cog(Premium(bot))
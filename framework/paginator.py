from time import time

class Paginator:
    def __init__(
        self,
        ctx,
        embeds: list,
        ratelimit: int = 1,
        max_time: int = 20,
        next_emoji: str = "▶️",
        previous_emoji: str = "◀️",
        start_emoji: str = "⏮",
        end_emoji: str = "⏭",
        close_emoji: str = "❌",
        show_page_count: bool = False,
        auto_set_color: bool = False
    ):
        
        self.embeds = embeds
        if auto_set_color:
            for embed in self.embeds:
                embed.color = ctx.me.color
        if show_page_count:
            _embed_index = 1
            for embed in self.embeds:
                embed.set_author(name=f"Page {_embed_index}/{len(embeds)}")
                self.embeds[_embed_index - 1] = embed
                _embed_index += 1
        self.ctx, self.max_time, self.ratelimit, self.index, self.last_reaction, self.max = ctx, max_time, ratelimit, 0, time(), len(embeds)
        self.valid_emojis = (start_emoji, previous_emoji, close_emoji, next_emoji, end_emoji)
        self.check = (lambda reaction, user: (str(reaction.emoji) in self.valid_emojis) and (user == self.ctx.author))
    
    def __del__(self):
        """ Let the object kill itself first before getting deleted. """
        del self.ctx, self.max_time, self.ratelimit, self.index, self.last_reaction, self.max
        del self.valid_emojis, self.check
        del self.embeds
    
    async def resolve_reaction(self, reaction):
        current_time = time()
        if (current_time - self.last_reaction) <= self.ratelimit:
            return
        self.last_reaction = current_time
        if (str(reaction.emoji) == self.valid_emojis[0]) and self.index: self.index = 0
        elif (str(reaction.emoji) == self.valid_emojis[1]) and self.index: self.index -= 1
        elif (str(reaction.emoji) == self.valid_emojis[2]):
            await self.delete()
            return -1
        elif (str(reaction.emoji) == self.valid_emojis[3]) and (self.index < (self.max - 1)): self.index += 1
        elif (str(reaction.emoji) == self.valid_emojis[4]) and (self.index < (self.max - 1)): self.index = (self.max - 1)
        else: return
        await self.message.edit(content='', embed=self.embeds[self.index])

    async def execute(self):
        self.message = await self.ctx.send(embed=self.embeds[0])
        for i in self.valid_emojis:
            await self.message.add_reaction(i)
        
        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for("reaction_add", timeout=self.max_time, check=self.check)
                resolve = await self.resolve_reaction(reaction)
                assert resolve != -1
                del reaction, user, resolve
            except:
                break

    async def delete(self):
        if not hasattr(self, "message"):
            raise TypeError("Message has not been sent.")
        return await self.message.delete()
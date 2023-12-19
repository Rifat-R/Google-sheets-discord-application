import disnake
import asyncio
import datetime
import random
from settings import config

class GiveawayModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Duration",
                placeholder="E.g 10 Minutes",
                custom_id="duration",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Number of winners",
                placeholder="E.g 1",
                custom_id="num_of_winners",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Prize",
                custom_id="prize",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Description",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create a Giveaway", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Giveaway!", colour = config.EMBED_COLOUR)
        user = inter.author
        channel = inter.channel
        items = dict(inter.text_values.items())
        duration = items.get("duration").lower()
        num_of_winners = items.get("num_of_winners")
        prize = items.get("prize")
        description = items.get("description")

        try:
            num_of_winners = int(num_of_winners)
        except ValueError as e:
            await inter.response.send_message(f"You entered text inside the `Number of winners` section. Please try again.", ephemeral=True)
            print(str(e))
            return

        # Split input into quantity and unit
        duration = duration.split()
        if len(duration) != 2:
            await inter.response.send_message(f"You have not written the duration in a correct format. Please try again.", ephemeral=True)
            return

        try:
            quantity = int(duration[0])
        except ValueError as e:
            print(str(e))
            await inter.response.send_message(f"You have written the quantity of your duration wrong. Please try again.", ephemeral=True)
            return
        unit = duration[1]

        if not unit.endswith("s"):
            unit += "s"

        # Create timedelta object based on user input
        if unit == "seconds":
            delta = datetime.timedelta(seconds=quantity)
        elif unit == "minutes":
            delta = datetime.timedelta(minutes=quantity)
        elif unit == "hours":
            delta = datetime.timedelta(hours=quantity)
        elif unit == "days":
            delta = datetime.timedelta(days=quantity)
        elif unit == "weeks":
            delta = datetime.timedelta(weeks=quantity)
        else:
            # raise ValueError("Invalid duration unit")
            await inter.response.send_message(f"Invalid duration unit. Please use `seconds, minutes, hours, days, weeks` and try again.", ephemeral=True)
            return

        # Get current datetime
        now = datetime.datetime.now()

        # Add the timedelta object to the current datetime to get the resulting datetime
        result = now + delta
        timestamp = int(datetime.datetime.timestamp(result))
        relative_seconds = delta.total_seconds()

        embed.add_field(name = f"End of giveaway", value = f"<t:{timestamp}:R> (<t:{timestamp}:F>)", inline=False)
        embed.add_field(name = f"Hosted by", value = f"{user.mention}", inline=False)
        embed.add_field(name = f"Prize", value = f"{prize}", inline=False)
        embed.description = description
        msg:disnake.Message = await channel.send(embed=embed)
        await inter.response.send_message(f"Created giveaway successfully.", ephemeral=True)
        await msg.add_reaction("🎉")
        print(f"Giveaway going to sleep for {relative_seconds}")
        await asyncio.sleep(relative_seconds)
        new_msg = await channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(new_msg.author))
        print(users)
        if len(users) == 0:
            await channel.send(f"No one has won the giveaway due to no one participating :(")
            return
        if num_of_winners > len(users):
            num_of_winners = len(users)
        winner = random.sample(users, k=num_of_winners)
        await new_msg.reply(f"{winner.mention} won {prize}. Congratulations!")

    # async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
    #     await inter.response.send_message(f"An error occurred!\n```{error}```", ephemeral=True)

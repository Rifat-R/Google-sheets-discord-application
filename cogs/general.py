import disnake
from disnake.ext import commands
from disnake.ui import Select, View
from utils import modal, util_buttons, giveaway_modal, funcs
import asyncio
from settings import config
import datetime
import pytz

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def create_giveaway(self, inter:disnake.CommandInteraction):
        await inter.response.send_modal(giveaway_modal.GiveawayModal())

    @commands.slash_command()
    async def create_poll(self, inter:disnake.CommandInteraction,
                          title:str,
                          options:str,
                          description:str,
                          anonymous:commands.option_enum(["True","False"]),
                          image_url:str = None,
                          role_mention:disnake.Role = None):
        # await inter.response.send_modal(modal.PollModal())
        await inter.send(f"You successfully created a poll!", ephemeral=True)
        channel = inter.channel
        description = description + "\n\n"
        if anonymous == "True":
            anonymous = True
        if anonymous == "False":
            anonymous = False

        user = inter.author

        embed = disnake.Embed(title = f"{title}", colour=config.EMBED_COLOUR)
        embed.set_image(url = image_url)
        options = options.split(",")
        buttons = []
        if isinstance(options, list) is False:
            await inter.send(f"You must enter options seperated by commas.", ephemeral=True)
            return

        description_template = lambda index, option_name, percentage, votes: f"{index}) {option_name} | {percentage}% ({votes})\n"
        description_vote_section = ""
        for index, option in enumerate(options):
            description_vote_section+=description_template(index+1, option, 0, 0)
            buttons.append(util_buttons.PollButton(index+1, anonymous))


        embed.description = description + description_vote_section

        view = disnake.ui.View(timeout=None)

        for button in buttons:
            view.add_item(button)

        if anonymous is False:
            view.add_item(util_buttons.VotersButton())


        msg = await channel.send(role_mention,embed=embed, view=view)
        while True:
            await asyncio.sleep(2)
            votes = [i.vote_counter for i in buttons]
            total_votes = sum(votes)
            if total_votes != 0:
                new_vote_section = ""
                for index, option in enumerate(options):
                    new_vote_section += description_template(index+1, option, round((votes[index]/total_votes)*100,2), votes[index])

                if new_vote_section != description_vote_section:
                    embed.description = description + new_vote_section
                    await msg.edit(embed=embed)
                    description_vote_section = new_vote_section
                    print(f"Edited poll")

    @commands.slash_command()
    async def lend(self, inter:disnake.CommandInteraction):
        await inter.response.send_modal(modal.LendModal())

    @commands.slash_command()
    async def event(self, inter:disnake.CommandInteraction,
                    title:str,
                    date,
                    time,
                    description: str,
                    duration:commands.Range[1,...],
                    channel:disnake.TextChannel,
                    image=None,
                    on_create_mention:disnake.Role=None,
                    on_start_mention:disnake.Role=None):

        """
        Create an event.

        Parameters
        ----------
        title: text, event title
        date: The date that the event will take place e.g. 22/04/2023 OR Time till event e.g. 5 weeks
        time: The time the event will take place e.g 14:00
        description: text, describe the event
        duration: in hours
        channel: @channel to post to
        image: link to display image in channel
        on_create_mentions: @role to mention
        on_start_mentions: @role to mention
        """

        # Considering date is in dd/mm/yyyy format
        dt_string = date + " " + time
        duration = int(duration)
        if "/" not in date:
            print("nice")
            date = date.split(" ")
            quantity = int(date[0])
            unit = date[1].lower()
            if "week" in unit:
                timestamp = datetime.datetime.now() + datetime.timedelta(weeks=quantity)
            if "day" in unit:
                timestamp = datetime.datetime.now() + datetime.timedelta(days=quantity)
            if "hour" in unit:
                timestamp = datetime.datetime.now() + datetime.timedelta(hours=quantity)
        else:
            timestamp = datetime.datetime.strptime(dt_string, "%d/%m/%Y %H:%M")

        formatted_datetime = timestamp.strftime("%A, %d %B %Y %H:%M %I:%M %p")
        print(timestamp)
        unix_timestamp = round(datetime.datetime.timestamp(timestamp))
        diff_dt = timestamp - datetime.datetime.now()
        print(diff_dt)
        diff_seconds = diff_dt.total_seconds()

        # convert the UTC datetime object to datetime objects in each time zone
        est_dt = timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern')).strftime("%A, %d %B %Y %H:%M %I:%M %p")
        cst_dt = timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Central')).strftime("%A, %d %B %Y %H:%M %I:%M %p")
        mst_dt = timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Mountain')).strftime("%A, %d %B %Y %H:%M %I:%M %p")
        pst_dt = timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Pacific')).strftime("%A, %d %B %Y %H:%M %I:%M %p")



        embed = disnake.Embed(title = title, description=description, color = config.EMBED_COLOUR)
        embed.set_image(url = image)
        embed.add_field(name = "Time", value = f"`{formatted_datetime}` (UTC)", inline=False)
        embed.add_field(name = "Duration", value = f"{duration} {'hour' if duration == 1 else 'hours'}", inline=False)
        if on_create_mention != None:
            msg = await channel.send(on_create_mention.mention, embed=embed)
        else:
            msg = await channel.send(embed=embed)
        timezone_embed = disnake.Embed(title = f"Converted Timezones", color = config.EMBED_COLOUR)
        timezone_embed.add_field(name = f"EST", value = f"`{est_dt}`", inline=False)
        timezone_embed.add_field(name = f"MST", value = f"`{cst_dt}`", inline=False)
        timezone_embed.add_field(name = f"CST", value = f"`{mst_dt}`", inline=False)
        timezone_embed.add_field(name = f"PST", value = f"`{pst_dt}`", inline=False)
        await msg.reply(embed=timezone_embed)
        await inter.send(f"Created event successfully.", ephemeral=True)
        print(diff_seconds)
        if on_start_mention != None:
            await asyncio.sleep(diff_seconds)
            await msg.reply(on_start_mention.mention)


    @commands.slash_command()
    async def role_chooser(self, inter:disnake.CommandInteraction):
        guild = inter.guild
        channel = inter.channel
        attack_role = guild.get_role(config.ATTACK_ROLE_ID)
        strength_role = guild.get_role(config.STRENGTH_ROLE_ID)
        defence_role = guild.get_role(config.DEFENCE_ROLE_ID)
        ranged_role = guild.get_role(config.RANGED_ROLE_ID)
        prayer_role = guild.get_role(config.ATTACK_ROLE_ID)

        select = Select(
            placeholder="Click here ->",
            options = [
                disnake.SelectOption(label = "99 Attack", value = "attack", emoji = config.ATTACK_ROLE_EMOJI),
                disnake.SelectOption(label = "99 Strength", value = "strength", emoji = config.STRENGTH_ROLE_EMOJI),
                disnake.SelectOption(label = "99 Defence", value = "defence", emoji = config.DEFENCE_ROLE_EMOJI),
                disnake.SelectOption(label = "99 Ranged", value = "ranged", emoji = config.RANGED_ROLE_EMOJI),
                disnake.SelectOption(label = "99 Prayer", value = "prayer", emoji = config.PRAYER_ROLE_EMOJI),
            ]
        )
        async def my_callback(interaction:disnake.CommandInteraction):
            user = interaction.author
            if select.values[0] == "attack":
                await user.add_roles(attack_role)
                await interaction.response.send_message(f"You have been given the {attack_role.mention} role.", ephemeral=True)
            if select.values[0] == "strength":
                await user.add_roles(strength_role)
                await interaction.response.send_message(f"You have been given the {strength_role.mention} role.", ephemeral=True)
            if select.values[0] == "defence":
                await user.add_roles(defence_role)
                await interaction.response.send_message(f"You have been given the {defence_role.mention} role.", ephemeral=True)
            if select.values[0] == "ranged":
                await user.add_roles(ranged_role)
                await interaction.response.send_message(f"You have been given the {ranged_role.mention} role.", ephemeral=True)
            if select.values[0] == "prayer":
                await user.add_roles(prayer_role)
                await interaction.response.send_message(f"You have been given the {prayer_role.mention} role.", ephemeral=True)

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed = disnake.Embed(title = f"If you have 99 in one or more skills, please react accordingly.")
        await channel.send(embed=embed, view=view)
        await inter.send(f"Successfully sent role chooser selection!", ephemeral=True)


def setup(bot):
    bot.add_cog(General(bot))

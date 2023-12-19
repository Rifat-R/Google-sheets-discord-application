import disnake
import asyncio
from utils import google_sheet
from settings import config

class Modal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="Foo Tag",
                custom_id="name",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create Tag", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Tag Creation", colour = config.EMBED_COLOUR)
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        await inter.response.send_message(embed=embed)






class PollButton(disnake.ui.Button):
    voters = []
    def __init__(self, label):
        super().__init__(label=label, style = disnake.ButtonStyle.blurple)
        self.vote_counter = 0

    async def callback(self, interaction:disnake.CommandInteraction):
        user = interaction.author
        if user in self.voters:
            await interaction.send(f"You already voted!", ephemeral=True)
            return
        self.voters.append(user)
        self.vote_counter += 1
        await interaction.send(f"Thank you for voting!", ephemeral=True)



class PollModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Title",
                custom_id="title",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Options",
                placeholder="E.g Dogs, Cats, Bird",
                custom_id="options",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            # disnake.ui.TextInput(
            #     label="Single Vote",
            #     placeholder="True/False",
            #     custom_id="single_vote",
            #     style=disnake.TextInputStyle.short,
            #     max_length=50,
            # ),
            disnake.ui.TextInput(
                label="Anonymous",
                placeholder="True/False",
                custom_id="anonymous",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Image URL",
                custom_id="image_url",
                style=disnake.TextInputStyle.short,
                max_length=200,
            ),
            disnake.ui.TextInput(
                label="Description",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create Poll", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        await inter.send(f"You successfully created a poll!", ephemeral=True)
        channel = inter.channel
        items = dict(inter.text_values.items())
        title = items.get("title")
        options = items.get("options")
        print(options)
        single_vote = items.get("single_vote")
        anonymous = items.get("anonymous")
        image_url = items.get("image_url")
        print(image_url)
        description = items.get("description") + "\n\n"

        user = inter.author

        embed = disnake.Embed(title = f"{title}", colour = config.EMBED_COLOUR)
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
            buttons.append(PollButton(index+1))

        embed.description = description + description_vote_section

        view = disnake.ui.View()
        for button in buttons:
            view.add_item(button)

        msg = await channel.send(embed=embed, view=view)
        while True:
            await asyncio.sleep(2)
            votes = [i.vote_counter for i in buttons]
            print(votes)
            total_votes = sum(votes)
            print(total_votes)
            if total_votes != 0:
                new_vote_section = ""
                for index, option in enumerate(options):
                    new_vote_section += description_template(index+1, option, round((votes[index]/total_votes)*100,2), votes[index])

                if new_vote_section != description_vote_section:
                    embed.description = new_vote_section
                    await msg.edit(embed=embed)
                    description_vote_section = new_vote_section
                    print(f"Edited poll")


class LendModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Name1",
                placeholder="Who is lending?",
                custom_id="name1",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Name2",
                placeholder ="The person borrowing the item",
                custom_id="name2",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Item",
                placeholder="The item being lent",
                custom_id="item",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Collateral",
                placeholder="The collateral being collected",
                custom_id="collateral",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Duration",
                placeholder="Date picker or type format of date month/day/year",
                custom_id="duration",
                style=disnake.TextInputStyle.short,
                max_length=50
            )
        ]
        super().__init__(title="Lend post to Google Sheet", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        channel = inter.channel
        user = inter.author
        items = dict(inter.text_values.items())
        name1 = items.get("name1")
        name2 = items.get("name2")
        item = items.get("item")
        collateral = items.get("collateral")
        duration = items.get("duration")
        await google_sheet.update_sheet(config.GOOGLE_SHEET_NAME, name1, name2, item, collateral, duration)
        await inter.response.send_message(f"Successfully updated the google sheet.", ephemeral=True)

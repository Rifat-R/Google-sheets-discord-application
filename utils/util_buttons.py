import disnake
from settings import config

class PollButton(disnake.ui.Button):
    voters = []
    vote_dict = {}
    def __init__(self, button_name, anonymous = False):
        super().__init__(label=button_name, style = disnake.ButtonStyle.blurple)
        self.vote_counter = 0
        self.vote_dict[str(button_name)] = []

    async def callback(self, interaction:disnake.CommandInteraction):
        user = interaction.author
        # if user in self.voters:
        #     await interaction.send(f"You already voted!", ephemeral=True)
        #     return
        self.voters.append(user)
        self.vote_counter += 1
        self.vote_dict[str(self.label)].append(str(user))
        print(self)
        print(self.vote_dict)
        await interaction.send(f"Thank you for voting!", ephemeral=True)


class VotersButton(disnake.ui.Button):
    vote_dict = PollButton.vote_dict
    def __init__(self):
        super().__init__(label="Voters", style = disnake.ButtonStyle.blurple)

    async def callback(self, interaction:disnake.CommandInteraction):
        print(self.vote_dict)
        button_names = list(self.vote_dict.keys())
        embed = disnake.Embed(title = f"Voters list", description = "Please choose an option from the poll",color = config.EMBED_COLOUR)
        select = disnake.ui.Select(
            placeholder="Choose a poll",
            options=[disnake.SelectOption(label=button_name) for button_name in button_names]
        )
        async def select_callback(select_interaction:disnake.CommandInteraction):
            selected_value = select.values[0]
            print(selected_value)
            users = self.vote_dict.get(selected_value)
            print(users)
            print(type(users))
            if len(users) == 0:
                embed.description = "No one has voted for this option yet!"
            else:
                description = ""
                for index, user in enumerate(users):
                    description += f"{index+1}) {user}\n"
                embed.description = description

            await select_interaction.response.edit_message(embed=embed)

        select.callback = select_callback
        view = disnake.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

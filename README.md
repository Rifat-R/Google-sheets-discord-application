# Discord Bot with Giveaways, Polls, and Google Sheet Integration

This Discord bot is built using Python and the Disnake library. It includes several features, including giveaways, polls, and integration with a Google Sheet for data storage.

## Features

### Giveaways

The bot can host giveaways in a specified channel. Users can enter the giveaway by reacting to a specific message with a specified emoji. The bot will then randomly select a winner from the list of entrants and announce them in the same channel.

### Polls

The bot can also create polls in a specified channel. Users can vote on the poll by reacting with a specified emoji. The bot will then tally the votes and display the results in the same channel.

### Google Sheet Integration

The bot can write data to a specified Google Sheet. This feature can be used to store information related to giveaways or polls, or any other data that needs to be persisted across sessions.

## Installation

1. Clone this repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Create a Discord bot application and obtain its token.
5. Create a Google API project and obtain its credentials.
6. Create a Google Sheet and share it with the service account associated with your Google API project.
7. Rename `.env.example` to `.env` and fill in the required values.
8. Run the bot using `python bot.py`.

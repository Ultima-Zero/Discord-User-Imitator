# native library imports
from os import getenv
from random import choice

# Third party imports -- installed via requirements.txt
from dotenv import load_dotenv
from disnake import Client, Webhook, Intents



intents = Intents.default()
intents.members = True
bot = Client(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord and listening for events.")


@bot.event
async def on_message(message):
    """
    Discord on_message event listener

    Takes in the Discord message object and verifies
    that is not a bot message, or a DM message

    It will then delete the original message, randomly
    select a non bot member from the guild, create a
    webhook within that channel, and re-send
    that message as the randomly selected member
    (includes display name and avatar)
    """

    # return instantly if message author is a bot,
    # message has attachments or message does not originate from guild
    if message.author.bot or message.guild is None:
        return

    if message.content is None:
        return

    content = message.content
    author = message.author
    channel = message.channel
    guild = message.guild

    # create a list of human members from the message guild
    members = [
        member for member in guild.members if not member.bot and member != author
    ]

    # get a random member from the members list
    member = choice(members)
    avatar = member.display_avatar.url
    name = member.display_name

    # get webhooks from the message channel if webhook name == April Fools
    apr_fools_webhook = [wh for wh in await channel.webhooks() if wh.name == 'April Fools'][0]

    # if no webhook with name April Fools, create it
    if not apr_fools_webhook:
        apr_fools_webhook = await channel.create_webhook(name='April Fools')

    # delete the original message
    await message.delete()

    # send the message content to the webhook
    await apr_fools_webhook.send(content=content, username=name, avatar_url=avatar)



load_dotenv()
bot.run(getenv("TOKEN"))

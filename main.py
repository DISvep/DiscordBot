import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import random
import sqlite3
import atexit
import os

db = sqlite3.connect("SERVER.db")
c = db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS server (
    id INTEGER PRIMARY KEY,
    cash INTEGER
)""")
db.commit()

token = os.environ["TOKEN"]
prefix = ",,"


Loose_rate = {0: 80, 10: 74, 30: 69, 50: 66, 70: 61, 100: 60, 200: 60, 300: 60}
Lucky_rate = {0: 1, 10: 5, 30: 7, 50: 9, 70: 11.5, 100: 12, 200: 14, 300: 16}

wins = {1: "🌐🌐🌐", 2: "💤💤💤", 3: "🔗🔗🔗", 4: "🧧🧧🧧", 5: "🎑🎑🎑"}
jackpots = {1: "🎁🎁🎁", 2: "🥼🥼🥼", 3: "🔴🔴🔴", 4: "🏹🏹🏹", 5: "🥏🥏🥏", 6: "🎨🎨🎨", 7: "🎒🎒🎒", 8: "🏸🏸🏸", 9: "🥊🥊🥊", 10: "🎇🎇🎇", 11: "💥💥💥", 12: "👁‍🗨👁‍🗨👁‍🗨", 13: "🏴‍☠️🏴‍☠️🏴‍☠️", 14: "🎃🎃🎃", 15: "📀📀📀", 16: "✨✨✨"}
emotes = ["🌐", "💤", "🔗", "🧧", "🎑", "🎁", "🥼", "🔴", "🏹", "🥏", "🎨", "🎒", "🏸", "🥊", "🎇", "💥", "👁‍🗨", "🏴‍☠️", "🎃", "📀", "✨"]

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print("Бот готов.")


class kazikButtons(nextcord.ui.View):
    @nextcord.ui.button(label="Да", style=nextcord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction):
        try:
            c.execute('SELECT cash FROM server WHERE id=?', (interaction.user.id,))
            a = c.fetchone()
            money = a[0]
        except Exception as e:
            money = 0
        if money >= 10:
            c.execute('SELECT cash FROM server WHERE id=?', (interaction.user.id,))
            a = c.fetchone()
            need = a[0] + -10
            c.execute("""INSERT OR REPLACE INTO server (id, cash) VALUES (?, ?)""", (interaction.user.id, need))
            db.commit()
            zero = nextcord.utils.get(interaction.guild.roles, id=1136290056412352553)
            ten = nextcord.utils.get(interaction.guild.roles, id=1137803459647787088)
            thirty = nextcord.utils.get(interaction.guild.roles, id=1137803907586867290)
            fifty = nextcord.utils.get(interaction.guild.roles, id=1137803973680709654)
            seventy = nextcord.utils.get(interaction.guild.roles, id=1137804087258263653)
            hundred = nextcord.utils.get(interaction.guild.roles, id=1137804181688832094)
            two_hundred = nextcord.utils.get(interaction.guild.roles, id=1137804696573202578)
            max = nextcord.utils.get(interaction.guild.roles, id=1137804783739211799)

            if zero in interaction.user.roles:
                lvl = 0
            if ten in interaction.user.roles:
                lvl = 10
            if thirty in interaction.user.roles:
                lvl = 30
            if fifty in interaction.user.roles:
                lvl = 50
            if seventy in interaction.user.roles:
                lvl = 70
            if hundred in interaction.user.roles:
                lvl = 100
            if two_hundred in interaction.user.roles:
                lvl = 200
            if max in interaction.user.roles:
                lvl = 300

            rate = Loose_rate[lvl]
            winRate = Lucky_rate[lvl]

            num = random.randint(1, 100)
            num2 = random.randint(1, 100)
            if num >= rate:
                if num2 <= winRate:
                    prizeNum = random.randint(1, 16)
                    prize = jackpots[prizeNum]
                    await interaction.response.send_message(f"Поздравляю с выигрышем джекпота! Вам выпал приз: {prize} Надеюсь, ты насладишься своей наградой!", ephemeral=True)
                    await bot.get_channel(1192124129063731280).send(f"<@{interaction.user.id}> выиграл джекпот! Приз: {prize}")
                else:
                    prizeNum = random.randint(1, 5)
                    prize = wins[prizeNum]
                    await interaction.response.send_message(f"Вы выиграли! Вам выпал приз: {prize}", ephemeral=True)
            else:
                first = random.choice(emotes)
                second = random.choice(emotes)
                third = random.choice(emotes)
                if second == third:
                    third = emotes[emotes.index(third) + 1]
                prize = f"{first}{second}{third}"
                await interaction.response.send_message(f"Вам выпали: {first}{second}{third}. К сожалению вы не выиграли и не получили ничего!", ephemeral=True)
            await bot.get_channel(1192153287974211706).send(f"<@{interaction.user.id}> получил {prize}.\nЧисло выигрыша - {num}, шанс - >={rate}, Число подходит? - **{num >= rate}**.\nЧисло джекпота - {num2}, шанс - <={winRate}. Число подходит? - **{num2 <= winRate}**")
        else:
            await interaction.response.send_message("У вас не хватает <:crystalfromocean:1191844196773015683>!")

    @nextcord.ui.button(label="Позже зайду", style=nextcord.ButtonStyle.blurple)
    async def button_later_callback(self, button, interaction):
        await interaction.response.send_message("Ждем вас снова", ephemeral=True)


class mainButtons(nextcord.ui.View):
    @nextcord.ui.button(label="Открыть слот машину", style=nextcord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction):
        try:
            c.execute('SELECT cash FROM server WHERE id=?', (interaction.user.id,))
            a = c.fetchone()
            money = a[0]
        except Exception as e:
            money = 0
        embed = nextcord.Embed(title="Слот машина", description=f"Цена прокрутки слот машины - **10** <:crystalfromocean:1191844196773015683>.У вас **{money}** <:crystalfromocean:1191844196773015683>. Вы точно хотите сыграть?")
        await interaction.response.send_message(view=kazikButtons(), embed=embed, ephemeral=True)

    @nextcord.ui.button(label="Купить монетки", style=nextcord.ButtonStyle.blurple)
    async def button_money_callback(self, button, interaction):
        await interaction.response.send_message("монетки", ephemeral=True)


@bot.slash_command(name="change_money", description="change money", default_member_permissions=(nextcord.Permissions(administrator=True)), guild_ids=[1132218511083700235])
async def change_money(interaction: Interaction, user: nextcord.User, amount: int):
    if user.bot:
        await interaction.response.send_message("Ты не можешь менять значение ботам!", ephemeral=True)
    else:
        c.execute("""INSERT OR REPLACE INTO server (id, cash) VALUES (?, ?)""", (user.id, amount))
        db.commit()
        await interaction.response.send_message(f"У <@{user.id}> значение <:crystalfromocean:1191844196773015683> теперь {amount}", ephemeral=True)
        await bot.get_channel(1192405156600492133).send(f"У <@{user.id}> значение <:crystalfromocean:1191844196773015683> теперь {amount}. Изменил <@{interaction.user.id}>")


@bot.slash_command(name="add_money", description="add money", default_member_permissions=(nextcord.Permissions(administrator=True)), guild_ids=[1132218511083700235])
async def add_money(interaction: Interaction, user: nextcord.User, amount: int):
    if user.bot:
        await interaction.response.send_message("Ты не можешь менять значение ботам!", ephemeral=True)
    else:
        c.execute('SELECT cash FROM server WHERE id=?', (user.id,))
        a = c.fetchone()
        try:
            need = a[0] + amount
        except:
            need = amount
        c.execute("""INSERT OR REPLACE INTO server (id, cash) VALUES (?, ?)""", (user.id, need))
        db.commit()
        await interaction.response.send_message(f"К баллансу <@{user.id}> было добавлено {amount} <:crystalfromocean:1191844196773015683>, теперь у него {need} <:crystalfromocean:1191844196773015683>", ephemeral=True)
        await bot.get_channel(1192405156600492133).send(f"У <@{user.id}> значение <:crystalfromocean:1191844196773015683> теперь {need} (добавлено {amount}). Изменил <@{interaction.user.id}>")


@bot.slash_command(name="money", description="money", guild_ids=[1132218511083700235])
async def money(interaction: Interaction, user: nextcord.User):
    try:
        c.execute('SELECT cash FROM server WHERE id=?', (user.id,))
        a = c.fetchone()
        await interaction.response.send_message(f"<@{user.id}> имеет {a[0]} <:crystalfromocean:1191844196773015683>", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"<@{user.id}> не имеет <:crystalfromocean:1191844196773015683>", ephemeral=True)


@bot.slash_command(name="info", description="info", default_member_permissions=(nextcord.Permissions(administrator=True)), guild_ids=[1132218511083700235])
async def test(interaction: Interaction):
    embed = nextcord.Embed(title="Приветствую, любитель азартных игр. Чем могу помочь?", color=0xab0e4)
    await bot.get_channel(1184229619243692072).send(embed=embed, view=mainButtons())


def onExit():
    print("Бот ушел.")
    c.close()
    db.close()


atexit.register(onExit)
bot.run(token)
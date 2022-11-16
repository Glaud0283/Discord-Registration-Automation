import discord
from discord import app_commands
from discord.ext import commands
from discord import ui

class Questionnaire(ui.Modal, title='Kayıt'):
	'''Creates the Modal object'''
	name = ui.TextInput(label='Ad Soyad', required = True, placeholder =  "Ders ve Ödevler İçin Önemli",  style = discord.TextStyle.short)

	async def on_submit(self, interaction: discord.Interaction):
		member = interaction.user
		if((interaction.channel != interaction.guild.get_channel(1033487911250833430)) or (interaction.guild.get_role(1033484249958981642) in member.roles)):
			await interaction.response.send_message("Kaydınızı alırken hata oluştu!!", ephemeral=True)
			return
		await member.add_roles(interaction.guild.get_role(1033484249958981642))
		await member.edit(nick = self.name.value)
		embed = discord.Embed(title = "Yeni bir üye kaydoldu!",description = f"ID: {member.id}\nÜye: {member.mention}\nİsim: {self.name.value}", color = 0xecf8ba)
		await interaction.guild.get_channel(1034146197746753606).send(embed=embed)
		await interaction.response.send_message(f'Başarıyla kaydınız alındı, {self.name}!', ephemeral=True)
	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		await interaction.response.send_message('Kaydınızı alırken hata oluştu!', ephemeral=True)



class Registry(commands.Cog):
	'''
	Cog subclass
	'''
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		'''
		Sets the inital variables
		'''
		self.guild = self.bot.get_guild(1033482696074199040)
		self.channel_entrylog = self.guild.get_channel(1034146197746753606)
		self.channel_welcome = self.guild.get_channel(1033487911250833430)
		self.role_member = self.guild.get_role(1033484249958981642)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		'''
		New Member Notification
		'''
		await member.guild.get_channel(1033487911250833430).send(
		 f"{member.mention} Hoş Geldin!\n`/register` komutunu kullanarak sunucuya katılabilirsin."
		)
	@commands.guild_only()
	@app_commands.command()
	async def kayıt(self, interaction: discord.Interaction):
		"""Slash command to send Modal to Member"""
		await interaction.response.send_modal(Questionnaire())

	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def sync(self, ctx) -> None:
		'''
		Slash Command Sync Command
		'''
		await ctx.bot.tree.sync()
		await ctx.send("Synced Succesfully!")
		return


async def setup(bot):
	await bot.add_cog(Registry(bot))

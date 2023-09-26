import discord

max_value = 10

class VoteView(discord.ui.View):
    @discord.ui.button(label="Right", style=discord.ButtonStyle.primary, emoji="➡️")
    async def right_button_callback(self, button, interaction):
        value = value + 1
        if value == max_value:
            await interaction.response.send_message(self.right_name + " wins!")
        await interaction.response.send_message("Test1" + ("_" * (max_value + value)) + "\U0001F40C" + (
                    "_" * (max_value - value)) + "Test2")
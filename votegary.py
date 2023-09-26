import discord

max_value = 10

class VoteView(discord.ui.View):
    @discord.ui.button(label="Left", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def left_button_callback(self, button, interaction):
        self.value = self.value - 1
        if self.value == (max_value * -1):
            await interaction.response.send_message(self.right_name + " wins!")
        await interaction.response.send_message(self.display())

    @discord.ui.button(label="Right", style=discord.ButtonStyle.primary, emoji="➡️")
    async def right_button_callback(self, button, interaction):
        self.value = self.value + 1
        if self.value == max_value:
            await interaction.response.send_message(self.right_name + " wins!")
        await interaction.response.send_message("Test1" + ("_" * (max_value + self.value)) + "\U0001F40C" + (
                    "_" * (max_value - self.value)) + "Test2")
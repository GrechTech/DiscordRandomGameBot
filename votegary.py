import discord

max_value = 10


class VoteView(discord.ui.View):
    def __init__(self, left, right):
        self.left_name = left
        self.right_name = right
        self.value = 0

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
        await interaction.response.send_message(self.display())

    def display(self):
        string = self.left_name + ("_" * (max_value + self.value)) + "\U0001F40C" + (
                    "_" * (max_value - self.value)) + self.right_name
        return string

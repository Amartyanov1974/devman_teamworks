import discord
from discord.ext import commands
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from devman.models import TeamWork


class Command(BaseCommand):
    def handle(self, *args, **options):
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix='!', intents=intents)
        token = settings.DISCORD_BOT_TOKEN
        groups = []
        for group in TeamWork.objects.all():
            groups.append(group.project_manager)

        @bot.event
        async def on_ready():
            print(f'Бот {bot.user} готов к работе')

            for guild in bot.guilds:
                current_month = datetime.datetime.now().strftime('%B')

                new_guild_name = f'Сервер - {current_month}'
                await guild.edit(name=new_guild_name)

                for category in guild.categories:
                    await category.delete()

                for voice_channel in guild.voice_channels:
                    await voice_channel.delete()

                for text_channel in guild.text_channels:
                    await text_channel.delete()

                for group in groups:
                    category_name = f'Группа: ПМ - {group}'
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True)
                    }
                    voice_category = await guild.create_category(category_name, overwrites=overwrites)
                    await guild.create_voice_channel(f'Голосовой канал', category=voice_category)
                    await guild.create_text_channel(f'Текстовый канал', category=voice_category)

        bot.run(token)


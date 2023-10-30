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
        groups = {}
        discord_invites = {}
        for group in TeamWork.objects.all():

            students = []
            for student in group.students.all():
                students.append(student.name)

            try:
                groups[group.id] = {'project_manager': group.project_manager.name,
                                    'student_1': students[0],
                                    'student_2': students[1],
                                    'student_3': students[2]
                                    }
            except IndexError:
                groups[group.id] = {'project_manager': group.project_manager.name,
                                    'student_1': students[0],
                                    'student_2': students[1],
                                    'student_3': None
                                    }

        @bot.event
        async def on_ready():
            print(f'Бот {bot.user} готов к работе')

            for guild in bot.guilds:
                current_month = datetime.datetime.now().strftime('%B')

                new_guild_name = f'Project.{current_month}'
                await guild.edit(name=new_guild_name)

                for category in guild.categories:
                    await category.delete()

                for voice_channel in guild.voice_channels:
                    await voice_channel.delete()

                for text_channel in guild.text_channels:
                    await text_channel.delete()

                for group_number in groups:
                    category_name = f'Группа {group_number}: ПМ - {groups[group_number]["project_manager"]} Студенты - {groups[group_number]["student_1"]}, {groups[group_number]["student_2"]}, {groups[group_number]["student_3"]}'
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True)
                    }
                    voice_category = await guild.create_category(category_name, overwrites=overwrites)
                    voice_channel = await guild.create_voice_channel(f'Голосовой канал', category=voice_category)
                    discord_invite = await voice_channel.create_invite(max_age=0, max_uses=0)

                    discord_invites[group_number] = discord_invite.url

                    await guild.create_text_channel(f'Текстовый канал', category=voice_category)

            await bot.close()
        bot.run(token)
        print(discord_invites)

        for group_number, invite_url in discord_invites.items():
            TeamWork.objects.filter(id=group_number).update(discord_link=invite_url)

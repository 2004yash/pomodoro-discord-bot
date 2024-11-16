import discord
from discord.ext import commands, tasks
import asyncio
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable receiving message content events
intents.members = True  # Enable member events if you want to track users joining, etc.

# Set up the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables for Pomodoro state
session_active = False
session_type = None
remaining_time = 0
participants = []  # List of users in the current session
leaderboard_data = {}  # Dictionary to track users' completed sessions
tasks_data = {}  # Dictionary to store users' tasks

# Load leaderboard and task data from JSON files at startup
def load_data():
    global leaderboard_data, tasks_data
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard_data = json.load(file)
    except FileNotFoundError:
        leaderboard_data = {}

    try:
        with open("tasks.json", "r") as file:
            tasks_data = json.load(file)
    except FileNotFoundError:
        tasks_data = {}

# Save leaderboard and task data to JSON files
def save_data():
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard_data, file)
    with open("tasks.json", "w") as file:
        json.dump(tasks_data, file)

@bot.command(name="bothelp")
async def bot_help(ctx):
    """List all bot commands with explanations."""
    help_message = """
**Pomodoro Bot Commands**

**Task Management:**
1. `!addtask <task>` - Add a task to your task list for the day.
2. `!viewtasks` - View your tasks for today.
3. `!deletetask <task_number>` - Delete a task by its number from your task list.

**Pomodoro Session Management:**
1. `!start <minutes>` - Start a Pomodoro session with a customizable duration (default is 25 minutes).
2. `!join` - Join an ongoing Pomodoro session.
3. `!status` - Check the status of the current Pomodoro session, including remaining time and participants.
4. `!stop` - Stop the current Pomodoro session.

**Leaderboard:**
1. `!leaderboard` - View the leaderboard of users by completed focus sessions.

**Additional Commands:**
1. `!bothelp` - List all bot commands with explanations.

"""
    await ctx.send(help_message)


@bot.event
async def on_ready():
    load_data()
    print(f'{bot.user} is now online!')

# Task Management Commands

@bot.command()
async def addtask(ctx, *, task: str):
    """Add a task to your task list for the day."""
    user_id = str(ctx.author.id)
    if user_id not in tasks_data:
        tasks_data[user_id] = []
    tasks_data[user_id].append(task)
    save_data()
    await ctx.send(f"Task added: {task}")

@bot.command()
async def viewtasks(ctx):
    """View your tasks for the day."""
    user_id = str(ctx.author.id)
    if user_id not in tasks_data or not tasks_data[user_id]:
        await ctx.send("You have no tasks for today.")
    else:
        task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks_data[user_id])])
        await ctx.send(f"**Your Tasks for Today:**\n{task_list}")

@bot.command()
async def deletetask(ctx, task_number: int):
    """Delete a task by its number from your task list."""
    user_id = str(ctx.author.id)
    if user_id not in tasks_data or task_number <= 0 or task_number > len(tasks_data[user_id]):
        await ctx.send("Invalid task number.")
    else:
        task = tasks_data[user_id].pop(task_number - 1)
        save_data()
        await ctx.send(f"Task removed: {task}")

# Pomodoro Commands

@bot.command()
async def start(ctx, minutes: int = 25):
    """Start a group Pomodoro session with a customizable duration (default 25 min focus)"""
    global session_active, session_type, remaining_time, participants
    if session_active:
        await ctx.send("A session is already running! Type `!join` to participate.")
        return
    session_active = True
    session_type = "focus"
    remaining_time = minutes * 60  # Convert minutes to seconds
    participants = [ctx.author]  # Initialize with the user who started the session
    await ctx.send(f"Pomodoro session started by {ctx.author.mention} for {minutes} minutes! Type `!join` to join this session.")
    await run_session(ctx)

@bot.command()
async def join(ctx):
    """Join an ongoing Pomodoro session"""
    global session_active, participants
    if not session_active:
        await ctx.send("There's no active session. Start one with `!start`.")
        return
    if ctx.author in participants:
        await ctx.send(f"{ctx.author.mention}, you're already in the session!")
        return
    participants.append(ctx.author)
    await ctx.send(f"{ctx.author.mention} has joined the session! Let's stay focused together!")

async def run_session(ctx):
    """Run the countdown timer for the current session"""
    global session_active, remaining_time, participants
    while remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        timer = f'{mins:02d}:{secs:02d}'
        await ctx.send(f'{timer} remaining for the {session_type}.')
        await asyncio.sleep(60)  # Update every minute
        remaining_time -= 60
    session_active = False
    await ctx.send(f"Time's up! {session_type.capitalize()} session is over. Great job!")
    if session_type == "focus":
        update_leaderboard(participants)
    if participants:
        mentions = " ".join(user.mention for user in participants)
        await ctx.send(f"{mentions}, session complete! Take a break or start a new session.")

@tasks.loop(hours=24)
async def daily_report():
    timezone = pytz.timezone("YOUR_TIMEZONE")  # Replace with your timezone, e.g., "US/Eastern"
    now = datetime.now(timezone)
    
    # Run at 10 PM in the specified timezone
    if now.hour == 22:
        for guild in bot.guilds:
            report_channel = discord.utils.get(guild.text_channels, name="daily-reports")
            if not report_channel:
                continue
            
            report_message = "**📋 Daily Report - Unaccomplished Tasks**\n"
            for user_id, tasks in tasks_data.items():
                incomplete_tasks = [task for task in tasks]
                
                if incomplete_tasks:
                    user = bot.get_user(int(user_id))
                    report_message += f"\n**{user.display_name}'s Incomplete Tasks:**\n"
                    for task in incomplete_tasks:
                        report_message += f"• {task}\n"
                    
            await report_channel.send(report_message)

# Leaderboard Functions

def update_leaderboard(users):
    """Update the leaderboard with completed sessions"""
    global leaderboard_data
    for user in users:
        user_id = str(user.id)
        if user_id in leaderboard_data:
            leaderboard_data[user_id]["sessions"] += 1
        else:
            leaderboard_data[user_id] = {
                "name": user.name,
                "sessions": 1
            }
    save_data()  # Save data to JSON file

@bot.command()
async def leaderboard(ctx):
    """Display the leaderboard of users by completed focus sessions"""
    if not leaderboard_data:
        await ctx.send("No data in the leaderboard yet. Start completing sessions to appear on it!")
        return
    sorted_leaderboard = sorted(leaderboard_data.items(), key=lambda x: x[1]["sessions"], reverse=True)
    leaderboard_message = "**Leaderboard:**\n"
    for i, (user_id, data) in enumerate(sorted_leaderboard[:10], start=1):
        leaderboard_message += f"{i}. {data['name']} - {data['sessions']} sessions\n"
    await ctx.send(leaderboard_message)

@bot.command()
async def status(ctx):
    """Check the status of the current session."""
    if not session_active:
        await ctx.send("No session is currently active.")
    else:
        mins, secs = divmod(remaining_time, 60)
        timer = f'{mins:02d}:{secs:02d}'
        participants_list = ", ".join([user.mention for user in participants])
        await ctx.send(f"Current session: {session_type} - {timer} remaining.\nParticipants: {participants_list}")

@bot.command()
async def stop(ctx):
    """Stop the current session."""
    global session_active, session_type, remaining_time, participants
    if not session_active:
        await ctx.send("No session to stop.")
        return
    session_active = False
    session_type = None
    remaining_time = 0
    participants = []
    await ctx.send("Session stopped.")

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')  # Replace 'YOUR_BOT_TOKEN' with the actual token in a secure way

# Pomodoro Discord Bot

A productivity-focused Discord bot designed to help users stay organized and efficient using the **Pomodoro Technique**. This bot allows users to manage their tasks, participate in group Pomodoro sessions, and track progress with a leaderboard.

---

## Features

### 🎯 **Task Management**
- **Add Tasks**: Organize your day by adding tasks.
- **View Tasks**: Review your task list at any time.
- **Delete Tasks**: Remove completed or unnecessary tasks.

### ⏱️ **Pomodoro Sessions**
- Start a group Pomodoro session with a customizable focus time.
- Join ongoing sessions and collaborate with other participants.
- Track time and session progress in real-time.

### 🏆 **Leaderboard**
- Keep track of completed focus sessions.
- Compete with others on the server for higher productivity.

### 📝 **Daily Reports**
- Generate a daily summary at 10 PM showing unaccomplished tasks for all users.

### 🔍 **Command Reference**
- A built-in command to list and explain all features of the bot.

---

## Installation

### Prerequisites
1. [Python 3.10+](https://www.python.org/downloads/)
2. [Discord Developer Portal Bot Token](https://discord.com/developers/applications)
3. Required Python packages:
   ```bash
   pip install discord.py
   ```

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/2004yash/pomodoro-discord-bot.git
   cd pomodoro-discord-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a file named `.env` to store your bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

---

## Commands

| Command             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `!addtask <task>`   | Add a task to your list.                                                    |
| `!viewtasks`        | View your current tasks for the day.                                        |
| `!deletetask <num>` | Delete a specific task from your list using its number.                     |
| `!start <minutes>`  | Start a Pomodoro session for the specified duration (default is 25 minutes).|
| `!join`             | Join an ongoing Pomodoro session.                                           |
| `!status`           | Check the current session's status.                                         |
| `!stop`             | Stop the ongoing session.                                                  |
| `!leaderboard`      | View the leaderboard of completed sessions.                                |
| `!bothelp`          | List all bot commands with explanations.                                   |

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
Special thanks to the [discord.py](https://discordpy.readthedocs.io/) community for providing an excellent framework for building Discord bots.

---

Enjoy productive collaboration with the **Pomodoro Discord Bot**! 🎉

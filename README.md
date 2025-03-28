# MCPtelebot

MCPtelebot is an advanced Telegram bot designed to manage messages efficiently in groups. It includes features such as user information retrieval, profile picture fetching, group mentions, rule management, scheduled messaging, and user moderation.

 Features:
 User Info Lookup: Fetch details of a user using `/info @username`.
 Profile Picture Fetching: Retrieve a user's profile picture with `/getpfp @username`.
 Mention All Members: Use `/mentionall` to tag all users (limited to avoid spam).
 Group Rules Management: Admins can set and retrieve group rules with `/setrules` and `/rules`.
 Message Scheduling: Schedule messages using `/schedule HH:MM Message`.
 Find Users: Search for users in the group using `/finduser keyword`.
 Auto Moderation: Detects and deletes messages containing offensive words.
 Logging: Captures bot activities for easy debugging.
 Automated Response System: Set automated replies based on specific keywords.
 MultiLanguage Support: Translate messages between languages using AI.
 Enhanced Security: Allows muting, banning, and reporting users for violations.

 Installation

 Prerequisites
 Python 3.8+ is enough.
 `pip` package manager
A Telegram Bot Token (from [BotFather](https://t.me/botfather))
Install required dependencies using:
sh
pip install python-telegram-bot==20.0 asyncio logging datetime

Setup & Running the Bot

1. Clone the repository:
   sh:
   git clone <https://github.com/karnkarthik2005/MCPtelebot.git>
   cd TGMCPBot
2. Get a Telegram Bot Token
Open Telegram and search for @BotFather.
Type /newbot and follow the instructions to create a bot.
Copy the bot token given by BotFather.
Replace "YOUR_BOT_TOKEN" in your script with the actual token.

3. Run the Script
Save your script as bot.py and run it using:
python bot.py
If you are using Linux/macOS, you may need:
python3 bot.py
4. Deploy the Bot (Optional)
If you want your bot to run 24/7:
Use a cloud service like Heroku, Railway, or VPS.
Run it on a Raspberry Pi for a local solution.
Use a service like PythonAnywhere for easy deployment.

5. Add the Bot to a Group
Search for your bot in Telegram.
Add it to a group.
Promote it as an admin to allow moderation features.
 Usage:
 Start the bot: `/start`
 Get user info: `/info @username`
 Get profile picture: `/getpfp @username`
 Mention all members: `/mentionall`
 Set group rules (Admins only): `/setrules [new rules]`
 View group rules: `/rules`
 Schedule a message: `/schedule HH:MM Your message`
 Find users: `/finduser keyword`
 Enable automoderation: `/enablemod`
 Mute a user: `/mute @username time`
 Unmute a user: `/unmute @username`
 Translate message: `/translate enes Your message`

 Deployment
To keep your bot running 24/7, consider deploying on a cloud platform like:
 [Heroku](https://www.heroku.com/)
 [AWS Lambda](https://aws.amazon.com/lambda/)
 [Google Cloud Run](https://cloud.google.com/run/)
 [VPS](https://www.digitalocean.com/)

 Contributing

1. Fork the repository
2. Create a new branch (`featurenewfeature`)
3. Commit your changes (`git commit m "Added a new feature"`)
4. Push to the branch (`git push origin featurenewfeature`)
5. Open a pull request

 License
This project is licensed under the MIT License.

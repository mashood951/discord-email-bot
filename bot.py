import discord
from discord.ext import commands
import smtplib
from decouple import config
from email.message import EmailMessage

prefix = "$"
check_email = False
check_subject = False
check_body = False
can_send_mail = False

def send_mail(sender, reciever, sub, context):
    mssg = EmailMessage()
    mssg.set_content(context)

    mssg['Subject'] = sub
    mssg['From'] = sender
    mssg['To'] = reciever

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, config('EMAIL_PASSWORD'))
    server.send_message(mssg)
    server.quit()

# client = commands.Bot(command_prefix="!")
client = discord.Client()

@client.event
async def on_message(message):
    global check_email 
    global check_subject
    global check_body
    global can_send_mail
    global email
    global subject
    global body
    global temp_email

    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith(prefix + "email"):
        email = msg.split(prefix + "email ", 1)[1]
        temp_email = email
        check_email = True
        print("email:", email)

    if msg.startswith(prefix + "subject"):
        subject = msg.split(prefix + "subject ", 1)[1]
        check_subject = True
        print("subject:", subject)

    if msg.startswith(prefix + "body"):
        check_body = True
        body = msg.split(prefix + "body ", 1)[1]
        print("body:", body)

    # if msg.startswith(prefix + "new"):
    #     # subject = ""
    #     # body = ""
    #     check_subject = False
    #     check_body = False
    #     can_send_mail = False

    if check_subject == True and check_body == True:
        can_send_mail = True

    if check_email == True and can_send_mail == True:
        check_subject = False
        check_body = False
        can_send_mail = False
        sender_email = config('EMAIL')
        send_mail(sender_email, email, subject, body)
        await displayEmbed(message.channel)
        

async def displayEmbed(ctx):
    embed = discord.Embed(
        title="Notification",
        description="Email Sent!"
    )
    await ctx.send(embed=embed)

token = config('TOKEN')
client.run(token)

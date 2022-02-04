# -*- coding: utf-8 -*-
"""
Created on Sun Nov 7 16:34:58 2021

@author: ANANT PRAKASH SINGH
@GitHub: https://github.com/TheViking733n

"""

import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import threading
import time

from variables import *
from all_cutoff import *

no_of_branches_per_college = 3


# Below dictionary stores the latest replies of all the user in format-
# { (user_id, chat_id) : [user_msg] }
# to take input from that user
ALL_REPLIES = {}



# Below dictionary stores True if a INPUT() is waiting from a user for input-
# {(user_id, chat_id) : True }
# /cancel commands sets False to it
WAITING_FOR_INPUT = {}










# Bot TOKEN initialisation
TOKEN ="YOUR-BOT-TOKEN-HERE"
APP_NAME = "YOUR-HEROKU-APP-LINK-HERE"


# Important!!! bot_trigger_method = "polling" or "webhook"
bot_trigger_method = "webhook"


# Creating Bot object
bot = telegram.Bot(token=TOKEN)
PORT = int(os.environ.get('PORT', '8443'))


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


# Defining bot commands jo ham logo ka bot padhega aur reply karega

def start(update, context):
    # Starting start command in new thead
    # I'm starting this command in new thread because it contains INPUT() which is blocking CommandHandeler to call further commands
    thread1 = threading.Thread(target=start_in_newThread, args=(update, context))
    thread1.start()

def start_in_newThread(update, context):
    uid = update.message.from_user.id
    uname = update.message.from_user.username
    cid = update.effective_chat.id
    displayname = update.message.from_user.full_name

    msg = f"""🎉🎉Welcome <a href="tg://user?id={uid}">{displayname}</a> to the help section of this bot🎉🎉.\n\nI will tell you about what colleges you can get according to your rank in JEE.\n\nPlease answer few questions about yourself!"""
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)

    msg = f"<i>{list_to_index_msg(ALL_STATES)}</i>\n\n<b>Enter index of state from which you passed class 12th:</b>"
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)
    user_input = INPUT(uid, cid)
    state_index = parse_user_input(user_input)
    if user_input == "TIME UP":
        msg = "⚠Time Up...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    elif user_input == None:
        # It means user gave /cancel command
        return
    elif state_index not in range(32):
        msg = "⚠Invalid Input...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    state = ALL_STATES[state_index]

    msg = f"<i>{list_to_index_msg(ALL_GENDERS)}</i>\n\n<b>Enter index of gender:</b>"
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)
    user_input = INPUT(uid, cid)
    gender_index = parse_user_input(user_input)
    if user_input == "TIME UP":
        msg = "⚠Time Up...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    elif user_input == None:
        # It means user gave /cancel command
        return
    elif gender_index not in range(3):
        msg = "⚠Invalid Input...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    gender = ALL_GENDERS[gender_index]
    if gender == 'Female':
        gender = 'Female-only'
    else:
        gender = 'Gender-Neutral'

    msg = f"<i>{list_to_index_msg(ALL_CATEGORIES)}</i>\n\n<b>Enter index of your category:</b>"
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)
    user_input = INPUT(uid, cid)
    category_index = parse_user_input(user_input)
    if user_input == "TIME UP":
        msg = "⚠Time Up...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    elif user_input == None:
        # It means user gave /cancel command
        return
    elif category_index not in range(10):
        msg = "⚠Invalid Input...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    category = ALL_CATEGORIES[category_index]


    # context.bot.send_message(chat_id=cid, text=f"{state}\n\n{gender}\n\n{category}")

    msg = f"Enter your <b>JEE Mains <i>{category}</i></b> category rank: "
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)
    user_input = INPUT(uid, cid)
    jm_rank = parse_user_input(user_input)
    if user_input == "TIME UP":
        msg = "⚠Time Up...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    elif user_input == None:
        # It means user gave /cancel command
        return
    elif jm_rank not in range(1,10000001): # rank can't be greater than 1 crore
        msg = "⚠Invalid Input...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return

    msg = f"Enter your <b>JEE Advanced <i>{category}</i></b> category rank:\n<i>(if not qualified then enter -1)</i>"
    context.bot.send_message(chat_id=cid, text=msg, parse_mode=ParseMode.HTML)
    user_input = INPUT(uid, cid)
    ja_rank = parse_user_input(user_input)
    if user_input == "TIME UP":
        msg = "⚠Time Up...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return
    elif user_input == None:
        # It means user gave /cancel command
        return
    elif ja_rank < 0:
        # It means user didn't qualified in JEE Adv.
        ja_rank = 10000000
    elif ja_rank not in range(1,10000001): # rank can't be greater than 1 crore
        msg = "⚠Invalid Input...⚠\n\n\nYour current operation cancelled.\n\n Please use /start to restart the bot."
        context.bot.send_message(chat_id=cid, text=msg)
        return

    # context.bot.send_message(chat_id=cid, text=f"{state}\n\n{gender}\n\n{category}\n\n{jm_rank}\n\n{ja_rank}")


    #####################################
    # Job of taking input from user done!
    #####################################

    ######################################
    # Now Finding eligible college of IITs
    ######################################
    eligible_colleges = {}
    iit_branch_count = 0

    for row in IIT_CUTOFF:
        _college = row[0]
        _branch = row[1]
        _quota = row[2]
        _category = row[3]
        _gender = row[4]
        _or = row[5]
        _cr = row[6]

        if _category == category and _gender == gender and _cr >= ja_rank:
            iit_branch_count += 1
            tup = (_cr, _branch)
            if _college in eligible_colleges:
                eligible_colleges[_college].append(tup)
            else:
                eligible_colleges[_college] = [tup]

    if iit_branch_count > 0:
        iit_msg = f"😉<u><b>Total {iit_branch_count} branches in {len(eligible_colleges)} different IIT colleges available for you.😉</b></u>\n\n"
        iit_msg += f"<i>Displaying atmost top <b>{no_of_branches_per_college}</b> branches of each college</i>\n\n"
        iit_msg_list = [] # Making a list so that message doesn't become too long
        for college_name, branch_list in eligible_colleges.items():
            branch_list.sort()
            temp = f"😎<u><b>{college_name}</b></u>😎"
            count = 1
            for branch in branch_list:
                temp += f"\n✅ <i>{branch[1]}</i>"
                count += 1
                if count > no_of_branches_per_college:
                    break
            iit_msg_list.append(temp)

        if len(iit_msg_list) > 15:
            msg1 = iit_msg + "\n\n\n".join(iit_msg_list[:15])
            msg2 = "\n\n\n".join(iit_msg_list[15:])
            context.bot.send_message(chat_id=cid, text=msg1, parse_mode=ParseMode.HTML)
            context.bot.send_message(chat_id=cid, text=msg2, parse_mode=ParseMode.HTML)
        
    else:
        iit_msg = "😢 <i>Sorry, you can't get any branch in IITs.</i>"
        context.bot.send_message(chat_id=cid, text=iit_msg, parse_mode=ParseMode.HTML)


    time.sleep(3)
    ##################################
    # Finding eligible college of NITs
    ##################################
    eligible_colleges = {}
    nit_branch_count = 0

    for row in NIT_CUTOFF:
        _college = row[0]
        _branch = row[1]
        _quota = row[2]
        _category = row[3]
        _gender = row[4]
        _or = row[5]
        _cr = row[6]

        # Checking state reservation quota for the student
        if NIT_LOC[_college] == state:
            quota = ['HS']
        else:
            quota = ['AI', 'OS']

        if _category == category and _gender == gender and _quota in quota and _cr >= jm_rank:
            nit_branch_count += 1
            tup = (_cr, _branch)
            if _college in eligible_colleges:
                eligible_colleges[_college].append(tup)
            else:
                eligible_colleges[_college] = [tup]

    if nit_branch_count > 0:
        nit_msg = f"😉<u><b>Total {nit_branch_count} branches in {len(eligible_colleges)} different NIT colleges available for you.😉</b></u>\n\n"
        nit_msg += f"<i>Displaying atmost top <b>{no_of_branches_per_college}</b> branches of each college</i>\n\n"
        nit_msg_list = [] # Making a list so that message doesn't become too long
        for college_name, branch_list in eligible_colleges.items():
            branch_list.sort()
            temp = f"😁<u><b>{college_name}</b></u>😁"
            count = 1
            for branch in branch_list:
                temp += f"\n✅ <i>{branch[1]}</i>"
                count += 1
                if count > no_of_branches_per_college:
                    break
            nit_msg_list.append(temp)

        if len(nit_msg_list) > 15:
            msg1 = nit_msg + "\n\n\n".join(nit_msg_list[:15])
            msg2 = "\n\n\n".join(nit_msg_list[15:])
            context.bot.send_message(chat_id=cid, text=msg1, parse_mode=ParseMode.HTML)
            context.bot.send_message(chat_id=cid, text=msg2, parse_mode=ParseMode.HTML)
        
    else:
        nit_msg = "😢 <i>Sorry, you can't get any branch in NITs.</i>"
        context.bot.send_message(chat_id=cid, text=nit_msg, parse_mode=ParseMode.HTML)



    time.sleep(3)
    ###################################
    # Finding eligible college of IIITs
    ###################################
    eligible_colleges = {}
    iiit_branch_count = 0

    for row in IIIT_CUTOFF:
        _college = row[0]
        _branch = row[1]
        _quota = row[2]
        _category = row[3]
        _gender = row[4]
        _or = row[5]
        _cr = row[6]

        if _category == category and _gender == gender and _cr >= jm_rank:
            iiit_branch_count += 1
            tup = (_cr, _branch)
            if _college in eligible_colleges:
                eligible_colleges[_college].append(tup)
            else:
                eligible_colleges[_college] = [tup]

    if iiit_branch_count > 0:
        iiit_msg = f"😉<u><b>Total {iiit_branch_count} branches in {len(eligible_colleges)} different IIIT colleges available for you.😉</b></u>\n\n"
        iiit_msg += f"<i>Displaying atmost top <b>{no_of_branches_per_college}</b> branches of each college</i>\n\n"
        iiit_msg_list = [] # Making a list so that message doesn't become too long
        for college_name, branch_list in eligible_colleges.items():
            branch_list.sort()
            temp = f"🙃<u><b>{college_name}</b></u>🙃"
            count = 1
            for branch in branch_list:
                temp += f"\n✅ <i>{branch[1]}</i>"
                count += 1
                if count > no_of_branches_per_college:
                    break
            iiit_msg_list.append(temp)

        if len(iiit_msg_list) > 15:
            msg1 = iiit_msg + "\n\n\n".join(iiit_msg_list[:15])
            msg2 = "\n\n\n".join(iiit_msg_list[15:])
            context.bot.send_message(chat_id=cid, text=msg1, parse_mode=ParseMode.HTML)
            context.bot.send_message(chat_id=cid, text=msg2, parse_mode=ParseMode.HTML)
        
    else:
        iiit_msg = "😢 <i>Sorry, you can't get any branch in IIITs.</i>"
        context.bot.send_message(chat_id=cid, text=iiit_msg, parse_mode=ParseMode.HTML)



    time.sleep(3)
    ###################################
    # Finding eligible college of GFTIs
    ###################################
    eligible_colleges = {}
    gfti_branch_count = 0

    for row in GFTI_CUTOFF:
        _college = row[0]
        _branch = row[1]
        _quota = row[2]
        _category = row[3]
        _gender = row[4]
        _or = row[5]
        _cr = row[6]

        # Checking state reservation quota for the student
        if GFTI_LOC[_college] == state:
            quota = ['HS']
        else:
            quota = ['AI', 'OS']

        if _category == category and _gender == gender and _quota in quota and _cr >= jm_rank:
            gfti_branch_count += 1
            tup = (_cr, _branch)
            if _college in eligible_colleges:
                eligible_colleges[_college].append(tup)
            else:
                eligible_colleges[_college] = [tup]

    if gfti_branch_count > 0:
        gfti_msg = f"😉<u><b>Total {gfti_branch_count} branches in {len(eligible_colleges)} different GFTI colleges available for you.</b></u>😉\n\n"
        gfti_msg += f"<i>Displaying atmost top <b>{no_of_branches_per_college}</b> branches of each college</i>\n\n"
        gfti_msg_list = [] # Making a list so that message doesn't become too long
        for college_name, branch_list in eligible_colleges.items():
            branch_list.sort()
            temp = f"😐<u><b>{college_name}</b></u>😐"
            count = 1
            for branch in branch_list:
                temp += f"\n✅ <i>{branch[1]}</i>"
                count += 1
                if count > no_of_branches_per_college:
                    break
            gfti_msg_list.append(temp)
        if len(gfti_msg_list) > 15:
            msg1 = gfti_msg + "\n\n\n".join(gfti_msg_list[:15])
            msg2 = "\n\n\n".join(gfti_msg_list[15:])
            context.bot.send_message(chat_id=cid, text=msg1, parse_mode=ParseMode.HTML)
            context.bot.send_message(chat_id=cid, text=msg2, parse_mode=ParseMode.HTML)
        
    else:
        gfti_msg = "😢 <i>Sorry, you can't get any branch in GFTIs.</i>"
        context.bot.send_message(chat_id=cid, text=gfti_msg, parse_mode=ParseMode.HTML)


    msg = "🙃Thanks for using me🙃\n\nHope to see you soon.\nUse /start to restart"
    context.bot.send_message(chat_id=cid, text=msg)



def help(update, context):
    uid = update.message.from_user.id
    uname = update.message.from_user.username
    cid = update.effective_chat.id
    displayname = update.message.from_user.full_name

    context.bot.send_message(chat_id=cid, text=help_reply.format(uid, displayname), parse_mode=ParseMode.HTML)

def about(update, context):
    uid = update.message.from_user.id
    uname = update.message.from_user.username
    cid = update.effective_chat.id
    displayname = update.message.from_user.full_name

    context.bot.send_message(chat_id=cid, text=about_reply.format(uid, displayname), parse_mode=ParseMode.HTML)


def cancel(update, context):
    global WAITING_FOR_INPUT

    uid = update.message.from_user.id
    uname = update.message.from_user.username
    cid = update.effective_chat.id

    key = (uid, cid)
    WAITING_FOR_INPUT[key] = False
    msg = "⚠Your current operation cancelled.⚠\n\n Please use /start to restart the bot."
    context.bot.send_message(chat_id=cid, text=msg)

def noncommand(update, context):
    global ALL_REPLIES

    uid = update.message.from_user.id
    uname = update.message.from_user.username
    cid = update.effective_chat.id
    user_input = update.message.text

    key = (uid, cid)
    ALL_REPLIES[key] = [user_input]
    print(ALL_REPLIES)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def INPUT(uid, cid):
    global ALL_REPLIES
    global WAITING_FOR_INPUT

    # Deleting last input from user (if available)
    key = (uid, cid)
    if key in ALL_REPLIES:
        temp = ALL_REPLIES.pop(key)
    
    WAITING_FOR_INPUT[key] = True

    # Waiting for input from user for 2 minutes

    for i in range(120):
        time.sleep(1)
        if key in ALL_REPLIES:
            return ALL_REPLIES[key][0]
        if WAITING_FOR_INPUT[key] == False:
            return None
    return "TIME UP"



def parse_user_input(user_input):
    try:
        num = int(user_input)
    except ValueError:
        num = None
    except TypeError:
        num = None   

    return num


def list_to_index_msg(lst):
    msg = ""
    for i in range(len(lst)):
        msg += f"{i} -> {lst[i]}\n"
    return msg[:-1]






def main():
    # This function will start the Bot
    # Creating Updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # If user typed any command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("cancel", cancel))
    
    # If user typed any non-command message
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, noncommand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot

    if bot_trigger_method == "polling":
        updater.start_polling()

    elif bot_trigger_method == "webhook":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(APP_NAME + TOKEN)

    else:
        print("Invalid bot trigger method")
        
    # Bot will run until we press Ctrl-C or the process receives SIGINT ,SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
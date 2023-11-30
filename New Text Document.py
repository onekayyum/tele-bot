from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with the actual token from BotFather
TOKEN = '6413853374:AAGSdFr6_2-XGmt-QD8JVZcf7hSR7GBU_3I'

# Replace 'CHANNEL_2_ID' with the ID of your private content channel
CHANNEL_2_ID = '+sAYa7xKGizgyMmVl'

# Replace 'ADMIN_CHAT_ID' with your admin chat ID
ADMIN_CHAT_ID = 5447083924

# Dictionary to map content file IDs to content start links
content_links = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Check if the user is a subscriber (you need to implement this check)
    if is_subscriber(user_id):
        # Fetch content file ID from the command (e.g., /start CONTENT_FILE_ID)
        content_file_id = context.args[0] if context.args else None
        
        if content_file_id and content_file_id in content_links:
            # Forward the content to the user
            context.bot.forward_message(chat_id=update.message.chat_id, from_chat_id=CHANNEL_2_ID, message_id=content_links[content_file_id])
        else:
            update.message.reply_text("Invalid content file ID. Please specify a valid content file ID.")
    else:
        update.message.reply_text("You are not a subscriber. Subscribe to get access to the content.")

def is_subscriber(user_id):
    # Implement your subscriber check logic here (e.g., check against a list or database)
    # Return True if the user is a subscriber, otherwise return False
    return True  # Change this to your actual logic

def save_content_link(content_file_id, message_id):
    # Save the content link for the given content file ID
    content_links[content_file_id] = message_id

def handle_new_content(update: Update, context: CallbackContext) -> None:
    # This function is triggered when new content is posted in Channel 2
    content_file_id = str(update.message.document.file_id)  # Assuming content is sent as a document
    message_id = update.message.message_id
    
    # Generate the start link for the content
    start_link = f"https://t.me/{context.bot.username}?start={content_file_id}"
    
    # Save the content link
    save_content_link(content_file_id, message_id)
    
    # Print or log the start link (you can use it when posting in Channel 1)
    print(f"Start Link for Content: {start_link}")
    
    # Optionally, you can send this link to your admin chat
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Start Link for Content: {start_link}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(MessageHandler(Filters.document & ~Filters.forwarded, handle_new_content))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

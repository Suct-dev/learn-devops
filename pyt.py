import linux_check
import check_pass
import find_email
import find_phone
import work_with_db
import logging
import math
import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')


logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'


def findPhoneNumbers(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов
    context.user_data['phone'] = find_phone.find_numbers(user_input)
    update.message.reply_text(context.user_data['phone'])
    if context.user_data['phone'] == 'No phone numbers in text':
        return ConversationHandler.END
    else:
        update.message.reply_text('Введите yes, если требуется сохранить в базу, введите not, если нет')
        return 'writePhoneNumbers'


def writePhoneInDB(update: Update, context):
    reply = work_with_db.insert_in_phonenumbers(context.user_data['phone'])
    update.message.reply_text(reply)


def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email: ')
    return 'findEmails'


def findEmails(update: Update, context):
    user_input = update.message.text
    context.user_data['email'] = find_email.find_emails(user_input)
    update.message.reply_text(context.user_data['email'])
    if context.user_data['email'] == 'No emails in text':
        return ConversationHandler.END
    else:
        update.message.reply_text('Введите yes, если требуется сохранить в базу, введите not, если нет')
        return 'writeEmails'


def writeEmailsInDB(update: Update, context):
    reply = work_with_db.insert_in_emails(context.user_data['email'])
    update.message.reply_text(reply)

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности: ')
    return 'verifyPassword'


def verifyPassword(update: Update, context):
    user_input = update.message.text
    if check_pass.check_password(user_input):
        reply = 'Пароль сложный'
    else:
        reply = 'Пароль простой'
    update.message.reply_text(reply)
    return ConversationHandler.END


def release(update: Update, context):
    res=linux_check.get_information_from_commands('cat /etc/os-release')
    update.message.reply_text(res)


def uname(update: Update, context):
    res = linux_check.get_information_from_commands('uname -a')
    update.message.reply_text(res)


def uptime(update: Update, context):
    res = linux_check.get_information_from_commands('uptime')
    update.message.reply_text(res)


def df(update: Update, context):
    res = linux_check.get_information_from_commands('df -h')
    update.message.reply_text(res)


def free(update: Update, context):
    res = linux_check.get_information_from_commands('free -h')
    update.message.reply_text(res)


def mpstat(update: Update, context):
    res = linux_check.get_information_from_commands('mpstat')
    update.message.reply_text(res)


def whos(update: Update, context):
    res = linux_check.get_information_from_commands('who -q')
    update.message.reply_text(res)


def auths(update: Update, context):
    res = linux_check.get_information_from_commands('last -10 -R')
    update.message.reply_text(res)


def crits(update: Update, context):
    res = linux_check.get_information_from_commands('journalctl -n5 -p crit')
    update.message.reply_text(res)


def process(update: Update, context):
    res = linux_check.get_information_from_commands('ps')
    update.message.reply_text(res)


def socketstats(update: Update, context):
    res = linux_check.get_information_from_commands('ss -tul')
    update.message.reply_text(res)


def services(update: Update, context):
    res = linux_check.get_information_from_commands('systemctl list-units --state=failed')
    update.message.reply_text(res)


def aptListCommand(update: Update, context):
    update.message.reply_text('Введите all для вывода всех установленных пакетов или введите имя пакета ')
    return 'Choose'


def allAptList(update: Update, context):
    list_apt = linux_check.get_information_from_commands('apt list --installed | cut -d "/" -f 1')
    if len(list_apt) > 4100:
        for i in range(math.ceil(len(list_apt) / 4100)):
            mes = list_apt[i * 4100: (i + 1) * 4100]
            update.message.reply_text(mes)
    else:
        update.message.reply_text(list_apt)
    return ConversationHandler.END


def AptPacket(update: Update, context):
    user_input = update.message.text
    apt_packet = linux_check.get_information_from_commands('apt search ' + '\'^' + user_input + '$\'' + ' | tail -n 10')
    update.message.reply_text(apt_packet)
    return ConversationHandler.END


def repl_logs(update: Update, context):
    res = linux_check.get_information_from_commands('cat /var/log/postgresql/postgresql-14-main.log | grep -i repl | tail -10')
    update.message.reply_text(res)


def get_emails(update: Update, context):
    res = work_with_db.select_in_emails()
    update.message.reply_text(res)


def get_phone_numbers(update: Update, context):
    res = work_with_db.select_in_phonenumbers()
    update.message.reply_text(res)


def cancel(update: Update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'writePhoneNumbers': [MessageHandler(Filters.regex('^yes$'), writePhoneInDB),
                                  MessageHandler(Filters.regex('.*'), cancel)],
        },
        fallbacks=[]
    )

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'writeEmails': [MessageHandler(Filters.regex('^yes$'), writeEmailsInDB),
                       MessageHandler(Filters.regex('.*'), cancel)],
        },
        fallbacks=[]
    )

    convHandlerCheckPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

    convHandlerAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', aptListCommand)],
        states={
            'Choose': [MessageHandler(Filters.regex('^all$'), allAptList),
                       MessageHandler(Filters.regex('.*'), AptPacket)],
        },
        fallbacks=[]
    )

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerCheckPass)
    dp.add_handler(convHandlerAptList)
    dp.add_handler(CommandHandler("get_release", release))
    dp.add_handler(CommandHandler("get_uname", uname))
    dp.add_handler(CommandHandler("get_uptime", uptime))
    dp.add_handler(CommandHandler("get_df", df))
    dp.add_handler(CommandHandler("get_free", free))
    dp.add_handler(CommandHandler("get_mpstat", mpstat))
    dp.add_handler(CommandHandler("get_w", whos))
    dp.add_handler(CommandHandler("get_auths", auths))
    dp.add_handler(CommandHandler("get_critical", crits))
    dp.add_handler(CommandHandler("get_ps", process))
    dp.add_handler(CommandHandler("get_ss", socketstats))
    dp.add_handler(CommandHandler("get_services", services))
    dp.add_handler(CommandHandler("get_repl_logs", repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()

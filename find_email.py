import re

def main():
    test_email = 'dd@t.com bb..@dt.aaa'
    print(find_emails(test_email))


def find_emails(message_from_user):
    email_regex = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')  # формат 8 (000) 000-00-00
    email_list = email_regex.findall(message_from_user)
#    print(email_list)
    emails = ''
    if not email_list:
        emails = 'No emails in text'
    else:
        for i in range(len(email_list)):
            emails += f'{i+1}. {email_list[i]}\n'
    return emails

#r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

if __name__ == '__main__':
    main()

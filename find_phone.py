import re


def main():
    test_number = '89999999999 +7-123-233-23-23 7777 asdasd 77878as asd 87 234 234 234 34 23 234234234 83333333333'
    print(find_numbers(test_number))

def find_numbers(message_from_user):
    phone_num_regex = re.compile(r'((8|\+7)(-| |)(\(| |)\d{3}(| |\))(-| |)\d{3}(-| |)\d{2}(-| |)\d{2})')  # формат 8 (000) 000-00-00
    phone_num_list = phone_num_regex.findall(message_from_user)
#    print(phone_num_list)
    phone_numbers = ''
    if not phone_num_list:
        phone_numbers = 'No phone numbers in text'
    else:
        for i in range(len(phone_num_list)):
            phone_numbers += f'{i+1}. {phone_num_list[i][0]}\n'
    return phone_numbers

# (8|\+7(-| |)(\(| |)\d{3}(| |\))(-| |)\d{3}(-| |)\d{2}(-| |)\d{2})
if __name__ == '__main__':
    main()

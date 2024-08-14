import re


def main():
    test_pass = '!!DDDDdddd224442'
    print(check_password(test_pass))


def check_password(pass_text):
    strength_pass = False
    pass_regex = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])(?=.*[!@#$%^&*()]).*$')
    if len(pass_text) < 8:
        strength_pass = False
    else:
        pass_list = pass_regex.search(pass_text)
        if pass_list is None:
            strength_pass = False
        else:
            strength_pass = True
    return strength_pass


if __name__ == '__main__':
    main()

# coding:utf-8
import datetime


def check_id_card(id_card):
    # 位权
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码
    check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    if len(id_card) != 18:
        return False
    id_card = id_card.upper()
    if not id_card[:-1].isdigit():
        return False

    if not check_birthday(id_card):
        return False
    sums = 0
    for i in range(17):
        sums += int(id_card[i]) * weight[i]
    remainder = sums % 11
    if id_card[-1] != check_code[remainder]:
        return False
    return True


def check_birthday(id_card):
    birthday = id_card[6:14]
    try:
        birth_date = datetime.datetime.strptime(birthday, '%Y%m%d')
    except ValueError:
        return False
    now = datetime.datetime.now()
    age = now.year - birth_date.year
    if now.month < birth_date.month or (now.month == birth_date.month and now.day < birth_date.day):
        age -= 1
    if age < 0 or age > 150:
        return False
    return True


def main(id_card):
    if check_id_card(id_card):
        print(id_card + " is valid")
    else:
        print(id_card + " is invalid")


if __name__ == '__main__':
    main('500234199102182434')

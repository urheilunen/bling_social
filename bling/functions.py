import datetime


def how_old_is_this_datetime(datetime_attr):
    # generating the list of each unit of posts's age
    date_list = [
        datetime.datetime.now(datetime.timezone.utc).year - datetime_attr.year,
        datetime.datetime.now(datetime.timezone.utc).month - datetime_attr.month,
        datetime.datetime.now(datetime.timezone.utc).day - datetime_attr.day,
        datetime.datetime.now(datetime.timezone.utc).hour - datetime_attr.hour,
        datetime.datetime.now(datetime.timezone.utc).minute - datetime_attr.minute,
        datetime.datetime.now(datetime.timezone.utc).second - datetime_attr.second
    ]
    declension_list = [
        ['год', 'года', 'лет'],
        ['месяц', 'месяца', 'месяцев'],
        ['день', 'дня', 'дней'],
        ['час', 'часа', 'часов'],
        ['минуту', 'минуты', 'минут'],
        ['секунду', 'секунды', 'секунд']
    ]

    def get_declension(num):
        if 5 <= num <= 19:
            return 2
        elif num % 10 == 1:
            return 0
        elif 2 <= (num % 10) <= 4:
            return 1
        else:
            return 2

    age = ''

    for i in range(6):
        if date_list[i] == 0:
            pass
        else:
            # describe all russian words to every kind of number and datetime attribute name
            age = str(date_list[i]) + ' ' + declension_list[i][get_declension(date_list[i])] + ' назад'
            break
    if age == '':
        age = 'только что'
    return age

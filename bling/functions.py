import datetime


def how_old_is_this_datetimefield(datetime_attr):
    def get_declension(num):
        if 5 <= num <= 19:
            return 2
        elif num % 10 == 1:
            return 0
        elif 2 <= (num % 10) <= 4:
            return 1
        else:
            return 2

    declension_list = [
        ['год', 'года', 'лет'],
        ['месяц', 'месяца', 'месяцев'],
        ['день', 'дня', 'дней'],
        ['час', 'часа', 'часов'],
        ['минуту', 'минуты', 'минут'],
        ['секунду', 'секунды', 'секунд']
    ]

    age_in_units = round(datetime.datetime.now(datetime.timezone.utc).timestamp() - datetime_attr.timestamp())

    if age_in_units == 0:
        age_stringed = 'только что'
    elif age_in_units < 60:
        age_stringed = str(age_in_units) + ' ' + declension_list[5][get_declension(age_in_units)] + ' назад'
    elif age_in_units < 3600:
        age_in_units //= 60
        age_stringed = str(age_in_units) + ' ' + declension_list[4][get_declension(age_in_units)] + ' назад'
    elif age_in_units < 86400:
        age_in_units //= 3600
        age_stringed = str(age_in_units) + ' ' + declension_list[3][get_declension(age_in_units)] + ' назад'
    elif age_in_units < 604800:
        age_in_units //= 86400
        age_stringed = str(age_in_units) + ' ' + declension_list[2][get_declension(age_in_units)] + ' назад'
    elif age_in_units < 31536000:
        age_in_units //= 2592000
        age_stringed = str(age_in_units) + ' ' + declension_list[1][get_declension(age_in_units)] + ' назад'
    else:
        age_in_units //= 31536000
        age_stringed = str(age_in_units) + ' ' + declension_list[0][get_declension(age_in_units)] + ' назад'

    return age_stringed

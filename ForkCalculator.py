from AllLibraries import *

def who_is_first(first_bk, second_bk):
    dict_order_bookmakers = {
        'fonbet pinnacle': 'fonbet',  # в последствии он будет заполнятся из настроек
        'ggbet pinnacle': 'ggbet',
        'fonbet ggbet': 'unknown',
    }
    bookmakers_list = [first_bk, second_bk]
    bookmakers_list.sort()
    bookmakers_pair = ' '.join(bookmakers_list)
    first_name = dict_order_bookmakers[bookmakers_pair]
    if first_name:
        return first_name
    else:
        return None
def order_total_bet(first_bet_name, how_do_total):

    #определяем где тотал больше, а где меньше
    if 'OVER' in first_bet_name.replace('_', ' ').replace('(', ' ').replace('  ', ' ').split(' '):
        first_value = 'OVER'
    else:
        first_value = 'UNDER'

    if how_do_total == 2:
        # ставим сначала больше
        if first_value == 'OVER':
            return True
        else:
            return False
    else:
        if first_value == 'UNDER':
            return True
        else:
            return False
def order_handicap_bet(first_bet_name, how_do_handicap):
    # определяем какая фора (положительная или отрицаельная) у первой бк
    if first_bet_name.replace('(', ' ').split(' ')[1][0] == '-':
        first_value = '-'
    else:
        first_value = '+'

    # определяем нужно ли менять местами первую и вторую бк
    if how_do_handicap == 2:
        if first_value == '+':
            return True
        else:
            return False
    else:
        if first_value == '-':
            return True
        else:
            return False

def order_of_betting(first_bk, first_cf, first_limit, second_bk, second_cf, second_limit, first_bet_name, second_bet_name, bet_type, how_do_total, how_do_handicap):
    dict_order_bookmakers = {
        'fonbet pinnacle': 'fonbet',         # в последствии он будет заполнятся из настроек
        'ggbet pinnacle': 'ggbet',
        'fonbet ggbet': 'unknown',
    }

    # правило проставления у тотала
    if how_do_total != 0:
        if 'TOTALS' in bet_type.split('_'):
            print('Работает особое правило проставления Тотал')
            if order_total_bet(first_bet_name=first_bet_name, how_do_total=how_do_total):
                print('Последовательность остается')
                return first_bk, first_cf, first_limit, second_bk, second_cf, second_limit
            else:
                print('Последовательность меняется')
                return second_bk, second_cf, second_limit, first_bk, first_cf, first_limit,

    # правило проставления форы
    if how_do_handicap != 0:
        if 'HANDICAP' in bet_type.split('_'):
            print('Работает особое правило проставления Форы')
            if order_handicap_bet(first_bet_name=first_bet_name, how_do_handicap=how_do_handicap):
                print('Последовательность остается')
                return first_bk, first_cf, first_limit, second_bk, second_cf, second_limit
            else:
                print('Последовательность меняется')
                return second_bk, second_cf, second_limit, first_bk, first_cf, first_limit,

    print('Особое правило не подействовало, определяем порядок по умолчанию (правила проставления)')
    bookmakers_list = [first_bk, second_bk]
    bookmakers_list.sort()
    bookmakers_pair = ' '.join(bookmakers_list)
    try:
        who_is_first = dict_order_bookmakers[bookmakers_pair]
    except:
        return None, None, None, None, None, None
    if who_is_first == first_bk:
        return first_bk, first_cf, first_limit, second_bk, second_cf, second_limit
    else:
        return second_bk, second_cf, second_limit, first_bk, first_cf, first_limit,


def is_fork_fit(bet_sum, bet_limit, bet_cf, exchange_rate,
                        another_limit, another_cf, another_exchange_rate,
                        min_profit, max_profit, min_cf, max_cf):
    # рассчитываем новую прибыль
    try:
        income = (((bet_cf * another_cf) / (bet_cf + another_cf)) * 100) - 100
    except:
        print("проблемы с расчетом выгоды")
        return False
    if income < min_profit or income > max_profit:
        print('Прибыль:', income)
        return False

    # рассчитываем не мешает ли лимит первой бк сделать ставку
    if bet_sum > bet_limit:
        print('Фиксированная сумма ставки:', bet_sum)
        print('Лимит по ставке:', bet_sum)
        return False

    # рассчитываем не мешает ли лимит второй бк сделать ставку
    another_bet_sum = round(((bet_sum * bet_cf * exchange_rate) / another_cf) / another_exchange_rate)
    if another_bet_sum > another_limit:
        print('Сумма для перекрытия 2ого плеча:', another_bet_sum)
        print('Лимит по ставке (2ой):', another_limit)
        return False

    # проверяем находится ли коэффициент первой бк в заданном диапазоне
    if bet_cf < min_cf or bet_cf > max_cf:
        print('Первый кф:', bet_cf)
        return False

    # проверяем находится ли коэффициент второй бк в заданном диапазоне
    if another_cf < min_cf or another_cf > max_cf:
        print('Второй кф:', another_cf)
        return False

    return True
from AllLibraries import *


def bet_calc(pin_cf, ggbet_cf, pin_limit, ggbet_limit,
             is_rub_pin, is_rub_ggbet, ggbet_exchange_rate, pin_exchange_rate,
             settings_type_limit, settings_sum_limit):
    print('Pinnacle    ', pin_cf, pin_limit)
    print('GGbet    ', ggbet_cf, ggbet_limit)
    print(is_rub_pin, is_rub_ggbet)
    print(pin_exchange_rate, ggbet_exchange_rate)
    print(type(pin_exchange_rate), type(ggbet_exchange_rate))
    print(settings_type_limit, settings_sum_limit)

    total_prob = 1 / ggbet_cf + 1 / pin_cf
    print(total_prob)
    if total_prob > 1:
        print('Данная вилка исчезла')
        return 0
    pin_exchange_rate = float(pin_exchange_rate)
    ggbet_exchange_rate = float(ggbet_exchange_rate)
    rub_pin_limit = pin_limit * pin_exchange_rate
    rub_ggbet_limit = ggbet_limit * ggbet_exchange_rate

    if not is_rub_pin and is_rub_ggbet:  # если пинка не в рублях, а бетка в рублях
        print('start bet calc')
        if settings_type_limit == 1:  # задана общая сумма двух ставок
            print('start type 1')
            # определяем, сколько ставить на пинку
            rub_pinnacle_sum_bet = math.ceil(1 / pin_cf / total_prob * float(settings_sum_limit))
            # если ставка больше лимита, то ставка равняется лимиту
            if rub_pinnacle_sum_bet > rub_pin_limit:
                rub_pinnacle_sum_bet = rub_pin_limit

            # избавляемся от центов
            rub_pinnacle_sum_bet = (rub_pinnacle_sum_bet // pin_exchange_rate) * pin_exchange_rate

            # рассчитываем вторую ставку (ggbet)
            rub_ggbet_sum_bet = math.ceil((rub_pinnacle_sum_bet * pin_cf) / ggbet_cf)
            # если ставка больше лимита, то ставка равняется лимиту
            if rub_ggbet_sum_bet > rub_ggbet_limit:
                rub_ggbet_sum_bet = rub_ggbet_limit
                # заново рассчитываем ставку на пинке
                rub_pinnacle_sum_bet = math.ceil((rub_ggbet_sum_bet * ggbet_cf) / pin_cf)
                # округляем новую ставку на пинке
                rub_pinnacle_sum_bet = (rub_pinnacle_sum_bet // pin_exchange_rate) * pin_exchange_rate
                # считаем по новой ставке ставку на ggbet
                rub_ggbet_sum_bet = math.ceil((rub_pinnacle_sum_bet * pin_cf) / ggbet_cf)

            pinnacle_sum_bet = int(rub_pinnacle_sum_bet / pin_exchange_rate)
            ggbet_sum_bet = int(rub_ggbet_sum_bet / ggbet_exchange_rate)

        if settings_type_limit == 2:    # задана ставка для пинки

            rub_pinnacle_sum_bet = settings_sum_limit

            # если ставка больше лимита, то ставка равняется лимиту
            if rub_pinnacle_sum_bet > rub_pin_limit:
                rub_pinnacle_sum_bet = rub_pin_limit

            # округляем ставку на пинке (убираем копейке в валюте)
            rub_pinnacle_sum_bet = (rub_pinnacle_sum_bet // pin_exchange_rate) * pin_exchange_rate

            # рассчитываем вторую ставку (ggbet)
            rub_ggbet_sum_bet = math.ceil((rub_pinnacle_sum_bet * pin_cf) / ggbet_cf)

            # если ставка больше лимита, то ставка равняется лимиту
            if rub_ggbet_sum_bet > rub_ggbet_limit:
                rub_ggbet_sum_bet = rub_ggbet_limit
                # заново рассчитываем ставку на пинке
                rub_pinnacle_sum_bet = math.ceil((rub_ggbet_sum_bet * ggbet_cf) / pin_cf)
                # округляем новую ставку на пинке
                rub_pinnacle_sum_bet = (rub_pinnacle_sum_bet // pin_exchange_rate) * pin_exchange_rate
                # считаем по новой ставке ставку на ggbet
                rub_ggbet_sum_bet = math.ceil((rub_pinnacle_sum_bet * pin_cf) / ggbet_cf)

            pinnacle_sum_bet = int(rub_pinnacle_sum_bet / pin_exchange_rate)
            ggbet_sum_bet = int(rub_ggbet_sum_bet / ggbet_exchange_rate)


        if settings_type_limit == 3:    # задана ставка для ggbet
            rub_ggbet_sum_bet = settings_sum_limit

            # если ставка больше лимита, то ставка равняется лимиту
            if rub_ggbet_sum_bet > rub_ggbet_limit:
                rub_ggbet_sum_bet = rub_ggbet_limit

            # рассчитываем ставку для пинки
            rub_pinnacle_sum_bet = math.ceil((rub_ggbet_sum_bet * ggbet_cf) / pin_cf)

            # если ставка больше лимита, то ставка равняется лимиту
            if rub_pinnacle_sum_bet > rub_pin_limit:
                rub_pinnacle_sum_bet = rub_pin_limit

            # округляем ставку на пинке
            rub_pinnacle_sum_bet = (rub_pinnacle_sum_bet // pin_exchange_rate) * pin_exchange_rate
            # рассчитываем ставку на ггбет
            rub_ggbet_sum_bet = math.ceil((rub_pinnacle_sum_bet * pin_cf) / ggbet_cf)

            pinnacle_sum_bet = int(rub_pinnacle_sum_bet / pin_exchange_rate)
            ggbet_sum_bet = int(rub_ggbet_sum_bet / ggbet_exchange_rate)

    # далее, если ggbet не в рублях


    if is_rub_pin and is_rub_ggbet:     # далее, если оба бк в рублях
        print('Этот раздел')

        if settings_type_limit == 1:  # задана общая сумма двух ставок
            print('вход')
            # рассчитываем сумму для пинки
            pinnacle_sum_bet = math.ceil(1 / pin_cf / total_prob * float(settings_sum_limit))
            ggbet_sum_bet = math.ceil(1 / ggbet_cf / total_prob * float(settings_sum_limit))

            if pinnacle_sum_bet > pin_limit:
                pinnacle_sum_bet = pin_limit
                ggbet_sum_bet = math.ceil((pinnacle_sum_bet * pin_cf) / ggbet_cf)

            if ggbet_sum_bet > ggbet_limit:
                ggbet_sum_bet = ggbet_limit
                pinnacle_sum_bet = math.ceil((ggbet_sum_bet * ggbet_cf) / pin_cf)

        if settings_type_limit == 2:  # задана ставка для пинки
            print('вход')
            pinnacle_sum_bet = settings_sum_limit

            print('1 чекпоинт')
            #если ставка больше лимита, то ставка равняется лимиту
            if pinnacle_sum_bet > pin_limit:
                pinnacle_sum_bet = pin_limit
            print('2 чекпоинт')
            ggbet_sum_bet = math.ceil((pinnacle_sum_bet * pin_cf) / ggbet_cf)
            if ggbet_sum_bet > ggbet_limit:
                ggbet_sum_bet = ggbet_limit
                pinnacle_sum_bet = math.ceil((ggbet_sum_bet * ggbet_cf) / pin_cf)

            print('выход')

        if settings_type_limit == 3:  # задана ставка для ггбета

            ggbet_sum_bet = settings_sum_limit

            #если ставка больше лимита, то ставка равняется лимиту
            if ggbet_sum_bet > ggbet_limit:
                ggbet_sum_bet = ggbet_limit

            # рассчитываем сумму второго плеча
            pinnacle_sum_bet = math.ceil((ggbet_sum_bet * ggbet_cf) / pin_cf)
            # если ставка больше лимита, то ставка равняется лимиту
            if pinnacle_sum_bet > pin_limit:
                pinnacle_sum_bet > pin_limit
                ggbet_sum_bet = math.ceil((pinnacle_sum_bet * pin_cf) / ggbet_cf)


    return pinnacle_sum_bet, ggbet_sum_bet


"""
if __name__ == "__main__":
    first_cf = 1.24
    second_cf = 5.7
    first_ex = 50
    second_ex = 1
    a = bet_calc(pin_cf=first_cf, ggbet_cf=second_cf, pin_limit=100, ggbet_limit=1000000,
                 is_rub_pin=False, is_rub_ggbet=True, ggbet_exchange_rate=second_ex, pin_exchange_rate=first_ex,
                 settings_type_limit=1, settings_sum_limit=1000)
    if a != 0:
        first_bet_sum = a[0]
        second_bet_sum = a[1]
    print('V1')
    print('First | сумма ставки:', first_bet_sum*first_ex, 'кф:', first_cf, 'чистый выигрыш:', first_bet_sum*first_ex*(first_cf-1))
    print('Second | сумма ставки:', second_bet_sum*second_ex, 'кф:', second_cf, 'чистый выигрыш:', second_bet_sum * second_ex * (second_cf - 1))
    print()

    first_cf = 1.24
    second_cf = 5.7
    first_ex = 50
    second_ex = 1
    a = bet_calc(pin_cf=first_cf, ggbet_cf=second_cf, pin_limit=1000, ggbet_limit=100,
                 is_rub_pin=False, is_rub_ggbet=True, ggbet_exchange_rate=second_ex, pin_exchange_rate=first_ex,
                 settings_type_limit=2, settings_sum_limit=1760)
    if a != 0:
        first_bet_sum = a[0]
        second_bet_sum = a[1]
    print('V2')
    print('First | сумма ставки:', first_bet_sum * first_ex, 'кф:', first_cf, 'чистый выигрыш:',
          first_bet_sum * first_ex * (first_cf - 1))
    print('Second | сумма ставки:', second_bet_sum * second_ex, 'кф:', second_cf, 'чистый выигрыш:',
          second_bet_sum * second_ex * (second_cf - 1))
    print()

    first_cf = 1.24
    second_cf = 5.7
    first_ex = 50
    second_ex = 1
    a = bet_calc(pin_cf=first_cf, ggbet_cf=second_cf, pin_limit=37, ggbet_limit=350,
                 is_rub_pin=False, is_rub_ggbet=True, ggbet_exchange_rate=second_ex, pin_exchange_rate=first_ex,
                 settings_type_limit=3, settings_sum_limit=1000)
    if a != 0:
        first_bet_sum = a[0]
        second_bet_sum = a[1]
    print('V3')
    print('First | сумма ставки:', first_bet_sum * first_ex, 'кф:', first_cf, 'чистый выигрыш:',
          first_bet_sum * first_ex * (first_cf - 1))
    print('Second | сумма ставки:', second_bet_sum * second_ex, 'кф:', second_cf, 'чистый выигрыш:',
          second_bet_sum * second_ex * (second_cf - 1))
    print()

    first_cf = 3.33
    second_cf = 1.47
    first_ex = 1
    second_ex = 1
    a = bet_calc(pin_cf=first_cf, ggbet_cf=second_cf, pin_limit=64300, ggbet_limit=240000,
                 is_rub_pin=True, is_rub_ggbet=True, ggbet_exchange_rate=second_ex, pin_exchange_rate=first_ex,
                 settings_type_limit=2, settings_sum_limit=1000)
    if a != 0:
        first_bet_sum = a[0]
        second_bet_sum = a[1]
    print('V4')
    print('First | сумма ставки:', first_bet_sum * first_ex, 'кф:', first_cf, 'чистый выигрыш:',
          first_bet_sum * first_ex * (first_cf - 1))
    print('Second | сумма ставки:', second_bet_sum * second_ex, 'кф:', second_cf, 'чистый выигрыш:',
          second_bet_sum * second_ex * (second_cf - 1))
    print()"""
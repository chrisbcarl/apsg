import sys
import math
from random import uniform, randint

def generate_stock_data(start, end, low, high, console_log=False):
    output = 'data/data' + '-'.join([str(start), str(end), str(low), str(high)]) + '.dat'
    with open(output, 'w') as f:
        total = end - start
        console_threshold = 1000
        j = 0

        if console_log:
            print ('generating...0%', end="\r")
        intraday = [(high + low) / 2]
        for i in range(1, end - start):
            intraday_prev = intraday[i - 1]
            if intraday_prev > 0:
                intraday_new = intraday_prev + randint(-1,1) * uniform(0, 1)
                # intraday_new = intraday_prev + randint(-1, 2) * randint(-1,1) * uniform(0, 1)
            else:
                intraday_new = 0 + randint(-1, 2) * randint(-1,1) * uniform(0, 1)
                intraday_new = intraday_new if intraday_new > 0 else 0
            intraday.append(intraday_new)
            f.write(str(intraday_new) + ' ')
            if console_log and i % console_threshold == 0:
                j += 1
                print('generating...{0:0.3f}%'.format(j * console_threshold / total * 100), end='\r')

        print('generated 100%          ', end='\n\n')
        f.close()
        return intraday
    return[0]


def trade_commodity(trade, capital_in_bank, capital_in_commodities, commodity_price):
    if trade == 'sell':
        if capital_in_commodities > 0:
            capital_in_commodities -= commodity_price
            capital_in_bank += commodity_price
    elif trade == 'buy':
        if capital_in_bank > 0:
            capital_in_commodities += commodity_price
            capital_in_bank -= commodity_price
    elif trade == 'hold':
        capital_in_commodities += 0
        capital_in_bank += 0

    return capital_in_bank, capital_in_commodities

def buy_commodity(capital_in_commodities, commodity_price):
    capital_in_commodities = capital_in_commodities + commodity_price
    return capital_in_commodities

def func(principal, start, end, low, high, sample_rate, trading_threshold, command_line=False):
    capital_in_commodities = principal / 2
    capital_in_bank =  principal / 2

    intraday = generate_stock_data(0, end - start, low, high, command_line)
    print(intraday)


if __name__ == '__main__':
    principal = 1000
    start = 0
    end = 10000
    low = 100
    high = 200
    sample_rate = 1
    trading_threshold = 0.03
    func(principal, start, end, low, high, sample_rate, trading_threshold, True)
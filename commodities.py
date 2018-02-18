import sys
import math
from random import uniform, randint
from matplotlib import pyplot as pt



def generate_stock_data(start, end, low, high, console_log=False):
    with open('data' + '-'.join([str(start), str(end), str(low), str(high)]) + '.dat', 'w') as f:
        total = end - start
        console_threshold = 1000
        j = 0

        print ('generating...0%', end="\r")
        intraday = [(high + low) / 2]
        for i in range(1, end - start):
            intraday_prev = intraday[i - 1]
            if intraday_prev > 0:
                intraday_new = intraday_prev + randint(-1, 2) * randint(-1,1) * uniform(0, 1)
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

def func(principal, start, end, low, high):
    principal = 1000
    capital_in_commodities = principal / 2
    capital_in_bank =  principal / 2
    time_quantum = 60
    difference_threshold = 0.03

    intraday = generate_stock_data(0, end - start, low, high, True)
    print('plotting...', end='')
    pt.figure(figsize=(16,9), dpi=300)
    pt.plot(intraday)
    pt.savefig('./graph' + '-'.join([str(start), str(end), str(low), str(high)]) + '.png')
    print('saved graph')

    for s in range(1, len(intraday), time_quantum):
        commodity_price = intraday[s]
        commodity_price_prev = intraday[s-time_quantum]
        if commodity_price_prev:
            difference = ( commodity_price - commodity_price_prev ) / commodity_price_prev
        else:
            difference = 0

        if abs(difference) > difference_threshold:    
            if difference < 0:
                capital_in_bank, capital_in_commodities = trade_commodity('buy', capital_in_bank, capital_in_commodities, commodity_price)
            elif difference > 0:
                capital_in_bank, capital_in_commodities = trade_commodity('sell', capital_in_bank, capital_in_commodities, commodity_price)
            elif difference < difference_threshold:
                capital_in_bank, capital_in_commodities = trade_commodity('hold', capital_in_bank, capital_in_commodities, commodity_price)

    print('principal', principal)
    print('capital_in_bank', capital_in_bank)
    print('capital_in_commodities', capital_in_commodities)

if __name__ == '__main__':
    func(1000, 0, 1000000, 100, 200)
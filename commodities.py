import sys
import math
from random import uniform, randint
from matplotlib import pyplot as pt
import argparse

parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--width", "-w", help="set output width")

parser = argparse.ArgumentParser(description='Generate stock market data as well as compute profitability of several algorithms')

# positional arguments
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')

# optional arguments
parser.add_argument("-pr", "--principal", action="store", type=float,
                    help="principal amount of money to invest at the start")
parser.add_argument("-st", "--start", action="store", type=int,
                    help="timestamp in seconds of when to start")
parser.add_argument("-en", "--end", action="store", type=int,
                    help="timestamp in seconds of when to stop")
parser.add_argument("-lo", "--low", action="store", type=float,
                    help="lowest 'bound' of commodity price (inital commodity price will be average of low and high)")
parser.add_argument("-hi", "--high", action="store", type=float,
                    help="highest 'bound' of commodity price (inital commodity price will be average of low and high)")
parser.add_argument("-sr", "--sample_rate", action="store", type=int,
                    help="sampling rate")
parser.add_argument("-tt", "--trading_threshold", action="store", type=float,
                    help="absolute trading threshold in decimal, 0 <= tt <= 1")


parser.add_argument("-o", "--output", action="store", type=str,
                    help="output file path array of commodity prices, relative to pwd")
parser.add_argument("-g", "--graph", action="store", type=str,
                    help="graph output file path of commodity prices")                    
parser.add_argument("-l", "--log", action="store", type=str,
                    help="log out all of the trades and history to the log file")
parser.add_argument("-i", "--input", action="store", type=str,
                    help="input file, array of commodity prices, relative to pwd")                    
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")

args = parser.parse_args()


def generate_stock_data(start, end, low, high, console_log=False):
    output = args.output if args.output else '/data/data' + '-'.join([str(start), str(end), str(low), str(high)]) + '.dat'
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

        if args.verbose:
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

    intraday = generate_stock_data(0, end - start, low, high, args.verbose)
    if command_line:
        print('plotting...', end='')
    pt.figure(figsize=(16,9), dpi=300)
    pt.plot(intraday)
    graph = args.graph if args.graph else 'graphs/graph' + '-'.join([str(start), str(end), str(low), str(high)]) + '.png'
    pt.savefig(graph)
    if command_line:
        print('saved graph')

    log = args.log if args.log else 'logs/log' + '-'.join([str(start), str(end), str(low), str(high)]) + '.txt'

    with open(log, 'w') as f:
        f.write('')
        f.close()
    with open (log, 'a') as f:
        for s in range(1, len(intraday), sample_rate):
            commodity_price = intraday[s]
            commodity_price_prev = intraday[s-sample_rate]
            if commodity_price_prev:
                difference = ( commodity_price - commodity_price_prev ) / commodity_price_prev
            else:
                difference = 0

            trade = ''
            if abs(difference) > trading_threshold:    
                if difference < 0:
                    trade = 'buy'
                elif difference > 0:
                    trade = 'sell'
            else:
                trade = 'hold'
            capital_in_bank, capital_in_commodities = trade_commodity(trade, capital_in_bank, capital_in_commodities, commodity_price)
            cli = '{0}\tprice == ${1:0.2f}\n\tprev == ${2:0.2f}\n\tdiff == {3:0.2f}%\t\t{4} {5:2.2f}%'.format(
                trade,
                commodity_price, 
                commodity_price_prev, 
                difference * 100,
                'above' if difference > trading_threshold else 'below',
                trading_threshold * 100
            )
            f.write(cli + '\n')
            if args.verbose:
                
                print(cli)

    output = args.output if args.output else 'data/summary' + '-'.join([str(start), str(end), str(low), str(high)]) + '.txt'
    with open(output, 'w') as f:
        if args.verbose:
            print('writing summary to', output, end="...")
        keys = ['principal', 'start', 'end', 'low', 'high', 'sample_rate', 'trading_threshold', 'capital_in_bank', 'capital_in_commodities']
        values = [principal, start, end, low, high, sample_rate, trading_threshold, capital_in_bank, capital_in_commodities]
        f.write(','.join(map(lambda key: str(key), keys)))
        f.write('\n')
        f.write(','.join(map(lambda val: str(val), values)))
        if args.verbose:
            print('file written')
        f.close()


if __name__ == '__main__':
    principal = args.principal if args.principal else 1000
    start = args.start if args.start else 0
    end = args.end if args.end else 10000
    low = args.low if args.low else 100
    high = args.high if args.high else 200
    sample_rate = args.sample_rate if args.sample_rate else 60
    trading_threshold = args.trading_threshold if args.trading_threshold else 0.03
    func(principal, start, end, low, high, sample_rate, trading_threshold, args.verbose)
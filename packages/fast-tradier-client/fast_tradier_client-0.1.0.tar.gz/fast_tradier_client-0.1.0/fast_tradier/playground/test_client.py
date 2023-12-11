from fast_tradier.FastTradierAsyncClient import FastTradierAsyncClient
from fast_tradier.FastTradierClient import FastTradierClient
from fast_tradier.utils.YFinanceQuoteProvider import YFinanceQuoteProvider
from fast_tradier.models.market_data.Quote import Quote
from fast_tradier.models.trading.OptionOrder import OptionLeg, OptionOrder
from fast_tradier.models.trading.EquityOrder import EquityOrder
from fast_tradier.models.trading.Sides import OptionOrderSide, EquityOrderSide
from fast_tradier.models.trading.PriceTypes import OptionPriceType, EquityPriceType
from fast_tradier.models.trading.Duration import Duration

from pathlib import Path
from datetime import datetime, timedelta
import asyncio
import json


#TODO: replace the client_id and sandbox access token with yours
sandbox_client_id = 'VA7432928'
sandbox_at = 'VuX3WA9Aq0mfORazBNM4d5bUA4zb'
yfin_real_quote_provider = YFinanceQuoteProvider()

def mock_order() -> OptionOrder:
    ticker = 'SPX'
    order_status = 'pending'
    option_symbols = ['SPXW_110223C4210', 'SPXW_110223C4220'] #TODO: replace option symbols
    sides = [OptionOrderSide.SellToOpen, OptionOrderSide.BuyToOpen]
    option_legs = []

    for i in range(len(sides)):
        opt_symbol = option_symbols[i]
        side = sides[i]
        option_legs.append(OptionLeg(underlying_symbol=ticker, option_symbol=opt_symbol, side=side, quantity=1))

    option_order = OptionOrder(ticker=ticker,
                            price=3.2,
                            price_type=OptionPriceType.Credit,
                            duration=Duration.Day,
                            option_legs=option_legs)
    return option_order

def mock_equity_order() -> EquityOrder:
    symbol = 'SPY'
    price = 379.0
    quantity = 1.0
    return EquityOrder(ticker=symbol, quantity=quantity, price=price, side=EquityOrderSide.Buy, price_type=EquityPriceType.Limit, duration=Duration.Gtc)

async def async_test():
    tasks = []
    count = 4
    tradier_client = FastTradierAsyncClient(sandbox_at, sandbox_client_id, is_prod=False, real_time_quote_provider=yfin_real_quote_provider)

    # quote1 = await tradier_client.get_quotes_async(['MSFT'])
    # print('quote1 last price: ', quote1[0].last)

    for i in range(count):
        m_order = mock_order()
        cloned_legs = m_order.clone_option_legs()
        assert cloned_legs[0].option_symbol == m_order.option_legs[0].option_symbol
        assert cloned_legs[0].side == m_order.option_legs[0].side
        tasks.append(asyncio.ensure_future(tradier_client.place_option_order_async(m_order)))

    order_ids = await asyncio.gather(*tasks)
    cancel_tasks = []
    for order_id in order_ids:
        print('order_id: ', order_id)
        cancel_tasks.append(asyncio.ensure_future(tradier_client.cancel_order_async(order_id)))

    is_canceled = await asyncio.gather(*cancel_tasks)
    for canceled in is_canceled:
        print('canceled? ', canceled)
    ### test equity order:
    equity_order = mock_equity_order()
    order_id = await tradier_client.place_equity_order_async(equity_order)
    print('equity order id: ', order_id)
    equity_order_canceled = await tradier_client.cancel_order_async(order_id)
    print('equity order canceld? ', equity_order_canceled)
    ### get option chain for spx
    ticker = 'spx'
    expiration = '2023-08-31' #TODO: replace the expiration date
    opt_chain_result = await tradier_client.get_option_chain_async(symbol=ticker, expiration=expiration)
    print('result of option chain: ', opt_chain_result)
    positions = await tradier_client.get_positions_async()
    print('positions: ', positions)
    exps = await tradier_client.get_option_expirations_async(symbol=ticker)
    print(f'ticker: {ticker} has exps: {exps}')

    print('------' * 10)
    balances = await tradier_client.get_account_balance_async()
    print('balances: ', balances.total_cash)
    account_orders = await tradier_client.get_account_orders_async()
    print('account orders count: ', len(account_orders))
    orders_json = []
    for acc in account_orders:
        print('acc: ', acc.to_json())
        orders_json.append(acc.to_json())
    json_file = Path(Path(__file__).resolve().parent, "orders_json.json")
    with open(json_file, 'w') as fp:
        fp.write(json.dumps(orders_json))

    if hasattr(balances, 'dt') and balances.pdt is not None:
        print('balances.pdt.to_json(): ', balances.pdt.to_json())
    elif hasattr(balances, 'margin') and balances.margin is not None:
        print('balances.margin.to_json: ', balances.margin.to_json())
    elif hasattr(balances, 'cash') and balances.cash is not None:
        print('balances.cash.to_json: ', balances.cash.to_json())

async def real_test_async():
    prod_at = 'OLtA2pZ3A9FFY7ZIsKcfcKRhJYAd'
    client_id = '6YA19668'
    tradier_client = FastTradierAsyncClient(prod_at, client_id, is_prod=True, real_time_quote_provider=yfin_real_quote_provider)
    expiration = '2023-10-20'
    ticker = 'spx'
    result = await tradier_client.get_option_chain_async(symbol=ticker, expiration=expiration)
    call_df, put_df = result['call_chain'], result['put_chain']
    call_df.to_csv('call_df.csv')
    put_df.to_csv('put_df.csv')
    print(call_df.head())
    print('------')
    print(put_df.head())

def sync_test():
    count = 4
    tradier_client = FastTradierClient(sandbox_at, sandbox_client_id, is_prod=False, real_time_quote_provider=yfin_real_quote_provider)
    # quote1 = tradier_client.get_quotes(['MSFT'])
    # print('quote1 last price: ', quote1[0].last)
    
    # m_order = mock_order()
    # cloned_legs = m_order.clone_option_legs()
    # assert cloned_legs[0].option_symbol == m_order.option_legs[0].option_symbol
    # assert cloned_legs[0].side == m_order.option_legs[0].side

    # order_id = tradier_client.place_option_order(m_order)
    # print('option order id: ', order_id)
    # order_status = tradier_client.get_order_status(order_id=order_id)
    # print(f'order_status: {order_status} for order_id: {order_id}')
    # canceled_order = tradier_client.cancel_order(order_id)
    # print('canceled order? ', canceled_order)
    
    # print('-------' * 10)
    # ### test equity order:
    # equity_order = mock_equity_order()
    # order_id = tradier_client.place_equity_order(equity_order)
    # print('equity order id: ', order_id)
    # equity_order_canceled = tradier_client.cancel_order(order_id)
    # print('equity order canceld? ', equity_order_canceled)

    # ### get option chain for spx
    # ticker = 'spx'
    # expiration = '2023-08-31' #TODO: replace the expiration date
    # opt_chain_result = tradier_client.get_option_chain(symbol=ticker, expiration=expiration)
    # print('result of option chain: ', opt_chain_result)
    # exps = tradier_client.get_option_expirations(symbol=ticker)
    # print(f'ticker: {ticker} has exps: {exps}')
    # positions = tradier_client.get_positions()
    # print('positions: ', positions)

    print('------' * 10)
    balances = tradier_client.get_account_balance()
    print('balances: ', balances.total_cash)
    if hasattr(balances, 'dt') and balances.pdt is not None:
        print('balances.pdt.to_json(): ', balances.pdt.to_json())
    elif hasattr(balances, 'margin') and balances.margin is not None:
        print('balances.margin.to_json: ', balances.margin.to_json())
    elif hasattr(balances, 'cash') and balances.cash is not None:
        print('balances.cash.to_json: ', balances.cash.to_json())

def get_history():
    ticker = 'SPY'
    start_date = datetime.now() + timedelta(days=-30)
    end_date = datetime.now() + timedelta(days=-2)
    # print(f'start_date: {start_date.date()}')
    # tradier_client = FastTradierClient(sandbox_at, sandbox_client_id, is_prod=False, real_time_quote_provider=yfin_real_quote_provider)
    # result_df = tradier_client.get_history(symbol=ticker, start_date=start_date.date(), end_date=end_date.date())
    # print('result_df: ', result_df)

async def get_history_async():
    ticker = 'SPY'
    start_date = datetime.now() + timedelta(days=-30)
    end_date = datetime.now() + timedelta(days=-2)
    tradier_client = FastTradierAsyncClient(sandbox_at, sandbox_client_id, is_prod=False, real_time_quote_provider=yfin_real_quote_provider)
    result_df = await tradier_client.get_history_async(symbol=ticker, start_date=start_date, end_date=end_date)
    print('result_df: ', result_df)

def get_order():
    order_id = '9389363'
    tradier_client = FastTradierClient(sandbox_at, sandbox_client_id, is_prod=False, real_time_quote_provider=yfin_real_quote_provider)
    cur_orders = tradier_client.get_account_orders()
    for cur_o in cur_orders:
        print(f'cur_o: {cur_o.to_json()}')

'''
cur_o: {'id': 9389363, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': -2.25, 'exec_quantity': 2.0, 'last_fill_price': 0.0, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:44:06.399Z', 'transaction_date': '2023-12-07T15:44:06.399Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 9389364, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': 3.5, 'exec_quantity': 1.0, 'last_fill_price': 3.5, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:44:06.399Z', 'transaction_date': '2023-12-07T15:44:06.399Z', 'class': 'option', 'option_symbol': 'SPXW231207C04590000'}, {'id': 9389365, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': 1.25, 'exec_quantity': 1.0, 'last_fill_price': 1.25, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:44:06.399Z', 'transaction_date': '2023-12-07T15:44:06.399Z', 'class': 'option', 'option_symbol': 'SPXW231207C04600000'}]}
cur_o: {'id': 9389401, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': -2.45, 'exec_quantity': 2.0, 'last_fill_price': 0.0, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:46:04.473Z', 'transaction_date': '2023-12-07T15:46:04.473Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 9389402, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': 3.9, 'exec_quantity': 1.0, 'last_fill_price': 3.9, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:46:04.473Z', 'transaction_date': '2023-12-07T15:46:04.473Z', 'class': 'option', 'option_symbol': 'SPXW231207C04590000'}, {'id': 9389403, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 1.8, 'avg_fill_price': 1.45, 'exec_quantity': 1.0, 'last_fill_price': 1.45, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T15:46:04.473Z', 'transaction_date': '2023-12-07T15:46:04.473Z', 'class': 'option', 'option_symbol': 'SPXW231207C04600000'}]}
cur_o: {'id': 9390234, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'canceled', 'duration': 'day', 'price': 0.8, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T16:20:04.707Z', 'transaction_date': '2023-12-07T16:24:04.813Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 9390235, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'canceled', 'duration': 'day', 'price': 0.8, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T16:20:04.707Z', 'transaction_date': '2023-12-07T16:24:04.813Z', 'class': 'option', 'option_symbol': 'SPXW231207P04545000'}, {'id': 9390236, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'canceled', 'duration': 'day', 'price': 0.8, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T16:20:04.707Z', 'transaction_date': '2023-12-07T16:24:04.813Z', 'class': 'option', 'option_symbol': 'SPXW231207P04535000'}]}
cur_o: {'id': 9395790, 'type': 'debit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.45, 'exec_quantity': 2.0, 'last_fill_price': 0.0, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:05.939Z', 'transaction_date': '2023-12-07T20:37:13.533Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 9395791, 'type': 'debit', 'symbol': 'SPX', 'side': 'buy_to_close', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.5, 'exec_quantity': 1.0, 'last_fill_price': 0.5, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:05.939Z', 'transaction_date': '2023-12-07T20:37:13.533Z', 'class': 'option', 'option_symbol': 'SPXW231207C04590000'}, {'id': 9395792, 'type': 'debit', 'symbol': 'SPX', 'side': 'sell_to_close', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.05, 'exec_quantity': 1.0, 'last_fill_price': 0.05, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:05.939Z', 'transaction_date': '2023-12-07T20:37:13.533Z', 'class': 'option', 'option_symbol': 'SPXW231207C04600000'}]}
cur_o: {'id': 9395793, 'type': 'debit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.45, 'exec_quantity': 2.0, 'last_fill_price': 0.0, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:07.018Z', 'transaction_date': '2023-12-07T20:37:03.361Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 9395794, 'type': 'debit', 'symbol': 'SPX', 'side': 'buy_to_close', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.5, 'exec_quantity': 1.0, 'last_fill_price': 0.5, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:07.018Z', 'transaction_date': '2023-12-07T20:37:03.361Z', 'class': 'option', 'option_symbol': 'SPXW231207C04590000'}, {'id': 9395795, 'type': 'debit', 'symbol': 'SPX', 'side': 'sell_to_close', 'quantity': 1.0, 'status': 'filled', 'duration': 'day', 'price': 0.45, 'avg_fill_price': 0.05, 'exec_quantity': 1.0, 'last_fill_price': 0.05, 'last_fill_quantity': 1.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:34:07.018Z', 'transaction_date': '2023-12-07T20:37:03.361Z', 'class': 'option', 'option_symbol': 'SPXW231207C04600000'}]}
cur_o: {'id': 9396783, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.476Z', 'transaction_date': '2023-12-07T20:52:45.550Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000', 'leg': [{'id': 9396787, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.476Z', 'transaction_date': '2023-12-07T20:52:45.546Z', 'class': 'option', 'option_symbol': 'SPXW231102C04210000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}, {'id': 9396792, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.476Z', 'transaction_date': '2023-12-07T20:52:45.548Z', 'class': 'option', 'option_symbol': 'SPXW231102C04220000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}]}
cur_o: {'id': 9396784, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.550Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000', 'leg': [{'id': 9396788, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.546Z', 'class': 'option', 'option_symbol': 'SPXW231102C04210000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}, {'id': 9396791, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.548Z', 'class': 'option', 'option_symbol': 'SPXW231102C04220000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}]}
cur_o: {'id': 9396785, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.477Z', 'transaction_date': '2023-12-07T20:52:45.550Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000', 'leg': [{'id': 9396789, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.477Z', 'transaction_date': '2023-12-07T20:52:45.546Z', 'class': 'option', 'option_symbol': 'SPXW231102C04210000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}, {'id': 9396793, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.477Z', 'transaction_date': '2023-12-07T20:52:45.549Z', 'class': 'option', 'option_symbol': 'SPXW231102C04220000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}]}
cur_o: {'id': 9396782, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.551Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000', 'leg': [{'id': 9396786, 'type': 'credit', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.547Z', 'class': 'option', 'option_symbol': 'SPXW231102C04210000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}, {'id': 9396790, 'type': 'credit', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'rejected', 'duration': 'day', 'price': 3.2, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:45.465Z', 'transaction_date': '2023-12-07T20:52:45.549Z', 'class': 'option', 'option_symbol': 'SPXW231102C04220000', 'reason_description': 'There is no price. Security symbol: SPXW231102C04210000'}]}
cur_o: {'id': 9396797, 'type': 'limit', 'symbol': 'SPY', 'side': 'buy', 'quantity': 1.0, 'status': 'canceled', 'duration': 'gtc', 'price': 379.0, 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 0.0, 'create_date': '2023-12-07T20:52:46.371Z', 'transaction_date': '2023-12-07T20:52:46.788Z', 'class': 'equity'}

'''

# asyncio.run(async_test())
# asyncio.run(real_test_async())
print('-------finished async tests--------')
# sync_test()
print('-------finished sync tests-------')
# get_order()
# get_history()
asyncio.run(get_history_async())
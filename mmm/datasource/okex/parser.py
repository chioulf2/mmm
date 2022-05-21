from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from mmm.events import TradesEvent, OrderBookEvent
from mmm.events.parser import Parser


class ParserFactory:
    def __init__(self):
        self.__register__ = {}

    def get_parser(self, channel: str) -> "Parser":
        try:
            return self.__register__[channel]
        except KeyError:
            raise RuntimeError(f'找不到{channel}对应的解析器')

    def add_parser(self, channel: str, parser: "Parser"):
        self.__register__[channel] = parser


class TradesParser(Parser):

    def parse(self, data: Dict) -> "TradesEvent" or List["TradesEvent"]:
        result = []
        data = data['data']
        for each in data:
            ticker = TradesEvent(each['instId'], Decimal(each['px']), Decimal(each['sz']), each['side'],
                                 datetime.fromtimestamp(int(each['ts'])/1000))
            result.append(ticker)
        return result


class OrderbookParser(Parser):

    def parse(self, data: Dict) -> "OrderBookEvent":
        return OrderBookEvent()  # todo


parser_factory = ParserFactory()
parser_factory.add_parser('trades', TradesParser())
parser_factory.add_parser('books', OrderbookParser())


















import json
import time
from googlefinance import getQuotes
from TextMessage import TextMessage

class StockNotification:
	def __init__(self, stock_dict): #stock_dict {stock_name: notification_stock_price}
		self._stock_dict = stock_dict
		self._message_sent = False
		
	def _get_current_market_price(self, stock_name):
		return json.dumps(getQuotes(stock_name)[0]['LastTradePrice'])[1:-1]

	def _stock_is_greater(self, stock_name, wanted_stock_price):
		return float(self._get_current_market_price(stock_name)) >= float(wanted_stock_price)
	
	def _message_to_send(self, stock_name):
		return stock_name+': '+str(self._get_current_market_price(stock_name))
	
	def notify(self):
		for stock_info in self._stock_dict.items():
			stock_name = stock_info[0]
			wanted_stock_price = stock_info[1]
			if (self._stock_is_greater(stock_name, wanted_stock_price)):
				message = self._message_to_send(stock_name)
				server = TextMessage()
				server.send_message(message)
				print(message)
				self._message_sent = True
	
	def message_sent(self):
		return self._message_sent
	
if __name__ == "__main__":
	stockNotification = StockNotification({'EFOI': 9})
	while (True):
		stockNotification.notify()
		if (stockNotification.message_sent()):
			break
		time.sleep(5)
		
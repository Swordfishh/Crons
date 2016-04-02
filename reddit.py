import praw		# reddit api
import time
import datetime
from TextMessage import TextMessage

class BuildAPcNotification:
	
	def __init__(self):
		self._CHARACTER_COUNT = 150 # get msg less than 150 character count
		self.send_msg = False
		self.message = 'testing'
		self.message_counter = 1;
		
	def get_new_reddit_post(self, category = 'all'): # category = 'all' for all categories
		self.send_msg = False
		
		r = praw.Reddit(user_agent='')
		submissions = r.get_subreddit('buildapcsales').get_new(limit=1)
		for submission in submissions:
			if (category == 'all' or (category != 'all' and category.lower() == str(vars(submission)['link_flair_text']).lower())):
				title = vars(submission)['title']
				url = vars(submission)['url']
				if (len(url) + len(title) >= self._CHARACTER_COUNT): # max character count 160
					if (len(url) >= self._CHARACTER_COUNT):
						this_msg = str(title[:self._CHARACTER_COUNT-1])
					else:
						title = title[0:(self._CHARACTER_COUNT - 1 - len(url))] # assume length or url is less than 160
						this_msg = str(title)+' - '+str(url)
				else:
					this_msg = str(title)+' - '+str(url)
				if (this_msg != self.message):			
					self.message = this_msg
					self.send_msg = True

	def send_text(self):
		if self.send_msg == True:
			server = TextMessage()
			server.send_message(self.message)			
			print('message '+str(self.message_counter)+' sent @: '+self._get_current_datetime())
			print('message '+str(self.message_counter)+' info: '+self.message)
			print('\n')
			self.message_counter += 1			
	
	def _get_current_datetime(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	def run(self):
		while True:
			self.get_new_reddit_post('all')
			self.send_text()
			time.sleep(5)
		
		
		
if __name__ == "__main__":
	reddit_bot = BuildAPcNotification()
	reddit_bot.run()
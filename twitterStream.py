from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

#Necesita un archivo txt que contenga en la primera linea la clave Consumer Key, en la segunda Consumer Secret, tercera Access Token y cuarta Access Token Secret
twitterDevData = open("TwitterKeys.txt")
ckey = twitterDevData.readline().rstrip('\n')
csecret = twitterDevData.readline().rstrip('\n')
atoken = twitterDevData.readline().rstrip('\n')
asecret = twitterDevData.readline().rstrip('\n')
twitterDevData.close()

class listener(StreamListener):

	def on_data(self, data):
		try:
			#print (data)

			tweet = data.split(',"text":"')[1].split('","source')[0]
			print (tweet)

			#saveFile = open('twitDB.csv','a')
			#saveFile.write(data)
			saveFile = open('twitDB2.csv','a')
			saveThis = str(time.time()) + '::' + tweet
			saveFile.write(saveThis)
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException:
			print ('failed ondata')
			time.sleep(5)

	def on_error(self, status):
		print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["aaahhlas12ded"])

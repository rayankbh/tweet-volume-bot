
# importing modules
import requests
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import tweepy, time
import operator

#Twitter credentials for Tweepy / setting up API 
CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'
ACCESS_KEY = 'xxxx'
ACCESS_SECRET = 'xxxx'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# establishing Twitter API bearer token and search URL (tweet count data)
bearer_token = "xxxx"
search_url = "https://api.twitter.com/2/tweets/counts/recent"

#Tweepy Client for sending tweets
client = tweepy.Client(bearer_token=bearer_token, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_KEY, access_token_secret=ACCESS_SECRET)


# bearer authentication and endpoint extracted from official twitterAPI site. 
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    #print(response.status_code) used to see if connected to endpoint successfully
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# Query for recent tweet count with parameters (volume of query per hour)
query_params = {'query': '','granularity': 'hour'}

#List of popular hashtags/tickers (currently crypto hastags, but can be cashtags once approved for elevated access)
ticker_list = ['#BTC', '#SHIB', '#Safemoon', '#Luna', '#ETH', '#XRP', '#USDT', '#BNB', '#Cardano', '#Solana', '#DOGE', '#Ripple']

  
# creating a dictionary and storing tweet volume (value) for each query (key)
tweet_count_dict = {}
for ticker in ticker_list:
    
    query_params['query'] = ticker

    json_response = connect_to_endpoint(search_url, query_params)
    tweet_counter = json_response['meta'] #accessing metadata 
    
    #extracting total tweet count from meta data 
    total_tweets = int(tweet_counter['total_tweet_count']) 

    #storing values into the empty dictionary tweet_count_dict
    tweet_count_dict[ticker] = total_tweets




def main():
   """stores sorted dictionary values in a .txt file which is used to then auto-tweet the information on bot twitter account"""
    
    # opening a txt file, storing for loop output inside 
    with open("tweet_data.txt", "w") as text_file:
        text_file.write("Here's the number of tweets sent out in the last hour per crypto hashtag: \n")
        
        # sorting the dictionary using operator module
        for k, v, in sorted(tweet_count_dict.items(),key=operator.itemgetter(1),reverse=True):
            text_file.write(f' {k}: {v:,}\n')

    text_file.close()


    #updating tweet status (posting)
    with open ('tweet_data.txt') as f:
        client.create_tweet(text = f.read())
        print(f.read())

    f.close()
    print('Success!')

    time.sleep(3600) #hourly update when code runs



def plot_data():
    """Converts dictionary to dataframe, and plots a horizontal bar graph in descending order """

    tweet_df = pd.DataFrame(list(tweet_count_dict.items()), columns = ['Hashtag', 'Number of Tweets'])

    fig, ax = plt.subplots(1, figsize=(8,8))

    # bar color gradient for graph
    bar_colors = ['#fafa6e', '#cdef72','#a4e27a', '#7dd382', '#58c389',  '#35b28e', '#0ea18f', '#008f8c', '#007d85', '#146b79', '#23596a', '#2a4858']
    

    #sorting values of dictionary and plotting into horizontal barplot
    tweet_df.sort_values(by='Number of Tweets').plot.barh(x='Hashtag',
                      y='Number of Tweets',
                      ax=ax,
                      color= bar_colors,
                      edgecolor = 'black')
    

    # removing scientific notion from y axis and converting to xxx,xxx,xxx format
    ax.get_xaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


    # bar plot properties 
    fig.set_tight_layout(True)
    ax.set_title("Tweet Volume of Popular Crypto Hashtags in the Last Hour", fontweight = 'bold')
    ax.set_facecolor(('#D6E5E3'))
    fig.set_facecolor(('#D6E5E3'))
    plt.show()


if __name__ == "__main__":
    main()
    plot_data()


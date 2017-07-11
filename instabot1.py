import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from clarifai.rest import  ClarifaiApp

APP_ACCESS_TOKEN = '1525979253.7d7ade8.a2d201f6ad2a4bbf9eded13b9094308f' #My own access token
API_KEY ='8yuXGEPkygEXsta5zfGza8JkD9EqleC7guz2xmS2BEE' #key for parallel dots
BASE_URL = 'https://api.instagram.com/v1/' #basic url of instagram
BASE_URL_paralleldots='https://apis.paralleldots.com/'  #url of parallel dots

def self_info():  #Getting our own details of instagram account
    request_url = (BASE_URL + 'users/self/?access_token=%s') %(APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_user_id(insta_username):  #Getting user id
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()



def get_user_info(insta_username):  #Fetching details of the user
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



def get_own_post():  #Getting our own post
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'




def get_user_post(insta_username): #Getting friends recent post
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_post_id(insta_username): #getting post id of user
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



def like_a_post(insta_username):  #Liking the most recent post of user
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'



def post_a_comment(insta_username):  #Commenting the recent post of user
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

def comment_analyse(insta_username):  #Analysing the comment based on sentiments
    media_id = get_post_id(insta_username)
    payload = {"access_token": APP_ACCESS_TOKEN}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'GET request url : %s' % (request_url)
    if media_id==None:
        print "No media exist"
        exit()
        if media_id['data']['text']==None:
            print "there is no comment to analyse"
        else:
            request_url = BASE_URL_paralleldots + 'sentiment?sentence1=%s&apikey=%s' % (input, API_KEY)
            response = requests.get(request_url).json()
            print response
            if response > 0.7:
                print "the response is positive"
            else:
                print "the response is negative"

def image_analyse(insta_username): #analyse the image based on sentiments
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "User does not exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url=user_media['data'][0]['images']['standard_resolution']['url']
            app = ClarifaiApp(api_key='f46c3d88d4a747598d8c109b244f366b')
            model = app.models.get('general-v1.0')
            response = model.predict_by_url('image-url=image_url')
            input = response
            request_url = BASE_URL_paralleldots + 'sentiment?sentence1=%s&apikey=%s' % (input, API_KEY)
            response = requests.get(request_url).json()
            print response
        else:
            print "image does not exist"
    else:
        print "status code other than 200"

def delete_negative_comment(insta_username):  #Deleting the negative comments
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def start_bot():  #Starting my own Instabot
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.Like the recent post of a user"
        print "f.Make a comment on the recent post of a user"
        print "g.Delete negative comments from the recent post of a user"
        print "h.Analyse a comment"
        print "i.Analyse an image"
        print "j.Exit"


        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            comment_analyse(insta_username)
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            image_analyse(insta_username)
        elif choice == "j":
            exit()
        else:
            print "wrong choice"

start_bot()

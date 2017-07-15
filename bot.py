import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored

# Storing access token in a variable
access_token = "1438763650.15994de.413f7ba570f34e6fa0f36fc4bdb6a021"
# Storing base url in a variable
base_url = "https://api.instagram.com/v1/"
# storing username
username = "kansal.isha"

# Function to retrieve  users id
def get_user_id(instagram_username):
    try:
        # URL with endpoint to search user id
        url = base_url + "users/search/?q=%s&access_token=%s" % (instagram_username, access_token)
        # Display the get url
        print "Get Search Request Url: %s" % url
        # storing the data in a variable...data returned by the url is in json form
        user_info = requests.get(url).json()
        # If status code is 200...proceed
        if user_info['meta']['code'] == 200:
            # If there is info in json data array
            if len(user_info['data']):
                # Returning users id
                return user_info['data'][0]['id']
            else:
                # If no data then return nothing
                return None
        else:
            # If request url is incorrect or there is some other problem
            print colored("Status code is other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to get post id
def get_post_id(instagram_user_id):
    try:
        # Checking if user exist or not...If not then exit
        if instagram_user_id is None:
            print colored("user does not exist", 'red')
        else:
            # url to get the most recent media of user or another user
            url = (base_url + 'users/%s/media/recent/?access_token=%s') % (instagram_user_id, access_token)
            # Display get url
            print "Get post id url: %s" % url
            # storing the data in a variable...data returned by the url is in json form
            media = requests.get(url).json()
            # Variable for index like 1, 2, 3...
            j = 1
            # Checking if request has been accepted....if accepted thn proceed
            if media['meta']['code'] == 200:
                # Checking if data is there or not
                if len(media['data']):
                    # Display the id's of most recent posts
                    for i in range(len(media['data'])):
                        print colored((("%s." + media['data'][i]['id']) % j), 'blue')
                        j += 1
                    # Select the index of id to perform further operations
                    choice = int(raw_input(colored("Select the index of id", 'green')))
                    if choice <= len(media['data']):
                        # returning the id of the selected post
                        return media['data'][choice-1]['id']
                    else:
                        print colored("You entered wrong choice", 'red')
                else:
                    # If there is no data
                    print colored("There is no recent post ", 'red')
                    return None
            else:
                # If request url is incorrect or there is some other problem
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to retrieve self or other user's information
def users_info(instagram_username):
    try:
        # url to get information
        url = (base_url + "users/%s/?access_token=%s") % (instagram_username, access_token)
        # Display  Get url
        print "GET User_info Request Url: %s" % url
        # Requesting get method to get information and response is stored in a variable
        user_info = requests.get(url).json()
        # Checking if status code is 200 or not
        if user_info['meta']['code'] == 200:
            # If 200 Checking there is some info in json data array
            if len(user_info['data']):
                # If true printing info
                print "Username=%s" % colored(user_info['data']['username'], 'blue')
                print "User Id=%s" % colored(user_info['data']['id'], 'blue')
                print "Full name=%s" % colored(user_info['data']['full_name'], 'blue')
                print "No. of people you are following=%s" % colored(user_info['data']['counts']['follows'], 'blue')
                print "No. of people following you=%s" % colored(user_info['data']['counts']['followed_by'], 'blue')
                print "No. of posts=%s" % colored(user_info['data']['counts']['media'], 'blue')
                print "Website=%s" % colored(user_info['data']['website'], 'blue')
                print "Bio=%s" % colored(user_info['data']['bio'], 'blue')
            else:
                # If false then user does not exist
                print colored("User does not exist", 'red')
        else:
            # Is status code is not 200
            print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to get a list of likes
def get_likes_list(instagram_post_id):
    try:
        # list to store the name of users who like the post
        list1 = []
        # If there are no posts
        if instagram_post_id is None:
            print colored("There is no media", 'red')
        else:
            # Url to get list of likes
            url = (base_url + "media/%s/likes/?access_token=%s") % (instagram_post_id, access_token)
            # Display get url
            print "Get request Url:%s" % url
            # Requesting get method to get likes list and response is stored in a variable
            like_list = requests.get(url).json()
            # variable for index
            j = 1
            # If request is accepted
            if like_list['meta']['code'] == 200:
                #  If there is some data
                if len(like_list['data']):
                    # List of persons who liked this post
                    print colored("The person who liked this post are:", 'green')
                    for i in range(len(like_list['data'])):
                        print "%s." % j + colored(like_list['data'][i]['username'], 'blue')
                        list1.append(like_list['data'][i]['username'])
                        j += 1
                    # Returning list of person who liked this post
                    return list1
                else:
                    # If there is no data
                    print colored("No likes on this post", 'red')
            else:
                # If request url is incorrect or there is some other problem
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to like a post
def post_is_liked(instagram_post_id):
    try:
        # If there is no post
        if instagram_post_id is None:
            print colored("There is no post", 'red')
        else:
            # url to like a post
            url = (base_url + 'media/%s/likes') % instagram_post_id
            # Extra information to be given in case of Post method
            payload = {"access_token": access_token}
            # Display Post url
            print "Post request url:%s " % url
            # Requesting post method to like a post and response is stored in a variable
            post_like = requests.post(url, payload).json()
            # If request has been accepted
            if post_like['meta']['code'] == 200:
                print colored("Post liked successfully", 'blue')
            else:
                # If request url is incorrect or there is some other problem
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to check post will be liked or not
def like_a_post(instagram_post_id):
    try:
        # Get list of users who liked the post
        list2 = get_likes_list(instagram_post_id)
        if list2 is not None:
            # Check if it is liked by self or not...if yes display message
            if username in list2:
                print colored("You have already liked this post", 'red')
            else:
                # call a function to like a post
                post_is_liked(instagram_post_id)
        # If post is not liked by anyone then call a function to like post
        else:
            post_is_liked(instagram_post_id)
    except:
        print colored("There must be some problem", 'red')

# Function to delete like from post
def unlike_a_post(instagram_post_id):
    try:
        # Get list of users who liked the post
        list3 = get_likes_list(instagram_post_id)
        # Check if list of likes is empty or user itself has not liked the post....then there is nothing to unlike
        if list3 is None or username not in list3:
            print colored("Nothing to unlike...or you have not liked this post", 'red')
        # If above conditions are not satisfied thn proceed
        else:
            # If there is no media
            if instagram_post_id is None:
                print colored("There is no media in this account", 'red')
            # Otherwise the post will be unlike
            else:
                # Url to unlike a post
                url = base_url + 'media/%s/likes/?access_token=%s' % (instagram_post_id, access_token)
                # Display delete like url
                print "Delete request url: %s" % url
                # Requesting delete method to like a post and response is stored in a variable
                del_like = requests.delete(url).json()
                # If request is accepted
                if del_like['meta']['code'] == 200:
                    print colored(" Successfully unlike the post", 'blue')
                # If request url is incorrect or there is some other problem
                else:
                    print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Get recent media liked by user
def recent_media_liked():
    try:
        # url to get the list of recently liked posts
        url = (base_url + "users/self/media/liked/?access_token=%s") % access_token
        # Display get request url
        print "Get recent media liked url: %s" % url
        # Requesting get method to get a list of recently liked  posts and response is stored in a variable
        recent_media = requests.get(url).json()
        # If request is accepted
        if recent_media['meta']['code'] == 200:
            # If you have recently liked
            if len(recent_media['data']):
                # Displaying posts with username and post-id
                for i in range(len(recent_media['data'])):
                    print " You have recently like %s post with post id %s" \
                          % (colored(recent_media['data'][i]['user']['username'], 'blue'),
                             colored(recent_media['data'][i]['id'], 'blue'))
            else:
                # If no post is liked recently
                print colored("There is no media you have recently liked", 'red')
        # If request url is incorrect or there is some other problem
        else:
            print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to get list of comments
def get_comment_list(instagram_post_id):
    try:
        list4 = []
        # If there are no posts
        if instagram_post_id is None:
            print colored("There is no media", 'red')
        # proceed if media-id is returned
        else:
            # Url to get list of comments on a post
            url = base_url + "media/%s/comments/?access_token=%s" % (instagram_post_id, access_token)
            # Display get request url
            print "Get request url:%s" % url
            # Requesting get method to get a list of comments on post and response is stored in a variable
            comment_list = requests.get(url).json()
            # variable for index
            j = 1
            # If request is accepted
            if comment_list['meta']['code'] == 200:
                # If there are comments on post
                if len(comment_list['data']):
                    # Displaying comments posted by users
                    print colored("The person who commented on this post are:", 'green')
                    for i in range(len(comment_list['data'])):
                        print "%s. Comment: %s Posted by: %s" \
                              % (j, colored(comment_list['data'][i]['text'], 'blue'),
                                 colored(comment_list['data'][i]['from']['username'], 'blue'))
                        j += 1
                        list4.append(comment_list['data'][i]['from']['username'])
                    return list4
                else:
                    # If there are no comments
                    print colored("No comments on this post", 'red')
            # If request url is incorrect or there is some other problem
            else:
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to comment on a post
def post_comment(instagram_post_id):
    try:
        # If there are no posts
        if instagram_post_id is None:
            print colored("There is no media", 'red')
        # proceed if media-id is returned
        else:
            # url to like a post
            url = (base_url + 'media/%s/comments') % instagram_post_id
            # what user wants to comment..
            comment_text = raw_input(colored("Enter your comment", 'green'))
            # Extra information to be given in case of Post method
            payload = {"access_token": access_token, "text": comment_text}
            # Display Post url
            print "Post request url:%s " % url
            # Requesting post method to like a post and response is stored in a variable
            comment_post = requests.post(url, payload).json()
            # If request has been accepted
            if comment_post['meta']['code'] == 200:
                print colored("Comment posted successfully", 'blue')
            else:
                # If request url is incorrect or there is some other problem
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to decide from whose(self or other user) post you want to delete negative comments
def delete_negative_comments(instagram_user_id):
    try:
        # Get id of post
        media_id = get_post_id(instagram_user_id)
        # variable for index like 1,2,3....
        j = 1
        # If there are no posts
        if media_id is None:
            print colored("There is no media", 'red')
        # proceed if media-id is returned
        else:
            # Url to get list of comments on a post
            url = base_url + "media/%s/comments/?access_token=%s" % (media_id, access_token)
            # Display get request url
            print "Get request url:%s" % url
            # Requesting get method to get a list of comments on post and response is stored in a variable
            comment_list = requests.get(url).json()
            # If request is accepted
            if comment_list['meta']['code'] == 200:
                # If there are comments on post
                if len(comment_list['data']):
                        # If user wants to delete comments on other's post
                        if instagram_user_id is not "self":
                            for i in range(len(comment_list['data'])):
                                # If user has commented on that post
                                if username in comment_list['data'][i]['from']['username']:
                                    # Display all his comments
                                    print "%s. Comment posted by you is:%s " % \
                                          (j, colored(comment_list['data'][i]['text'], 'blue'))
                                    j += 1
                                    # Calling function to delete negative comments
                                    comment_is_deleted(comment_list['data'][i]['id'],
                                                       comment_list['data'][i]['text'], media_id)
                        # If user wants to delete negative comments from own post
                        else:
                            for i in range(len(comment_list['data'])):
                                # Calling function to delete negative comments
                                comment_is_deleted(comment_list['data'][i]['id'],
                                                   comment_list['data'][i]['text'], media_id)
    except:
        print colored("There must be some problem", 'red')

# Function to delete negative comments
def comment_is_deleted(c_id, text, media_id):
    try:
        # Storing the comment text
        comment_text = text
        # Storing comment id
        comment_id = c_id
        # Analysing the positivity and negativity of comment
        blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
        # If negative....delete the comment
        if blob.sentiment.p_neg > blob.sentiment.p_pos:
            print "Comment %s is negative" % colored(comment_text, 'red')
            url = (base_url + "media/%s/comments/%s") % (media_id, comment_id)
            print "Delete request url :%s" % url
            del_comment = requests.delete(url).json()
            if del_comment['meta']['code'] == 200:
                print colored("Negative comment deleted", 'blue')
            else:
                print colored("Request is not processed", 'red')
        # If average ask the user what to do
        elif blob.sentiment.p_neg == blob.sentiment.p_pos:
            print colored("Comment is average", 'blue')
            choice = raw_input(colored("Do you want to delete comment(Y/N)??", 'green'))
            # If user says yes delete the comment
            if choice.capitalize() == "Y":
                url = (base_url + "media/%s/comments/%s") % (media_id, comment_id)
                print "Delete request url :%s" % url
                del_comment = requests.delete(url).json()
                if del_comment['meta']['code'] == 200:
                    print colored("Comment deleted", 'blue')
                else:
                    print colored("Request is not processed", 'red')
            # otherwise not
            else:
                print colored("Comment is not deleted", 'blue')
        # If comment is positive
        else:
            print colored("Comment is positive", 'blue')
    except:
        print colored("There must be some problem", 'red')

# Function to get most recent post
def get_recent_post(instagram_user_id):
    try:
        # If id is there or not
        if instagram_user_id is None:
            print colored("User does not exist", 'red')
        else:
            # Url to fetch recent media
            url = (base_url + "users/%s/media/recent/?access_token=%s") % (instagram_user_id, access_token)
            # Display Get url
            print "Get recent post request url:%s" % url
            # Requesting get method to fetch recent  posts and response is stored in a variable
            media = requests.get(url).json()
            # If request has been accepted
            if media['meta']['code'] == 200:
                # Variable for index like 1,2,3....
                k = 1
                # If there are posts
                if len(media['data']):
                    # Traversing the json array if there are more tha  one post
                    for i in range(len(media['data'])):
                        # Checking the type of image
                        if media['data'][i]['type'] == "image":
                            print "%s. %s" % (k, colored(media['data'][i]['id'], 'blue'))
                        elif media['data'][i]['type'] == "carousel":
                            print colored("Carousel Images", 'magenta')
                            for j in range(len(media['data'][i]['carousel_media'])):
                                print "%s. (%s) %s" % (k, j, colored(media['data'][i]['id'], 'blue'))
                        else:
                            print colored("%s. This type of media is not supported", 'red') % k
                        k += 1
                    # Taking  index as  input from user
                    choice = int(raw_input(colored("Enter the index of post id", 'green')))
                    # asking what user want to do with the selected post
                    print colored("What u want to do??\n "
                                  "1.Download post\n "
                                  "2.Like post\n "
                                  "3.Comment on post\n", 'green')
                    choice2 = int(raw_input(colored("Enter your choice", 'blue')))
                    # Download post
                    if choice2 == 1:
                        image_name = media['data'][choice-1]['id'] + ".jpeg"
                        image_url = media['data'][choice-1]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print colored("Your image has been downloaded!!!", 'blue')
                    # like post
                    elif choice2 == 2:
                        like_a_post(instagram_user_id)
                    # Comment on post
                    elif choice2 == 3:
                        post_comment(instagram_user_id)
                else:
                    # If no posts by user
                    print colored("No Post is there", 'red')
            # If request url is incorrect or there is some other problem
            else:
                    print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to like post for special cases
def like_post_special_cases(post_id):
    try:
        if post_id is None:
            print 'No media '
        else:
            list6 = get_likes_list(post_id)
            if username in list6:
                print colored("You already liked this post", 'red')
            else:
                url = (base_url + "media/%s/likes") % post_id
                payload = {"access_token": access_token}
                print "Post request url:%s" % url
                post_like = requests.post(url, payload).json()
                if post_like['meta']['code'] == 200:
                    print colored("Post liked successfully", 'blue')
                else:
                    print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function for some special cases for posts
def special_posts(instagram_user_id):
    try:
        # If user-id is not returned
        if instagram_user_id is None:
            print colored("User does not exist", 'red')
        else:
            # url for fetch recent posts
            url = base_url + "users/%s/media/recent/?access_token=%s" % (instagram_user_id, access_token)
            # Display get request url
            print "Get request url:%s" % url
            # Requesting get method to fetch recent  posts and response is stored in a variable
            recent_media = requests.get(url).json()
            # If request has been accepted
            if recent_media['meta']['code'] == 200:
                # If there are posts
                if len(recent_media['data']):
                    # Asking user which type posts want to fetch
                    print colored("Choose one option from the following\n"
                                  " 1.Choose post with minimum no. of likes\n " 
                                  "2.Choose post with a particular text in caption\n", 'green')
                    choice = int(raw_input(colored("Enter your choice", 'blue')))
                    # If 1 user wants to fetch posts with minimum likes
                    if choice == 1:
                        # list to store likes count
                        like_list = []
                        # list to urls
                        url_list = []
                        # Traversing the array
                        for i in range(len(recent_media['data'])):
                            # Appending the likes count in list
                            like_list.append(recent_media['data'][i]['likes']['count'])
                            # Appending the urls
                            url_list.append(recent_media['data'][i]['images']['standard_resolution']['url'])
                        # initializing the variables to the first element of list
                        min_like_count = like_list[0]
                        # List of url
                        min_like_count_url = []
                        # List of id's
                        min_like_count_id = []
                        for j in range(1, len(like_list)):
                            # checking if there is other likes count less than min_count_variable
                            if min_like_count >= like_list[j]:
                                # if yes update the variable
                                min_like_count = like_list[j]
                        for s in range(len(recent_media['data'])):
                            if recent_media['data'][s]['likes']['count'] == min_like_count:
                                # Display the post with least likes
                                print "Post with least count likes %s is %s" \
                                      % (colored(min_like_count, 'blue'),
                                         colored(recent_media['data'][s]['images']['standard_resolution']['url'], 'blue'))
                                # add the url in url list
                                min_like_count_url.append(recent_media['data'][s]['images']['standard_resolution']['url'])
                                # add id in id list
                                min_like_count_id.append(recent_media['data'][s]['id'])
                        # Asking the user what you want to do with the post
                        print colored("What do you want to do with the post with minimum likes??\n "
                                      "1.Like post\n "
                                      "2. Download post\n ", 'green')
                        choice = int(raw_input(colored("Enter your choice", 'blue')))
                        t = 1
                        # If 1 like post
                        if choice == 1:
                            # If more than one post same minimum no of likes
                            for k in range(len(min_like_count_id)):
                                like_post_special_cases(min_like_count_id[k])
                        # If 2 download post
                        elif choice == 2:
                            # If more than one post same minimum no of likes
                            for k in range(len(min_like_count_url)):
                                image_name = "%s.Minimum_like_post.jpeg" % t
                                image_url = min_like_count_url[k]
                                urllib.urlretrieve(image_url, image_name)
                                print colored("Your image has been downloaded", 'blue')
                                t += 1
                        # wrong choice entered by user
                        else:
                            print colored("You entered wrong choice", 'red')
                            return
                    # If 2 user wants to fetch posts with particular words in caption
                    elif choice == 2:
                        # List to store image name
                        image_name_list = []
                        # List to store urls
                        image_url_list = []
                        # List to store id's
                        image_id = []
                        # Asking the user which word want to search
                        word = raw_input(colored("Enter the particular word you want to search in caption??", 'blue'))
                        # variable for index like 1,2,3..
                        c = 1
                        # Traversing the json array
                        for i in range(len(recent_media['data'])):
                            # If there is caption in post
                            if recent_media['data'][i]['caption'] is not None:
                                # If the word is in caption
                                if word in recent_media['data'][i]['caption']['text']:
                                    # name the image
                                    name_image = "%s.Post with particular word in caption.jpeg" % c
                                    c += 1
                                    # append the name to image name list
                                    image_name_list.append(name_image)
                                    # append the url to url list
                                    image_url_list.append(recent_media['data'][i]['images']['standard_resolution']['url'])
                                    image_id.append(recent_media['data'][i]['id'])
                        # Checking if there is any post with particular word
                        if len(image_name_list) > 0:
                            # If yes asking the user what to do with the posts
                            print colored("What you want to do with "
                                          "the posts with particular word in caption??\n"
                                          "1. Like posts\n"
                                          "2. Download posts\n", 'green')
                            choice = int(raw_input(colored("Enter your choice", 'blue')))
                            # If 1 like post
                            if choice == 1:
                                # If more than one post same word
                                for k in range(len(image_name_list)):
                                    like_post_special_cases(image_id[k])
                            # if 2 download images
                            elif choice == 2:
                                # If more than one post same word
                                for k in range(len(image_name_list)):
                                    urllib.urlretrieve(image_url_list[k], image_name_list[k])
                                    print colored("Your images has been downloaded", 'blue')
                        # If no post with particular word display message
                        else:
                            print colored("No post with this particular word", 'red')
                    # User entered wrong choice
                    else:
                        print colored("You entered wrong choice", 'red')
                # If there are no posts
                else:
                    print colored("No recent posts", 'red')
            # If request url is incorrect or there is some other problem
            else:
                print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to get natural calamity images
def natural_calamity_pics():
    try:
        # User's input for location
        location = raw_input(colored("Enter the location for which you want to inspect pics??", 'green'))
        # url to find coordinates
        google_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" % location
        # Get location coordinates
        location_coordinates = requests.get(google_url).json()
        # Get latitude
        location_latitude = location_coordinates['results'][0]['geometry']['location']['lat']
        # Get longitude
        location_longitude = location_coordinates['results'][0]['geometry']['location']['lng']
        # Print coordinates  of location
        print colored("coordinates of location: %s" % location, 'blue')
        print colored("Location Longitude:%s" % location_longitude, 'blue')
        print colored("Location Latitude: %s" % location_latitude, 'blue')
        # Url to search for location
        url = (base_url + "locations/search/?lat=%s&lng=%s&access_token=%s") % \
              (location_latitude, location_longitude, access_token)
        # Display get request url
        print "Get request url for location id :%s" % url
        # Requesting get method to fetch location info and response is stored in a variable
        location_info = requests.get(url).json()
        # List of natural disasters
        disasters = ['Floods', 'Tsunami', 'Earthquakes', 'Volcanoes', 'Drought', 'Hail', 'Hurricanes', 'Thunderstorms',
                     'Landslides', 'Tornadoes', 'Wildfire', 'WinterStorm', 'Sinkholes']
        # Variable to check if there is natural calamity
        c = 0
        # If request has been accepted
        if location_info['meta']['code'] == 200:
            # If there is some location info
            if len(location_info['data']):
                # Store location id
                location_id = location_info['data'][0]['id']
                # url to get recent media at that location
                url2 = (base_url + "locations/%s/media/recent/?access_token=%s") % (location_id, access_token)
                # Display get request url
                print "Get request url for recent media :%s " % url2
                # Requesting get method to fetch recent  posts and response is stored in a variable
                location_recent_media = requests.get(url2).json()
                # If request has been accepted
                if location_recent_media['meta']['code'] == 200:
                    # If there are recent posts
                    if len(location_recent_media['data']):
                        # Traversing the json array
                        for i in range(len(location_recent_media['data'])):
                            # Checking if there is caption on post
                            if location_recent_media['data'][i]['caption'] is not None:
                                # Traversing the disaster list
                                for j in range(len(disasters)):
                                    # Checking if any word in list is there in caption
                                    if disasters[j] in location_recent_media['data'][i]['caption']['text']:
                                        if location_recent_media['data'][i]['type'] == 'image':
                                            # If yes than download that image
                                            print "This image is about %s in %s" % (colored(disasters[j], 'blue'),
                                                                                    colored(location, 'blue'))
                                            image_name = "%s in %s pic.jpeg" % (disasters[j], location)
                                            image_url = location_recent_media['data'][i]['images']['standard_resolution']['url']
                                            urllib.urlretrieve(image_url, image_name)
                                            print colored("Your image has been downloaded", 'blue')
                                            c += 1
                                        elif location_recent_media['data'][i]['type'] == 'carousel':
                                            print colored("Carousel Images", 'magenta')
                                            for k in range(len(location_recent_media['data'][i]['carousel_media'])):
                                                # If yes than download that image
                                                print "This image is about %s in %s" % (colored(disasters[j], 'blue'),
                                                                                        colored(location, 'blue'))
                                                image_name = "%s in %s pic.jpeg" % (disasters[j], location)
                                                image_url = location_recent_media['data'][i]['carousel_media'][k]['images']['standard_resolution']['url']
                                                urllib.urlretrieve(image_url, image_name)
                                                print colored("Your image has been downloaded", 'blue')
                                                c += 1
                                        else:
                                            print colored("This type of media in not supported", 'red')
                                # Checking if there is any natural calamity at that location
                                if c > 0:
                                    print colored("There is natural calamity in this place", 'blue')
                                # If no then display message
                                else:
                                    print colored("No natural calamity in this place", 'red')
                            # if no caption in post
                            else:
                                print colored("No caption on this post", 'red')
                    # if there are no recent post for location
                    else:
                        print colored("No posts for this location", 'red')
                # If request url is incorrect or there is some other problem
                else:
                    print colored("Status code other than 200", 'red')
            # If no info about location
            else:
                print colored("Location does not exist or some other problem", 'red')
        # If request url is incorrect or there is some other problem
        else:
            print colored("Status code other than 200", 'red')
    except:
        print colored("There must be some problem", 'red')

# Function to start the application
def start_bot():
    try:
        show_menu = True
        # Showing menu choices until user close the application
        while show_menu:
            print colored(" 1. Get your own details\n " 
                          "2. Get users details by username\n " 
                          "3. Get own recent posts\n " 
                          "4. Get recent posts of user by username\n" 
                          " 5. Like your own post\n" 
                          " 6. like other user post\n " 
                          "7. Get list of likes on our post\n" 
                          " 8. Get list of like on users post\n" 
                          " 9. Unlike our post\n" 
                          "10. Unlike other users post\n" 
                          "11. Get recent media liked by self\n" 
                          "12. Post a comment on self post\n" 
                          "13. Post a comment on user post\n" 
                          "14. Get list of comments on our post\n"
                          "15. Get list of comments on users post \n" 
                          "16. Delete negative comments on our post\n"
                          "17. Delete negative comments on other user post\n"
                          "18  Handle posts with special cases for self\n"
                          "19. Handle posts with special cases for other users\n"
                          "20. Get information about natural calamity for particular location\n"
                          "21. Compare Comments on self post\n"
                          "22. Compare comments on users post\n"
                          "23. Close Application", 'magenta')
            # Input the choice from user
            choice = int(raw_input(colored("Enter your choice", 'green')))
            if choice == 1:
                users_info("self")
            elif choice == 2:
                name = raw_input(colored("Enter the username of a user", 'blue'))
                user_id = get_user_id(name)
                users_info(user_id)
            elif choice == 3:
                get_recent_post("self")
            elif choice == 4:
                name = raw_input(colored("Enter the username of a user", 'blue'))
                user_id = get_user_id(name)
                get_recent_post(user_id)
            elif choice == 5:
                post_id = get_post_id("self")
                like_a_post(post_id)
            elif choice == 6:
                name = raw_input(colored("Enter the username of user you want to like a post", 'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                like_a_post(post_id)
            elif choice == 7:
                post_id = get_post_id("self")
                get_likes_list(post_id)
            elif choice == 8:
                name = raw_input(colored("Enter the username of user you want to get a list of likes", 'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                get_likes_list(post_id)
            elif choice == 9:
                post_id = get_post_id("self")
                unlike_a_post(post_id)
            elif choice == 10:
                name = raw_input(colored("Enter the username of user you want to unlike post", 'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                unlike_a_post(post_id)
            elif choice == 11:
                recent_media_liked()
            elif choice == 12:
                post_id = get_post_id("self")
                post_comment(post_id)
            elif choice == 13:
                name = raw_input(colored("Enter the username of user you want to  post a comment", 'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                post_comment(post_id)
            elif choice == 14:
                post_id = get_post_id("self")
                get_comment_list(post_id)
            elif choice == 15:
                name = raw_input(colored("Enter the username of user you want to get list of comments", 'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                get_comment_list(post_id)
            elif choice == 16:
                delete_negative_comments("self")
            elif choice == 17:
                name = raw_input(colored("Enter the username of user from whose post you want to delete comments",
                                         'blue'))
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                # get list of comments on post
                list5 = get_comment_list(post_id)
                # Checking if there are comments on post
                if list5 is not None:
                    # If Yes...checking user itself has commented on post or not
                    if username in list5:
                        # If yes...then delete negative comments
                        delete_negative_comments(user_id)
                    else:
                        # If not...no need to delete
                        print colored("You have not commented on this post", 'red')
            elif choice == 18:
                special_posts("self")
            elif choice == 19:
                name = raw_input(colored("Enter username for which you want to handle special cases", 'blue'))
                user_id = get_user_id(name)
                special_posts(user_id)
            elif choice == 20:
                natural_calamity_pics()
            elif choice == 21:
                post_id = get_post_id("self")
                list7 = get_comment_list(post_id)
                plot_pie_chart(list7)
            elif choice == 22:
                name = raw_input("Enter the username for whose post you want to compare comments")
                user_id = get_user_id(name)
                post_id = get_post_id(user_id)
                list7 = get_comment_list(post_id)
                plot_pie_chart(list7)
            elif choice == 23:
                print colored("Closing Application.....\nClosed", 'blue')
                show_menu = False
            else:
                print colored("You entered wrong choice!! Enter your choice from above list", 'red')
                start_bot()
    except:
        print colored("There must be some problem", 'red')

# Starting the application
print colored(" Welcome to insta_bot\n" 
              " Here are some menu choices", "blue")
# Calling the main function
start_bot()
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Storing access token in a variable
access_token = "1438763650.15994de.413f7ba570f34e6fa0f36fc4bdb6a021"
# Storing base url in a variable
base_url = "https://api.instagram.com/v1/"
# storing username
username = "kansal.isha"

# Function to retrieve  users id
def get_user_id(instagram_username):
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
        print "Status code is other than 200"

# Function to get post id
def get_post_id(instagram_user_id):
    # Checking if user exist or not...If not then exit
    if instagram_user_id is None:
        print "user does not exist"
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
                    print ("%s." + media['data'][i]['id']) % j
                    j += 1
                # Select the index of id to perform further operations
                choice = int(raw_input("Select the index of id"))
                # returning the id of the selected post
                return media['data'][choice-1]['id']
            else:
                # If there is no data
                print "There is no recent post "
                return None
        else:
            # If request url is incorrect or there is some other problem
            print "Status code other than 200"

# Function to retrieve self or other user's information
def users_info(instagram_username):
    # url to get information
    url = (base_url + "users/%s/?access_token=%s") % (instagram_username, access_token)
    # Display  Get url
    print "GET User_info Request Url: %s" % url
    # Fetching data using get method of request library....data is returned in json object form and storing in variable
    user_info = requests.get(url).json()
    # Checking if status code is 200 or not
    if user_info['meta']['code'] == 200:
        # If 200 Checking there is some info in json data array
        if len(user_info['data']):
            # If true printing info
            print "Username=%s" % user_info['data']['username']
            print "User Id=%s" % user_info['data']['id']
            print "Full name=%s" % user_info['data']['full_name']
            print "No. of people you are following=%s" % user_info['data']['counts']['follows']
            print "No. of people following you=%s" % user_info['data']['counts']['followed_by']
            print "No. of posts=%s" % user_info['data']['counts']['media']
            print "Website=%s" % user_info['data']['website']
            print "Bio=%s" % user_info['data']['bio']
        else:
            # If false then user does not exist
            print "User does not exist"
    else:
        # Is status code is not 200
        print"Status code other than 200"

# Function to get a list of likes
def get_likes_list(instagram_user_id):
    # Function call to get id of post and save it in a variable
    media_id = get_post_id(instagram_user_id)
    # list to store the name of users who like the post
    list1 = []
    # If there are no posts
    if media_id is None:
        print "There is no media"
    else:
        # Url to get list of likes
        url = (base_url + "media/%s/likes/?access_token=%s") % (media_id, access_token)
        # Display get url
        print "Get request Url:%s" % url
        # Response is stored in a variable
        like_list = requests.get(url).json()
        # variable for index
        j = 1
        # If request is accepted
        if like_list['meta']['code'] == 200:
            #  If there is some data
            if len(like_list['data']):
                # List of persons who liked this post
                print "The person who liked this post are:"
                for i in range(len(like_list['data'])):
                    print ("%s." + like_list['data'][i]['username']) % j
                    list1.append(like_list['data'][i]['username'])
                    j += 1
                # Returning list of person who liked this post
                return list1
            else:
                # If there is no data
                print "No likes on this post"
        else:
            # If request url is incorrect or there is some other problem
            print "Status code other than 200"

# Function to like a post
def post_is_liked(instagram_user_id):
    # Get id of post
    media_id = get_post_id(instagram_user_id)
    # If id is none then there is no post
    if media_id is None:
        print "There is no post"
    else:
        # url to like a post
        url = (base_url + 'media/%s/likes') % media_id
        # Extra information to be given in case of Post method
        payload = {"access_token": access_token}
        # Display Post url
        print "Post request url:%s " % url
        # Requesting post method to like a post and response is stored in a variable
        post_like = requests.post(url, payload).json()
        # If request has been accepted
        if post_like['meta']['code'] == 200:
            print "Post liked successfully"
        else:
            # If request url is incorrect or there is some other problem
            print "Status code other than 200"


# Function to check post will be liked or not
def like_a_post(instagram_user_id):
    # Get list of users who liked the post
    list2 = get_likes_list(instagram_user_id)
    if list2 is not None:
        # Check if it is liked by self or not...if yes display message
        if username in list2:
            print "You have already liked this post"
        else:
            # call a function to like a post
            post_is_liked(instagram_user_id)
    # If post is not liked by anyone then call a function to like post
    else:
        post_is_liked(instagram_user_id)

# Function to delete like from post
def unlike_a_post(instagram_user_id):
    # Get list of users who liked the post
    list3 = get_likes_list(instagram_user_id)
    # Check if list of likes is empty or user itself has not liked the post....then there is nothing to unlike
    if list3 is None or username not in list3:
        print "Nothing to unlike...or you have not liked this post"
    # If above conditions are not satisfied thn proceed
    else:
        # get id of post to unlike
        media_id = get_post_id(instagram_user_id)
        # If no media id
        if media_id is None:
            print "There is no media in this account"
        # Otherwise the post will be unlike
        else:
            # Url to unlike a post
            url = base_url + 'media/%s/likes/?access_token=%s' % (media_id, access_token)
            # Display delete like url
            print "Delete request url: %s" % url
            # Requesting delete method to like a post and response is stored in a variable
            del_like = requests.delete(url).json()
            # If request is accepted
            if del_like['meta']['code'] == 200:
                print " Successfully unlike the post"
            # If request url is incorrect or there is some other problem
            else:
                print "Status code other than 200"

# Get recent media liked by user
def recent_media_liked():
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
                      % (recent_media['data'][i]['user']['username'],  recent_media['data'][i]['id'])
        else:
            # If no post is liked recently
            print "There is no media you have recently liked"
    # If request url is incorrect or there is some other problem
    else:
        print "Status code other than 200"


# Function to get list of comments
def get_comment_list(instagram_user_id):
    list4 = []
    # Get id of post
    media_id = get_post_id(instagram_user_id)
    # If there are no posts
    if media_id is None:
        print "There is no media"
    # proceed if media-id is returned
    else:
        # Url to get list of comments on a post
        url = base_url + "media/%s/comments/?access_token=%s" % (media_id, access_token)
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
                print "The person who commented on this post are:"
                for i in range(len(comment_list['data'])):
                    print "%s. Comment: %s Posted by: %s" \
                          % (j, comment_list['data'][i]['text'], comment_list['data'][i]['from']['username'])
                    j += 1
                    list4.append(comment_list['data'][i]['from']['username'])
                return list4
            else:
                # If there are no comments
                print "No comments on this post"
        # If request url is incorrect or there is some other problem
        else:
            print "Status code other than 200"

# Function to comment on a post
def post_comment(instagram_user_id):
    media_id = get_post_id(instagram_user_id)
    # If there are no posts
    if media_id is None:
        print "There is no media"
    # proceed if media-id is returned
    else:
        # url to like a post
        url = (base_url + 'media/%s/comments') % media_id
        # what user wants to comment..
        comment_text = raw_input("Enter your comment")
        # Extra information to be given in case of Post method
        payload = {"access_token": access_token, "text": comment_text}
        # Display Post url
        print "Post request url:%s " % url
        # Requesting post method to like a post and response is stored in a variable
        comment_post = requests.post(url, payload).json()
        # If request has been accepted
        if comment_post['meta']['code'] == 200:
            print "Comment posted successfully"
        else:
            # If request url is incorrect or there is some other problem
            print "Status code other than 200"

# Function to delete negative comments
def delete_negative_comments(instagram_user_id):
    # Get id of post
    media_id = get_post_id(instagram_user_id)
    # If there are no posts
    if media_id is None:
        print "There is no media"
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
                # If there are more than one comment
                for i in range(len(comment_list['data'])):
                    # Storing the comment
                    comment_text = comment_list['data'][i]['text']
                    # Storing comment id
                    comment_id = comment_list['data'][i]['id']
                    # Analysing the positivity and negativity of comment
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                    # If negative....delete the comment
                    if blob.sentiment.p_neg > blob.sentiment.p_pos:
                        print "Comment %s is negative" % comment_text
                        url = (base_url + "media/%s/comments/%s") % (media_id, comment_id)
                        print "Delete request url :%s" % url
                        del_comment = requests.delete(url).json()
                        if del_comment['meta']['code'] == 200:
                            print "Negative comment deleted"
                        else:
                            print "Request is not processed"
                    # If average ask the user what to do
                    elif blob.sentiment.p_neg == blob.sentiment.p_pos:
                        print "Comment is average"
                        choice = raw_input("Do you want to delete comment(Y/N)??")
                        # If user says yes delete the comment
                        if choice.capitalize() == "Y":
                            url = (base_url + "media/%s/comments/%s") % (media_id, comment_id)
                            print "Delete request url :%s" % url
                            del_comment = requests.delete(url).json()
                            if del_comment['meta']['code'] == 200:
                                print "Negative comment deleted"
                            else:
                                print "Request is not processed"
                        # otherwise not
                        else:
                            print "Comment is not deleted"
                    # If comment is positive
                    else:
                        print "Your comment is positive"

# Function to get most recent post
def get_recent_post(instagram_user_id):
    # If id is there or not
    if instagram_user_id is None:
        print "User does not exist"
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
                        print "%s. %s" % (k, media['data'][i]['id'])
                        k += 1
                    elif media['data'][i]['type'] == "carousel":
                        for j in range(len(media['data'][i]['carousel_media'])):
                            print "%s. %s" % (k, media['data'][j]['id'])
                            k += 1
                    else:
                        print "This type of media is not supported"
                # Taking  index as  input from user
                choice = int(raw_input("Enter the index of post id"))
                # asking what user want to do with the selected post
                choice2 = int(raw_input("What u want to do??\n 1.Download post\n 2.Like post\n 3.Comment on post"))
                # Download post
                if choice2 == 1:
                    image_name = media['data'][choice-1]['id'] + ".jpeg"
                    image_url = media['data'][choice-1]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print "Your image has been downloaded!!!"
                # like post
                elif choice2 == 2:
                    like_a_post(instagram_user_id)
                # Comment on post
                elif choice2 == 3:
                    post_comment(instagram_user_id)
            else:
                # If no posts by user
                print "No Post is there"
        # If request url is incorrect or there is some other problem
        else:
                print "Status code other than 200"

# Function for some special cases for posts
def special_posts(instagram_user_id):
    # If user-id is not returned
    if instagram_user_id is None:
        print "User does not exist"
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
                print " Choose one option from the following\n" \
                      " 1.Choose post with minimum no. of likes\n " \
                      "2.Choose post with a particular text in caption"
                # Taking input from user
                choice = int(raw_input("Enter your choice"))
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
                    min_like_count_url = url_list[0]
                    for j in range(len(like_list)):
                        # checking if there is other likes count less than min_count_variable
                        if min_like_count > like_list[j]:
                            # if yes update the variables
                            min_like_count = like_list[j]
                            min_like_count_url = url_list[j]
                    # Display the post with least likes
                    print "Post with least count likes %s is %s" % (min_like_count, min_like_count_url)
                    # Asking the user what you want to do with the post
                    choice = int(raw_input("What do you want to do with the post with minimum likes??\n "
                                           "1.Like post\n "
                                           "2. Download post"))
                    # If 1 like post
                    if choice == 1:
                        like_a_post(instagram_user_id)
                    # If 2 download post
                    elif choice == 2:
                        image_name = "Minimum_like_post.jpeg"
                        image_url = min_like_count_url
                        urllib.urlretrieve(image_url, image_name)
                        print "Your image has been downloaded"
                    # wrong choice entered by user
                    else:
                        print "You entered wrong choice"
                        return
                # If 2 user wants to fetch posts with particular words in caption
                elif choice == 2:
                    # List to store image name
                    image_name_list = []
                    # List to store urls
                    image_url_list = []
                    # Asking the user which word want to search
                    word = raw_input("Enter the particular word you want to search in caption??")
                    # variable for index like 1,2,3..
                    c = 1
                    # Traversing the json array
                    for i in range(len(recent_media['data'])):
                        # If there is caption in post
                        if recent_media['data'][i]['caption']['text'] is not None:
                            # If the word is in caption
                            if word in recent_media['data'][i]['caption']['text']:
                                # name the image
                                name_image = "%s.Post with particular word in caption.jpeg" % c
                                c += 1
                                # append the name to image name list
                                image_name_list.append(name_image)
                                # append the url to url list
                                image_url_list.append(recent_media['data'][i]['images']['standard_resolution']['url'])
                    # Checking if there is any post with particular word
                    if len(image_name_list) > 0:
                        # If yes asking the user what to do with the posts
                        choice = int(raw_input("What you want to do with the posts with particular word in caption??\n"
                                               "1. Like posts\n"
                                               "2. Download posts"))
                        # If 1 like post
                        if choice == 1:
                            like_a_post(instagram_user_id)
                        # if 2 download images
                        elif choice == 2:
                            for k in range(len(image_name_list)):
                                urllib.urlretrieve(image_url_list[k], image_name_list[k])
                            print "Your images has been downloaded"
                    # If no post with particular word display message
                    else:
                        print "No post with this particular word"
                # User entered wrong choice
                else:
                    print "You entered wrong choice"
                    return
            # If there are no posts
            else:
                print " No recent posts"
        # If request url is incorrect or there is some other problem
        else:
            print "Status code other than 200"

# Function to start the application
def start_bot():
    show_menu = True
    # Showing menu choices until user cloase the application
    while show_menu:
        print " 1. Get your own details\n " \
              "2. Get users details by username\n " \
              "3. Get own recent posts\n " \
              "4. Get recent posts of user by username\n" \
              " 5. Like your own post\n" \
              " 6. like other user post\n " \
              "7. Get list of likes on our post\n" \
              " 8. Get list of like on users post\n" \
              " 9. Unlike our post\n" \
              "10. Unlike other users post\n" \
              "11. Get recent media liked by self\n" \
              "12. Post a comment on self post\n" \
              "13. Post a comment on user post\n" \
              "14. Get list of comments on our post\n" \
              "15. Get list of comments on users post \n" \
              "16. Delete negative comments on our post\n" \
              "17. Delete negative comments on other user post\n" \
              "18  Handle posts with special cases for self\n" \
              "19. Handle posts with special cases for other users\n" \
              "20. Close Application"
        # Input the choice from user
        choice = int(raw_input("Enter your choice"))
        if choice == 1:
            users_info("self")
        elif choice == 2:
            name = raw_input("Enter the username of a user")
            user_id = get_user_id(name)
            users_info(user_id)
        elif choice == 3:
            get_recent_post("self")
        elif choice == 4:
            name = raw_input("Enter the username of a user")
            user_id = get_user_id(name)
            get_recent_post(user_id)
        elif choice == 5:
            like_a_post("self")
        elif choice == 6:
            name = raw_input("Enter the username of user you want to like a post")
            user_id = get_user_id(name)
            like_a_post(user_id)
        elif choice == 7:
            get_likes_list("self")
        elif choice == 8:
            name = raw_input("Enter the username of user you want to get a list of likes")
            user_id = get_user_id(name)
            get_likes_list(user_id)
        elif choice == 9:
            unlike_a_post("self")
        elif choice == 10:
            name = raw_input("Enter the username of user you want to unlike post")
            user_id = get_user_id(name)
            unlike_a_post(user_id)
        elif choice == 11:
            recent_media_liked()
        elif choice == 12:
            post_comment("self")
        elif choice == 13:
            name = raw_input("Enter the username of user you want to  post a comment")
            user_id = get_user_id(name)
            post_comment(user_id)
        elif choice == 14:
            get_comment_list("self")
        elif choice == 15:
            name = raw_input("Enter the username of user you want to get list of comments")
            user_id = get_user_id(name)
            get_comment_list(user_id)
        elif choice == 16:
            delete_negative_comments("self")
        elif choice == 17:
            name = raw_input("Enter the username of user from whose post you want to delete comments")
            user_id = get_user_id(name)
            # get list of comments on post
            list5 = get_comment_list(user_id)
            # Checking if there are comments on post
            if list5 is not None:
                # If Yes...checking user itself has commented on post or not
                if username in list5:
                    # If yes...then delete negative comments
                    delete_negative_comments(user_id)
                else:
                    # If not...no need to delete
                    print "You have not commented on this post"
        elif choice == 18:
            special_posts("self")
        elif choice == 19:
            name = raw_input("Enter username for which you want to handle special cases")
            user_id = get_user_id(name)
            special_posts(user_id)
        elif choice == 20:
            print "Closing Application.....\nClosed"
            show_menu = False
        else:
            print "You entered wrong choice!! Enter your choice from above list"
            start_bot()

# Starting the application
print " Welcome to insta_bot"
print " Here are some menu choices"
# Calling the main function
start_bot()
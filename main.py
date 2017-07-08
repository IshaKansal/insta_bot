import requests
import urllib

# Storing access token in a variable
access_token = "1438763650.15994de.413f7ba570f34e6fa0f36fc4bdb6a021"
# Storing base url in a variable
base_url = "https://api.instagram.com/v1/"

# Function to retrieve  users id
def get_user_id(instagram_username):
    # URL with endpoint to search user id
    url = base_url + "users/search/?q=%s&access_token=%s" % (instagram_username, access_token)
    print "Get Search Request Url: %s" % url
    user_info = requests.get(url).json()
    # If status code is 200...proceed
    if user_info['meta']['code'] == 200:
        # If there is info in json data array
        if len(user_info['data']):
            # Returning users id
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print "Status code is other than 200"

# Function to get post id
def get_post_id(instagram_username):
    if instagram_username is "Self":
        name = raw_input("Enter your own username")
        user_id = get_user_id(name)
    else:
        user_id = get_user_id(instagram_username)
    if user_id is None:
        print "user does not exist"
        exit()
    url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print "Get post id url: %s" % url
    media = requests.get(url).json()
    j = 1
    if media['meta']['code'] == 200:
        if len(media['data']):
            for i in range(len(media['data'])):
                print ("%s." + media['data'][i]['id']) % j
                j += 1
            choice = int(raw_input("Select the index of id"))
            return media['data'][choice-1]['id']
        else:
            print "There is no recent post "
            return None
    else:
        print "Status code other than 200"

# Function to retrieve self information
def users_info(instagram_username):
    url = (base_url + "users/%s/?access_token=%s") % (instagram_username, access_token)
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

# Function to get most recent post
def get_recent_post(insta_username):
    if insta_username is "Self":
        url = (base_url + "users/self/media/recent/?access_token=%s") % access_token
    else:
        user_id = get_user_id(insta_username)
        if user_id is None:
            print "User does not exist"
            exit()
        url = (base_url + "users/%s/media/recent/?access_token=%s") % (user_id, access_token)
    print "Get recent post request url:%s" % url
    media = requests.get(url).json()
    if media['meta']['code'] == 200:
        if len(media['data']):
            for i in range(len(media['data'])):
                image_name = media['data'][i]['id'] + ".jpeg"
                image_url = media['data'][i]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print "Your image has been downloaded!!!"
        else:
            print "No Post is there"
    else:
        print "Status code other than 200"

def name():
    url = (base_url + "users/self/?access_token=%s") % access_token
    print "GET User_info Request Url: %s" % url
    # Fetching data using get method of request library....data is returned in json object form and storing in variable
    user_info = requests.get(url).json()
    # Checking if status code is 200 or not
    if user_info['meta']['code'] == 200:
        # If 200 Checking there is some info in json data array
        if len(user_info['data']):
            # If true printing info
            return user_info['data']['username']
        else:
            print "User does not exist"
    else:
        print "Status code other than 200"

# Function to get a list of likes
def get_likes_list(instagram_username):
    media_id = get_post_id(instagram_username)
    list1 = []
    if media_id is None:
        print "There is no media"
    else:
        url = (base_url + "media/%s/likes/?access_token=%s") % (media_id, access_token)
        print "Get request Url:%s" % url
        like_list = requests.get(url).json()
        j = 1
        if like_list['meta']['code'] == 200:
            if len(like_list['data']):
                print "The person who liked this post are:"
                for i in range(len(like_list['data'])):
                    print ("%s." + like_list['data'][i]['username']) % j
                    list1.append(like_list['data'][i]['username'])
                    j += 1
                return list1
            else:
                print "No likes on this post"
        else:
            print "Status code other than 200"

def like_post(instagram_username):
    media_id = get_post_id(instagram_username)
    if media_id is None:
        print "There is no post"
    else:
        url = (base_url + 'media/%s/likes') % media_id
        payload = {"access_token": access_token}
        print "Post request url:%s " % url
        post_like = requests.post(url, payload).json()
        if post_like['meta']['code'] == 200:
            print "Post liked successfully"
        else:
            print "Unsuccessful"


# Function to like post
def like_a_post(instagram_username):
    list2 = get_likes_list(instagram_username)
    self_name = name()
    if list2 is not None:
        if self_name in list2:
            print "You have already liked this post"
        else:
            like_post(instagram_username)
    else:
        like_post(instagram_username)

# Function to delete like from post
def unlike_a_post(instagram_username):
    list3 = get_likes_list(instagram_username)
    self_name = name()
    if list3 is None or self_name not in list3:
        print "Nothing to unlike...or you have not liked this post"
    else:
        media_id = get_post_id(instagram_username)
        if media_id is None:
            print "There is no media in this account"
        else:
            url = base_url + 'media/%s/likes/?access_token=%s' % (media_id, access_token)
            print "Delete request url: %s" % url
            del_post = requests.delete(url).json()
            if del_post['meta']['code'] == 200:
                print " Successfully unlike the post"
            else:
                print "Request is not fulfilled"

# Function to start the application
def start_bot():
    show_menu = True
    while show_menu:
        print " 1. Get your own details\n " \
              "2. Get users details by username\n " \
              "3.Get own recent posts\n " \
              "4. Get recent posts of user by username\n" \
              " 5. Like your own post\n" \
              " 6. like other user post\n " \
              "7. get list of likes on our post\n" \
              " 8. Get list of like on users post\n" \
              " 9. Unlike our post\n" \
              " 10. Unlike other users post\n" \
              " 11. Close Application"
        choice = int(raw_input(" Enter your choice"))
        if choice == 1:
            users_info("self")
        elif choice == 2:
            name = raw_input("Enter the username of a user")
            user_id = get_user_id(name)
            users_info(user_id)
        elif choice == 3:
            get_recent_post("Self")
        elif choice == 4:
            name = raw_input("Enter the username of a user")
            get_recent_post(name)
        elif choice == 5:
            like_a_post("Self")
        elif choice == 6:
            name = raw_input("Enter the username of user you want to like a post")
            like_a_post(name)
        elif choice == 7:
            get_likes_list("Self")
        elif choice == 8:
            name = raw_input("Enter the username of user you want to get a list of likes")
            get_likes_list(name)
        elif choice == 9:
            unlike_a_post("Self")
        elif choice == 10:
            name = raw_input("Enter the username of user you want to unlike post")
            unlike_a_post(name)
        elif choice == 11:
            print " Closing Application.....\n Closed"
            show_menu = False
        else:
            print "You entered wrong choice!! Enter your choice from above list"
            start_bot()

print " Welcome to insta_bot"
print " Here are some menu choices"
start_bot()
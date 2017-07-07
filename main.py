import urllib
import requests

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

# Function to retrieve self information
def users_info(instagram_username):
    # Checking if user wants to retrieve own info..If yes endpoint for self is used
    if instagram_username is "Self":
        # adding endpoints and access token in  base url
        url = (base_url + "users/self/?access_token=%s") % access_token
    # If user wants to access other user's info
    else:
        # Calling get_user_id(name) function to get  id of user and storing that id
        user_id = get_user_id(instagram_username)
        if user_id is None:
            print "User does not exist"
            exit()
        # Endpoint for accessing other user'info will be used
        url = (base_url + "users/%s/?access_token=%s") % (user_id, access_token)
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

def start_bot():
    show_menu = True
    while show_menu:
        print " 1. Get your own details\n " \
              "2. Get users details by username\n " \
              "3.Get own recent posts\n " \
              "4. Get recent posts of user by username\n" \
              " 5. Close Application"
        choice = int(raw_input(" Enter your choice"))
        if choice == 1:
            users_info("Self")
        elif choice == 2:
            name = raw_input("Enter the username of a user")
            users_info(name)
        elif choice == 3:
            get_recent_post("Self")
        elif choice == 4:
            name = raw_input("Enter the username of a user")
            get_recent_post(name)
        elif choice == 5:
            print " Closing Application.....\n Closed"
            show_menu = False
        else:
            print "You entered wrong choice!! Enter your choice from above list"
            start_bot()

print " Welcome to insta_bot"
print " Here are some menu choices"
start_bot()
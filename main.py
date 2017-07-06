import requests

# Storing access token in a variable
access_token = "1438763650.15994de.413f7ba570f34e6fa0f36fc4bdb6a021"
# Storing base url in a variable
base_url = "https://api.instagram.com/v1/"

def get_user_id(instagram_username):
    # URL with endpoint to search user id
    url = base_url + "users/search/?q=%s&access_token=%s" % (instagram_username, access_token)
    print "Get Search Request Url: %s" % url
    user_info = requests.get(url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print "Status code is other than 200"

# Function to retrieve self information
def users_info(instagram_username):
    # Checking if user wants to retrieve own info..If yes endpoint for self is used
    if instagram_username.capitalize() == "Self":
        # adding endpoints and access token in  base url
        url = (base_url + "users/self/?access_token=%s") % access_token
    # If user wants to access other user's info
    else:
        # Calling get_user_id(name) function to get  id of user and storing that id
        user_id = get_user_id(instagram_username)
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



# calling self_info() function
users_info("Self")
users_info("priyanka_verma96")
users_info("iamhssingh")



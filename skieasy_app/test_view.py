from bs4 import BeautifulSoup
from selenium import webdriver

def initiate_web_driver(link):
    '''Start the Chrome web driver and return the driver'''

    driver = webdriver.Chrome()
    driver.get(link)

    return driver

def test_welcome_page():
    '''Test the view of the welcome page'''

    driver = initiate_web_driver("https://skieasy.fly.dev/")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    h1_tags = soup.find_all("h1")
    found_welcome_message = False

    for heading_tag in h1_tags:
        if "Welcome to SkiEasy" in heading_tag.text:
            found_welcome_message = True

    if found_welcome_message:
        assert(True)
    else:
        assert(False)

    found_register_message = False
    found_login_message = False

    h3_tags = soup.find_all("h3")
    for heading_tag in h3_tags:
        if "Register" in heading_tag.text:
            found_register_message = True
        if "Login" in heading_tag.text:
            found_login_message = True
    
    if found_register_message and found_login_message:
        assert(True)
    else:
        assert(False)

def main():
    '''Main function to run all tests'''
    test_welcome_page()

if __name__ == "__main__":
    main()

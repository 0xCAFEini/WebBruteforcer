# WebBruteforcer

WebBruteforcer uses Selenium to perform password brute-forcing on any website where the username and password fields are located on the same page.

## Requirements

* Python 3.10 or later
* Chrome, Firefox, or Edge browsers
* Selenium and Colorama Python modules

## Usage

Git clone this repository

```
git clone https://github.com/yannawr/WebBruteforcer && cd WebBruteforcer
```

Install Python modules

```
pip install -r requirements.txt
```
Usage (--help or -h):

```
python web_bruteforcer.py <login_url> <username_name> <password_name> <username> <message> <browser> <wordlist>

    <login_url>           - URL of the login page
    <username_name>       - value of the "name" attribute for the username field in the form
    <password_name>       - value of the "name" attribute for the password field in the form
    <username>            - username to be tested
    <message>             - message expected to appear on the next page after a successful login, provided to confirm successful login
    <browser>             - browser to be used (Chrome, Firefox, or Edge)
    <wordlist>            - wordlist to be used

WebBruteforcer can attempt to automatically discover the form's name attributes using the --auto command:

python web_bruteforcer.py <login_url> --auto <username> <message> <browser> <wordlist>
```

## Example

```
▶ python web_bruteforcer.py https://google-gruyere.appspot.com/657831885437972335537186182995004819742/login --auto generic_user "Gruyere: Home" chrome wordlist.txt

[+] Login successful!
[+] Password: test1234
```
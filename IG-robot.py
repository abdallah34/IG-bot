from time import sleep
import requests
import json

class AbdullahCoder():
    def __init__(self):
        self.hosturl = "https://www.instagram.com/"
        self.loginurl = "https://www.instagram.com/accounts/login/ajax/"
        self.editurl = "https://www.instagram.com/accounts/web_change_profile_picture/"
        self.editdata = {"Content-Disposition": "form-data", "name": "profile_pic","filename": "profilepic.jpg", "Content-Type": "image/jpeg"}
        self.session = requests.Session()
        self.session.headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36', 'Referer': self.hosturl}
        self.headers = {"Host": "www.instagram.com","Accept": "*/*","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br","Referer": "https://www.instagram.com/accounts/edit/","X-IG-App-ID": "936619743392459","X-Requested-With": "XMLHttpRequest","DNT": "1","Connection": "keep-alive",}
        self.pcnm = int(input('Number of photos: '))
        self.X = int(input('Sleep : '))
      
        if self.AddCH() == False:
            self.login()
            self.Save_login()
        
        while True:
            n = 0
            while n < self.pcnm:
                self.change(n)
                n+=1

     
    def login(self):
            username = str(input('Username : '))
            password = input('Password : ')
            resp = self.session.get(self.hosturl)
            self.session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
            login_data = {'username': username, 'enc_password': '#PWD_INSTAGRAM_BROWSER:0:&:'+password}
            login_resp = self.session.post(self.loginurl, data=login_data, allow_redirects=True)
            if login_resp.json()['authenticated']:
                print("Login successful")
                self.session.headers.update({'X-CSRFToken': login_resp.cookies['csrftoken']})
            else:
                print("Login failed!")
                self.login()

    def Save_login(self):
        with open('cookies.txt', 'w+') as f:
            json.dump(self.session.cookies.get_dict(), f)
        with open('headers.txt', 'w+') as f:
            json.dump(self.session.headers, f)

    def AddCH(self):
        try:
            with open('cookies.txt', 'r') as f:
                self.session.cookies.update(json.load(f))
            with open('headers.txt', 'r') as f:
                self.session.headers = json.load(f)
        except:
            return False

    def change(self,n):
        try:
            with open("imgs/photo"+str(n)+".jpg", "rb") as resp:
                f = resp.read()
            p_pic = bytes(f)
            p_pic_s = len(f)
            self.session.headers.update({'Content-Length': str(p_pic_s)})
            files = {'profile_pic': p_pic}
            r = self.session.post(self.editurl, files=files, data=self.editdata)
            if r.json()['changed_profile']:
                print(f"Profile picture changed | photo{str(n)}")
            else:
                print(f"Something went wrong | photo{str(n)}")
            sleep(self.X)
        except Exception as e:
            print(e)
            sleep(10)

AbdullahCoder()

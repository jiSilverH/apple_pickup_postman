import requests
from email.message import EmailMessage
import smtplib
import time
import pandas as pd

# Before run this code, you've to make authentification of less secure apps available.
# Link : https://myaccount.google.com/u/1/lesssecureapps?pli=1

# Global variables
# Check a pickup-availability every INTERVAL seconds.
INTERVAL = 10

# Model name to consider.
MODEL = 'MK183KH/A' #MacBook Pro 16' space grey 10core, 16gpu, 512GB
# MODEL = 'MU102KH_A' # ipad pro 3rd generation, 11-inch 256gb wifi + cellular model

# Request url
# Reference : https://nuridol.net/stock_pad_kr.html
# URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20json%20where%20url%3D%22https%3A%2F%2Fwww.apple.com%2Fkr%2Fshop%2Fretail%2Fpickup-message%3Fpl%3Dtrue%26searchNearby%3Dtrue%26store%3DR692%26parts.0%3DMTXP2KH%2FA%26parts.1%3DMTXR2KH%2FA%26parts.2%3DMTXU2KH%2FA%26parts.3%3DMTXW2KH%2FA%26parts.4%3DMTXN2KH%2FA%26parts.5%3DMTXQ2KH%2FA%26parts.6%3DMTXT2KH%2FA%26parts.7%3DMTXV2KH%2FA%26parts.8%3DMU0U2KH%2FA%26parts.9%3DMU172KH%2FA%26parts.10%3DMU1M2KH%2FA%26parts.11%3DMU222KH%2FA%26parts.12%3DMU0M2KH%2FA%26parts.13%3DMU102KH%2FA%26parts.14%3DMU1F2KH%2FA%26parts.15%3DMU1V2KH%2FA%26parts.16%3DMTEM2KH%2FA%26parts.17%3DMTFN2KH%2FA%26parts.18%3DMTFQ2KH%2FA%26parts.19%3DMTFT2KH%2FA%26parts.20%3DMTEL2KH%2FA%26parts.21%3DMTFL2KH%2FA%26parts.22%3DMTFP2KH%2FA%26parts.23%3DMTFR2KH%2FA%26parts.24%3DMTHP2KH%2FA%26parts.25%3DMTJ62KH%2FA%26parts.26%3DMTJJ2KH%2FA%26parts.27%3DMTJV2KH%2FA%26parts.28%3DMTHJ2KH%2FA%26parts.29%3DMTHV2KH%2FA%26parts.30%3DMTJD2KH%2FA%26parts.31%3DMTJP2KH%2FA%22&format=json'
# URL = 'https://www.apple.com/kr/shop/retail/pickup-message?pl=true&searchNearby=true&store=R692&parts.0=MGN63KH/A&parts.1=MGND3KH/A&parts.2=MGN93KH/A&parts.3=MGN73KH/A&parts.4=MGNE3KH/A&parts.5=MGNA3KH/A&parts.6=MYD82KH/A&parts.7=MYDA2KH/A&parts.8=MYD92KH/A&parts.9=MYDC2KH/A&parts.10=MGNR3KH/A&parts.11=MGNT3KH/A&_=1641626450497'
# URL = 'https://www.apple.com/kr/shop/retail/pickup-message?pl=true&searchNearby=true&store=R692&parts.0=MK183KH/A'
URL = 'https://www.apple.com/kr/shop/retail/pickup-message?pl=true&searchNearby=true&store=R692&parts.0='+ MODEL # 스그, 내가 사려는 것

def is_pickup_possible(model):
  r = requests.get(URL)
  print('status:', r.status_code)

  # print(r.json())

  d = r.json()

  product_info_garo = d['body']['stores'][0]['partsAvailability'] #[0]: 가로수길, [1]: 여의도


  # print(product_info_garo)

  # df = pd.DataFrame.from_dict(d)
  # print(df['pickupDisplay'])

  # print(df.info)
  print('----------------')
  if r.status_code == 200 and d is not None:
    try:
      product_info_garo = d['body']['stores'][0]['partsAvailability'][model] #[0]: 가로수길, [1]: 여의도
      product_selection_enabled_garo = product_info_garo['storeSelectionEnabled']
      print(product_selection_enabled_garo)
      print(type(product_selection_enabled_garo))

      product_info_yeo = d['body']['stores'][1]['partsAvailability'][model]
      product_selection_enabled_yeo = product_info_garo['storeSelectionEnabled']
      print(product_selection_enabled_yeo)

      if product_selection_enabled_garo == 1:
        return True
      else:
        print('in else')
        return False
    except Exception as e:
      print(e)
      return False
  else:
    return False
  
  
def mail_me(model):
  msg = EmailMessage()
  msg.set_content('Order %s right now.'% model)
  msg['Subject'] = 'Wake up! pickup %s ordering is possible now.' % model
  msg['From'] = 'your_gmail_address'
  msg['To'] = 'your_gmail_address'

  # connect to SMTP server
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login('your_gmail_address', 'your_gmail_password')

  # Send the message via our own SMTP server.
  # server.send_message(msg)
  server.sendmail('your_gmail_address', 'your_gmail_address', msg.as_string())
  server.quit()
  

def main():
  while(1):
    possibility = is_pickup_possible(MODEL)
    print(possibility)
    if possibility == False:
      time.sleep(INTERVAL)
    else:
      break
    
  mail_me(MODEL)
  print('sending mail is complete.')
  
  
if __name__ == '__main__':
  main()

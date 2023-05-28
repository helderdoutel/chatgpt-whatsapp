from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import hashlib
import openai
from decouple import config
from time import sleep
from selenium.webdriver.common.keys import Keys

openai.api_key = config('OPENAI_KEY') 

profile = webdriver.FirefoxProfile(r"C:\Users\helde\AppData\Roaming\Mozilla\Firefox\Profiles\70rtx7gn.default-release")
driver = webdriver.Firefox(firefox_profile=profile)
driver.get('https://web.whatsapp.com/')
if input('Continuar? [y/n]\n') != 'y':
    raise Exception('Break')

def make_message_index(message_panel):
    message_index = {}
    for message in message_panel:
        temp_message = message.text.split('\n')
        message_index[temp_message[0]] = {
            'message': temp_message[-1],
            'hash': hashlib.md5(temp_message[-1].encode('utf-8')).hexdigest(),
            'object': message
        }
    return message_index

message_panel = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div')
message_panel = make_message_index(message_panel)
# import ipdb;ipdb.set_trace()
while True:
    message_panel_reload = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div')
    message_panel_reload = make_message_index(message_panel_reload)
    for user_name in message_panel.keys():
        if not message_panel_reload.get(user_name, None):
            continue
        if message_panel[user_name]['hash'] != message_panel_reload[user_name]['hash']:
            message_panel[user_name]['object'].click()
            messages = []
            for mess in driver.find_elements(By.CLASS_NAME, 'focusable-list-item'):
                try:
                    this_message = mess.find_element(By.CLASS_NAME, 'copyable-text').text
                except:
                    continue
                if 'message-in' in mess.get_attribute('class'):
                    messages.append(f'Outra pessoa: {this_message}')
                elif 'message-out' in mess.get_attribute('class'):
                    messages.append(f'Eu: {this_message}')
                else:
                    pass
                print(messages)
            if len(messages) > 0:
                if 'Eu: ' in messages[-1]:
                    continue
                prompt_inicial = 'Imagine que você é eu e está participando de uma conversa via whastapp. Responsa a seguinte conversa\n'
                for m in messages:
                    prompt_inicial += (m + '\n')
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt_inicial}
                    ]
                )
                message_box = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')[0]
                chatgpt_message = completion.choices[0].message.content
                chatgpt_message = chatgpt_message.replace('Eu:', '')
                for key in chatgpt_message:
                    message_box.send_keys(key)
                message_box.send_keys(Keys.ENTER)
                message_panel_reload = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div')
                message_panel_reload = make_message_index(message_panel_reload)
    message_panel = message_panel_reload
    sleep(1)
print(last_message)



# import ipdb; ipdb.set_trace()
#     if message_loaded_message != last_message:
#         print(last_message)
#         message_element = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/span')
#         message_element[0].click()
#         message_loaded_message = message_element[0].text
#         messages = []
#         for mess in driver.find_elements(By.CLASS_NAME, 'focusable-list-item'):
#             try:
#                 this_message = mess.find_element(By.CLASS_NAME, 'copyable-text').text
#             except:
#                 continue
#             if 'message-in' in mess.get_attribute('class'):
#                 messages.append(f'Outra pessoa: {this_message}')
#             elif 'message-out' in mess.get_attribute('class'):
#                 messages.append(f'Eu: {this_message}')
#             else:
#                 import ipdb; ipdb.set_trace()
#             print(messages)
#     last_message = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/span')[0].text
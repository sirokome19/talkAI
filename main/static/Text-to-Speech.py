import json
import os
import requests
import time
from xml.etree import ElementTree

try:
    input = raw_input
except NameError:
    pass
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class TextToSpeech(object):
    def __init__(self, subscription_key, resource_name):
        self.subscription_key = subscription_key
        self.tts = input("音声に変換するテキストを入力：")
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.resource_name = resource_name

    def get_token(self):
        '''
        subscription_keyからaccess_tokenを取得
        '''
        fetch_token_url = "https://japaneast.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://japaneast.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': self.resource_name
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24kRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample-answer.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")


if __name__ == "__main__":
    with open("./subscription_key.json", "r") as f:
        json_load = json.load(f)
    subscription_key = json_load["key"]
    resource = json_load["resource"]
    app = TextToSpeech(subscription_key, resource)
    app.get_token()
    app.save_audio()

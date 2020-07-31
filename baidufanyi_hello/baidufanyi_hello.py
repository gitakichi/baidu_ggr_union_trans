import PySimpleGUI as sg
import json
import random
import hashlib
from urllib import parse
import http.client
from api_secret import *
import time
from googletrans import Translator
import sys
from pypinyin import pinyin, lazy_pinyin


class BaiduTranslate:
    def __init__(self,fromLang,toLang):
        self.url = "/api/trans/vip/translate"
        self.appid = API_ID
        self.secretKey = API_PASS
        self.fromLang = fromLang
        self.toLang = toLang
        self.salt = str(random.randint(32768, 65536))

    def BdTrans(self,text):
        sign = self.appid + text + self.salt + self.secretKey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        myurl = self.url + \
                '?appid=' + self.appid + \
                '&q=' + parse.quote(text) + \
                '&from=' + self.fromLang + \
                '&to=' + self.toLang + \
                '&salt=' + self.salt + \
                '&sign=' + sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            html = response.read().decode('utf-8')
            html = json.loads(html)
            dst = html["trans_result"][0]["dst"]
            return  True , dst
        except Exception as e:
            return False , e

#  セクション1 - オプションの設定と標準レイアウト
sg.theme('Dark Blue 3')

layout = [
    [sg.Text('原文', size=(5, 1)), sg.Multiline(default_text = "",size=(80,5), key="tx1", border_width=2)],
    [sg.Text('機能', size=(5, 1)), sg.Submit(button_text="中→日"),sg.Submit(button_text="日→中"), sg.Submit(button_text="中→英"),sg.Submit(button_text="英→中"), sg.Submit(button_text="英→日"),sg.Submit(button_text="日→英")],
    [sg.Text('', size=(5, 1)), sg.Submit(button_text="中→英→中"),sg.Submit(button_text="中→日→中"),sg.Submit(button_text="中→英→日"),sg.Submit(button_text="日→英→中")],
    [sg.Text('', size=(5, 1)), sg.Checkbox('ピンイン有', default=True, key="pinyin_status")],
    [sg.Text('訳文', size=(5, 1)), sg.Multiline(default_text = "",size=(80,5), key="tx2", border_width=2)]
]

# セクション 2 - ウィンドウの生成
window = sg.Window("第三方百度翻译桌面版", layout)

# セクション 3 - イベントループ
while True:
    event, values = window.read()

    if event is None:
        print('exit')
        break
    
    if len(values["tx1"]) > 1:
        if event == '中→日':
            BaiduTranslate_test = BaiduTranslate('zh','jp')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            window["tx2"]. Update(res_str1)

        if event == '日→中':
            BaiduTranslate_test = BaiduTranslate('jp','zh')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
  
            if values["pinyin_status"] == True:
                py_r = pinyin(res_str1)
                window["tx2"]. Update(res_str1+"\n"+str(py_r))
            else:
                window["tx2"]. Update(res_str1)

        if event == '中→英':
            BaiduTranslate_test = BaiduTranslate('zh','en')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            window["tx2"]. Update(res_str1)

        if event == '英→中':
            BaiduTranslate_test = BaiduTranslate('en','zh')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            window["tx2"]. Update(res_str1)

        if event == '英→日':
            translator = Translator()
            translated = translator.translate(values["tx1"] ,src='en' ,dest="ja");
            window["tx2"]. Update(translated.text)

        if event == '日→英':
            translator = Translator()
            translated = translator.translate(values["tx1"] ,src='ja' ,dest="en");
            window["tx2"]. Update(translated.text)

        if event == '中→英→中':
            BaiduTranslate_test = BaiduTranslate('zh','en')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            time.sleep(1)
            BaiduTranslate_test = BaiduTranslate('en','zh')
            Results,res_str2 = BaiduTranslate_test.BdTrans(res_str1)#要翻译的词组
            window["tx2"]. Update(res_str2)

        if event == '中→日→中':
            BaiduTranslate_test = BaiduTranslate('zh','jp')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            time.sleep(1)
            BaiduTranslate_test = BaiduTranslate('jp','zh')
            Results,res_str2 = BaiduTranslate_test.BdTrans(res_str1)#要翻译的词组
            window["tx2"]. Update(res_str2)

        if event == '中→英→日':
            BaiduTranslate_test = BaiduTranslate('zh','en')
            Results,res_str1 = BaiduTranslate_test.BdTrans(values["tx1"])#要翻译的词组
            translator = Translator()
            translated = translator.translate(res_str1 ,src='en' ,dest="ja");
            window["tx2"]. Update(translated.text)

        if event == '日→英→中':
            translator = Translator()
            translated = translator.translate(values["tx1"] ,src='ja' ,dest="en");
            res_str1 = translated.text
            BaiduTranslate_test = BaiduTranslate('en','zh')
            Results,res_str2 = BaiduTranslate_test.BdTrans(res_str1)#要翻译的词组
            window["tx2"]. Update(res_str2)

# セクション 4 - ウィンドウの破棄と終了
window.close()
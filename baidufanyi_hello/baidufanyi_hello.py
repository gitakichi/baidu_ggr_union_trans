import json
import random
import hashlib
from urllib import parse
import http.client
from api_secret import *

class BaiduTranslate:
    def __init__(self,fromLang,toLang):
        self.url = "/api/trans/vip/translate"
        self.appid = API_ID
        self.secretKey = API_PASS
        self.fromLang = fromLang
        self.toLang = toLang
        self.salt = random.randint(32768, 65536)

    def BdTrans(self,text):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        myurl = self.url + \
                '?appid=' + self.appid + \
                '&q=' + parse.quote(text) + \
                '&from=' + self.fromLang + \
                '&to=' + self.toLang + \
                '&salt=' + str(self.salt) + \
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
if __name__=='__main__':
    #BaiduTranslate_test = BaiduTranslate('jp','zh')
    #Results = BaiduTranslate_test.BdTrans("新闻联播は中国共産党中央の意見を中国14億の人民に周知することを目的に放送されています")#要翻译的词组
    
    BaiduTranslate_test = BaiduTranslate('zh','en')
    #Results,str = BaiduTranslate_test.BdTrans("真正决定各国国际竞争力的，不是一个国家在国际体系中挤压他国甚至破坏整个国际体系的能力，而是其提升国内治理水平、解决自身问题的能力。")#要翻译的词组
    Results,str = BaiduTranslate_test.BdTrans("谢谢。新冠肺炎疫情结束后，一起讲中文交流吧。")#要翻译的词组

    #BaiduTranslate_test = BaiduTranslate('en','zh')
    #Results = BaiduTranslate_test.BdTrans("Hello, World!")#要翻译的词组
    
    #print(Results)



    from googletrans import Translator
    import sys

    translator = Translator()
    
    translated = translator.translate(str ,src='en' ,dest="ja");
    print(translated.text)
    
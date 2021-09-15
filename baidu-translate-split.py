from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import win32clipboard

def BaiduTranslate(text_list):
    with Chrome() as driver:
        # print(driver.window_handles)
        driver.get('https://fanyi.baidu.com/')

        for i in range(len(text_list)):
            driver.execute_script("window.open('http://fanyi.baidu.com/')")
        
        # make sure all the windows exist
        WebDriverWait(driver, 10).until(lambda x: len(driver.window_handles) == len(text_list) + 1)
        
        for text, window in zip(text_list, driver.window_handles[-1:0:-1]):
            driver.switch_to.window(window)
            
            element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('baidu_translate_input'))
            
            element.click()
            
            win32clipboard.OpenClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            element.send_keys(Keys.CONTROL, 'v')
            #print('paste')
            
            #滚动到浏览器顶部
            #time.sleep(3)
            #driver.execute_async_script("window.scrollBy(0,0)", ""); 
            #time.sleep(10)
        
        
        
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        
        while True:
            time.sleep(1)
            if len(driver.get_log('driver')):
                print(driver.get_log('driver'))
                break
        
    


def SplitTextBySentenceAndCharLimit(text):
    result = []
    while (len(text) > 5000):
         clip = text[0:5000]
         index = clip.rfind(".")
         #if (index < 0)
         clip = text[0:index+1]
         result.append(clip)
         text = text[index+1:]
    
    result.append(text)
    print(len(result))
    return result
        

if __name__ == '__main__':
    
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

    clip_list = SplitTextBySentenceAndCharLimit(text)
    BaiduTranslate(clip_list)


    #win32clipboard.OpenClipboard()
    #win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    #win32clipboard.CloseClipboard()

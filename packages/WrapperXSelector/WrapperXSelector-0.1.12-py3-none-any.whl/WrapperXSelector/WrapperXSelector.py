import ssl
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import uuid
import time

module_dir = os.path.dirname(__file__) 

def generateWrapper(wrapper_name, url, repeated_pattern='no'):
    try:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        js_file_path = os.path.join(module_dir, 'jquery-3.7.1.min.js')
        with open(js_file_path, 'r') as js_file:
            script = js_file.read()
            driver.execute_script(script)

        js_file_path = os.path.join(module_dir, 'jquery.alerts.js')
        with open(js_file_path, 'r') as js_file:
            script = js_file.read()
            driver.execute_script(script)

        css_file_path = os.path.join(module_dir, 'jquery.alerts.css')
        with open(css_file_path, 'r') as css_file:
            css_content = css_file.read()
            driver.execute_script(f'''
                var style = document.createElement('style');
                style.type = 'text/css';
                style.innerHTML = `{css_content}`;
                document.head.appendChild(style);
            ''')

        js_file_path = os.path.join(module_dir, 'operation.js')
        with open(js_file_path, 'r') as js_file:
            script = js_file.read()
            driver.execute_script(f"window.repeated_pattern = {repr(repeated_pattern)};\n{script}")

        while not driver.execute_script("return window.userTasksCompleted"):
            time.sleep(1)

        input_field_values = driver.execute_script("return window.inputFieldValues")
        
        wrapper_list = []
        for xpath_pair in input_field_values:
            key = xpath_pair['attribute_name']
            xpath_root = xpath_pair['attribute_value_parent']
            xpath_sub = xpath_pair['attribute_value']
            key = key.strip()
            xpath_root = xpath_root.strip()
            xpath_sub = xpath_sub.strip()

            dics = {}
            if key == '':
                dics['attribute'] = 'Undefined'
            else:
                dics['attribute'] = key
            if repeated_pattern == 'yes':
                dics['value'] = "//*[@class='"+xpath_root+"']//*[@class='"+xpath_sub+"']"
            else:
                dics['value'] = xpath_root

            wrapper_list.append(dics)

        unique_wrapper_name = wrapper_name + '_' + str(uuid.uuid4()) + '.json'
        with open(unique_wrapper_name, 'w') as json_file:
            json.dump(wrapper_list, json_file)
            return unique_wrapper_name
    except Exception as error:
        return error
    


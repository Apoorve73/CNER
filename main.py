from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


def read_csv(filename: str, columns: list):
    dataframe = pd.read_csv(filename, names=columns, skiprows=[0])
    result_array = []
    if len(columns) > 0:
        result_array = list(dataframe[columns[0]])

    return result_array


sentences = read_csv('database/train/query_db.csv', ['query'])

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(0.5)

count = 0
for sentence in sentences[100:200]:
    driver.get("https://www.google.com/")
    driver.implicitly_wait(0.5)
    print("Processing...  " + sentence)
    try:
        m = driver.find_element(By.NAME, "q")
        m.send_keys(sentence)
        m.send_keys(Keys.ENTER)
    except:
        continue


    try:
        news = driver.find_element(By.ID, 'hdtb-msb')
    except: continue

    try:
        navs = news.find_elements(By.TAG_NAME, 'a')
    except: continue
    actions = ActionChains(driver)
    n = ''
    data_row = {}
    # data = list()
    for nav in navs:
        if nav and nav.text == 'News':
            actions.click(nav)
            actions.perform()

            try:
                n = driver.find_element(By.ID, 'search')
            except: break


            news_links = n.find_elements(By.TAG_NAME, 'a')

            data_row['query'] = sentence
            link_count = 1
            for link in news_links:

                href = link.get_attribute('href')
                text = link.text
                if (href):
                    data_row["link"+str(link_count)] = href
                else:
                    data_row["link" + str(link_count)] = ""

                if (text):
                    data_row['text'+str(link_count)] = link.text
                else:
                    data_row['text'+str(link_count)] = ""

                link_count += 1

            df = pd.DataFrame(data_row, index = [count])
            df.to_csv('./database/train/query_db_final_2.csv', mode="a", header=False)

        if n != '':

            break

    # if len(data_row) == 21:
    #     data.append(data_row)
    count += 1
    print("Processed ", count)
    print ("\n***********************\n\n")

    driver.implicitly_wait(10)

# #

#

# # data = [[1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17,18,19,20]]
# def write_to_csv(data: list, filename: str):
#
#         columns = ['query', 'link1', 'text1', 'link2', 'text2', 'link3', 'text3', 'link4', 'text4', 'link5', 'text5',
#                    'link6', 'text6', 'link7', 'text7', 'link8', 'text8', 'link9', 'text9', 'link10', 'text10']
#         dataframe = pd.DataFrame(data, columns=columns)
#
#         dataframe.to_csv(filename)
#
# write_to_csv(data, './database/train/query_db_final.csv')

#launch URL
# driver.get("https://www.google.com/")
# #identify search box
# m = driver.find_element(By.NAME, "q")
# #enter search text
# m.send_keys("Tutorialspoint")
# time.sleep(0.2)
# #perform Google search with Keys.ENTER
# m.send_keys(Keys.ENTER)
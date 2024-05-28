import time
from selenium import webdriver
import sqlite3



def create_table():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS stock_list (stock text unique,do_flag integer)")
    con.commit()
    con.close()

def insert_data(stock):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO stock_list VALUES (?,'0')",(stock,))
    con.commit()
    con.close()
    

def get_stock_code_data():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    stock_code_list = []
    cur.execute("select * from stock_list where do_flag = 0")
    for row in cur:
        stock_code_list.append(row[0])
    con.close()
    #print(stock_code_list)
    return stock_code_list

def set_stock_code(stock):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(f"UPDATE stock_list SET do_flag = 1 WHERE stock = ?",stock)
    con.commit()
    con.close()

def refresh_all_stock_code():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("UPDATE stock_list SET do_flag = 0")
    con.commit()
    con.close()

def scrapying_stock_list():
    #del_all_stock_code()#clear db
    refresh_all_stock_code()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver=webdriver.Chrome(options=options)
    #driver=webdriver.Chrome()
    driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/psi")
    
    try:
        """ start = time.time() """
        button = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[6]/td/input')
        button.click()
        date_list_str = driver.find_element('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody")    #"tr[1""]"
        stock_code = date_list_str.find_elements('xpath',"./*")
        for i in stock_code:
            print(i.find_element('xpath',"./td[1]").text + " " + str(len(i.find_element('xpath',"./td[1]").text)))
            if len(i.find_element('xpath',"./td[1]").text) == 4:
                insert_data(i.find_element('xpath',"./td[1]").text)
        option = driver.find_element('xpath',"/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[1]/td[2]/select/option[2]")
        option.click()
        button = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[6]/td/input')
        button.click()
        date_list_str = driver.find_element('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody")    #"tr[1""]"
        stock_code = date_list_str.find_elements('xpath',"./*")
        for i in stock_code:
            print(i.find_element('xpath',"./td[1]").text + " " + str(len(i.find_element('xpath',"./td[1]").text)))
            if len(i.find_element('xpath',"./td[1]").text) == 4:
                insert_data(i.find_element('xpath',"./td[1]").text)
        """ end = time.time()
        print(end-start) """
    except:
        pass    
    #for i in stock_code:
    #    print(i.find_element('xpath',"./td[1]").text)
""" if __name__ == '__main__':
    scrapying_stock_list() """
'''
for i in stock_code:
    print(i)
'''
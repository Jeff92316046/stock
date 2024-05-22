from selenium import webdriver
import sqlite3



def create_table():
    con = sqlite3.connect('stock_code_list.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE data (stock text)")
    con.commit()
    con.close()

def insert_data(stock):
    con = sqlite3.connect('stock_code_list.db')
    cur = con.cursor()

    cur.execute("INSERT INTO data VALUES (" + "'" + str(stock) + "')")

    con.commit()
    con.close()

def get_stock_code_data():
    stock_code_list = []
    con = sqlite3.connect('stock_code_list.db')
    cur = con.cursor()

    cur.execute("select * from data")
    for row in cur:
        stock_code_list.append(row[0])
    con.commit()
    con.close()
    return stock_code_list

def del_stock_code(stock):
    con = sqlite3.connect('stock_code_list.db')
    cur = con.cursor()
    cur.execute("DELETE FROM data WHERE stock = " + str(stock))
    con.commit()
    con.close()

def del_all_stock_code():
    con = sqlite3.connect('stock_code_list.db')
    cur = con.cursor()
    cur.execute("DELETE FROM data")
    con.commit()
    con.close()

def scrapying_1():
    print("開始下載股票代碼清單")
    del_all_stock_code()#clear db
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver=webdriver.Chrome(options=options)
    #driver=webdriver.Chrome()
    driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/psi")

    button = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[6]/td/input')
    button.click()

    

    date_list_str = driver.find_element('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody")    #"tr[1""]"

    
    stock_code = date_list_str.find_elements('xpath',"./*")

    for i in stock_code:
        print(i.find_element('xpath',"./td[1]").text + " " + str(len(i.find_element('xpath',"./td[1]").text)))
        if len(i.find_element('xpath',"./td[1]").text) == 4:
            insert_data(i.find_element('xpath',"./td[1]").text)
        
    #for i in stock_code:
    #    print(i.find_element('xpath',"./td[1]").text)
def scrapying_2():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver=webdriver.Chrome(options=options)
    #driver=webdriver.Chrome()
    try:
        driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/psi")

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
    except:
        
        pass
    print("股票代碼清單下載完畢")


'''
for i in stock_code:
    print(i)
'''
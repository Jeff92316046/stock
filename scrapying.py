from selenium import webdriver
import time
import get_stock_code
import sqlite3
import logging

people = []
shares = []
con = sqlite3.connect('database.db')
cur = con.cursor()
#date_start = 0

def clean_str(a):
    return str(a).replace(",","")


def scrapying_2(week):
    #create_table()
    #get_stock_code.create_table()
    get_stock_code.refresh_all_stock_code()
    get_stock_code.scrapying_stock_list()
    logging.basicConfig(level=logging.INFO,filename='std.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',encoding="utf-8")
    logging.info("開始下載股票資訊")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    #driver = webdriver.Chrome(options=options)
    driver=webdriver.Chrome()
    driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/qryStock")
    """ get_stock_code.scrapying_1()
    get_stock_code.scrapying_2() """
    
    #gsc = ['0050','0051']
    while(True):
        gsc = get_stock_code.get_stock_code_data()
        if len(gsc) == 0:
            break
        try :
            for k in range(0,len(gsc)):  
                code = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[2]/td[2]/input')
                code.clear()
                code.send_keys(gsc[k])
                logging.info(f"{gsc[k]}")
                time.sleep(0.2)
                date_list_str = "/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[1]/td[2]/select/option"
                for j in range(0,week) :
                    #try:
                    date_option = driver.find_element('xpath',f"{date_list_str}[{str(j+1)}]")
                    date_text = date_option.text
                    date_option.click()
                    time.sleep(0.3)
                    #if j == 0:
                    #    date = clean_str(date_option.text)
                    click1 = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[4]/form/table/tbody/tr[4]/td/input')
                    click1.click()
                    time.sleep(0.4)
                    c_counter = 0
                    while c_counter<16:
                        temp_1 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(c_counter+1)+"]/td[3]")
                        temp_2 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(c_counter+1)+"]/td[4]")
                        if len(temp_1) != 0 and len(temp_2)!=0 :
                            insert_data(clean_str(gsc[k]),clean_str(date_text),clean_str(c_counter+1),clean_str(temp_1[0].text),clean_str(temp_2[0].text))
                            c_counter += 1
                        else:
                            temp_3 = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr/td/span').text
                            if temp_3 == '查無此資料':
                                logging.warning(f"stock :1295,date :{clean_str(date_text)} || no data")
                                break
                            c_counter -= 1
                get_stock_code.set_stock_code(gsc[k])
                time.sleep(0.1)
            con.commit()
        except :
            con.commit()
            pass
    logging.info("股票資訊下載完畢")
    con.close()


def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT,stock text , date_time text , number integer , people integer , share integer )")
    con.commit()
    con.close()

    
def insert_data(stock ,date ,number ,people ,share):
    #用?
    print(f"INSERT INTO data(stock,date_time,number,people,share) VALUES" 
                f"('{stock}'," 
                f"'{date}',"
                f"'{number}',"
                f"'{people}',"
                f"'{share}')")
    logging.info(f"stock :{stock}, date :{date}, number :{number}")
    cur.execute(f"INSERT INTO data(id,stock,date_time,number,people,share) SELECT " 
                f"NULL,"
                f"'{stock}'," 
                f"'{date}',"
                f"'{number}',"
                f"'{people}',"
                f"'{share}' "
                f"WHERE NOT EXISTS(SELECT * FROM data WHERE "
                f"stock='{stock}' and "
                f"date_time='{date}' and "
                f"number='{number}')")
    
if __name__ == '__main__':
    scrapying_2(1)
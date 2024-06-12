from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import get_stock_code
import sqlite3
import logging

people = []
shares = []
t = time.time()
#date_start = 0

def clean_str(a):
    return str(a).replace(",","")


def scrapying_2(week):
    now_time = time.localtime(t)
    file_time_str = time.strftime('%Y%m%d%H%M%S',now_time)
    logging.basicConfig(level=logging.INFO,filename=f'std{file_time_str}.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',encoding="utf-8")
    logging.info("start execute program")
    create_table()
    get_stock_code.create_table()
    logging.info("scrapying stock list")
    #get_stock_code.scrapying_stock_list()
    
    """ get_stock_code.scrapying_1()
    get_stock_code.scrapying_2() """
    
    #gsc = ['0050','0051']
    while(True):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
        #driver=webdriver.Chrome()
        driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/qryStock")
        logging.info("get stock code")
        gsc = get_stock_code.get_stock_code_data()
        print(gsc)
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
                    temp = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/*")
                    print(len(temp))
                    if len(temp)==16:
                        for i in range(16):
                            temp_1 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(i+1)+"]/td[3]")
                            temp_2 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(i+1)+"]/td[4]")
                            if len(temp_1) != 0 and len(temp_2)!=0 :
                                insert_data(clean_str(gsc[k]),clean_str(date_text),clean_str(i+1),clean_str(temp_1[0].text),clean_str(temp_2[0].text))
                                logging.info(f"insert || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : {clean_str(i+1)}")
                            else:
                                temp_3 = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr/td/span').text
                                if temp_3 == '查無此資料':
                                    logging.warning(f"no data || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : {clean_str(i+1)}")
                                    break
                    elif len(temp) == 17:
                        flag = 0
                        for i in range(15):
                            temp_1 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(i+1)+"]/td[3]")
                            temp_2 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr["+str(i+1)+"]/td[4]")
                            if len(temp_1) != 0 and len(temp_2)!=0 :
                                insert_data(clean_str(gsc[k]),clean_str(date_text),clean_str(i+1),clean_str(temp_1[0].text),clean_str(temp_2[0].text))
                                logging.info(f"insert || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : {clean_str(i+1)}")
                            else:
                                temp_3 = driver.find_element('xpath','/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr/td/span').text
                                if temp_3 == '查無此資料':
                                    logging.warning(f"no data || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : {clean_str(i+1)}")
                                    flag = 1
                                    break
                        if flag == 0:
                            temp_1 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr[17]/td[3]")
                            temp_2 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr[17]/td[4]")
                            logging.info(f"insert || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : 16")
                            insert_data(clean_str(gsc[k]),clean_str(date_text),"16",clean_str(temp_1[0].text),clean_str(temp_2[0].text))
                            temp_1 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr[16]/td[3]")
                            temp_2 = driver.find_elements('xpath',"/html/body/div[1]/div[1]/div/main/div[6]/div/table/tbody/tr[16]/td[4]")
                            logging.info(f"insert || stock : {clean_str(gsc[k])}, date : {clean_str(date_text)}, number : 17")
                            insert_data(clean_str(gsc[k]),clean_str(date_text),"17","nod",clean_str(temp_2[0].text))#Number of differences
                logging.info(f"{gsc[k]} finish")
                get_stock_code.set_stock_code(gsc[k])
                
                time.sleep(0.1)
        except Exception as e:
            logging.error(f"error:{e}")
            pass
    logging.info("all finish")


def create_table():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT,stock text , date_time text , number integer , people integer , share integer )")
    con.commit()
    con.close()

    
def insert_data(stock ,date ,number ,people ,share):
    #用?
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    """ print(f"INSERT INTO data(stock,date_time,number,people,share) VALUES" 
                f"('{stock}'," 
                f"'{date}',"
                f"'{number}',"
                f"'{people}',"
                f"'{share}')") """
    print(f"{stock} {date} {number}")
    #logging.info(f"stock :{stock}, date :{date}, number :{number}")
    cur.execute(f"INSERT INTO data(stock,date_time,number,people,share) SELECT " 
                f"?,?,?,?,? "
                f"WHERE NOT EXISTS"
                f"(SELECT * FROM data WHERE "
                f"stock=? and "
                f"date_time=? and "
                f"number=?)",(stock,date,number,people,share,stock,date,number,))
    
    con.commit()
    con.close()

def get_data():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT DISTINCT date_time FROM data ORDER BY date_time ASC")
    temp = cur.fetchall()
    print(temp)
    con.commit()
    con.close()
if __name__ == '__main__':
    scrapying_2(2)
    # insert_data("0050","20240517","1","380744","103226454")
    # con.commit()
    # con.close()
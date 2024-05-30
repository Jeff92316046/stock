import sqlite3

def clean_str(a):
    return str(a).replace(",","")

def insert_data(stock ,date ,number ,people ,share):
    #用?
    con = sqlite3.connect('database.db')
    cur = con.cursor()
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
    con = sqlite3.connect('olddb.db')
    cur = con.cursor()
    cur.execute("SELECT DISTINCT stock FROM data ORDER BY stock ASC")
    temp = cur.fetchall()
    con.commit()
    con.close()
    return temp

if __name__ == '__main__':
    data_list = get_data()
    for i in data_list:
        con = sqlite3.connect('olddb.db')
        cur = con.cursor()
        cur.execute("SELECT DISTINCT date FROM data Where stock=? ORDER BY date ASC",i)
        temp = cur.fetchall()
        con.close()
        for j in temp:
            con = sqlite3.connect('olddb.db')
            cur = con.cursor()
            cur.execute("SELECT DISTINCT * FROM data Where stock=? and date=? ORDER BY number ASC",(i[0],j[0]))
            datas = cur.fetchall()
            con.close()
            sum_of_people = 0
            sum_of_share = 0
            for k in datas:
                print((k[0],k[1],k[2],clean_str(k[3]),clean_str(k[4])))
                insert_data(k[0],k[1],k[2],clean_str(k[3]),clean_str(k[4]))
                sum_of_people += int(clean_str(k[3]))
                sum_of_share += int(clean_str(k[4]))
            print((i[0],j[0],16,sum_of_people,sum_of_share))
            insert_data(i[0],j[0],16,sum_of_people,sum_of_share)
            # 
            # insert_data(temp[i][0],temp[i][1],temp[i][2],temp[i][3],temp[i][4])
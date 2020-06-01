from requests import Session
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import time

class FinanceInfo():
    def __init__(self):
        driver = webdriver.Chrome()
        username = input("Please enter username / email address")
        password = input("Please enter password")
        if pd.read_csv("transactions"):
            df = pd.read_csv("transactions")
        else:
            df = False
    

    def mint_login(self):
        print("going to mint sign in page")
        self.driver.get("https://accounts.intuit.com/index.html?offering_id=Intuit.ifs.mint&namespace_id=50000026&redirect_url=https%3A%2F%2Fmint.intuit.com%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown%26ivid%3Dba4d1414-e702-4303-8410-a9f0019dd4bc%26adobe_mc%3DMCMID%253D19539525595619935599106334886326313394%257CMCORGID%253D969430F0543F253D0A4C98C6%252540AdobeOrg%257CTS%253D1589072739%26ivid%3Dba4d1414-e702-4303-8410-a9f0019dd4bc")
        time.sleep(3)
        print("entering username")
        self.driver.find_element_by_id("ius-userid").send_keys(self.username)
        print("entering password")
        self.driver.find_element_by_id("ius-password").send_keys(self.password)
        print("clicking sign-in")
        self.driver.find_element_by_name("SignIn").click()
        time.sleep(10)
        print("logged_in")

    def mint_get_transactions(self, df):
        #go to transaction page
        self.driver.get("https://mint.intuit.com/transaction.event")
        time.sleep(3)
        #get transactions
        transactions_html = driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/table").get_attribute("innerHTML")
        bs_content = bs(transactions_html, 'html.parser')
        #get date, money, and description
        html_date = np.array(bs_content.find_all("td", class_="date"))
        html_money = np.array(bs_content.find_all("td", class_="money"))
        html_description = np.array(bs_content.find_all("td", class_="description noattachcol"))
        #remove empty values
        html_date = html_date[html_date != '']
        html_money = html_money[html_date != '']
        html_description = html_description[html_description != '']
        #keep track of when to stop adding date and money to csv
        tracker = 0
        new_transaction = ''
        if df:
            last_transaction = df.iloc(-1)
            while last_transaction != new_transaction:
                new_transaction = get_transaction(tracker, html_date, html_money, html_description)
                df.append(new_transaction)
                tracker += 1
        else:
            df = pd.DataFrame()
            for i in range(len(html_date)):
                new_transaction = get_transaction(tracker, html_date, html_money, html_description)
                df.append(new_transaction)
                tracker += 1
        return df

    def get_transaction(self, tracker, html_date, html_money, html_description):
        date = html_date[tracker].get_text()
        money = html_money[tracker].get_text()
        description = html_description[tracker].get_text()
        month = date.split(" ")[0]
        amount = float(html_money[index].get_text().replace("$","").replace(",",""))
        #get account
        if tracker == 0:
            account = driver.find_element_by_id("txn-detail-details").get_attribute("innerHTML")
        else:
            tracker +=1
            self.driver.find_element_by_xpath(f"/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/table/tbody/tr[{tracker}]/td[8]").click()
            account = self.driver.find_element_by_id("txn-detail-details").get_attribute("innerHTML")
        trans_account = bs(trans_account, "html.parser")
        account = trans_account.find("dd").get_text()

        transaction = pd.DataFrame([
                                    date,
                                    description,
                                    money,
                                    account,
                                    ],
                                    columns=[
                                            "Date", 
                                            "Description", 
                                            "Amount", 
                                            "Account"
                                            ]
                                    )
        return transaction

if __name__ == __main__:
    financeObj = FinanceInfo()
    financeObj.mint_login()
    #bs_transactions = mint_get_transactions()
    transactions = financeObj.mint_get_transactions()

    html_date = transactions.find_all("td", class_="date")
    html_money = transactions.find_all("td", class_="money")

    months = []
    money = []

    for index in range(len(html_date)):
        print(html_date[index].get_text(), html_money[index].get_text())
        date = html_date[index].get_text()
        if date == "":
            break
        month = date.split(" ")[0]
        amount = float(html_money[index].get_text().replace("$","").replace(",",""))
        if month not in months:
            months.append(month)
            money.append(amount)
        else:
            money[months.index(month)] += amount

    print("Month\tMoney")
    for i in range(len(months)):
        print(months[i], "\t", money[i])


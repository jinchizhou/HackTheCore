import requests
import json

cardtoken = "1ae72c89-3a4d-4979-bf1c-026b63826909"
customertoken = "9d18e7f7-24c2-4eb2-ba8c-30d063489856"
deposittoken = "f14e68f1-1563-4dbb-8673-60295583db5c"
loantoken = "e430fcde-7131-4a71-9712-cf676cc4c138"
taxID1 = "588302286"
# takes taxID of person, returns json data 
def customer_profile(taxID):
    url = "https://srvpocanz001.csc-fsg.com/CeleritiCustomersAPI/services/v1/customers/taxID%3D" + taxID + "/profile"
    headers = {
                'accept': "application/json",
                    'authorization': "Bearer " + customertoken,
                        'cache-control': "no-cache",
                            'postman-token': "8d8c92c5-9b88-87d4-fbb2-fa298f76f246"
                                }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    return data
# takes acctnum returns json data of acct, returns transaction info
def card_transactions(acctnum):

    url = "https://srvpocanz001.csc-fsg.com/CeleritiCardsAPI/services/v1/cardAccounts/" + acctnum + "/transactions"

    headers = {
                'authorization': "Bearer " + cardtoken,
                    'cache-control': "no-cache",
                        'postman-token': "43072743-07c0-aae5-c0df-6803acb4e6f7"
                            }

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text)
    return data
# takes json data from customer profile, prints out name
def name(data):
    if data["customerInfo"]["customerNameLine2"] is not None:
        print("User:    " + data["customerInfo"]["customerNameLine1"] + data["customerInfo"]["customerNameLine2"])
    else:
        print("User:    " + data["customerInfo"]["customerNameLine1"])
# takes transaction data, get total of transactionAmt
def transaction_total(data):
    total = 0
    for amts in data["transactionInfo"]:
        total += amts["transactionAmt"]
    return total
# takes json data, dict, puts acctnum in dict
def accounts(data, dicti):
    # Assumming just one card and deposit account
    for product in data["accountInformation"]:
        if product["productCd"] == "DDA":
            dicti["dda"] = parse_accountnbr(product["accountNbr"])
        elif product["productCd"] == "CRD":
            dicti["crd"] = parse_accountnbr(product["accountNbr"])
        elif product["productCd"] == "CLS":
            dicti["cls"] = product["accountNbr"]
    return dicti
# takes account num, parses the "*"
def parse_accountnbr(cardnum):
    cn = ""
    for a in range(len(cardnum)):
        if cardnum[a:a + 1] == "*" or cardnum[a:a + 1] == "-":
            continue;
        cn += cardnum[a:a + 1]
    return cn
# takes acctnum, returns deposit acct info
def dep_acct_info(acctnum):
    url = "https://srvpocanz001.csc-fsg.com/CeleritiDepositsAPI/services/v1/depositAccountsDda/" + acctnum
    querystring = {"companyNbr":"11","accountType":"DDA","extendsFields":"all"}
    headers = {
                'authorization': "Bearer " + deposittoken,
                    'cache-control': "no-cache",
                        'postman-token': "9320b245-3033-f0e6-abb4-ca9c834fb84c"
                            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data
# takes json data, parses current balance
def get_currentBalance(data):
    return data["balancePostingInformation"]["currentBalance"]
# takes acctnum, returns deposit acct transactions
def deposit_transactions(acctnum):
    url = "https://srvpocanz001.csc-fsg.com/CeleritiDepositsAPI/services/v1/depositAccounts/" + acctnum + "/transactions"
    querystring = {"accountType":"DDA"}
    headers = {
                'authorization': "Bearer " + deposittoken,
                    'cache-control': "no-cache",
                        'postman-token': "bed14bde-902a-413f-6413-3128c6d5d767"
                            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data
# takes deposit acct data, parses each separate deposit
def print_dep_trans_total(data):
    trancount = 1
    print("List of Deposit Transactions: ")
    for trans in data["transaction"]:
        curr = trans["tranAmt"]
        print("\tTransaction " + str(trancount) + ": $" + str(curr))
        trancount += 1
# takes CLS acctnum, loantoken, ret loan info 
def get_loan_info(acctnum):
    url = "https://srvpocanz001.csc-fsg.com/CeleritiLoansAPI/services/v1/loanAccounts/" + acctnum
    querystring = {"companyNbr":"11","productCd":"CLS","extendsFields":"all"}
    headers = {
                'authorization': "Bearer " + loantoken,
                    'cache-control': "no-cache",
                        'postman-token': "9c77e3ca-4fd0-801b-9850-aab3a9ba6ee9"
                            }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data
# takes loan json, ret amtdue
def loan_amt_due(data):
    return data["loanAccountData"]["amountDue"]
def main():
    # customer profile
    # Art Venere
    profile_data = customer_profile(taxID1)
    # print user name
    name(profile_data)
    # card info in dict, contains crd, dda, bor, cls
    acct_num_dict = {}
    acct_num_dict = accounts(profile_data, acct_num_dict)
    # loans
    loan_info = get_loan_info(acct_num_dict["cls"])
    monthlydue = loan_amt_due(loan_info)
    print("Amount Due from your loan this month: $" + str(monthlydue))
    # cards 
    card_transaction_data = card_transactions(acct_num_dict["crd"])
    trans_total = transaction_total(card_transaction_data)
    print("Transaction Total from Total Cards: $" + str(trans_total))
    # deposit accounts
    deposit_data = dep_acct_info(acct_num_dict["dda"])
    deposit_balance = get_currentBalance(deposit_data)
    dep_trans_data = deposit_transactions(acct_num_dict["dda"])
    print_dep_trans_total(dep_trans_data)
    print("Current Balance in Account is: $" + str(deposit_balance))
if __name__ == "__main__":
    main()

import requests
import json

cardtoken = "fd4d83f3-5fc9-455c-b3d4-ddac40f7ad04"
customertoken = "9372dbf4-839a-48f8-89d5-a2b9031a58c1"
depositstoken = "08b2ea9a-d2b0-4775-9314-e5b1ce10f920"
loanstoken = "45a414b3-dae4-4c7c-902c-48b4ce035535"

# takes taxID of person, returns json data 
def customer_profile(taxID, customertoken):
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
def transactions(acctnum, cardtoken):

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
# takes json data, prints separates "product types"
def accounts(data):
    # Assumming just one card and deposit account
    for product in data["accountInformation"]:
        if product["productCd"] == "DDA":
            dda_acct_num = product["accountNbr"]
        elif product["productCd"] == "CRD":
            card_account_num = parse_accountnbr(product["accountNbr"])
    return dda_acct_num, card_account_num
# takes account num, parses the "*"
def parse_accountnbr(cardnum):
    cn = ""
    for a in range(len(cardnum)):
        if cardnum[a:a + 1] == "*":
            continue;
        cn += cardnum[a:a + 1]
    return cn
def main():
    # Art Venere
    taxID1 = "588302286"
    profile_data = customer_profile(taxID1, customertoken)
    # print user name
    name(profile_data)
    # card info
    dda_acct_num, card_acctnum = accounts(profile_data)
    transaction_data = transactions(card_acctnum, cardtoken)
    trans_total = transaction_total(transaction_data)
    print("Transaction Total from Total Cards: $" + str(trans_total))
if __name__ == "__main__":
    main()

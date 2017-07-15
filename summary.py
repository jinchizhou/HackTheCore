import requests
import json

# takes url, taxID of person, returns json data 
def customer_profile(url, taxID):
    url = "https://srvpocanz001.csc-fsg.com/CeleritiCustomersAPI/services/v1/customers/taxID%3D" + taxID + "/profile"
    headers = {
                'accept': "application/json",
                    'authorization': "Bearer 37ae7f42-e804-4d37-9d24-0f05e5b826a5",
                        'cache-control': "no-cache",
                            'postman-token': "8d8c92c5-9b88-87d4-fbb2-fa298f76f246"
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
# takes json data, prints separates "product types"
def accounts(data):
    #int start = 0
    #while(
    for product in data["accountInformation"]:
        if product["productCd"] == "DDA":
            print(product["accountNbr"])
        elif product["productCd"] == "CRD":
            card_account_num = parse_accountnbr(product["accountNbr"])
            print(card_account_num)
# takes account num, parses the "*"
def parse_accountnbr(cardnum):
    cn = ""
    for a in range(len(cardnum)):
        if cardnum[a:a + 1] == "*":
            continue;
        cn += cardnum[a:a + 1]
    return cn
def main():
    url = "https://srvpocanz001.csc-fsg.com/CeleritiCustomersAPI/services/v1/customers/taxID%3D588302286/profile"
    # Art Venere
    taxID1 = "588302286"
    data = customer_profile(url, taxID1)
    # print user name
    name(data)
    # card info
    accounts(data)

if __name__ == "__main__":
    main()

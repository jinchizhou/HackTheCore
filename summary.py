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
    print(data["customerInfo"]["customerNameLine1"])
    return data
def main():
    url = "https://srvpocanz001.csc-fsg.com/CeleritiCustomersAPI/services/v1/customers/taxID%3D588302286/profile"
    # Art Venere
    taxID1 = "588302286"
    data = customer_profile(url, taxID1)

if __name__ == "__main__":
    main()

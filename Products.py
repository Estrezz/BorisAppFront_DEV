import requests
import pandas as pd

url = "https://api.tiendanube.com/v1/1447373/products"

payload={}
headers = {
  'User-Agent': 'Boris (erezzonico@borisreturns.com)',
  'Content-Type': 'application/json',
  'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
}

products = requests.request("GET", url, headers=headers, data=payload).json()

print(type(products))

print(products[1])
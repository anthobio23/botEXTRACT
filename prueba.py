x = "$ 8.800"
x2= (x.split("$ "))

price_value = int(float(x2[1])*1000/1)
price_30off = price_value - price_value*0.30
print(int(price_30off * 1.9))


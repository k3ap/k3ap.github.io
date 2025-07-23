import random


num = random.randint(1, 100)

print("Izmislil sem si število med 1 in 100. Ugibaj, katerega!")

while True:
    ugib = input("Zapiši ugib: ")
    try:
        ugib = int(ugib)
        if ugib < 1 or ugib > 100:
            raise Exception
    except:
        print("To ni število 1 do 100...")

    if ugib == num:
        print("Bravo! Pravilno.")
        break

    if ugib < num:
        print("Moje število je večje.")
    else:
        print("Moje število je manjše.")

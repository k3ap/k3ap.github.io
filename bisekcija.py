import random


num = random.randint(1, 100)

print("Izmislil sem si število med 1 in 100. Ugibaj, katerega!")

while True:
    ugib1 = input("Zapiši ugib: ")
    ugib = int(ugib1)

    if ugib == num:
        print("Bravo! Pravilno.")
        break

    if ugib < num:
        print("Moje število je večje.")
    else:
        print("Moje število je manjše.")

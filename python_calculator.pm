# Pokročilá kalkulačka v PyMartis (.pm)
print("==================================")
print("   VITÁ VÁS POKROČILÁ PYMARTIS KALKULAČKA")
print("==================================")

bezi = 1
while bezi == 1:
    print("")
    print("Vyber operaci:")
    print("1 - Sčítání (+)")
    print("2 - Odčítání (-)")
    print("3 - Násobení (*)")
    print("4 - Dělení (/)")
    print("5 - Konec")
    
    volba = input("Zadej číslo volby:")
    
    if volba == 5:
        print("Ukončuji kalkulačku. Měj se!")
        bezi = 0
    else:
        num1 = input("Zadej první číslo:")
        num2 = input("Zadej druhé číslo:")
        
        if volba == 1:
            vysledek = num1 + num2
            print("Výsledek sčítání je:")
            print(vysledek)
        elif volba == 2:
            vysledek = num1 - num2
            print("Výsledek odčítání je:")
            print(vysledek)
        elif volba == 3:
            vysledek = num1 * num2
            print("Výsledek násobení je:")
            print(vysledek)
        elif volba == 4:
            if num2 == 0:
                print("Chyba: Nelze dělit nulou!")
            else:
                vysledek = num1 / num2
                print("Výsledek dělení je:")
                print(vysledek)
        else:
            print("Neplatná volba operace. ")

print("Díky, že jsi využil PyMartis kalkulačku.")

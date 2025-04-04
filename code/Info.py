import sys

def chose_table_dim():
    dim = int(input("Unesite dimenzije table (8): "))
    while dim > 16 or dim < 8 or dim % 2 != 0:
        dim = int(input("Dimenzija nije validna, unesite ponovo (8): "))
    return dim

def chose_player():
    player = input("Ukoliko zelite da igrate prvi unesite X, u suprotnom unesite O: ").upper()
    while(player not in ['X', 'O']):
        player = input("Moguce je uneti X ili O: ")
    return player

def ai_play():
    racunar = input("Da li zelite da igrate protiv racunara? Odgovorite sa Da ili Ne. ").upper()
    while (racunar not in ["DA", "NE"]):
        racunar = input("Neispravan unos. Unesite da ili ne.").upper()
    if racunar == "DA":
        return True
    else:
        return False 


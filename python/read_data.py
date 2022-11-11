import io
import sys
# -*- encoding: utf-8 -*-
"""
Program czyście tekst ze znaków białych, symboli diakrytycznych, cyfr, 
a litery zamienia na małe oraz formatuje tekst w 7 kolumn po 5 znaków.
"""

def wczytaj(a,nazwa_pliku):
    try:
        t = io.open(nazwa_pliku,mode="r",encoding="utf-8")
        a = t.read()
        t.close()
        return a.lower()
    except:
        print("Niepoprawna nazwa pliku. \n")
        return wczytaj(a,nazwa_pliku)
    
    
def usun_znaki(table,rm_sp):
    print(table)
    sym=" .,'!:;/@#$%^&(*)-_+=[{]}|?\n\""
    if not rm_sp:
        return rm_sym(usun_plznaki(table),sym)

    s1=sys.argv[8]
    s2=sys.argv[9]
    
    return rm_sym(usun_plznaki(replace_sym(table,s1,s2)),sym)

def rm_sym(table,symbole):
    b=range(len(symbole))
    for i in b:
        table=table.replace(symbole[i],"")
    return(table)

def replace_sym(table,znaki,znaki2):
    b=range(len(znaki))
    for i in b:
        table=table.replace(znaki[i],znaki2[i]) 
    return(table)

def usun_plznaki(table):
    return replace_sym(table,"ąęółżźćń","aeolzzcn")


def usun_cyfry(table):
    cyfry="0123456789"
    b=range(len(cyfry))
    for i in b:
        table=table.replace(cyfry[i],"")
    return(table)     
    
def przeksztalcenie(table,table2):
    size = range(len(table))
    k = 0
    for i in size:
    
        if i%5 == 0 and i !=0 and i%35 !=0:
            k+=1
            table2 = table2+" "
            #table2[i+k]=" "
        if i%35==0 and i != 0:
            k+=1
            table2 = table2+"\n"
            #table2[i+k]="\n"
        table2 = table2 + table[i]
    return(table2)
    
def zapis(table2,print_file):
    if (print_file):
        print(table2)
    nazwa_pliku = sys.argv[2]
    f = io.open(nazwa_pliku, mode='w+',encoding='utf-8')
    f.write(table2)
    f.close()
    

if __name__=="__main__":
    table = ""   
    table2= ""
    fname=sys.argv[1]
    remove_nums=sys.argv[3].upper()=="T"
    remove_sym=sys.argv[4].upper()=="T"
    table_format=sys.argv[5].upper()=="T"
    to_upper=sys.argv[6].upper()=="T"
    print_file=sys.argv[7].upper()=="T"
    
    table = wczytaj(table,fname)

    if (remove_sym):
        table = usun_znaki(table,True)
    else:
        table = usun_znaki(table,False)

    if (remove_nums):
        table = usun_cyfry(table)

    if to_upper:
        table = table.upper()
    else:
        table = table.lower()

    if (table_format):
        table2 = przeksztalcenie(table,table2)
    else:
        table2=table

    zapis(table2,print_file)

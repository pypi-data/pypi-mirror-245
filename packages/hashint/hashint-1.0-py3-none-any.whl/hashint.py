import sys
__version__="1.0"
text="naame naraki"
carac=['.', '~', '7', ']', 'z', '3', 'B', 'f', ':', 'R', '_', '+', 'é', '2', ',', 'ù', 'E', 'J', '°', 'F', 'i', '5', 'e', 'S', 'G', 'à', 'T', 'k', 'l', '§', '"', '0', 'I', '{', 'A', '/', 'K', '!', 'g', 'o', '?', '#', 'C', 'n', 'è', 'w', '*', ')', 'ë', 'V', 'D', 'H', '6', ' ', '^', 'ê', '-', 'd', ';', 'c', 't', 'U', 'v', '1', 'µ', 'Q', '8', 'm', '$', 'u', 'q', '[', '9', 'X', 'ç', 'a', '£', 'p', '=', 'M', 'h', 'W', '4', 'r', 'P', 's', 'Y', '%', 'N', '}', '(', '@', ',', 'y', 'Z', '&', 'L', 'x', 'O', '\\', 'b', 'j']
carat=""
sys.set_int_max_str_digits(100000)
class HashError:
    pass
for i in range(len(carac)):
    carat=carat+carac[i]
def hash64(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+64)**64).endswith("0"):
                cara=str((carac.index(text[i])+64)**64)[::str((carac.index(text[i])+64)**64).index("0")]
            else:
                cara=str((carac.index(text[i])+64)**64)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash128(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+128)**128).endswith("0"):
                cara=str((carac.index(text[i])+128)**128)[::str((carac.index(text[i])+128)**128).index("0")]
            else:
                cara=str((carac.index(text[i])+128)**128)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash256(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+256)**256).endswith("0"):
                cara=str((carac.index(text[i])+256)**256)[::str((carac.index(text[i])+256)**256).index("0")]
            else:
                cara=str((carac.index(text[i])+256)**256)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash512(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+512)**512).endswith("0"):
                cara=str((carac.index(text[i])+512)**512)[::str((carac.index(text[i])+512)**512).index("0")]
            else:
                cara=str((carac.index(text[i])+512)**512)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash1024(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+1024)**1024).endswith("0"):
                cara=str((carac.index(text[i])+1024)**1024)[::str((carac.index(text[i])+1024)**1024).index("0")]
            else:
                cara=str((carac.index(text[i])+1024)**1024)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash2048(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+2048)**2048).endswith("0"):
                cara=str((carac.index(text[i])+2048)**2048)[::str((carac.index(text[i])+2048)**2048).index("0")]
            else:
                cara=str((carac.index(text[i])+2048)**2048)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash4096(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+4096)**4096).endswith("0"):
                cara=str((carac.index(text[i])+4096)**4096)[::str((carac.index(text[i])+4096)**4096).index("0")]
            else:
                cara=str((carac.index(text[i])+4096)**4096)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
def hash8192(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in carac:
            if str((carac.index(text[i])+8192)**8192).endswith("0"):
                cara=str((carac.index(text[i])+8192)**8192)[::str((carac.index(text[i])+8192)**8192).index("0")]
            else:
                cara=str((carac.index(text[i])+8192)**8192)
                newtext=newtext+cara
        else:
            raise HashError("'"+car+"' is not hashable")
    return newtext
if __name__=="__main__":
    netext=hash8192(text)
    texttxt=open("text.txt",'w')
    texttxt.write(netext)
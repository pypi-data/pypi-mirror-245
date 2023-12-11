import math
def squareRoot(num):
    term=math.sqrt(num/2)
    val=term
    term=term/3
    val+=term
    term=term/4
    val+=term
    term=term/34
    val-=term
    term=term/1154
    val-=term
    return val
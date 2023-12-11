import sys
import math
import itertools
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

varg={
        'क':1,
        'ख':2,
        'ग':3,
        'घ':4,
        'ङ':5,
        'च':6,
        'छ':7,
        'ज':8,
        'झ':9,
        'ञ':10,
        'ट':11,
        'ठ':12,
        'ड':13,
        'ढ':14,
        'ण':15,
        'त':16,
        'थ':17,
        'द':18,
        'ध':19,
        'न':20,
        'प':21,
        'फ':22,
        'ब':23,
        'भ':24,
        'म':25
    }
avarg={
        'य':3,
        'र':4,
        'ल':5,
        'व':6,
        'श':7,
        'ष':8,
        'स':9,
        'ह':10
    }
swar={
        "ा":{
            'varg':0,
            'avarg':1
        },
        'ि':{
            'varg':2,
            'avarg':3
        },
        'ु':{
            'varg':4,
            'avarg':5
        },
        'ृ':{
            'varg':6,
            'avarg':7
        },
        'ॄ':{
            'varg':8,
            'avarg':9
        },
        'ॆ':{
            'varg':10,
            'avarg':11
        },
        'े':{
            'varg':12,
            'avarg':13
        },
        'ो':{
            'varg':14,
            'avarg':15
        },
        'ौ':{
            'varg':16,
            'avarg':17
        }
}
def decode(sabd):
    i=0
    l=len(sabd)
    value=0
    while i < l :
        schwa=sabd[i]
        if(i!=l-1):
            # if half word 
            if(sabd[i+1]=='्'):
                matra=sabd[i+3]
                i=i+1
            elif(sabd[i+1] in swar):
                matra=sabd[i+1]
                i=i+1
            else:
                matra="ा"
        else:
            matra="ा"
        i=i+1
        type_of_schwa=""
        if(schwa in varg):
            scahwa_val=varg.get(schwa)
            type_of_schwa="varg"
        else:
            scahwa_val=avarg.get(schwa)
            type_of_schwa="avarg"
        value+=scahwa_val*math.pow(10,swar.get(matra).get(type_of_schwa))

    return int(value)
def encode(num):
    aksharList=[]
    posval=0
    while(num!=0):
        skipCnt=1
        fposval=posval
        d=num%10
        num=num//10
        # if number is less than 25 take two digits 
        prevd=num%10
        if posval%2==0:
            if(prevd*10+d<=25):
                d=prevd*10+d
                num=num//10
                skipCnt+=1
        else:
            if(d == 1 or d==2 ):
                d=d*10
                fposval=posval-1
        akshar=""
        # if digit is not zero then only akshar will be generated
        if(d!=0):
            # case varg as pos val is even 
            if(fposval%2==0):
                for key,val in varg.items():
                    if(val==d):
                        akshar+=key
                        break
                if(fposval!=0):
                    for matra,value in swar.items():
                        if value.get("varg")==fposval:
                            akshar+=matra
                            break
            # case avarg as pos val is odd 
            else:
                for key,val in avarg.items():
                    if(val==d):
                        akshar+=key
                        break
                if(fposval!=1):
                    for matra,value in swar.items():
                        if value.get("avarg")==fposval:
                            akshar+=matra
                            break
            if(akshar!=""):
                aksharList.append(akshar)
        posval=posval+skipCnt
    # As a number have multiple Aryabhatiya sabd generating all prmutation if words
    allSabdList=list(itertools.permutations(aksharList))
    # Converting tuple of akshars to string type 
    for i in range(len(allSabdList)):
        sabd=""
        for akshar in allSabdList[i]:
            sabd+=akshar
        allSabdList[i]=sabd
        
    return ({
        "sabd":allSabdList[0],
        "length":len(allSabdList),
        "allSabd":allSabdList
    })


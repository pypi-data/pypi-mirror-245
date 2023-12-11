def squareRoot(x):
    x_s=str(x)
    l=len(x_s)
    il=l%2
    if il==0:
        il=2
    x1=int(x_s[0:il])
    p=il
    for i in range(1,11):
        if(x1<i*i):
            a=i-1
            break
    res=a
    x2=x1-a*a
    if p==l:
        return res
    # while all digits are not completed
    while True:
        x3=x2*10+int(x_s[p])
        b=x3//(2*a)+1
        # while not subtraction is not positive 
        while True:
            b=b-1
            x4=x3-(2*a*b)
            x5=x4*10+int(x_s[p+1])
            x6=x5-b*b
            if(x4>=0 and x6>=0):
                res=res*10+b
                p=p+2
                break
        if(p<l-1):
            a=res
            x2=x6
        else:
            break
    return res


def cubeRoot(x,showSteps=0):
    x_s=str(x)
    l=len(x_s)
    il=l%3
    if il==0:
        il=3
    x1=int(x_s[0:il])
    if(showSteps):
        print(f"X1 = {x1}")
    p=il
    for i in range(1,11):
        if(x1<i*i*i):
            a=i-1
            break
    if(showSteps):
        print(f"a = {a}")
    res=a
    x2=x1-a*a*a
    if(showSteps):
        print(f"X2 = {x2}")
    if p==l:
        return res
    # while all digits are not completed
    while True:
        x3=x2*10+int(x_s[p])
        if(showSteps):
            print(f"X3 = {x3}")
        b=x3//(3*a*a)+1
        # while not subtraction is not positive 
        while True:
            b=b-1
            if(showSteps):
                print(f"b = {b}")
            x4=x3-(3*a*a*b)
            if(showSteps):
                print(f"X4 = {x4}")
            x5=x4*10+int(x_s[p+1])
            if(showSteps):
                print(f"X5 = {x5}")
            x6=x5-3*a*b*b
            if(showSteps):
                print(f"X6 = {x6}")
            x7=x6*10+int(x_s[p+2])
            if(showSteps):
                print(f"X7 = {x7}")
            x8=x7-b*b*b
            if(showSteps):
                print(f"X8 = {x8}")
            if(x4>=0 and x6>=0 and x8>=0):
                res=res*10+b
                p=p+3
                break
        if(p<l-1):
            a=res
            x2=x8
        else:
            break
    return res

# print(f"Result = {squareRoot(200)}")
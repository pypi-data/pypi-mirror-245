def result(y):
    for i in y:
        y=i.upper()
    match(y):
        case "F":
            return "Your Relationship is Friends"
        case "L":
            return "Your Relationship is Loving"
        case "A":
            return "Your Relationship is Affection"
        case "M":
            return "Your Relationship is Marriage"
        case "E":
            return "Your Relationship is Enemy"
        case "S":
            return "Your Relationship is Siblings"     
        case _:
            pass
def flames(main,times,time,i):
    try:
        temp=''
        lenght=len(main)
        if i==lenght:i=i-1
        while i<len(main):
            if len(main)==1:break
            if times==time:
                if len(main)-1==i:temp="y"
                del main[i]
                if temp=="y":i=0
                flames(main,times,time=1,i=i)
            if i==len(main)-1:flames(main,times,time=time+1,i=0)
            i+=1;time+=1
        if len(main) == 1:return main        
    except:
        print("Error")
def times(i):
    a=flames(main=['f','l','a','m','e','s'],times=i,time=1,i=0)
    return result(a)
if __name__=='__main__':
    print(times(2))

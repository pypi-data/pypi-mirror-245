try:
    def split(temp1,temp2):
        for i in temp1:
            if i in temp2:
                temp1.remove(i)
                temp2.remove(i)
                split(temp1,temp2)
        return len(temp1)+len(temp2)
    def setnames(n1,n2):
        k=0
        temp1=[]
        temp2=[]
        n1=n1.lower()
        n2=n2.lower()
        for i in n1:
            if i==' ':
                continue
            else:
                temp1+=i
        for i in n2:
            if i==' ':
                continue
            else:
                temp2+=i
        if len(n1)>len(n2) or len(n1)==len(n2):
            n=split(temp1,temp2)
        else:
            n=split(temp2,temp1)
        return n
    if __name__=='__main__':
        a=input("Enter The Name 1:")
        b=input("Enter The Name 2:")
        print(setnames(a,b))
except Exception as Argument:
    print("The Error Argument:"+Argument)
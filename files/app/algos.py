def gct(a,b):
    if len(a) == 0 or len(b) == 0:
        return []
    # if py>3.0, nonlocal is better
    class markit:
        a=[0]
        minlen=2
    markit.a=[0]*len(a)
    markit.minlen=2
    #output char index
    out=[]
    # To find the max length substr (index)
    # apos is the position of a[0] in origin string
    def maxsub(a,b,apos=0,lennow=0):
        if (len(a) == 0 or len(b) == 0):
            return []
        if (a[0]==b[0] and markit.a[apos]!=1 ):
            return [apos]+maxsub(a[1:],b[1:],apos+1,lennow=lennow+1)
        elif (a[0]!=b[0] and lennow>0):
            return []
        return max(maxsub(a, b[1:],apos), maxsub(a[1:], b,apos+1), key=len)
    while True:
        findmax=maxsub(a,b,0,0)
        if (len(findmax)<markit.minlen):
            break
        else:
            for i in findmax:
                markit.a[i]=1
            out+=findmax
    return [ a[i] for i in out]

def lccs(ord1,ord2):
    tempval = 0
    patt=list()
    for i in ord1:
        for ind,j in enumerate(ord2[tempval:]):
            if i==j:
                patt.append(i)
                tempval = ind
    return patt

if __name__ == '__main__':
    a=['2','3','1','4','6','8','5','9']
    b=['3','8','9','4','10','11','5']
    print ( lccs(a,b) )

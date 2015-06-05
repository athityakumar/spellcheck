from collections import defaultdict
import re
import sys

insd=defaultdict(int)
detd=defaultdict(int)
subd=defaultdict(int)
trsd=defaultdict(int)

insdg=defaultdict(int)
detdg=defaultdict(int)
subdg=defaultdict(int)
trsdg=defaultdict(int)

def min(a, b,c=1000):
    if a<b:
        if a<c:
            return (a,'ins')
        else:
            return (c,'sub')
    else:
        if b<c:
            return (b,'det')
        else:
            return (c,'sub')
def minof2(a,b):
    if a>b:
        return b
    else:
        return a

def editdist(str1, str2):
    m=len(str1)+1
    n=len(str2)+1
    table=[]
    for i in range(m):
        table.append([])
        for j in range(n):
            table[i].append(0)
    for i in range(m):
        table[i][0]=(i,'ins')
    for j in range(n):
        table[0][j]=(j,'det')
    for i in range(1,m):
        for j in range(1,n):
            if(str1[i-1]==str2[j-1]):
                cost=0
            else:
                cost=1
            ins=table[i-1][j][0]+1
            det=table[i][j-1][0]+1
            sub=table[i-1][j-1][0]+cost
            table[i][j]=min(ins,det,sub)
            if(i>1 and j>1 and str1[i-1]==str2[j-2] and str1[i-2]==str2[j-1]):
                table[i][j]=(minof2(table[i][j][0],table[i-2][j-2][0]+cost),'trs')
    i=m-1
    j=n-1
    code=0
    while(i!=0 or j!=0):
        if table[i][j][1]=='det':
            if(j>1):
                #print 'del - ', str2[j-1],'after',str2[j-2]
                detd[str2[j-2]+str2[j-1]]+=1
            if j==1:
                #print 'del -', str2[j-1],'at the beginning'
                detd[str2[j-1]]+=1
            j=j-1
        if table[i][j][1]=='ins':
            if i>1:
                #print 'ins - ', str1[i-1],'after',str1[i-2]
                insd[str1[i-2]+str1[i-1]]+=1
            if i==1:
                #print 'ins-', str1[i-1], 'at the beginning'
                insd[str1[i-1]]+=1
            i=i-1
        if table[i][j][1]=='sub':
            if(str2[j-1]!=str1[i-1]):
                #print 'sub - ', str2[j-1],'with',str1[i-1]
                subd[str2[j-1]+str1[i-1]]+=1
            i=i-1
            j=j-1
        if table[i][j][1]=='trs':
            if(str2[j-1]!=str2[j-2]):
                #print 'transpose - ', str2[j-1],'with',str2[j-2]
                trsd[str2[j-1]+str2[j-2]]+=1
            i=i-2
            j=j-2
    return table[m-1][n-1][0]

def editdistg(str1, str2):
    m=len(str1)+1
    n=len(str2)+1
    table=[]
    for i in range(m):
        table.append([])
        for j in range(n):
            table[i].append(0)
    for i in range(m):
        table[i][0]=(i,'ins')
    for j in range(n):
        table[0][j]=(j,'det')
    for i in range(1,m):
        for j in range(1,n):
            if(str1[i-1]==str2[j-1]):
                cost=0
            else:
                cost=1
            ins=table[i-1][j][0]+1
            det=table[i][j-1][0]+1
            sub=table[i-1][j-1][0]+cost
            table[i][j]=min(ins,det,sub)
            if(i>1 and j>1 and str1[i-1]==str2[j-2] and str1[i-2]==str2[j-1]):
                table[i][j]=(minof2(table[i][j][0],table[i-2][j-2][0]+cost),'trs')
    i=m-1
    j=n-1
    code=0
    while(i!=0 or j!=0):
        if table[i][j][1]=='det':
            if(j>1):
                #print 'del - ', str2[j-1],'after',str2[j-2]
                detdg[str2[j-2]+str2[j-1]]+=1
                return('det',str2[j-2]+str2[j-1])
                
            if j==1:
                #print 'del -', str2[j-1],'at the beginning'
                detdg[str2[j-1]]+=1
                return('det',str2[j-1])

            j=j-1
        if table[i][j][1]=='ins':
            if i>1:
                #print 'ins - ', str1[i-1],'after',str1[i-2]
                insdg[str1[i-2]+str1[i-1]]+=1
                return('ins',str1[i-2]+str1[i-1])
            if i==1:
                #print 'ins-', str1[i-1], 'at the beginning'
                insdg[str1[i-1]]+=1
                return('ins',str1[i-1])
            i=i-1
        if table[i][j][1]=='sub':
            if(str2[j-1]!=str1[i-1]):
                #print 'sub - ', str2[j-1],'with',str1[i-1]
                subdg[str2[j-1]+str1[i-1]]+=1
                return('sub',str2[j-1]+str1[i-1])
            i=i-1
            j=j-1
        if table[i][j][1]=='trs':
            if(str2[j-1]!=str2[j-2]):
                #print 'transpose - ', str2[j-1],'with',str2[j-2]
                trsdg[str2[j-1]+str2[j-2]]+=1
                return('trs',str2[j-1]+str2[j-2])
            i=i-2
            j=j-2
    return ('match','wut')

wf=open('american-english')
corp=wf.read()
NWORDS=[w.lower() for w in re.findall('\w+',corp)]

bf=open('big.txt')
corpa=bf.read()
corpus=re.findall('\w+',corpa)

alphabet='abcdefghijklmnopqrstuvwxyz'
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

f=open('mispled.txt')
error=f.readlines()
letter='a'

for i in error:
    words=re.findall('\w+\s?\w+',i)
    if words[0][0]!=letter:
        letter=words[0][0]
    for k in range(1, len(words)):
        editdist(words[k],words[0])

sentence='start'
while(sentence[0]!='exit'):
    print '\nEnter new sentence : '
    sentence=raw_input().split()
    for wrongword in sentence:
        word=wrongword
        #if wrongword in NWORDS:
         #   print wrongword,
          #  continue
        oneedits=edits1(wrongword)
        simiwords=known(oneedits)
        maxprob=0
        for i in simiwords:
            count=corpus.count(i)+NWORDS.count(i)
            editis=editdistg(i, wrongword)
            if editis[0]=='ins':
                multi=insd[editis[1]]
            if editis[0]=='det':
                multi=detd[editis[1]]
            if editis[0]=='sub':
                multi=subd[editis[1]]
            if editis[0]=='trs':
                multi=insd[editis[1]]
            if editis[0]=='match':
                multi=1000
            curr_prob=(count)*(multi+1)
            if maxprob<curr_prob:
                maxprob=curr_prob
                word=i
        print word,
    

    

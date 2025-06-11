from machine import Machine
import numpy as np
import time
import sys
import random
from math import log2, pow

#Machine parameters
k = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])
qber = int(sys.argv[4])
update_ind = int(sys.argv[5])
update_ind_eve = int(sys.argv[6]) if update_ind in [3, 4] else update_ind

#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk', 'dynamic_row', 'dynamic_matrix', 'random_eve']
update_rule = update_rules[update_ind]
update_rule_eve = update_rules[update_ind_eve]

def getBit(y, x):
    return str((x>>y)&1)

def tobin(x, count=8):
    shift = range(count-1, -1, -1)
    bits = map(lambda y: getBit(y, x), shift)
    return "".join(bits)

def toint(x):
    i=len(x)
    flag=1
    val=0
    for c in x:
        if(i==len(x)): 
            flag=1
        q=int(pow(-1,flag)*int(c)*pow(2,i-1))
        val+=int(pow(-1,flag)*int(c)*pow(2,i-1))
        flag=0
        i-=1
    return val

def ensure_qber(W, qber):
    bitsize=int(log2(l))+2
    keysize=k*n*bitsize
    keyY=""
    num_err = int(keysize*0.01*qber)
    Y =np.random.randint(0, 1, [k, n])
    for i in range(0,len(W)):
        for j in range(0,len(W[0])):
            keyY+=tobin(W[i][j],bitsize)
    indices=[]
    while num_err>0:
        ind=int(random.uniform(0, keysize-1))
        if ind in indices: continue
        rep = "0" if keyY[ind] == "1" else "1"
        mod=ind%bitsize
        str_ind = ind - (mod)
        num=keyY[str_ind:str_ind+bitsize]
        num=num[:mod]+rep+num[mod+1:]
        number=toint(num) # moze mapka dozwolonych wartosci
        if number >= -l and number <= l:
            num_err-=1
            keyY=keyY[:ind]+rep+keyY[ind+1:]
            indices.append(ind)
    for i in range(0,len(W)):
        for j in range(0,len(W[0])):
            if(len(keyY)>0):
                s=keyY[:bitsize]
                keyY=keyY[bitsize:]
                Y[i][j]=toint(s)
    print("qber " + str(qber) + "%")
    return Y

#Random number generator
def rand(x):
	return np.random.randint(-x, x + 1, [k, n])

#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
print("Creating machines : k=" + str(k) + ", n=" + str(n) + ", l=" + str(l))
if update_rule != update_rule_eve:
     print("Using " + update_rule + " update rule. Eve is using " + update_rule_eve + " update rule. ")
else:
     print("Using " + update_rule + " update rule.")

W=rand(l)
if(qber>0):
	Y=ensure_qber(W, qber)
else:
	Y=rand(l)
Z=rand(l)
Alice = Machine(k, n, l, W)
Bob = Machine(k, n, l, Y)
Eve = Machine(k, n, l, Z)


#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2):
	return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * l +1))

#Synchronize weights

sync = False # Flag to check if weights are sync
nb_updates = 0 # Update counter
nb_eve_updates = 0 # To count the number of times eve updated
start_time = time.time() # Start time
sync_history = [] # to store the sync score after every update

while(not sync):

	X = rand(l) # Create random vector of dimensions [k, n]

	tauA = Alice(X) # Get output from Alice
	tauB = Bob(X) # Get output from Bob
	tauE = Eve(X) # Get output from Eve

	Alice.update(tauB, update_rule) # Update Alice with Bob's output
	Bob.update(tauA, update_rule) # Update Bob with Alice's output

	#Eve would update only if tauA = tauB = tauE
	if tauA == tauB == tauE:
		Eve.update(tauA, update_rule_eve)
		nb_eve_updates += 1

	nb_updates += 1

	score = 100 * sync_score(Alice, Bob) # Calculate the synchronization of the 2 machines

	sync_history.append(score) # Add sync score to history, so that we can plot a graph later.

	#sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates) + " / Eve's updates = " + str(nb_eve_updates)) 
	if score == 100: # If synchronization score is 100%, set sync flag = True
		sync = True

end_time = time.time()
time_taken = end_time - start_time # Calculate time taken

#Print results
print ('\nMachines have been synchronized.')
print ('Time taken = ' + str(time_taken)+ " seconds.")
print ('Updates = ' + str(nb_updates) + ".")

#See if Eve got what she wanted:
eve_score = 100 * sync_score(Alice, Eve)

print("Eve's machine is only " + str(eve_score) + " % " + "synced with Alice's and Bob's and she did " + str(nb_eve_updates) + " updates.") 

# #Plot graph 
# import matplotlib.pyplot as mpl
# mpl.plot(sync_history)
# mpl.show()

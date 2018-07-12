# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 18:37:05 2018

@author: Gaurav
"""
import scipy as sci
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors


###############################################################################
#########################DEFINITION OF STARTING PARAMETERS#####################
#Define number of rows in the space (200 is too slow, 100 is decently fast)
rows=100
#Define number of columns in the space
cols=100
#Define number of infected people initially per 100 healthy people
ratio=40
#Define the max time for which the simulation will run
time=100
timespan=sci.arange(0,time,1) ##Do not touch this
#Define probabilities for death, infection and cure
die=0.008
infect=0.25
cure=0.1
vaccine=0.05
vaccinetime=time/2

#########################FUNCTION SPACE########################################
def AddPeople(space,ratio):
    init1=sci.zeros(100)
    init2=sci.ones(100)
    init3=sci.append(init1,init2)
    init4=sci.array([100]*ratio)
    initialize=sci.append(init3,init4)
    
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            space[i,j]=sci.random.choice(initialize)
        
    return space

def AddCustomPeople(space,ratio):
    init1=sci.zeros(100)
    init2=sci.ones(100)
    factor=4 #increase factor to increase infected people in smaller region
    ratio=int(factor*ratio)
    init3=sci.array([100]*ratio)
    temp1=sci.append(init1,init2)
    init_healthy=sci.append(temp1,sci.zeros(ratio))
    temp2=sci.append(init1,init3)
    init_infected=sci.append(temp2,sci.zeros(100))
    
    #add healthy people
    for i in range(30,70):
        for j in range(30,70):
            space[i,j]=sci.random.choice(init_infected)
            
#    for i in range(41,rows-1):
#        for j in range(1,cols-1):
#            space[i,j]=sci.random.choice(init_healthy)
            
    #add infected people
    for i in range(1,rows-1):
        for j in range(1,20):
            space[i,j]=sci.random.choice(init_healthy)
    
    for i in range(1,rows-1):
        for j in range(80,99):
            space[i,j]=sci.random.choice(init_healthy)
    
    for i in range(1,20):
        for j in range(20,80):
            space[i,j]=sci.random.choice(init_healthy)
    
    for i in range(80,99):
        for j in range(20,80):
            space[i,j]=sci.random.choice(init_healthy)        
            
    return space

def AddVaxSpace(space):
    [rows,cols]=space.shape
    vaxspace=sci.zeros((rows,cols))
    return vaxspace

def ImposeBorders(space):
    space[0,:]=0.1
    space[-1,:]=0.1
    space[:,0]=0.1
    space[:,-1]=0.1
    #Add case specific conditions here

    #End case specific conditions
    return space
     
def AddDirections(space):
    [rows,cols]=space.shape
    direction=sci.random.choice(range(8),(rows,cols))
    return direction

def CheckProbability(prob):
    proboutofthousand=int(prob*1000)
    poss1=sci.ones(proboutofthousand)
    poss2=sci.zeros(1000-proboutofthousand)
    possibilities=sci.append(poss1,poss2)
    verdict=sci.random.choice(possibilities)
    if(verdict==1):
        return True
    else:
        return False
    
def Move(prevspace,direction,timestep):
    space=sci.copy(prevspace)
    check=sci.zeros((space.shape[0],space.shape[1])) #zero indicates not moved
    [rows,cols]=space.shape
    rem=timestep%4
    if(rem==0):
        irange=range(1,rows-1)
        jrange=range(1,cols-1)
    if(rem==1):
        irange=range(1,rows-1)
        jrange=reversed(range(1,cols-1))
    if(rem==2):
        irange=reversed(range(1,rows-1))
        jrange=range(1,cols-1)
    else:
        irange=reversed(range(1,rows-1))
        jrange=reversed(range(1,cols-1))
    for i in irange:
        for j in jrange:
            direct=direction[i,j]
            if((space[i,j]==1 or space[i,j]==100) and check[i,j]==0):
                count=0
                shift=sci.random.choice([1,-1])
                while(space[i,j]!=0):
                    count+=1
                    if(direct==0 and space[i-1,j]==0):
                        space[i-1,j],space[i,j]=space[i,j],space[i-1,j]
                        check[i-1,j]=1
                    elif(direct==1 and space[i-1,j+1]==0):
                        space[i-1,j+1],space[i,j]=space[i,j],space[i-1,j+1]
                        check[i-1,j+1]=1
                    elif(direct==2 and space[i,j+1]==0):
                        space[i,j+1],space[i,j]=space[i,j],space[i,j+1]
                        check[i,j+1]=1
                    elif(direct==3 and space[i+1,j+1]==0):
                        space[i+1,j+1],space[i,j]=space[i,j],space[i+1,j+1]
                        check[i+1,j+1]=1
                    elif(direct==4 and space[i+1,j]==0):
                        space[i+1,j],space[i,j]=space[i,j],space[i+1,j]
                        check[i+1,j]=1
                    elif(direct==5 and space[i+1,j-1]==0):
                        space[i+1,j-1],space[i,j]=space[i,j],space[i+1,j-1]
                        check[i+1,j-1]=1
                    elif(direct==6 and space[i,j-1]==0):
                        space[i,j-1],space[i,j]=space[i,j],space[i,j-1]
                        check[i,j-1]=1
                    elif(direct==7 and space[i-1,j-1]==0):
                        space[i-1,j-1],space[i,j]=space[i,j],space[i-1,j-1]
                        check[i-1,j-1]
                    else:
                        direct+=shift
                        if(direct>7):
                           direct=0
                        elif(direct<0):
                            direct=7
                            
                    if(count>7):
                        break
                    
    return space

def CountNeighbours(space):
    [rows,cols]=space.shape
    N=sci.zeros((rows,cols))
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            N[i,j]=space[i+1,j]+space[i+1,j+1]+space[i,j+1]+space[i-1,j+1]+space[i-1,j]+space[i-1,j-1]+space[i,j-1]+space[i+1,j-1]
    N=sci.floor(N)
    return N

def CheckInfected(neighbours):
    N=neighbours
    infected=N//100
    healthy=N%100
    return [infected,healthy]

def Vaccinate(vaxspace,vaccine):
    [rows,cols]=vaxspace.shape
    vaxcount=0
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            if(vaxspace[i,j]==0):
                vaxresult=CheckProbability(vaccine)
                if(vaxresult==True):
                    vaxspace[i,j]=1
                    vaxcount+=1
    return [vaxspace,vaxcount]       

def CheckHealth(prevspace,neighbours,vaxspace,die,cure,infect,vaxflag):
    space=sci.copy(prevspace)
    [rows,cols]=space.shape
    [infected,healthy]=CheckInfected(neighbours)
    deathcount=0
    healcount=0

    for i in range(1,rows-1):
        for j in range(1,cols-1):
            if(space[i,j]==1 or space[i,j]==100):
                contagion=None
                death=None
                heal=None
                if(infected[i,j]>0 and space[i,j]!=100 and vaxspace[i,j]!=1):
                    contagion=CheckProbability(infect)
                    
                if(space[i,j]!=1 and space[i,j]==100):
                    death=CheckProbability(die)
                    heal=CheckProbability(cure)
                
                if(contagion==True):
                    space[i,j]=100
                
                if(death==True and heal==False):
                    space[i,j]=0
                    deathcount+=1
                
                if(death==False and heal==True):
                    space[i,j]=1
                    healcount+=1
                
                if(death==True and cure==True):
                    if(sci.random.choice([0,1])==0):
                        space[i,j]=0
                        deathcount+=1
                    else:
                        space[i,j]=1
                        healcount+=1
                
    return [space,deathcount,healcount]               
            
###########################ADJUST THE SPACE####################################
barren=sci.zeros((rows,cols))
aimless=sci.zeros((rows,cols))
vax=AddVaxSpace(barren)
populace=AddPeople(barren,ratio) #Change to AddCustomPeople for specifc geometries
populace=ImposeBorders(populace)
nextpop=populace
resultpop=sci.zeros((rows,cols,time+1))
resultpop[:,:,0]=nextpop

infectedpeople=sci.zeros(time)
healthypeople=sci.zeros(time)
deadpeople=sci.zeros(time)
healedpeople=sci.zeros(time)
vaccinatedpeople=sci.zeros(time)

vaxflag=False
vaxcount=0
for i in range(time):
    if(i%5==0):  #change directions every 5 timesteps
        direction=AddDirections(aimless)
    if(i>vaccinetime):
        vaxflag=True
        [vax,vaxcount]=Vaccinate(vax,vaccine)
        
    neighbours=CountNeighbours(nextpop)
    [alivepop,deadpop,healedpop]=CheckHealth(nextpop,neighbours,vax,die,cure,infect,vaxflag)
    infectedpeople[i]=sci.sum(len(nextpop[nextpop==100]))
    healthypeople[i]=sci.sum(len(nextpop[nextpop==1]))
    deadpeople[i]=deadpop
    healedpeople[i]=healedpop
    vaccinatedpeople[i]=vaxcount
    nextpop=Move(alivepop,direction,i)  
    resultpop[:,:,i+1]=nextpop
    print(time-i)

#Setting final arrays
alivepeople=healthypeople+infectedpeople
totaldead=sum(deadpeople)
totalhealed=sum(healedpeople)
totalvaccinated=sum(vaccinatedpeople)
percentdead=totaldead*100/alivepeople[0]

############################PLOTTING THE RESULTS###############################
#Plotting
#Results plot
fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(111)
ax.plot(timespan,healthypeople,"g",label="Healthy")
ax.plot(timespan,deadpeople,"k",label="Dead")
ax.plot(timespan,infectedpeople,"r",label="Infected")
ax.plot(timespan,healedpeople,"b",label="Healed")
ax.plot(timespan,alivepeople,"c",label="Alive")
ax.plot(timespan,vaccinatedpeople,"m",label="Vaccinated")
ax.legend(loc="upper right")
ax.text(time/2,alivepeople[0]-(alivepeople[0]/6),f"Initial population={alivepeople[0]}\nFinal Population={alivepeople[-1]}\nTotal Dead={totaldead}\nTotal Healed={totalhealed}\nInitial %infected={infectedpeople[0]*100/alivepeople[0]:.2f}\nFinal %Dead={percentdead:.2f}\nTotal Vaccinated={totalvaccinated}")
ax.set_xlim([0,time])
ax.set_ylim([0,alivepeople[0]])
fig.canvas.draw()    
    
#Population plot
cmap = colors.ListedColormap(['black','cyan', 'green','red'])
bounds=[0,0.09,0.99,1.1,100]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig1=plt.figure(figsize=(10,10))
ax1=fig1.add_subplot(111)
img1=ax1.imshow(populace,cmap=cmap,norm=norm)
ax1.set_title("Initial Populace")
ax1.text(len(populace)/2,len(populace)/50,"Green=Healthy,Red=Infected",bbox={'facecolor': 'white', 'pad': 10})

fig2=plt.figure(figsize=(10,10))
ax2=fig2.add_subplot(111)
img2=ax2.imshow(nextpop,cmap=cmap,norm=norm)
ax2.set_title("Final populace")
ax2.text(len(nextpop)/2,len(nextpop)/50,"Green=Healthy,Red=Infected",bbox={'facecolor': 'white', 'pad': 10})

fig1.canvas.draw()
fig2.canvas.draw()

imresult=[]
fig4=plt.figure(figsize=(10,10))
for i in range(time+1):
    im=plt.imshow(resultpop[:,:,i],cmap=cmap,norm=norm,animated=True)
    imresult.append([im])
    
ani = animation.ArtistAnimation(fig4,imresult, interval=80, blit=True)
    

    
###############################################################################



#####preberemo datoteki v tabeli
fileNBA0910=open('/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0910.txt','r')
fileNBA0809=open('/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0809.txt','r')
import csv
readerNBA0910=csv.reader(fileNBA0910)
readerNBA0809=csv.reader(fileNBA0809)
header=next(readerNBA0910)
next(readerNBA0809) #preskoci zaglavje
tableNBA0910=[row for row in readerNBA0910]
tableNBA0809=[row for row in readerNBA0809]
fileNBA0910.close()
fileNBA0809.close()
#####zdruzimo tabeli v eno
tableNBA0809.extend(tableNBA0910)
tekme=tableNBA0809
#####pretvori podatkovne tipe v tabeli
from datetime import date, datetime, timedelta
for row in tekme:
    row[0]=datetime.strptime(row[0],'%Y%m%d')
    for i in range(3,len(row)):
        row[i]=int(row[i])  
#####zagotovi, da je tabela sortirana po datumu!   
      
#####construct new attributes
for i in range(0,len(tekme)):
    #####prepare variables
    homeTeamName=tekme[i][2]
    awayTeamName=tekme[i][1]
    priorGames=tekme[:i]#for tekma[i]: construct only from data prior game
    homeTeamGames=[]#subset of matches where tekme[i]'s home team played     
    awayTeamGames=[]#subset of matches where tekme[i]'s away team played 
    homeVSawayGames=[]#subset of all matches where tekme[i]'s away team played versus home team
    for row in priorGames:
        if row[1]==homeTeamName or row[2]==homeTeamName:
            homeTeamGames.append(row)
        if row[1]==awayTeamName or row[2]==awayTeamName:
            awayTeamGames.append(row)    
        if (row[1]==awayTeamName and row[2]==homeTeamName) or (row[2]==awayTeamName and row[1]==homeTeamName):      
            homeVSawayGames.append(row)     
    homeTeamGamesWon=[] #subset of matches, where tekme[i]'s home time won
    homeTeamGamesLost=[] #subset of matches, where tekme[i]'s home time lost
    for row in homeTeamGames:
        if (row[1]==homeTeamName and row[28]>row[29]) or (row[2]==homeTeamName and row[29]>row[28]):
            homeTeamGamesWon.append(row)
        else:
            homeTeamGamesLost.append(row)                          
    awayTeamGamesWon=[] #subset of matches, where tekme[i]'s away time won
    awayTeamGamesLost=[] #subset of matches, where tekme[i]'s away time lost
    for row in awayTeamGames:
        if (row[1]==awayTeamName and row[28]>row[29]) or (row[2]==awayTeamName and row[29]>row[28]):
            awayTeamGamesWon.append(row)
        else:
            awayTeamGamesLost.append(row)
    homeVSawayGames_homeWin=[]
    homeVSawayGames_awayWin=[]
    for row in homeVSawayGames:
        if (row[1]==awayTeamName and row[28]>row[29]) or (row[2]==awayTeamName and row[29]>row[28]):
            homeVSawayGames_awayWin.append(row)
        else:
            homeVSawayGames_homeWin.append(row)            
    homeTeamNumberOfGamesWon=len(homeTeamGamesWon) #number of games won by home team
    homeTeamNumberOfGamesLost=len(homeTeamGamesLost) #number of games lost by home team
    awayTeamNumberOfGamesWon=len(awayTeamGamesWon) #number of games won by away team
    awayTeamNumberOfGamesLost=len(awayTeamGamesLost) #number of games lost by away team
    homeTeamWin=(True if tekme[i][29]>tekme[i][28] else False) #true if home team achieved more points than away team during this game
    finalPointsScoreDifferential=abs(tekme[i][29]-tekme[i][28]) #difference between home and away team scores after this match
    homeVSaway_winRatio=(len(homeVSawayGames_homeWin)-len(homeVSawayGames_awayWin))/(len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)) if len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)>0 else 0 #difference between past home team wins over away team; normaliset to [-1,1] interval 
    #####construct & append new atributes HERE
    tekme[i].append(finalPointsScoreDifferential)
    tekme[i].append(homeTeamWin)
    tekme[i].append(awayTeamNumberOfGamesWon)
    tekme[i].append(awayTeamNumberOfGamesLost)
    tekme[i].append(homeTeamNumberOfGamesWon)
    tekme[i].append(homeTeamNumberOfGamesLost)
    tekme[i].append(homeVSaway_winRatio)
       
#####update table header
header.append('finalScoreDifferential')
header.append('HOME_win') 
header.append('AWAY_GamesWon')
header.append('AWAY_GamesLost')
header.append('HOME_GamesWon')
header.append('HOME_GamesLost')
header.append('HOMEvsAWAY_winRatio')



#test print table
print(header)
for row in tekme:
    print(row)
#####output table to file
f=open('/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv','w')
f.write(','.join(header)+'\n')
for row in tekme:
    tmp=[str(x) for x in row]
    f.write(','.join(tmp)+'\n')
f.close()
        
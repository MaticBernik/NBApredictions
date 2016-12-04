"""""""""""""""""""""""""""""""""    IMPORT FILES     """""""""""""""""""""""""""""""""""""""
import csv
from datetime import date, datetime, timedelta

"""""""""""""""""""""""""""""""""    PATH VARIABLES     """""""""""""""""""""""""""""""""""""""
#matic
#file0809 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0809.txt'
#file0910 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0910.txt'
#output_file = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv'

#robert
file0809 = 'C:/Users/Robert/Documents/GitHub/NBApredictions/nba0809.txt'
file0910 = 'C:/Users/Robert/Documents/GitHub/NBApredictions/nba0910.txt'
output_file = 'C:/Users/Robert/Documents/GitHub/NBApredictions/games.csv'

"""""""""""""""""""""""""""""""""     read file    """""""""""""""""""""""""""""""""""""""
#####preberemo datoteki v tabeli
#open files
fileNBA0809=open(file0809,'r')
fileNBA0910=open(file0910,'r')

#read files
readerNBA0910=csv.reader(fileNBA0910)
readerNBA0809=csv.reader(fileNBA0809)
#store file into a list
header=next(readerNBA0910)
next(readerNBA0809) #preskoci zaglavje
tableNBA0910=[row for row in readerNBA0910]
tableNBA0809=[row for row in readerNBA0809]
#close file
fileNBA0910.close()
fileNBA0809.close()

"""""""""""""""""""""""""""""""""    prepare file content     """""""""""""""""""""""""""""""""""""""

#####zdruzimo tabeli v eno
tableNBA0809.extend(tableNBA0910)
tekme=tableNBA0809

#####pretvori podatkovne tipe v tabeli
for row in tekme:
    row[0]=datetime.strptime(row[0],'%Y%m%d').date()
    for i in range(3,len(row)):
        row[i]=int(row[i])  
#####zagotovi, da je tabela sortirana po datumu!
tekme = sorted(tekme, key = lambda row: row[0])

"""""""""""""""""""""""""""""""""    attribute manipulation     """""""""""""""""""""""""""""""""""""""
#####construct new attributes
for i in range(0,len(tekme)):
    #####prepare variables
    homeTeamName=tekme[i][2]    #selected home team
    awayTeamName=tekme[i][1]    #selected away team
    priorGames=tekme[:i]        #for tekma[i]: construct only from data prior game
    homeTeamGames=[]            #subset of matches where tekme[i]'s home team played
    awayTeamGames=[]            #subset of matches where tekme[i]'s away team played
    homeVSawayGames=[]          #subset of all matches where tekme[i]'s away team played versus home team
    for row in priorGames:
        if row[1]==homeTeamName or row[2]==homeTeamName:
            homeTeamGames.append(row)
        if row[1]==awayTeamName or row[2]==awayTeamName:
            awayTeamGames.append(row)    
        if (row[1]==awayTeamName and row[2]==homeTeamName) or (row[2]==awayTeamName and row[1]==homeTeamName):      
            homeVSawayGames.append(row)     

    homeTeamGamesWon=[]         #subset of matches, where tekme[i]'s home team won
    homeTeamGamesLost=[]        #subset of matches, where tekme[i]'s home team lost
    for row in homeTeamGames:
        if (row[1]==homeTeamName and row[28]>row[29]) or (row[2]==homeTeamName and row[29]>row[28]):
            homeTeamGamesWon.append(row)
        else:
            homeTeamGamesLost.append(row)                          
    awayTeamGamesWon=[]         #subset of matches, where tekme[i]'s away team won
    awayTeamGamesLost=[]        #subset of matches, where tekme[i]'s away team lost
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

    homeTeamNumberOfGamesWon=len(homeTeamGamesWon)                  #number of games won by home team
    homeTeamNumberOfGamesLost=len(homeTeamGamesLost)                #number of games lost by home team
    awayTeamNumberOfGamesWon=len(awayTeamGamesWon)                  #number of games won by away team
    awayTeamNumberOfGamesLost=len(awayTeamGamesLost)                #number of games lost by away team
    homeTeamWin=(True if tekme[i][29]>tekme[i][28] else False)      #true if home team achieved more points than away team during this game
    finalPointsScoreDifferential=abs(tekme[i][29]-tekme[i][28])     #difference between home and away team scores after this match
    homeVSaway_winRatio=(len(homeVSawayGames_homeWin)-len(homeVSawayGames_awayWin))/(len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)) if len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)>0 else 0 #difference between past home team wins over away team; normaliset to [-1,1] interval 

    #####construct & append new atributes HERE
    tekme[i].append(finalPointsScoreDifferential)
    tekme[i].append(homeTeamWin)
    tekme[i].append(awayTeamNumberOfGamesWon)
    tekme[i].append(awayTeamNumberOfGamesLost)
    tekme[i].append(homeTeamNumberOfGamesWon)
    tekme[i].append(homeTeamNumberOfGamesLost)
    tekme[i].append(round(homeVSaway_winRatio,2))


    #####append new statistical data for throws
    # 2 points throws
    away2pointAttempt = tekme[i][3]
    away2pointMade = tekme[i][4]
    home2pointAttempt = tekme[i][12]
    home2pointMade = tekme[i][13]
    # 3 points throw
    away3pointAttempt = tekme[i][5]
    away3pointMade = tekme[i][6]
    home3pointAttempt = tekme[i][14]
    home3pointMade = tekme[i][15]
    # free throws
    awayFtAttempts = tekme[i][7]
    awayFtMade = tekme[i][8]
    homeFtAttempts = tekme[i][16]
    homeFtMade = tekme[i][17]
    # 2 and 3 points made // all as in game, FT don't belong here.. just a boost
    awayAllAttempt = away2pointAttempt + away3pointAttempt
    awayAllMade = away2pointMade + away3pointMade
    homeAllAttempt = home2pointAttempt + home3pointAttempt
    homeAllMade = home2pointMade + home3pointMade

    #statistics
    away2percent = round(away2pointMade / away2pointAttempt, 2)
    away3percent = round(away3pointMade / away3pointAttempt, 2)
    awayFtpercent = round(awayFtMade / awayFtAttempts, 2)
    awayAllpercent = round((away2pointMade + away3pointMade) / (away2pointAttempt + away3pointAttempt), 2)
    home2percent = round(home2pointMade / home2pointAttempt, 2)
    home3percent = round(home3pointMade / home3pointAttempt, 2)
    homeFtpercent = round(homeFtMade / homeFtAttempts, 2)
    homeAllpercent = round((home2pointMade + home3pointMade) / (home2pointAttempt + home3pointAttempt), 2)

    #append throw statistics
    tekme[i].append(away2percent)
    tekme[i].append(away3percent)
    tekme[i].append(awayFtpercent)
    tekme[i].append(awayAllpercent)
    tekme[i].append(home2percent)
    tekme[i].append(home3percent)
    tekme[i].append(homeFtpercent)
    tekme[i].append(homeAllpercent)

    #tekme[i].append()

       
#####update table header
header.append('finalScoreDifferential')
header.append('HOME_win') 
header.append('AWAY_GamesWon')
header.append('AWAY_GamesLost')
header.append('HOME_GamesWon')
header.append('HOME_GamesLost')
header.append('HOMEvsAWAY_winRatio')
header.append('AWAY TEAM 2P %')
header.append('AWAY TEAM 3P %')
header.append('AWAY TEAM FT %')
header.append('AWAY TEAM ALL throws %')
header.append('HOME TEAM 2P %')
header.append('HOME TEAM 3P %')
header.append('HOME TEAM FT %')
header.append('HOME TEAM ALL throws %')


#test print table
print(header)
for row in tekme:
    print(row)

#####output table to file
f=open(output_file,'w')
f.write(','.join(header)+'\n')
for row in tekme:
    tmp=[str(x) for x in row]
    f.write(','.join(tmp)+'\n')
f.close()

"""""""""""""""""""""""""""""""""         """""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""   script ends      """""""""""""""""""""""""""""""""""""""

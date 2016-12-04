"""""""""""""""""""""""""""""""""    IMPORT FILES     """""""""""""""""""""""""""""""""""""""
import csv
from datetime import date, datetime, timedelta

"""""""""""""""""""""""""""""""""    PATH VARIABLES     """""""""""""""""""""""""""""""""""""""
#matic
file0809 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0809.txt'
file0910 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0910.txt'
output_file = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv'

#robert
#file0809 = 'C:/Users/Robert/Documents/GitHub/NBApredictions/nba0809.txt'
#file0910 = 'C:/Users/Robert/Documents/GitHub/NBApredictions/nba0910.txt'
#output_file = 'C:/Users/Robert/Documents/GitHub/NBApredictions/games.csv'

"""""""""""""""""""""""""""""""""     read file    """""""""""""""""""""""""""""""""""""""
#####preberemo datoteki v tabeli
#open files
fileNBA0809=open(file0809,'r')
fileNBA0910=open(file0910,'r')

#read files
readerNBA0910=csv.reader(fileNBA0910)
readerNBA0809=csv.reader(fileNBA0809)
#store file into a list
headerTekme=next(readerNBA0910)
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
#####create new table - where row represents a game described only by attributes derived from previous matches
games=[]
headerGames=["AWAY_NAME","HOME_NAME"]

#####construct new attributes
for i in range(0,len(tekme)):
    #####prepare variables
    homeTeamName=tekme[i][2]    #selected home team
    awayTeamName=tekme[i][1]    #selected away team
    priorGames=tekme[:i]        #for tekma[i]: construct only from data prior game
    homeTeamGames=[]            #subset of matches where tekme[i]'s home team played
    awayTeamGames=[]            #subset of matches where tekme[i]'s away team played
    homeVSawayGames=[]          #subset of all matches where tekme[i]'s away team played versus home team
    homeTeamWinningStreakLength=0 #maximum number of consecutive games home team won in a row
    awayTeamWinningStreakLength=0 #maximum number of consecutive games away team won in a row
    homeTeamLosingStreakLength=0 #maximum number of consecutive games home team lost in a row
    awayTeamLosingStreakLength=0 #maximum number of consecutive games away team lost in a row
    
    for row in priorGames:
        if row[1]==homeTeamName or row[2]==homeTeamName:
            homeTeamGames.append(row)
        if row[1]==awayTeamName or row[2]==awayTeamName:
            awayTeamGames.append(row)    
        if (row[1]==awayTeamName and row[2]==homeTeamName) or (row[2]==awayTeamName and row[1]==homeTeamName):      
            homeVSawayGames.append(row)     
    homeTeamAsHome=[] #subset of matches, where tekme[i]'s home team played as home team
    homeTeamAsAway=[] #subset of matches, where tekme[i]'s home team played as away team
    awayTeamAsHome=[] #subset of matches, where tekme[i]'s away team played as home team
    awayTeamAsAway=[] #subset of matches, where tekme[i]'s away team played as away team
    homeTeamAsHome_Win=[]
    homeTeamAsHome_Losts=[]
    homeTeamAsAway_Win=[]
    homeTeamAsAway_Losts=[]
    awayTeamAsHome_Win=[]
    awayTeamAsHome_Losts=[]
    awayTeamAsAway_Win=[]
    awayTeamAsAway_Losts=[]
    
    for row in homeTeamGames:
        if row[1]==homeTeamName:
            homeTeamAsAway.append(row)
            if row[28]>row[29]:
                homeTeamAsAway_Win.append(row)
            else:
                homeTeamAsAway_Losts.append(row)    
        else:
            homeTeamAsHome.append(row)
            if row[29]>row[28]:
                homeTeamAsHome_Win.append(row)
            else:
                homeTeamAsHome_Losts.append(row)  
    for row in awayTeamGames:
        if row[1]==awayTeamName:
            awayTeamAsAway.append(row)
            if row[28]>row[29]:
                awayTeamAsAway_Win.append(row)
            else:
                awayTeamAsAway_Losts.append(row)
        else:
            awayTeamAsHome.append(row)            
            if row[29]>row[28]:
                awayTeamAsHome_Win.append(row)
            else:
                awayTeamAsHome_Losts.append(row)
    homeTeamGamesWon=[]         #subset of matches, where tekme[i]'s home team won
    homeTeamGamesLost=[]        #subset of matches, where tekme[i]'s home team lost
    homeWinStreak=0
    homeLoseStreak=0
    awayWinStreak=0
    awayLoseStreak=0
    homeNonconsecutiveWins=0
    homeNonconsecutiveLosts=0
    awayNonconsecutiveWins=0
    awayNonconsecutiveLosts=0
    for row in homeTeamGames:
        if (row[1]==homeTeamName and row[28]>row[29]) or (row[2]==homeTeamName and row[29]>row[28]):
            homeTeamGamesWon.append(row) 
            if homeLoseStreak==1:
                homeNonconsecutiveLosts+=1               
            homeWinStreak+=1
            homeLoseStreak=0
            if homeWinStreak > homeTeamWinningStreakLength:
                homeTeamWinningStreakLength=homeWinStreak
        else:
            homeTeamGamesLost.append(row)
            if homeWinStreak==1:
                homeNonconsecutiveWins+=1  
            homeWinStreak=0
            homeLoseStreak+=1
            if homeLoseStreak > homeTeamLosingStreakLength:
                homeTeamLosingStreakLength=homeLoseStreak                        
    awayTeamGamesWon=[]         #subset of matches, where tekme[i]'s away team won
    awayTeamGamesLost=[]        #subset of matches, where tekme[i]'s away team lost
    for row in awayTeamGames:
        if (row[1]==awayTeamName and row[28]>row[29]) or (row[2]==awayTeamName and row[29]>row[28]):
            awayTeamGamesWon.append(row)
            if awayLoseStreak==1:
                awayNonconsecutiveLosts+=1
            awayWinStreak+=1
            awayLoseStreak=0
            if awayWinStreak > awayTeamWinningStreakLength:
                awayTeamWinningStreakLength=awayWinStreak
        else:
            awayTeamGamesLost.append(row)
            if awayWinStreak==1:
                awayNonconsecutiveLosts+=1
            awayWinStreak=0
            awayLoseStreak+=1
            if awayLoseStreak > awayTeamLosingStreakLength:
                awayTeamLosingStreakLength=awayLoseStreak
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
    homeTeam_homeTurfAdvantage=(len(homeTeamAsHome_Win)-len(homeTeamAsHome_Losts))/len(homeTeamAsHome) if len(homeTeamAsHome)>0 else 0 #value aproaches +1 as team was more successful playing as home team and approaches -1 if it was actually playing worse
    awayTeam_homeTurfAdvantage=(len(awayTeamAsHome_Win)-len(awayTeamAsHome_Losts))/len(awayTeamAsHome) if len(awayTeamAsHome)>0 else 0#value aproaches +1 as team was more successful playing as home team and approaches -1 if it was actually playing worse
    '''#####append new statistical data for throws TO INPUT TABLE'''
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
    
    gamesRow=[tekme[i][1],tekme[i][2]]
    '''#####construct & append new atributes TO NEW TABLE'''    
    gamesRow.append(awayTeamNumberOfGamesWon)
    gamesRow.append(awayTeamNumberOfGamesLost)
    gamesRow.append(homeTeamNumberOfGamesWon)
    gamesRow.append(homeTeamNumberOfGamesLost)
    gamesRow.append(round(homeVSaway_winRatio,2))
    gamesRow.append(awayTeamWinningStreakLength)
    gamesRow.append(awayTeamLosingStreakLength)
    gamesRow.append(homeTeamWinningStreakLength)
    gamesRow.append(homeTeamLosingStreakLength)
    gamesRow.append(awayTeam_homeTurfAdvantage)
    gamesRow.append(homeTeam_homeTurfAdvantage)
    gamesRow.append(finalPointsScoreDifferential) #TARGET VARIABLE FOR REGRESSION
    gamesRow.append(awayNonconsecutiveWins)
    gamesRow.append(awayNonconsecutiveLosts)
    gamesRow.append(homeNonconsecutiveWins)
    gamesRow.append(homeNonconsecutiveLosts)
    gamesRow.append(homeTeamWin) #TARGET VARIABLE FOR CLASSIFICATION
    
    ##### apend new row to game table
    games.append(gamesRow)


       
#####update table header
##### for input table headerTekme
headerTekme.append('AWAY TEAM 2P %')         
headerTekme.append('AWAY TEAM 3P %')
headerTekme.append('AWAY TEAM FT %')
headerTekme.append('AWAY TEAM ALL throws %')
headerTekme.append('HOME TEAM 2P %')
headerTekme.append('HOME TEAM 3P %')
headerTekme.append('HOME TEAM FT %')
headerTekme.append('HOME TEAM ALL throws %')

#for output table headerGames
headerGames.append('AWAY_GamesWon')
headerGames.append('AWAY_GamesLost')
headerGames.append('HOME_GamesWon')
headerGames.append('HOME_GamesLost')
headerGames.append('HOMEvsAWAY_winRatio')
headerGames.append('AWAY_longestWinStreak')
headerGames.append('AWAY_longestLoseStreak')
headerGames.append('HOME_longestWinStreak')
headerGames.append('HOME_longestLoseStreak')
headerGames.append('HOME_homeTurfAdvantage')
headerGames.append('AWAY_homeTurfAdvantage')
headerGames.append('AWAY_nonconsecutiveWins')
headerGames.append('AWAY_nonconsecutiveLosts')
headerGames.append('HOME_nonconsecutiveWins')
headerGames.append('HOME_nonconsecutiveLosts')
headerGames.append('finalScoreDifferential') #TARGET VARIABLE FOR REGRESSION
headerGames.append('HOME_win') #TARGET VARIABLE FOR CLASSIFICATION


#test print table
print(headerGames)
for row in games:
    print(row)

#####output table to file
f=open(output_file,'w')
f.write(','.join(headerGames)+'\n')
for row in games:
    tmp=[str(x) for x in row]
    f.write(','.join(tmp)+'\n')
f.close()

"""""""""""""""""""""""""""""""""         """""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""   script ends      """""""""""""""""""""""""""""""""""""""

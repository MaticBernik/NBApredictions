"""""""""""""""""""""""""""""""""    IMPORT FILES     """""""""""""""""""""""""""""""""""""""
import csv
from datetime import date, datetime, timedelta
from math import floor
"""""""""""""""""""""""""""""""""    PATH VARIABLES     """""""""""""""""""""""""""""""""""""""
#matic
# file0809 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0809.txt'
# file0910 = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/nba0910.txt'
# output_file = '/home/matic/Dropbox/Inteligentni Sistemi/Assigment1/games.csv'

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

    #print("home team games ", len(homeTeamGames), len(homeTeamGames[0]) if len(homeTeamGames) > 0 else 0," ",  homeTeamGames)
    #print(len(headerTekme))


    for row in homeTeamGames:
        if row[1]==homeTeamName:
            homeTeamAsAway.append(row)
            if row[29]>row[30]:
                homeTeamAsAway_Win.append(row)
            else:
                homeTeamAsAway_Losts.append(row)    
        else:
            homeTeamAsHome.append(row)
            if row[30]>row[29]:
                homeTeamAsHome_Win.append(row)
            else:
                homeTeamAsHome_Losts.append(row)  
    for row in awayTeamGames:
        if row[1]==awayTeamName:
            awayTeamAsAway.append(row)
            if row[29]>row[30]:
                awayTeamAsAway_Win.append(row)
            else:
                awayTeamAsAway_Losts.append(row)
        else:
            awayTeamAsHome.append(row)            
            if row[30]>row[29]:
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
        if (row[1]==homeTeamName and row[29]>row[30]) or (row[2]==homeTeamName and row[30]>row[29]):
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
        if (row[1]==awayTeamName and row[29]>row[30]) or (row[2]==awayTeamName and row[30]>row[29]):
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
        if (row[1]==awayTeamName and row[29]>row[30]) or (row[2]==awayTeamName and row[30]>row[29]):
            homeVSawayGames_awayWin.append(row)
        else:
            homeVSawayGames_homeWin.append(row)

    homeTeamNumberOfGamesWon=len(homeTeamGamesWon)                  #number of games won by home team
    homeTeamNumberOfGamesLost=len(homeTeamGamesLost)                #number of games lost by home team
    awayTeamNumberOfGamesWon=len(awayTeamGamesWon)                  #number of games won by away team
    awayTeamNumberOfGamesLost=len(awayTeamGamesLost)                #number of games lost by away team
    homeTeamWin=(True if tekme[i][30]>tekme[i][29] else False)      #true if home team achieved more points than away team during this game
    finalPointsScoreDifferential= tekme[i][30]-tekme[i][29]     #difference between home and away team scores after this match
    homeVSaway_winRatio=(len(homeVSawayGames_homeWin)-len(homeVSawayGames_awayWin))/(len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)) if len(homeVSawayGames_homeWin)+len(homeVSawayGames_awayWin)>0 else 0 #difference between past home team wins over away team; normaliset to [-1,1] interval 
    homeTeam_homeTurfAdvantage=round((len(homeTeamAsHome_Win)-len(homeTeamAsHome_Losts))/len(homeTeamAsHome), 4) if len(homeTeamAsHome)>0 else 0 #value aproaches +1 as team was more successful playing as home team and approaches -1 if it was actually playing worse
    awayTeam_homeTurfAdvantage=round((len(awayTeamAsHome_Win)-len(awayTeamAsHome_Losts))/len(awayTeamAsHome), 4) if len(awayTeamAsHome)>0 else 0#value aproaches +1 as team was more successful playing as home team and approaches -1 if it was actually playing worse



    """ APPEND EXPECTED GAME STATS, BASED OF PREVIOUS GAMES """
    away2percent = 0
    away3percent = 0
    awayFtpercent = 0
    awayAllpercent = 0

    home2percent = 0
    home3percent = 0
    homeFtpercent = 0
    homeAllpercent = 0

    # team fouls
    homeTeamFouls = 0
    awayTeamFouls = 0

    # turn overs and rebounds
    homeTeamTO = 0
    homeTeamOR = 0
    homeTeamDR = 0

    awayTeamTO = 0
    awayTeamOR = 0
    awayTeamDR = 0

    #due to + / - diff sign, this is only calculated for home team advantage / fallback
    q1_diff = 0
    q2_diff = 0
    q3_diff = 0
    q4_diff = 0

    if len(homeTeamGames) > 0:
        for row in homeTeamGames:
            home2pointAttempt = row[12]
            home2pointMade = row[13]
            home3pointAttempt = row[14]
            home3pointMade = row[15]
            homeFtAttempts = row[16]
            homeFtMade = row[17]
            homeAllAttempt = home2pointAttempt + home3pointAttempt
            homeAllMade = home2pointMade + home3pointMade

            home2percent += home2pointMade / home2pointAttempt
            home3percent += home3pointMade / home3pointAttempt
            homeFtpercent += homeFtMade / homeFtAttempts
            homeAllpercent += (home2pointMade + home3pointMade) / (home2pointAttempt + home3pointAttempt)
                            # away team ft attempts
            homeTeamFouls += (floor(row[7]/2))

            homeTeamTO += row[18]
            homeTeamOR += row[19]
            homeTeamDR += row[20]

            q1_diff += row[22] - row[21]
            q2_diff += row[24] - row[23]
            q3_diff += row[26] - row[25]
            q4_diff += row[28] - row[27]

        home2percent /= len(homeTeamGames)
        home3percent /= len(homeTeamGames)
        homeFtpercent /= len(homeTeamGames)
        homeAllpercent /= len(homeTeamGames)

        homeTeamFouls /= len(homeTeamGames)

        homeTeamTO /= len(homeTeamGames)
        homeTeamOR /= len(homeTeamGames)
        homeTeamDR /= len(homeTeamGames)

        q1_diff /= len(homeTeamGames)
        q2_diff /= len(homeTeamGames)
        q3_diff /= len(homeTeamGames)
        q4_diff /= len(homeTeamGames)

    #end if homeTeams

    if len(awayTeamGames) > 0:
        for row in awayTeamGames:
            away2pointAttempt = row[12]
            away2pointMade = row[13]
            away3pointAttempt = row[14]
            away3pointMade = row[15]
            awayFtAttempts = row[16]
            awayFtMade = row[17]
            awayAllAttempt = away2pointAttempt + away3pointAttempt
            awayAllMade = away2pointMade + away3pointMade

            away2percent += away2pointMade / away2pointAttempt
            away3percent += away3pointMade / away3pointAttempt
            awayFtpercent += awayFtMade / awayFtAttempts
            awayAllpercent += (away2pointMade + away3pointMade) / (away2pointAttempt + away3pointAttempt)

                            # home team ft attempts
            awayTeamFouls += (floor(row[16] / 2))

            awayTeamTO += row[9]
            awayTeamOR += row[10]
            awayTeamDR += row[11]

        away2percent /= len(awayTeamGames)
        away3percent /= len(awayTeamGames)
        awayFtpercent /= len(awayTeamGames)
        awayAllpercent /= len(awayTeamGames)

        awayTeamFouls /= len(awayTeamGames)

        awayTeamTO /= len(awayTeamGames)
        awayTeamOR /= len(awayTeamGames)
        awayTeamDR /= len(awayTeamGames)


    gamesRow=[tekme[i][1],tekme[i][2]]
    '''#####construct & append new atributes TO NEW TABLE'''    
    gamesRow.append(awayTeamNumberOfGamesWon)
    gamesRow.append(awayTeamNumberOfGamesLost)
    gamesRow.append(homeTeamNumberOfGamesWon)
    gamesRow.append(homeTeamNumberOfGamesLost)
    gamesRow.append(round(homeVSaway_winRatio,4))
    gamesRow.append(awayTeamWinningStreakLength)
    gamesRow.append(awayTeamLosingStreakLength)
    gamesRow.append(homeTeamWinningStreakLength)
    gamesRow.append(homeTeamLosingStreakLength)
    gamesRow.append(awayTeam_homeTurfAdvantage)
    gamesRow.append(homeTeam_homeTurfAdvantage)
    gamesRow.append(awayNonconsecutiveWins)
    gamesRow.append(awayNonconsecutiveLosts)
    gamesRow.append(homeNonconsecutiveWins)
    gamesRow.append(homeNonconsecutiveLosts)

    gamesRow.append(round(away2percent, 2))
    gamesRow.append(round(away3percent, 2))
    gamesRow.append(round(awayFtpercent, 2))
    gamesRow.append(round(awayAllpercent, 2))
    gamesRow.append(round(home2percent, 2))
    gamesRow.append(round(home3percent, 2))
    gamesRow.append(round(homeFtpercent, 2))
    gamesRow.append(round(homeAllpercent, 2))

    gamesRow.append(floor(awayTeamFouls))
    gamesRow.append(floor(homeTeamFouls))

    gamesRow.append(floor(awayTeamTO))
    gamesRow.append(floor(awayTeamOR))
    gamesRow.append(floor(awayTeamDR))
    gamesRow.append(floor(homeTeamTO))
    gamesRow.append(floor(homeTeamOR))
    gamesRow.append(floor(homeTeamDR))

    gamesRow.append(floor(q1_diff))
    gamesRow.append(floor(q2_diff))
    gamesRow.append(floor(q3_diff))
    gamesRow.append(floor(q4_diff))

    gamesRow.append(floor(finalPointsScoreDifferential)) # TARGET VARIABLE FOR REGRESSION
    gamesRow.append(floor(homeTeamWin)) #TARGET VARIABLE FOR CLASSIFICATION

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
headerGames.append('AWAY_homeTurfAdvantage')
headerGames.append('HOME_homeTurfAdvantage')
headerGames.append('AWAY_nonconsecutiveWins')
headerGames.append('AWAY_nonconsecutiveLosts')
headerGames.append('HOME_nonconsecutiveWins')
headerGames.append('HOME_nonconsecutiveLosts')

headerGames.append('AWAY TEAM 2P %')
headerGames.append('AWAY TEAM 3P %')
headerGames.append('AWAY TEAM FT %')
headerGames.append('AWAY TEAM ALL throws %')
headerGames.append('HOME TEAM 2P %')
headerGames.append('HOME TEAM 3P %')
headerGames.append('HOME TEAM FT %')
headerGames.append('HOME TEAM ALL throws %')

headerGames.append('AWAY TEAM FOULS')
headerGames.append('HOME TEAM FOULS')

headerGames.append('AWAY TEAM TO')
headerGames.append('AWAY TEAM OR')
headerGames.append('AWAY TEAM DR')
headerGames.append('HOME TEAM TO')
headerGames.append('HOME TEAM OR')
headerGames.append('HOME TEAM DR')

headerGames.append('Q1 lead HOME vs AWAY')
headerGames.append('Q2 lead HOME vs AWAY')
headerGames.append('Q3 lead HOME vs AWAY')
headerGames.append('Q4 lead HOME vs AWAY')

headerGames.append('finalScoreDifferential') #TARGET VARIABLE FOR REGRESSION
headerGames.append('HOME_win') #TARGET VARIABLE FOR CLASSIFICATION
#target variables

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

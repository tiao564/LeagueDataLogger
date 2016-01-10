#! /usr/bin/env python
from __future__ import print_function
import sqlite3
from decimal import *

###################
#Connect to the db#
###################
conn = sqlite3.connect('Champs.db')
################################
#cursor create, global variable#
################################
cursor = conn.cursor()

def tableCreate():
    cursor.execute("CREATE TABLE matchupData(adTeam TEXT, supTEAM TEXT, adENEMY TEXT, supENEMY TEXT, win INT, loss INT, totalGames INT)")

def dataEntry():
    #########################################
    #Get info to intert/ append to the table#
    #########################################

    ###############
    #Ask for input#
    ###############
    print ("Input the bottom lane match up: ")
    print ("Your team:")
    adTEAM = raw_input("Your teams ADC: \n>>")
    supTEAM = raw_input("Your teams Support: \n>>")
    print ("Enemy team: ")
    adENEMY = raw_input("Enemy teams ADC: \n>>")
    supENEMY = raw_input("Enemy teams Support: \n>>")
    win_loss = raw_input("Was the game a win or loss for YOUR team: \n>>")

    #########################
    #standardize inputs     #
    # This is to make sure  #
    # no double entries     #
    # accidentally occur    #
    #########################
    adTEAM = adTEAM.lower()
    supTEAM = supTEAM.lower()
    adENEMY = adENEMY.lower()
    supENEMY = supENEMY.lower()
    win_loss = win_loss.lower()

    ##########################################################
    #We attempt to execute an update to win and total games  #
    # if it is found that nothing is updated we make a new   #
    # entry for the match up and set win/loss to 1 and       #
    # total games to 1.                                      #
    #   The long execute is just making sure that the        #
    # exact match up ad/sup team and ad/sup enemy            #
    # is the correct entry.                                  #
    ##########################################################
    #######
    # Win #
    #######
    if (win_loss=="win"):
        cursor.execute("UPDATE matchupData SET win=win+1 WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adENEMY, 'supE':supENEMY})
        cursor.execute("UPDATE matchupData SET totalGames=totalGames+1 WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adENEMY, 'supE':supENEMY})
        if(cursor.rowcount == 0):
            cursor.execute("INSERT INTO matchupData VALUES(?,?,?,?,?,?,?)", (adTEAM, supTEAM, adENEMY, supENEMY, 1, 0, 1))

    ########
    # loss #
    ########
    if (win_loss=="loss"):
        cursor.execute("UPDATE matchupData SET loss=loss+1 WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adENEMY, 'supE':supENEMY})
        cursor.execute("UPDATE matchupData SET totalGames=totalGames+1 WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adENEMY, 'supE':supENEMY})
        if(cursor.rowcount == 0):
            cursor.execute("INSERT INTO matchupData VALUES(?,?,?,?,?,?,?)", (adTEAM, supTEAM, adENEMY, supENEMY, 0, 1, 1))

    ################
    #Commit changes#
    ################
    conn.commit()       #YOU NEED THIS
    print ("\nChanges complete\n")


def fetchData():
    ######################################################################################################
    #SELECT (WIN/LOSS/GAMES) from matchupData WHERE adcTEAM=W and supTEAM=X and adcENEMY=Y and supENEMY=Z#
    ######################################################################################################
    print (" 1: ADC VS ADC\n 2: ADC VS SUP\n 3: ADC VS ADC SUP\n 4: SUP VS ADC\n 5: SUP VS SUP\n 6: SUP VS ADC SUP\n 7: ADC SUP VS ADC\n 8: ADC SUP VS SUP\n 9: ADC SUP VS ADC SUP\n all: Dump the whole table!")
    roll_select = raw_input("Pick what match up to get data on: ")
    roll_select = roll_select.lower()
    allWins = 0
    allGames = 0
    #######
    # all #
    #######
    if(roll_select == "all"):
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData"):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            print ("")
    ################
    # 1 ADC vs ADC #
    ################
    elif(roll_select == "1"):
        adTEAM = raw_input("ADC TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        adTEAM = adTEAM.lower()
        adENEMY = adENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and adENEMY= :adE", {'adT':adTEAM, 'adE':adENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

    ################
    # 2 ADC vs SUP #
    ################
    elif(roll_select == "2"):
        adTEAM= raw_input("ADC TEAM\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        adTEAM = adTEAM.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and supENEMY= :supE", {'adT':adTEAM, 'supE':supENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

    ######################
    # 3 ADC vs ADC + SUP #
    ######################
    elif(roll_select == "3"):
        print ('\n\n fuck \n\n')
        adTEAM = raw_input("ADC TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        adTEAM = adTEAM.lower()
        adENEMY = adENEMY.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'adE':adENEMY, 'supE':supENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

    ################
    # 4 SUP vs ADC #
    ################
    if(roll_select == "4"):
        supTEAM = raw_input("SUP TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        supTEAM = supTEAM.lower()
        adENEMY = adENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE supTEAM= :supT and adENEMY= :adE", {'supT':supTEAM, 'adE':adENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

    ################
    # 5 SUP VS SUP #
    ################
    if(roll_select == "5"):
        supTEAM = raw_input("SUP TEAM\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        supTEAM = supTEAM.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE supTEAM= :supT and adENEMY= :supE", {'supT':supTEAM, 'supE':supENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

    ######################
    # 6 SUP VS ADC + SUP #
    ######################
    if(roll_select == "6"):
        supTEAM = raw_input("SUP TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        supTEAM = supTEAM.lower()
        adENEMY = adENEMY.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'supT':supTEAM, 'adE':adTEAM, 'supE':supENEMY }):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)    

    ######################
    # 7 ADC + SUP VS ADC #
    ######################
    if(roll_select == "7"):
        adTEAM = raw_input("ADC TEAM\n>>")
        supTEAM = raw_input("SUP TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        adTEAM = adTEAM.lower()
        supTEAM = supTEAM.lower()
        adENEMY = adENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adTEAM }):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)    

    ######################
    # 8 ADC + SUP VS SUP #
    ######################
    if(roll_select == "8"):
        adTEAM = raw_input("ADC TEAM\n>>")
        supTEAM = raw_input("SUP TEAM\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        adTEAM = adTEAM.lower()
        supTEAM = supTEAM.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and supTEAM= :supT and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'supE':supENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)  

    ############################
    # 9 ADC + SUP VS ADC + SUP #
    ############################
    if(roll_select == "9"):
        adTEAM = raw_input("ADC TEAM\n>>")
        supTEAM = raw_input("SUP TEAM\n>>")
        adENEMY = raw_input("ADC ENEMY\n>>")
        supENEMY = raw_input("SUP ENEMY\n>>")
        adTEAM = adTEAM.lower()
        adENEMY = adENEMY.lower()
        supTEAM = supTEAM.lower()
        supENEMY = supENEMY.lower()
        print ("{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}{:>14}".format("AdTEAM","SupTeam", "AdENEMY", "SupENEMY", "Win", "Loss", "Total Games"))
        for row in cursor.execute("SELECT * FROM matchupData WHERE adTEAM= :adT and supTEAM= :supT and adENEMY= :adE and supENEMY= :supE", {'adT':adTEAM, 'supT':supTEAM, 'adE':adENEMY, 'supE':supENEMY}):
            for i in range(len(row)):
                print ("{:>14}".format(str(row[i]).replace('u\'','').replace('(','').replace(')','').replace('\'','')), end="")
            percent = (Decimal(row[4])/Decimal(row[6])*100)
            print ("\n{:>80}".format("win percentage: %.2f"%percent))
            allWins = allWins + row[4]
            allGames = allGames + row[6]
        totalPercent = Decimal(allWins)/Decimal(allGames)*100
        print("\nTotal win loss in the match up: %.2f"%totalPercent)

def main():
    #############################################
    #Selection of data:                         #
    # does user want to input data or quirie,   #
    # later on there should be automatic data   #
    # fetching from the riot API                #
    #############################################
    print ("\nWelcome to the League matchup data logger!\nDo you want to (fetch) data or (input) data? Enter exit to leave the program")
    select = ""
    try:
        tableCreate()
    except sqlite3.OperationalError:
        print("")
    while(select != "exit"):
        select = raw_input("\ninput, fetch or exit\n>>")    
        select = select.lower()
        if(select=="input"):
            dataEntry()
        elif(select=="fetch"):
            fetchData()
        elif(select != "exit"):
            print ("Input was not recognized, please type in \"input\" or \"fetch\"\n>>")
    print ("\nHave a good day!\n")

if __name__ == "__main__":
    main()

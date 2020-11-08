# This script is where I will test the parsing abilities of Python for a test rocket league replay

import json
import numpy as np 

replayFile = open('Data Analysis Tool\\Testing\\test.txt')
replayDict = json.load(replayFile)

replayFile.close()

def searchActor(actorName, replayFrame): #Searches for a specific actor in all of the replay (all of the frames)
    #Output a dictionary. Key is frame_update, value is the actor matrix
    actorDict = {}
    actorData = np.zeros((4,4))
    frameCount = 1
    for frame in replayFrame:
        actorUpdates = frame['ActorUpdates']
        for update in actorUpdates:
            check = actorName in update
            if check: # If the actor exists, get the values
                val = update[actorName] #Yet another dictionary containing all the physics values...I think
                current = val['Position']
                if current != None:
                    actorData[0,0:3] = np.array([current['X'],current['Y'],current['Z']])
                current = val['Rotation']
                if current != None:
                    actorData[1,:] = np.array([current['X'],current['Y'],current['Z'],current['W']])
                current = val['LinearVelocity']
                if current != None:
                    actorData[2,0:3] = np.array([current['X'],current['Y'],current['Z']])
                current = val['AngularVelocity']
                if current != None:
                    actorData[3,0:3] = np.array([current['X'],current['Y'],current['Z']])
                #Assign the matrix to the dictionary
                name = str(frameCount) + '_' + str(update['Id'])
                frameCount = frameCount + 1
                actorDict[name] = actorData
                actorData = np.zeros((4,4))

    return actorDict
#This looks at how many times all the keys show up through the frames. Allows me to see which ones are important
def keyFrequency(replayFrames): 
    keyDict = {}
    for frame in replayFrames:
        actorUpdates = frame['ActorUpdates']
        for update in actorUpdates:
            #Get a list of the key values
            updateKeys = list(update.keys()) # This is a list
            for key in range(len(updateKeys)-1):
                keyVal = updateKeys[key]
                if keyVal in keyDict.keys(): # If the key already exists
                    val = keyDict[keyVal]
                    val = val + 1
                    keyDict[keyVal] = val
                else:
                    keyDict[keyVal] = 1
    return keyDict 

def getPlayers(replayDict): 
    # This function returns the names and id's of each player in the match
    replayProperties = replayDict['Properties']
    replayPlayers = replayProperties['PlayerStats']
    playerDict = {};
    for player in replayPlayers: # Loop through the dictionary and get each players name
        playerName = player['Name']
        teamNumber = player['Team']
        if teamNumber == 0:
            teamColor = 'Blue'
        elif teamNumber == 1:
            teamColor = 'Orange'
        playerDict[playerName] = {'Team': teamColor}
    playerDict['playerNames'] = list(playerDict.keys())
    
    return playerDict

# Now look through each frame and try and find out whats in there. Especially the ActorUpdates section of each frame
def main():
    replayFrames = replayDict['Frames'] # This is a list now
    #keyDict = keyFrequency(replayFrames)
    actorDict = searchActor('TAGame.RBActor_TA:ReplicatedRBState',replayFrames)
    numFrames = len(replayFrames) # Number of frame dictionaries in the list
    player = 'itsAdoozy'
    key = ':PlayerReplicationInfo'
    frameCount = 1
    physKey = 'TAGame.RBActor_TA:ReplicatedRBState'
    for frame in replayFrames: # loop through each frame
        #frame = replayFrames[i]
        updates = frame['ActorUpdates']
        for update in updates: # Loop through each ActorUpdate and search for a player
            #update = updates[j]
            check = 'Engine.PlayerReplicationInfo:PlayerName' in update
            keys = update.keys()
            values = update.values()
            checkVal = player in values 
            if check:
                print(update['Engine.PlayerReplicationInfo:PlayerName'])
                print('ActorID: ' + str(update['Id']))
            if checkVal:
                print('Found itsAdoozy')
                #print('ActorID: ' + str(update['Id']))
                playerId = update['Id']
                for keyVal in keys: #Loop through values of the dictionary and search for replicationinfo
                    checkKey = keyVal.find(key) # Check if the Replicationinfo exists in this update
                    if (checkKey >= 0):
                        #print(keys)
                        repInfo = update[keyVal]
                        checkPlayer = playerId in update[keyVal].values()
                        if checkPlayer: # itsAdoozy is the player being referenced
                            print('Updating Physics Data...')
                            if physKey in update.keys():
                                carData = update[physKey] # All of the physics data in the frame
                                current = carData['Position']
                                posVec = [current['X'], current['Y'], current['Z']]
                                current = carData['Rotation']
                                rotVec = [current['X'],current['Y'],current['Z'],current['W']]
                                current = carData['LinearVelocity']
                                linVelVec = [current['X'],current['Y'],current['Z']]
                                current = carData['AngularVelocity']
                                angVelVec = [current['X'],current['Y'],current['Z']]
                        print(keyVal)
            checkDataKey = physKey in update.keys()
            if checkDataKey:
                print('Found Car Data')
        print(frameCount)
        frameCount = frameCount + 1
    usercheck = 0;
    #NOTES: Right now that Engine.PlayerReplicationInfo:PlayerName tag only appears once per player in all of the frames.
    #Need to find a way to search the VALUES of each dictionary entry for the player info
    #Look for any tag that has 'PlayerReplicationInfo' in it

main()
print('Complete!')

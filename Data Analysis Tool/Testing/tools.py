import numpy as np

class player:
    def __init__(self):
        # Initializes the player object with all the values being empty
        self.position    = np.empty((3,1))
        self.velocity    = np.empty((3,1))
        self.angVelocity = np.empty((3,1))
        self.rotation    = np.empty((4,1)) # Quaternion with scalar last???

        self.name        = "none"
        
def track(frames, objectName):
    # This tracks the object specified throughout all the frames and returns the position over time
    # Track object position, velocity, angular velocity, and rotation quaternion
    timeStamps = [0]*len(frames)
    for iFrame in frames:
        frame = frames[iFrame]
        time = frame['Time']
        timeStamps[iFrame] = time

        # Now loop through the actor updates
        updates = frame['ActorUpdates']
        for iUpdate in updates:
            # Look to see if the update is relevant
            if iUpdate['ClassName'] == objectName:
                stateValues = iUpdate['TAGame.RBActor_TA:ReplicatedRBState']
                position    = list(stateValues['Position'].values())
                velocity    = list(stateValues['LinearVelocity'].values())
                angVelocity = list(stateValues['AngularVelocity'].values())
                rotation    = list(stateValues['Rotation'].values())
            else:
                
    return objectFrames
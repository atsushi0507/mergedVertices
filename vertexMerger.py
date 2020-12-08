import os
import ROOT as r
from utils import *

inputFile = "inputList.txt"
#inputFile = "mcList.txt"
doUnblind = False

m_pion = 139.57 * 0.001 # [GeV]

regions = {0 : "inside_BP",
           1 : "inside_IBL",
           2 : "PIX",
           3 : "inside_SCT"}

def getRegion(rxy):
    region = -1
    if (rxy < 25.):
        region = 0
    if (rxy >= 25 and rxy < 38.):
        region = 1
    if (rxy >= 38. and rxy < 145.):
        region = 2
    if (rxy > 145. and rxy < 300.):
        region = 3
    return region

f = open(inputFile, "r")
nFile = 1
counter = 0
missReco = 0
while True:
    line = f.readline().strip()
    if line:
        #print(line)
        inFile = r.TFile(line, "READ")
        t = inFile.Get("trees_SRDV_")
        #entries = t.GetEntries()

        outputDir = "new"
        if (not os.path.isdir(outputDir)):
            os.makedirs(outputDir)
        outputFileName = "output_{}.root".format(nFile)
        outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")

        eventID = 0
        events = getEvents(t, eventID, doUnblind)

        for iEvent in range(len(events)):
            eventID = events[iEvent][0]
            dv = events[iEvent][1]
            dvtracks = events[iEvent][2]
            for idv in range(len(dv)):
                m_dv = dv[idv][3]
                dv_tracks, nTracks, nTracksSel = getDVtracks(dvtracks[idv])
                m_tracks = dv_tracks.M()
                diff = r.TMath.Abs(m_dv - m_tracks)
                #print("m_DV: {} [GeV], m_tracks: {} [GeV]".format(m_dv, m_tracks))
                counter += 1

                if (dv[idv][5] != nTracks):
                    print("Not matched the number of tracks, reco: {}, and counted: {}".format(dv[idv][5], nTracks))
                if (dv[idv][6] != nTracksSel):
                    print("Not matched the number of tracks, reco: {}, and counted: {}".format(dv[idv][6], nTracksSel))
                if (diff > m_dv * 0.001):
                    print("event: {} Different mass, m_DV: {}, and m_tracks: {}".format(eventID, m_dv, m_tracks))
                    print(dvtracks[idv])
                    region = getRegion(dv[idv][4])
                    print(region)
                    missReco += 1
                """
                if (nTracks == 4 and m_dv > 10.):
                    print(m_dv)
                    print(dvtracks[idv])
                """


        outputFile.Write()
        outputFile.Close()
        nFile += 1
    else:
        break


print("Total DV: {}, mismatch DV: {}".format(counter, missReco))

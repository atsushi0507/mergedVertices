import os
import ROOT as r
import random
import argparse
from utils import *

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFile", help="Specify input file list", default="inputList.txt")
p.add_argument("-o", "--outputDir", help="Specify output directory", default="kshort-method")

args = p.parse_args()

inputFile = args.inputFile

m_pion = 139.57 * 0.001
m_kshort = 497.11 * 0.001

regions = {0 : "inside_BP",
           1 : "inside_IBL",
           2 : "PIX",
           3 : "inside_SCT"}

f = open(inputFile, "r")
nFile = 1

def trackCleaning(dv, track):
    passCleaning = True
    if (dv[3] != track[5]):
        passCleaning = False
    if (track[6] == 1):
        passCleaning = False
    if (track[4]):
        if (track[8] < 2.):
            passCleaning = False
        if (dv[2] > 85.5 and track[8] < 3.):
            passCleaning = False
    if ((dv[2] < 23.5) and track[7] < 15.):
        passCleaning = False
    if ((dv[2] < 119.3) and track[7] < 10.):
        passCleaning = False
    if ((dv[2] > 119.3) and track[7] < 10. and track[4] == 0):
        passCleaning = False
    return passCleaning
    
while True:
    line = f.readline().strip()
    if line:
        print(line)
        inFile = r.TFile(line, "READ")
        tree = inFile.Get("trees_SRDV_")
        outputDir = args.outputDir
        if (not os.path.isdir(outputDir)):
            os.makedirs(outputDir)
        name = line.split("/")[-1] # output_{fileNumber}.root
        number = name.split("_")[1].split(".")[0]
        outputFileName = "output_{}.root".format(number)
        outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")

        events = []
        for entry in range(tree.GetEntries()):
            ientry = tree.LoadTree(entry)
            if ientry < 0:
                break
            nb = tree.GetEntry(ientry)
            if nb <= 0:
                continue
            vertex = []
            tracks = []

            for idv in range(tree.DV_n):
                if (not tree.DV_passFiducialCut[idv]):
                    continue
                if (not tree.DV_passDistCut[idv]):
                    continue
                """
                if (not tree.DV_passChiSqCut[idv]):
                    continue
                """
                if (tree.DV_chisqPerDoF[idv] > 50.):
                    continue
                
                if (not tree.DV_passMaterialVeto[idv]):
                    continue
                if (not tree.DV_passMaterialVeto_strict[idv]):
                    continue
                
                if (tree.DV_nTracks[idv] >= 5. and tree.DV_m[idv] > 10.):
                    continue
                if (tree.DV_nTracks[idv] == 4 and tree.DV_m[idv] > 20.):
                    continue
                
                vertex.append([tree.DV_m[idv], tree.DV_nTracks[idv], tree.DV_rxy[idv], tree.DV_index[idv]])
                track = []

                for itrack in range(len(tree.dvtrack_ptWrtDV)):
                    if ((tree.DV_index[idv] != tree.dvtrack_DVIndex[itrack])):
                        continue
                    if (tree.dvtrack_failedExtrapolation[itrack] == 1):
                        continue
                    if (tree.dvtrack_isAssociated[itrack]):
                        if (tree.dvtrack_ptWrtDV[itrack] < 2.):
                            continue
                        if ( (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[itrack] < 3.) ):
                            continue
                    # d0-significance
                    d0sig = r.TMath.Abs(tree.dvtrack_d0[itrack] / tree.dvtrack_errd0[itrack])
                    if ( (tree.DV_rxy[idv] < 23.5) and (d0sig < 15.) ):
                        continue
                    if ( (tree.DV_rxy[idv] < 119.3) and (d0sig < 10.) ):
                        continue
                    if ( (tree.DV_rxy[idv] > 119.3) and (d0sig < 10.) and tree.dvtrack_isAssociated[itrack] == 0):
                        continue
                    track.append([tree.dvtrack_ptWrtDV[itrack],
                                  tree.dvtrack_etaWrtDV[itrack],
                                  tree.dvtrack_phiWrtDV[itrack],
                                  m_pion,
                                  tree.dvtrack_isAssociated[itrack],
                                  tree.dvtrack_DVIndex[itrack],
                                  tree.dvtrack_failedExtrapolation[itrack],
                                  r.TMath.Abs(tree.dvtrack_d0[itrack]/tree.dvtrack_errd0[itrack]),
                                  tree.dvtrack_charge[itrack]])
                tracks.append(track)
            if (len(vertex) == 0):
                continue
            events.append([vertex, tracks])

        ### Histograms
        h_2track_mass = r.TH1D("2track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)
        h_3track_mass = r.TH1D("3track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)
        h_4track_mass = r.TH1D("4track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)

        h_ditrack_3track = r.TH1D("ditrack_3track", ";m_{DV} [GeV]", 500, 0., 1.)
        h_ditrack_4track = r.TH1D("ditrack_4track", ";m_{DV} [GeV]", 500, 0., 1.)

        h_mv_4track = r.TH1D("mv_4track", "m_{DV} [GeV]", 1000, 0., 100.)

        # Track combination
        for iEvent in range(len(events)):
            dv = events[iEvent][0]
            dvtracks = events[iEvent][1]
            for idv in range(len(dv)):
                m_dv = dv[idv][0]
                #nTracks = dv[idv][1]
                nTracks = len(dvtracks[idv])
                if (nTracks != dv[idv][1]):
                    print(nTracks, dv[idv][1])
                dv_tracks = r.TLorentzVector()
                #for itrack in dvtracks[idv]:
                """
                track = r.TLorentzVector()
                    track.SetPtEtaPhiM(itrack[0],
                                       itrack[1],
                                       itrack[2],
                                       itrack[3])
                    dv_tracks += track
                """
                if (nTracks == 2):
                    
                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    h_2track_mass.Fill((track1+track2).M())
                    
                if (nTracks == 3):
                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track3 = r.TLorentzVector()
                    
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    track3.SetPtEtaPhiM(dvtracks[idv][2][0], dvtracks[idv][2][1], dvtracks[idv][2][2], dvtracks[idv][2][3])
                    
                    h_3track_mass.Fill((track1+track2+track3).M())
                    
                    mass_12 = (track1 + track2).M()
                    mass_13 = (track1 + track3).M()
                    mass_23 = (track2 + track3).M()
                    
                    pass_1 = trackCleaning(dv[idv], dvtracks[idv][0])
                    pass_2 = trackCleaning(dv[idv], dvtracks[idv][1])
                    pass_3 = trackCleaning(dv[idv], dvtracks[idv][2])
                    # Check if any of the 3-tracks were associated to the DV,
                    isAsso_1 = dvtracks[idv][0][4]
                    isAsso_2 = dvtracks[idv][1][4]
                    isAsso_3 = dvtracks[idv][2][4]

                    if ((not isAsso_1) and (not isAsso_2) and (pass_3)):
                        h_ditrack_3track.Fill(mass_12)
                    if ((not isAsso_1) and (not isAsso_3) and (pass_2)):
                        h_ditrack_3track.Fill(mass_13)
                    if ((not isAsso_2) and (not isAsso_3) and (pass_1)):
                        h_ditrack_3track.Fill(mass_23)
                        
                if (nTracks == 4):
                    #h_4track_mass.Fill(m_dv)

                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track3 = r.TLorentzVector()
                    track4 = r.TLorentzVector()
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    track3.SetPtEtaPhiM(dvtracks[idv][2][0], dvtracks[idv][2][1], dvtracks[idv][2][2], dvtracks[idv][2][3])
                    track4.SetPtEtaPhiM(dvtracks[idv][3][0], dvtracks[idv][3][1], dvtracks[idv][3][2], dvtracks[idv][3][3])

                    h_4track_mass.Fill((track1+track2+track3+track4).M())

                    mass_12 = (track1 + track2).M()
                    mass_13 = (track1 + track3).M()
                    mass_14 = (track1 + track4).M()
                    mass_23 = (track2 + track3).M()
                    mass_24 = (track2 + track4).M()
                    mass_34 = (track3 + track4).M()

                    charge1 = dvtracks[idv][0][8]
                    charge2 = dvtracks[idv][1][8]
                    charge3 = dvtracks[idv][2][8]
                    charge4 = dvtracks[idv][3][8]

                    # DV pair combination
                    # Pair = [(1,2), (3,4)] or [(1,3), (2,4)] or [(1,4), (2,3)]
                    diff12 = r.TMath.Abs(m_kshort - mass_12)
                    diff13 = r.TMath.Abs(m_kshort - mass_13)
                    diff14 = r.TMath.Abs(m_kshort - mass_14)
                    diff23 = r.TMath.Abs(m_kshort - mass_23)
                    diff24 = r.TMath.Abs(m_kshort - mass_24)
                    diff34 = r.TMath.Abs(m_kshort - mass_34)
                    charge12 = charge1 * charge2
                    charge13 = charge1 * charge3
                    charge14 = charge1 * charge4
                    charge23 = charge2 * charge3
                    charge24 = charge2 * charge4
                    charge34 = charge3 * charge4
                    
                    if (diff12 < 0.05 and diff34 < 0.05 and (charge12 == -1 and charge34 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())
                    if (diff13 < 0.05 and diff24 < 0.05 and (charge13 == -1 and charge24 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())
                    if (diff14 < 0.05 and diff23 < 0.05 and (charge14 == -1 and charge23 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())

                        
        outputFile.Write()
        outputFile.Close()
        nFile += 1
    else:
        break

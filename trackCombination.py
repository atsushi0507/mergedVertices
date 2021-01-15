import os
import ROOT as r
import random
import argparse
from utils import *
import itertools

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFile", help="Specify input file list", default="inputList.txt")
p.add_argument("-o", "--outputDir", help="Specify output directory", default="kshort-method")

args = p.parse_args()

inputFile = args.inputFile

m_pion = 139.57 * 0.001

regions = {0 : "inside_BP",
           1 : "inside_IBL",
           2 : "PIX",
           3 : "inside_SCT"}

f = open(inputFile, "r")
nFile = 1
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
                if (not tree.DV_passChiSqCut[idv]):
                    continue
                vertex.append([tree.DV_m[idv], tree.DV_nTracks[idv]])
                track = []
                for itrack in range(len(tree.dvtrack_ptWrtDV)):
                    if (tree.DV_index[idv] != tree.dvtrack_DVIndex[itrack]):
                        continue
                    if (tree.dvtrack_failedExtrapolation[itrack] == 1):
                        continue
                    if (tree.dvtrack_isAssociated[itrack]):
                        if (tree.dvtrack_ptWrtDV[itrack] < 2.):
                            continue
                        if ((tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[itrack] < 3.)):
                            continue
                    # d0-significance
                    d0sig = r.TMath.Abs(tree.dvtrack_d0[itrack]/tree.dvtrack_errd0[itrack])
                    if ((tree.DV_rxy[idv] < 23.5) and (d0sig < 15.)):
                        continue
                    if ((tree.DV_rxy[idv] < 119.3) and (d0sig < 10.)):
                        continue
                    if ((tree.DV_rxy[idv] > 85.5) and (d0sig < 10.) and tree.dvtrack_isAssociated[itrack] == 0):
                        continue
                    track.append([tree.dvtrack_ptWrtDV[itrack],
                                  tree.dvtrack_etaWrtDV[itrack],
                                  tree.dvtrack_phiWrtDV[itrack],
                                  m_pion])
                tracks.append(track)
            if (len(vertex) == 0):
                continue
            events.append([vertex, tracks])

        ### Histograms
        h_2track_mass = r.TH1D("2track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)
        h_3track_mass = r.TH1D("3track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)
        h_4track_mass = r.TH1D("4track_mass", ";m_{DV} [GeV]", 1000, 0., 5.)

        h_track1_mass = r.TH1D("track1", ";m_{DV} comb1 [GeV]", 2000, 0., 2.)
        h_track2_mass = r.TH1D("track2", ";m_{DV} comb2 [GeV]", 2000, 0., 2.)

        # test
        for iEvent in range(len(events)):
            dv = events[iEvent][0]
            dvtracks = events[iEvent][1]
            for idv in range(len(dv)):
                m_dv = dv[idv][0]
                nTracks = dv[idv][1]
                dv_tracks = r.TLorentzVector()
                for itrack in dvtracks[idv]:
                    track = r.TLorentzVector()
                    track.SetPtEtaPhiM(itrack[0],
                                       itrack[1],
                                       itrack[2],
                                       itrack[3])
                    dv_tracks += track
                if (nTracks == 2):
                    h_2track_mass.Fill(m_dv)
                if (nTracks == 3):
                    h_2track_mass.Fill(m_dv)
                    trk_a, trk_b, trk_c = r.TLorentzVector(), r.TLorentzVector(), r.TLorentzVector()
                if (nTracks == 4):
                    h_4track_mass.Fill(m_dv)

                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track3 = r.TLorentzVector()
                    track4 = r.TLorentzVector()
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    track3.SetPtEtaPhiM(dvtracks[idv][2][0], dvtracks[idv][2][1], dvtracks[idv][2][2], dvtracks[idv][2][3])
                    track4.SetPtEtaPhiM(dvtracks[idv][3][0], dvtracks[idv][3][1], dvtracks[idv][3][2], dvtracks[idv][3][3])
                    t = [track1, track2, track3, track4]
                    pairs = [[0,1,2,3], [0,2,1,3], [0,3,1,2]]
                    for index in range(len(pairs)):
                        i, j, k, l = pairs[index][0], pairs[index][1], pairs[index][2], pairs[index][3]
                        trackMass_1 = (t[i] + t[j]).M()
                        trackMass_2 = (t[k] + t[l]).M()
                        h_track1_mass.Fill(trackMass_1)
                        h_track2_mass.Fill(trackMass_2)
        

        outputFile.Write()
        outputFile.Close()
        nFile += 1
    else:
        break
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
    # DV properties
    DV_rxy = dv[2]
    DV_index = dv[4]
    # dvtrack properties
    dvtrack_ptWrtDV = track[0]
    dvtrack_etaWrtDV = track[1]
    dvtrack_phiWrtDV = track[2]
    dvtrack_m = track[3] # pion mass
    dvtrack_isAssociated = track[4]
    dvtrack_DVIndex = track[5]
    dvtrack_failedExtrapolation = track[6]
    d0sig = track[7]    
    
    passCleaning = True
    # Check DV_index and dvtrack_DVIndex
    if (DV_index != dvtrack_DVIndex):
        passCleaning = False
    # Check dvtrack_failedExtapolation
    if (dvtrack_failedExtrapolation == 1):
        passCleaning = False
    # Attached track pT cut
    if (dvtrack_isAssociated):
        if (dvtrack_ptWrtDV < 2.):
            passCleaning = False
        if (DV_rxy > 85.5 and dvtrack_ptWrtDV < 3.):
            passCleaning = False
    # d0-significance cut
    if ((DV_rxy < 23.5) and d0sig < 15.):
        passCleaning = False
    if ((DV_rxy < 119.3) and d0sig < 10.):
        passCleaning = False
    if ((DV_rxy > 119.3) and d0sig < 10. and dvtrack_isAssociated == 0):
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
        # File name: group.phys-susy.00284213.r9264_r10573_p3578_p4296.23081787._001321.trees.root
        #number = name.split("_")[1].split(".")[0]
        outputFileName = name.replace("group", "output")
        outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")

        events = []
        for entry in range(tree.GetEntries()):
            if (entry % 10000 == 0):
                print("Processed {}/{}".format(entry, tree.GetEntries()))
            ientry = tree.LoadTree(entry)
            if ientry < 0:
                break
            nb = tree.GetEntry(ientry)
            if nb <= 0:
                continue
            vertex = []
            tracks = []

            if (not ord(tree.DRAW_pass_triggerFlags)):
                continue

            for idv in range(tree.DV_n):
                # The DV passes
                # - DV in fiducial volume
                # - chisq/nDoF < 5 for DV fit
                # - DV > 4 mm from PV
                # No restrictions on DV mass or track-multiplicity
                if (tree.DV_passFiducialCut[idv] and tree.DV_passChiSqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMaterialVeto[idv]):
                    vertex.append([tree.DV_m[idv], tree.DV_nTracks[idv], tree.DV_rxy[idv], tree.DV_z[idv], tree.DV_index[idv]])
                    track = []
                    for itrack in range(len(tree.dvtrack_ptWrtDV)):
                        if (tree.DV_index[idv] != tree.dvtrack_DVIndex[itrack]):
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
        h_2track_mass = r.TH1D("2track_mass", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_2track_rxy = r.TH1D("2track_rxy", ";r_{xy} mm", 300, 0., 300.)
        h_2track_z = r.TH1D("2track_z", ";z mm", 600, -300., 300.)

        h_3track_mass_tight = r.TH1D("3track_mass_tight", ";m_{DV} [GeV]", 1000, 0., 1.)
        
        h_3track_mass = r.TH1D("3track_mass", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_3track_rxy = r.TH1D("3track_rxy", ";r_{xy} mm", 300, 0., 300.)
        h_3track_z = r.TH1D("3track_z", ";z mm", 600, -300., 300.)

        h_ks3trk_m = r.TH1D("ks_3trk_m", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_ks3trk_rxy = r.TH1D("ks_3trk_rxy", ";r_{xy} [mm]", 300, 0., 300.)
        h_ks3trk_z = r.TH1D("ks_3trk_z", ";z [mm]", 600, -300., 300.)
        h_ks4trk_m = r.TH1D("ks_4trk_m", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_ks4trk_rxy = r.TH1D("ks_4trk_rxy", ";r_{xy} [mm]", 300, 0., 300.)
        h_ks4trk_z = r.TH1D("ks_4trk_z", ";z [mm]", 600, -300., 300.)
        
        h_4track_mass = r.TH1D("4track_mass", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_4track_rxy = r.TH1D("4track_rxy", ";r_{xy} mm", 300, 0., 300.)
        h_4track_z = r.TH1D("4track_z", ";z mm", 600, -300., 300.)
        h_4track_mass_fullRange = r.TH1D("4track_mass_fullRange", ";m_{DV} [GeV]", 250, 0., 25.)

        h_ditrack_from3trk = r.TH1D("ditrack_from3trk", ";m_{DV} [GeV]", 500, 0., 1.)
        h_ditrack_from4trk = r.TH1D("ditrack_from4trk", ";m_{DV} [GeV]", 2500, 0., 5.)

        h_mv_4track = r.TH1D("mv_4track", ";m_{DV} [GeV]", 1000, 0., 100.)

        # For 2-track DV pairs' kinematics
        h_dPhi = r.TH1D("dPhi", ";d#phi", 640, -3.2, 3.2)
        h_dEta = r.TH1D("dEta", ";d#eta", 100, 0., 10.)
        h_dR = r.TH1D("dR", ";dR(DV_{1}, DV_{2})", 120, 0., 6.)

        # Track combination
        for iEvent in range(len(events)):
            dv = events[iEvent][0]
            dvtracks = events[iEvent][1]
            for idv in range(len(dv)):
                m_dv = dv[idv][0]
                nTracks = len(dvtracks[idv])
                dv_tracks = r.TLorentzVector()
                
                if (nTracks == 2):
                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    mass12 = (track1 + track2).M()
                    if (mass12 <= 1.):
                        h_2track_mass.Fill(mass12)
                        h_2track_rxy.Fill(dv[idv][2])
                        h_2track_z.Fill(dv[idv][3])
                    
                if (nTracks == 3):
                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track3 = r.TLorentzVector()
                    
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    track3.SetPtEtaPhiM(dvtracks[idv][2][0], dvtracks[idv][2][1], dvtracks[idv][2][2], dvtracks[idv][2][3])
                    
                    h_3track_mass.Fill((track1+track2+track3).M())
                    h_3track_rxy.Fill(dv[idv][2])
                    h_3track_z.Fill(dv[idv][3])
                    
                    mass_12 = (track1 + track2).M()
                    mass_13 = (track1 + track3).M()
                    mass_23 = (track2 + track3).M()

                    # Is track passed the trackCleaning?
                    pass_1 = trackCleaning(dv[idv], dvtracks[idv][0])
                    pass_2 = trackCleaning(dv[idv], dvtracks[idv][1])
                    pass_3 = trackCleaning(dv[idv], dvtracks[idv][2])
                    # Check if any of the 3-tracks were associated to the DV,
                    isAsso_1 = dvtracks[idv][0][4]
                    isAsso_2 = dvtracks[idv][1][4]
                    isAsso_3 = dvtracks[idv][2][4]

                    # Selected two tracks should selected-track, and the rest should pass track cleaning
                    if ((not isAsso_1) and (not isAsso_2) and (pass_3)):
                        h_ditrack_from3trk.Fill(mass_12)
                        if (mass_12 <= 1.):
                            if (not ((dv[idv][2] < 23.5) and isAsso_3)):
                                h_ks3trk_m.Fill(mass_12)
                                h_ks3trk_rxy.Fill(dv[idv][2])
                                h_ks3trk_z.Fill(dv[idv][3])
                    if ((not isAsso_1) and (not isAsso_3) and (pass_2)):
                        h_ditrack_from3trk.Fill(mass_13)
                        if (mass_13 <= 1.):
                            if (not ((dv[idv][2] < 23.5))):
                                h_ks3trk_m.Fill(mass_13)
                                h_ks3trk_rxy.Fill(dv[idv][2])
                                h_ks3trk_z.Fill(dv[idv][3])
                    if ((not isAsso_2) and (not isAsso_3) and (pass_1)):
                        h_ditrack_from3trk.Fill(mass_23)
                        if (mass_23 <= 1.):
                            if (not ((dv[idv][2] < 23.5) and isAsso_1)):
                                h_ks3trk_m.Fill(mass_23)
                                h_ks3trk_rxy.Fill(dv[idv][2])
                                h_ks3trk_z.Fill(dv[idv][3])

                    # Properties for accidental crossings mass template
                    if (not ord(tree.DRAW_pass_DVJETS)):
                        continue
                    print("Passed selection")
                    #if (not ord(tree.BaselineSel_pass)):
                    
                        
                if (nTracks == 4):
                    track1 = r.TLorentzVector()
                    track2 = r.TLorentzVector()
                    track3 = r.TLorentzVector()
                    track4 = r.TLorentzVector()
                    track1.SetPtEtaPhiM(dvtracks[idv][0][0], dvtracks[idv][0][1], dvtracks[idv][0][2], dvtracks[idv][0][3])
                    track2.SetPtEtaPhiM(dvtracks[idv][1][0], dvtracks[idv][1][1], dvtracks[idv][1][2], dvtracks[idv][1][3])
                    track3.SetPtEtaPhiM(dvtracks[idv][2][0], dvtracks[idv][2][1], dvtracks[idv][2][2], dvtracks[idv][2][3])
                    track4.SetPtEtaPhiM(dvtracks[idv][3][0], dvtracks[idv][3][1], dvtracks[idv][3][2], dvtracks[idv][3][3])
                    if ((track1 + track2 + track3 + track4).M() < 20.):
                        h_4track_mass.Fill((track1+track2+track3+track4).M())
                        h_4track_mass_fullRange.Fill((track1 + track2 + track3 + track4).M())

                    track12 = track1 + track2
                    track13 = track1 + track3
                    track14 = track1 + track4
                    track23 = track2 + track3
                    track24 = track2 + track4
                    track34 = track3 + track4

                    mass_12 = track12.M()
                    mass_13 = track13.M()
                    mass_14 = track14.M()
                    mass_23 = track23.M()
                    mass_24 = track24.M()
                    mass_34 = track34.M()

                    charge1 = dvtracks[idv][0][8]
                    charge2 = dvtracks[idv][1][8]
                    charge3 = dvtracks[idv][2][8]
                    charge4 = dvtracks[idv][3][8]

                    # DV pair's relation
                    h_dPhi.Fill(track12.DeltaPhi(track34))
                    h_dPhi.Fill(track13.DeltaPhi(track24))
                    h_dPhi.Fill(track14.DeltaPhi(track23))
                    h_dEta.Fill(r.TMath.Abs(track12.Eta() - track34.Eta()))
                    h_dEta.Fill(r.TMath.Abs(track13.Eta() - track24.Eta()))
                    h_dEta.Fill(r.TMath.Abs(track14.Eta() - track23.Eta()))
                    h_dR.Fill(track12.DeltaR(track34))
                    h_dR.Fill(track13.DeltaR(track24))
                    h_dR.Fill(track14.DeltaR(track23))

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
                    
                    if ((diff12 < 0.05 and charge12 == -1) or (diff34 < 0.05 and charge34 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())
                    if ((diff13 < 0.05 and charge13 == -1) or (diff24 < 0.05 and charge24 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())
                    if ((diff14 < 0.05 and charge14 == -1) or (diff23 < 0.05 and charge23 == -1)):
                        h_mv_4track.Fill((track1 + track2 + track3 + track4).M())
                        
                    if (diff12 < 0.05 and charge12 == -1):
                        h_ditrack_from4trk.Fill((track3 + track4).M())
                    if (diff34 < 0.05 and charge34 == -1):
                        h_ditrack_from4trk.Fill((track1 + track2).M())
                    if (diff13 < 0.05 and charge13 == -1):
                        h_ditrack_from4trk.Fill((track2 + track4).M())
                    if (diff24 < 0.05 and charge24 == -1):
                        h_ditrack_from4trk.Fill((track1 + track3).M())
                    if (diff14 < 0.05 and charge14 == -1):
                        h_ditrack_from4trk.Fill((track2 + track3).M())
                    if (diff23 < 0.05 and charge23 == -1):
                        h_ditrack_from4trk.Fill((track1 + track4).M())

                        
        outputFile.Write()
        outputFile.Close()
        nFile += 1
    else:
        break

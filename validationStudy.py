import os
import ROOT as r
import argparse

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFile", help="Specify input file list", default="inputList.txt")
p.add_argument("-o", "--outputDir", help="Specify output directory", default="mvValid")

args = p.parse_args()

inputFile = args.inputFile

m_pion = 139.57 * 0.001
m_kshort = 497.11 * 0.001

f = open(inputFile, "r")

def get_DVPV(idv, PV_x, PV_y, PV_z, DV_x, DV_y, DV_z):
    PV = r.TVector3(PV_x, PV_y, PV_z)
    DV = r.TVector3(DV_x[idv], DV_y[idv], DV_z[idv])
    vDVPV = DV - PV
    return vDVPV

def get_dEta(DV_PV, trackIndex, dvtrack_etaWrtDV):
    DVPV_zy = r.TVector2(DV_PV.Z(), DV_PV.Y())
    cosTheta = DV_PV.Z()/DVPV_zy.Mod()
    if (r.TMath.Abs(cosTheta) > 1.):
        print("Error! cosTheta = {}, DV_PV_z = {}, |DV-PV| = {}".format(cosTheta, DV_PV.Z(), DV_PV.Mag()))
        return 0.
    theta_DVPV = r.TMath.ACos(cosTheta)

    eta_DVPV = 1.*r.TMath.Log(r.TMath.Tan(theta_DVPV/2.))
    return (eta_DVPV - dvtrack_etaWrtDV[trackIndex])

def get_dPhi(DV_PV, trackIndex, dvtrack_phiWrtDV):
    phi_DVPV = DV_PV.Phi()
    phi_DV = dvtrack_phiWrtDV[trackIndex]
    dPhi = phi_DVPV - phi_DV
    if (dPhi >= r.TMath.Pi()):
        dPhi -= 2*r.TMath.Pi()
    if (dPhi < -r.TMath.Pi()):
        dPhi += 2*r.TMath.Pi()
    return dPhi
    

while True:
    line = f.readline().strip()
    if line:
        print(line)
        inFile = r.TFile(line, "READ")
        tree = inFile.Get("trees_SRDV_")
        outputDir = args.outputDir
        if (not os.path.isdir(outputDir)):
            os.makedirs(outputDir)
        name = line.split("/")[-1]
        outputFileName = name.replace("group", "output")
        outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")

        # Histograms
        h_mDV_2track = r.TH1D("mDV_2track", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2track_inside_BP = r.TH1D("mDV_2track_inside_BP", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2track_inside_IBL = r.TH1D("mDV_2track_inside_IBL", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2track_inside_PIX = r.TH1D("mDV_2track_inside_PIX", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2track_inside_SCT = r.TH1D("mDV_2track_inside_SCT", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_rxy_2track = r.TH1D("rxy_2track", ";r_{xy} mm", 300, 0., 300.)
        h_z_2track = r.TH1D("z_2track", ";z mm", 600, -300., 300.)

        h_mDV_2from3 = r.TH1D("mDV_2from3", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_3track = r.TH1D("mDV_3track", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_3track_full = r.TH1D("mDV_3track_full", ";m_{DV} [GeV]", 1000, 0., 100.)
        h_rxy_3track = r.TH1D("rxy_3track", ";r_{xy} mm", 300, 0., 300.)
        h_z_3track = r.TH1D("z_3track", ";z mm", 600, -300., 300.)

        h_mDV_2from4 = r.TH1D("mDV_2from4", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2from4_passTC = r.TH1D("mDV_2from4_passTC", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2from4_selected = r.TH1D("mDV_2from4_selected", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2from4_combination = r.TH1D("mDV_2from4_combination", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_2from4_noSel = r.TH1D("mDV_2from4_noSel", ";m_{DV} [GeV]", 5000, 0., 5.)
        h_mDV_4track = r.TH1D("mDV_4track", ";m_{DV} [GeV]", 1000, 0., 1.)
        h_mDV_4track_20GeV = r.TH1D("mDV_4track_20GeV", ";m_{DV} [GeV]", 220, 0., 22.)
        h_rxy_4track = r.TH1D("rxy_4track", ";r_{xy} mm", 300, 0., 300.)
        h_z_4track = r.TH1D("z_4track", ";z mm", 600, -300., 300.)
        h_mv_4track = r.TH1D("mv_4track", ";m_{DV} [GeV]", 100, 0., 50.)
        h_mv_4track_passTrackCleaning = r.TH1D("mv_4track_passTrackCleaning", ";m_{DV} [GeV]", 100, 0., 50.)
        h_mv_4track_onlySelected = r.TH1D("mv_4track_onlySelected", ";m_{DV} [GeV]", 100, 0., 50.)
        h_mv_4track_combination = r.TH1D("mv_4track_combination", ";m_{DV} [GeV]", 100, 0., 50.)

        h_inside_BP_associated_pT = r.TH1D("inside_BP_associated_pT", ";p_{T} [GeV]", 100, 0., 200.)
        h_inside_BP_associated_dPhi = r.TH1D("inside_BP_associated_dPhi", ";d#phi", 100, -6.3, 6.3)
        h_inside_BP_associated_eta = r.TH1D("inside_BP_associated_eta", ";#eta", 100, -2.5, 2.5)
        h_inside_BP_selected_pT = r.TH1D("inside_BP_selected_pT", ";p_{T} [GeV]", 100, 0., 200.)
        h_inside_BP_selected_dPhi = r.TH1D("inside_BP_selected_dPhi", ";d#phi", 100, -6.3, 6.3)
        h_inside_BP_selected_eta = r.TH1D("inside_BP_selected_eta", ";#eta", 100, -2.5, 2.5)
        h_inside_IBL_pT = r.TH1D("inside_IBL_pT", ";p_{T} [GeV]", 100, 0., 200.)
        h_inside_IBL_dPhi = r.TH1D("inside_IBL_dPhi", ";d#phi", 100, -6.3, 6.3)
        h_inside_IBL_eta = r.TH1D("inside_IBL_eta", ";#eta", 100, -2.5, 2.5)
        h_inside_PIX_pT = r.TH1D("inside_PIX_pT", ";p_{T} [GeV]", 100, 0., 200.)
        h_inside_PIX_dPhi = r.TH1D("inside_PIX_dPhi", ";d#phi", 100, -6.3, 6.3)
        h_inside_PIX_eta = r.TH1D("inside_PIX_eta", ";#eta", 100, -2.5, 2.5)
        h_inside_SCT_pT = r.TH1D("inside_SCT_pT", ";p_{T} [GeV]", 100, 0., 200.)
        h_inside_SCT_dPhi = r.TH1D("inside_SCT_dPhi", ";d#phi", 100, -6.3, 6.3)
        h_inside_SCT_eta = r.TH1D("inside_SCT_eta", ";#eta", 100, -2.5, 2.5)
        

        # Ks masses
        Ks4trkMass = []
        Ks3trkMass = []
        Ks2trkMass = []
        Ks4trk_R = []
        Ks3trk_R = []
        Ks2trk_R = []
        Ks4trk_z = []
        Ks3trk_z = []
        Ks2trk_z = []

        entries = tree.GetEntries()
        for entry in range(entries):
            if (entry % 10000 == 0):
                print("Processed {}/{}".format(entry, entries))
            ientry = tree.LoadTree(entry)
            if ientry < 0:
                break
            nb = tree.GetEntry(ientry)
            if nb <= 0:
                continue
            if (not ord(tree.DRAW_pass_triggerFlags)):
                continue
            for idv in range(len(tree.DV_m)):
                if (tree.DV_passFiducialCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passChiSqCut[idv] and tree.DV_passMaterialVeto[idv]):
                    for itrack in range(len(tree.dvtrack_ptWrtDV)):
                        if (tree.DV_index[idv] != tree.dvtrack_DVIndex[itrack]):
                            continue
                        nTracks = len(tree.dvtrack_ptWrtDV)
                        if (nTracks == 2):
                            track1 = r.TLorentzVector()
                            track2 = r.TLorentzVector()
                            track1.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[0],
                                                tree.dvtrack_etaWrtDV[0],
                                                tree.dvtrack_phiWrtDV[0],
                                                m_pion)
                            track2.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[1],
                                                tree.dvtrack_etaWrtDV[1],
                                                tree.dvtrack_phiWrtDV[1],
                                                m_pion)
                            m12 = (track1+track2).M()
                            if (m12 <= 1.):
                                h_mDV_2track.Fill(m12)
                                h_rxy_2track.Fill(tree.DV_rxy[idv])
                                h_z_2track.Fill(tree.DV_z[idv])
                                Ks2trkMass.append(m12)
                                Ks2trk_R.append(tree.DV_rxy[idv])
                                Ks2trk_z.append(tree.DV_z[idv])
                                if (tree.DV_rxy[idv] < 25.):
                                    h_mDV_2track_inside_BP.Fill(m12)
                                elif (tree.DV_rxy[idv] >= 25. and tree.DV_rxy[idv] < 38.):
                                    h_mDV_2track_inside_IBL.Fill(m12)
                                elif (tree.DV_rxy[idv] >= 38. and tree.DV_rxy[idv] < 145.):
                                    h_mDV_2track_inside_PIX.Fill(m12)
                                elif (tree.DV_rxy[idv] >= 145. and tree.DV_rxy[idv] < 300.):
                                    h_mDV_2track_inside_SCT.Fill(m12)
                                    
                        if (nTracks == 3):
                            track1 = r.TLorentzVector()
                            track2 = r.TLorentzVector()
                            track3 = r.TLorentzVector()
                            
                            track1.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[0],
                                                tree.dvtrack_etaWrtDV[0],
                                                tree.dvtrack_phiWrtDV[0],
                                                m_pion)
                            track2.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[1],
                                                tree.dvtrack_etaWrtDV[1],
                                                tree.dvtrack_phiWrtDV[1],
                                                m_pion)
                            track3.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[2],
                                                tree.dvtrack_etaWrtDV[2],
                                                tree.dvtrack_phiWrtDV[2],
                                                m_pion)
                            # in C++ mass_2trk = vector<pair<track number, 2trk mass from 3trk>> -> [()] ?
                            mass_2trk = []
                            mass_12 = (track1 + track2).M()
                            mass_13 = (track1 + track3).M()
                            mass_23 = (track2 + track3).M()

                            isAsso_1 = tree.dvtrack_isAssociated[0]
                            isAsso_2 = tree.dvtrack_isAssociated[1]
                            isAsso_3 = tree.dvtrack_isAssociated[2]

                            pass_1 = True
                            pass_2 = True
                            pass_3 = True
                            # For track1
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 15.)):
                                pass_1 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 10.)):
                                pass_1 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 10.) and tree.dvtrack_isAssociated[0] == 0):
                                pass_1 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[0] == 1) and (tree.dvtrack_ptWrtDV[0] < 2.)):
                                pass_1 = False
                            if ((tree.dvtrack_isAssociated[0] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[0] < 3.)):
                                pass_1 = False

                            # For track2
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 15.)):
                                pass_2 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 10.)):
                                pass_2 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 10.) and tree.dvtrack_isAssociated[1] == 0):
                                pass_2 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[1] == 1) and (tree.dvtrack_ptWrtDV[1] < 2.)):
                                pass_2 = False
                            if ((tree.dvtrack_isAssociated[1] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[1] < 3.)):
                                pass_2 = False

                            # For track3
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 15.)):
                                pass_3 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 10.)):
                                pass_3 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 10.) and tree.dvtrack_isAssociated[2] == 0):
                                pass_3 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[2] == 1) and (tree.dvtrack_ptWrtDV[2] < 2.)):
                                pass_3 = False
                            if ((tree.dvtrack_isAssociated[2] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[2] < 3.)):
                                pass_3 = False

                            h_mDV_3track.Fill((track1 + track2 + track3).M())
                            h_mDV_3track_full.Fill((track1 + track2 + track3).M())

                            # 2-track: selected-track, rest track: pass track cleaning
                            if ((not isAsso_1) and (not isAsso_2) and (pass_3)):
                                h_mDV_2from3.Fill(mass_12)
                                mass_2trk.append((2, mass_12))
                                if (mass_12 <= 1.):
                                    h_rxy_3track.Fill(tree.DV_rxy[idv])
                                    h_z_3track.Fill(tree.DV_z[idv])
                                    Ks3trkMass.append(mass_12)
                                    Ks3trk_R.append(tree.DV_rxy[idv])
                                    Ks3trk_z.append(tree.DV_z[idv])
                            if ((not isAsso_1) and (not isAsso_3) and (pass_2)):
                                h_mDV_2from3.Fill(mass_13)
                                mass_2trk.append((1, mass_13))
                                if (mass_13 <= 1.):
                                    h_rxy_3track.Fill(tree.DV_rxy[idv])
                                    h_z_3track.Fill(tree.DV_z[idv])
                                    Ks3trkMass.append(mass_13)
                                    Ks3trk_R.append(tree.DV_rxy[idv])
                                    Ks3trk_z.append(tree.DV_z[idv])
                            if ((not isAsso_2) and (not isAsso_3) and (pass_1)):
                                h_mDV_2from3.Fill(mass_23)
                                mass_2trk.append((0, mass_23))
                                if (mass_23 <= 1.):
                                    h_rxy_3track.Fill(tree.DV_rxy[idv])
                                    h_z_3track.Fill(tree.DV_z[idv])
                                    Ks3trkMass.append(mass_23)
                                    Ks3trk_R.append(tree.DV_rxy[idv])
                                    Ks3trk_z.append(tree.DV_z[idv])
                            
                            # Properties of accidental crossings mass template
                            if (not ord(tree.DRAW_pass_DVJETS)):
                                continue
                            if (not ord(tree.BaselineSel_pass)):
                                continue
                            if (len(mass_2trk) != 0):
                                # Only consider accidental crossing track whose 2-track pair is closest to Ks
                                minDiff = 1e12
                                for l in range(len(mass_2trk)):
                                    diff = r.TMath.Abs(m_kshort - mass_2trk[l][1])
                                    if (diff < minDiff):
                                        minDiff = diff
                                        index = l
                                # Onl keep tracks where the Ksh reconstructed is within 50 MeV of the Ksh
                                if (r.TMath.Abs(m_kshort - mass_2trk[index][1]) > 0.05):
                                    continue
                                # We have a 3-trk DV which is a 2-trk DV within 50 MeV of the Ksh mass + AX track
                                # AX track is associated to vertex
                                trackIndex = mass_2trk[index][0]

                                DV_PV = get_DVPV(idv, tree.PV_x, tree.PV_y, tree.PV_z, tree.DV_x, tree.DV_y, tree.DV_z)

                                dEta = get_dEta(DV_PV, trackIndex, tree.dvtrack_etaWrtDV)
                                dPhi = get_dPhi(DV_PV, trackIndex, tree.dvtrack_phiWrtDV)

                                track = [dEta,
                                         dPhi,
                                         tree.dvtrack_eta[trackIndex],
                                         tree.dvtrack_phi[trackIndex],
                                         tree.dvtrack_pt[trackIndex],
                                         tree.DV_z[idv],
                                         tree.DV_rxy[idv],
                                         tree.dvtrack_errPt[trackIndex],
                                         tree.dvtrack_isLRT[trackIndex],
                                         tree.dvtrack_charge[trackIndex],
                                         tree.dvtrack_d0[trackIndex],
                                         tree.dvtrack_z0[trackIndex],
                                         tree.dvtrack_d0WrtDV[trackIndex]
                                         ]

                                d0sig = r.TMath.Abs(tree.dvtrack_d0[trackIndex]/tree.dvtrack_errd0[trackIndex])
                                # See if AX track satisfy SR requirements
                                if (tree.DV_rxy[idv] < 23.5 and d0sig < 15.):
                                    continue
                                if (tree.DV_rxy[idv] < 119.3 and d0sig < 10.):
                                    continue
                                if (tree.DV_rxy[idv] > 119.3 and d0sig < 10. and tree.dvtrack_isAssociated[trackIndex] == 0):
                                    continue
                                if (tree.dvtrack_isAssociated[trackIndex] == 1 and tree.dvtrack_ptWrtDV[trackIndex] < 2.):
                                    continue
                                if (tree.dvtrack_isAssociated[trackIndex] == 1 and tree.DV_rxy[idv] > 85.5 and tree.dvtrack_ptWrtDV[trackIndex] < 3.):
                                    continue

                                if (tree.DV_rxy[idv]  <25.):
                                    if (tree.dvtrack_isAssociated[trackIndex]):
                                        h_inside_BP_associated_pT.Fill(tree.dvtrack_pt[trackIndex])
                                        h_inside_BP_associated_dPhi.Fill(dPhi)
                                        h_inside_BP_associated_eta.Fill(dEta)
                                    else:
                                        h_inside_BP_selected_pT.Fill(tree.dvtrack_pt[trackIndex])
                                        h_inside_BP_selected_dPhi.Fill(dPhi)
                                        h_inside_BP_selected_eta.Fill(dEta)
                                elif (tree.DV_rxy[idv] >= 25 and tree.DV_rxy[idv] < 38.):
                                    h_inside_IBL_pT.Fill(tree.dvtrack_pt[trackIndex])
                                    h_inside_IBL_dPhi.Fill(dPhi)
                                    h_inside_IBL_eta.Fill(dEta)
                                elif (tree.DV_rxy[idv] >= 38 and tree.DV_rxy[idv] < 145.):
                                    h_inside_PIX_pT.Fill(tree.dvtrack_pt[trackIndex])
                                    h_inside_PIX_dPhi.Fill(dPhi)
                                    h_inside_PIX_eta.Fill(dEta)
                                elif (tree.DV_rxy[idv] >= 145 and tree.DV_rxy[idv] < 300.):
                                    h_inside_SCT_pT.Fill(tree.dvtrack_pt[trackIndex])
                                    h_inside_SCT_dPhi.Fill(dPhi)
                                    h_inside_SCT_eta.Fill(dEta)
                                    
                        
                        # 4-track
                        if (nTracks == 4):
                            if (nTracks == 4 and tree.DV_m[idv] > 20.):
                                continue
                            
                            track1 = r.TLorentzVector()
                            track2 = r.TLorentzVector()
                            track3 = r.TLorentzVector()
                            track4 = r.TLorentzVector()
                            
                            track1.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[0],
                                                tree.dvtrack_etaWrtDV[0],
                                                tree.dvtrack_phiWrtDV[0],
                                                m_pion)
                            track2.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[1],
                                                tree.dvtrack_etaWrtDV[1],
                                                tree.dvtrack_phiWrtDV[1],
                                                m_pion)
                            track3.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[2],
                                                tree.dvtrack_etaWrtDV[2],
                                                tree.dvtrack_phiWrtDV[2],
                                                m_pion)
                            track4.SetPtEtaPhiM(tree.dvtrack_ptWrtDV[3],
                                                tree.dvtrack_etaWrtDV[3],
                                                tree.dvtrack_phiWrtDV[3],
                                                m_pion)
                            mass_4track = (track1 + track2 + track3 + track4).M()
                            h_mDV_4track.Fill(mass_4track)
                            if (mass_4track < 20.):
                                h_mDV_4track_20GeV.Fill(mass_4track)
                            # Calculate inv. mass from all combinatorial of 2-tracks out of the 4
                            mass_2outof4 = []
                            mass_12 = (track1 + track2).M()
                            mass_13 = (track1 + track3).M()
                            mass_14 = (track1 + track4).M()
                            mass_23 = (track2 + track3).M()
                            mass_24 = (track2 + track4).M()
                            mass_34 = (track3 + track4).M()

                            charge1 = tree.dvtrack_charge[0]
                            charge2 = tree.dvtrack_charge[1]
                            charge3 = tree.dvtrack_charge[2]
                            charge4 = tree.dvtrack_charge[3]

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

                            h_mDV_2from4_noSel.Fill(mass_12)
                            h_mDV_2from4_noSel.Fill(mass_13)
                            h_mDV_2from4_noSel.Fill(mass_14)
                            h_mDV_2from4_noSel.Fill(mass_23)
                            h_mDV_2from4_noSel.Fill(mass_24)
                            h_mDV_2from4_noSel.Fill(mass_34)

                            # Track cleaning
                            pass_1 = True
                            pass_2 = True
                            pass_3 = True
                            pass_4 = True
                            # For track1
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 15.)):
                                pass_1 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 10.)):
                                pass_1 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[0]/tree.dvtrack_errd0[0]) < 10.) and tree.dvtrack_isAssociated[0] == 0):
                                pass_1 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[0] == 1) and (tree.dvtrack_ptWrtDV[0] < 2.)):
                                pass_1 = False
                            if ((tree.dvtrack_isAssociated[0] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[0] < 3.)):
                                pass_1 = False

                            # For track2
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 15.)):
                                pass_2 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 10.)):
                                pass_2 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[1]/tree.dvtrack_errd0[1]) < 10.) and tree.dvtrack_isAssociated[1] == 0):
                                pass_2 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[1] == 1) and (tree.dvtrack_ptWrtDV[1] < 2.)):
                                pass_2 = False
                            if ((tree.dvtrack_isAssociated[1] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[1] < 3.)):
                                pass_2 = False

                            # For track3
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 15.)):
                                pass_3 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 10.)):
                                pass_3 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[2]/tree.dvtrack_errd0[2]) < 10.) and tree.dvtrack_isAssociated[2] == 0):
                                pass_3 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[2] == 1) and (tree.dvtrack_ptWrtDV[2] < 2.)):
                                pass_3 = False
                            if ((tree.dvtrack_isAssociated[2] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[2] < 3.)):
                                pass_3 = False

                            # For track3
                            # d0-sig
                            if ((tree.DV_rxy[idv] < 23.5) and (r.TMath.Abs(tree.dvtrack_d0[3]/tree.dvtrack_errd0[3]) < 15.)):
                                pass_4 = False
                            if ((tree.DV_rxy[idv] < 119.3) and (r.TMath.Abs(tree.dvtrack_d0[3]/tree.dvtrack_errd0[3]) < 10.)):
                                pass_4 = False
                            if ((tree.DV_rxy[idv] > 119.3) and (r.TMath.Abs(tree.dvtrack_d0[3]/tree.dvtrack_errd0[3]) < 10.) and tree.dvtrack_isAssociated[3] == 0):
                                pass_4 = False
                            # pT
                            if ((tree.dvtrack_isAssociated[3] == 1) and (tree.dvtrack_ptWrtDV[3] < 2.)):
                                pass_4 = False
                            if ((tree.dvtrack_isAssociated[3] == 1) and (tree.DV_rxy[idv] > 85.5) and (tree.dvtrack_ptWrtDV[3] < 3.)):
                                pass_4 = False

                            isAsso_1 = tree.dvtrack_isAssociated[0]
                            isAsso_2 = tree.dvtrack_isAssociated[1]
                            isAsso_3 = tree.dvtrack_isAssociated[2]
                            isAsso_4 = tree.dvtrack_isAssociated[3]
                            
                            if ((diff12 < 0.05 and charge12 == -1) and (diff34 < 0.05 and charge34 == -1)):
                                h_mv_4track.Fill(mass_4track)
                                if (pass_3 and pass_4):
                                    h_mv_4track_passTrackCleaning.Fill(mass_4track)
                                if (isAsso_1 and isAsso_2):
                                    h_mv_4track_onlySelected.Fill(mass_4track)
                                if ((isAsso_1 and isAsso_2) and (pass_3 and pass_4)):
                                    h_mv_4track_combination.Fill(mass_4track)
                            if ((diff13 < 0.05 and charge13 == -1) and (diff24 < 0.05 and charge24 == -1)):
                                h_mv_4track.Fill(mass_4track)
                                if (pass_2 and pass_4):
                                    h_mv_4track_passTrackCleaning.Fill(mass_4track)
                                if (isAsso_1 and isAsso_3):
                                    h_mv_4track_onlySelected.Fill(mass_4track)
                                if ((isAsso_1 and isAsso_3) and (pass_2 and pass_4)):
                                    h_mv_4track_combination.Fill(mass_4track)
                            if ((diff14 < 0.05 and charge14 == -1) and (diff23 < 0.05 and charge23 == -1)):
                                h_mv_4track.Fill(mass_4track)
                                if (pass_2 and pass_3):
                                    h_mv_4track_passTrackCleaning.Fill(mass_4track)
                                if (isAsso_1 and isAsso_4):
                                    h_mv_4track_onlySelected.Fill(mass_4track)
                                if ((isAsso_1 and isAsso_4) and (pass_2 and pass_3)):
                                    h_mv_4track_combination.Fill(mass_4track)

                            if (diff12 < 0.05 and charge12 == -1):
                                h_mDV_2from4.Fill(mass_34)
                                if (pass_3 and pass_4):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_1 and isAsso_2):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_3 and pass_4):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_12 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            if (diff13 < 0.05 and charge13 == -1):
                                h_mDV_2from4.Fill(mass_24)
                                if (pass_2 and pass_4):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_1 and isAsso_3):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_2 and pass_4):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_13 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            if (diff14 < 0.05 and charge14 == -1):
                                h_mDV_2from4.Fill(mass_23)
                                if (pass_2 and pass_3):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_1 and isAsso_4):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_2 and pass_3):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_14 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            if (diff23 < 0.05 and charge23 == -1):
                                h_mDV_2from4.Fill(mass_14)
                                if (pass_2 and pass_3):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_1 and isAsso_4):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_2 and pass_3):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_23 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            if (diff24 < 0.05 and charge24 == -1):
                                h_mDV_2from4.Fill(mass_13)
                                if (pass_2 and pass_4):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_1 and isAsso_3):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_2 and pass_4):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_24 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            if (diff34 < 0.05 and charge34 == -1):
                                h_mDV_2from4.Fill(mass_12)
                                if (pass_1 and pass_2):
                                    h_mDV_2from4_passTC.Fill(mass_34)
                                if (isAsso_3 and isAsso_4):
                                    h_mDV_2from4_selected.Fill(mass_34)
                                    if (pass_1 and pass_2):
                                        h_mDV_2from4_combination.Fill(mass_34)
                                if (mass_34 <= 1.):
                                    h_rxy_4track.Fill(tree.DV_rxy[idv])
                                    h_z_4track.Fill(tree.DV_z[idv])
                            
        outputFile.Write()
        outputFile.Close()

    else:
        break

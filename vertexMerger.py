import os
import ROOT as r
import random
import argparse
from utils import *

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFile", help="Specify input file list", default="inputList.txt")
p.add_argument("-o", "--outputDir", help="Specify output directory", default="output")
p.add_argument("-u", "--doUnblind", help="If this flag is used, the signal region will be opened", action="store_true")
p.add_argument("-w", "--doWeight", help="If this flag is used, merged mass weighting is applied", action="store_true")
args = p.parse_args()

inputFile = args.inputFile
doUnblind = args.doUnblind
doWeight = args.doWeight

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
        t = inFile.Get("trees_SRDV_")
        outputDir = args.outputDir
        if (not os.path.isdir(outputDir)):
            os.makedirs(outputDir)
        name = line.split("/")[-1] # output_{fileNumber}.root
        number = name.split("_")[1].split(".")[0]
        if (doWeight):
            outputFileName = "output_{}_Reweight.root".format(number)
            #outputFile = r.TFile("Reweighted/" + outputFileName, "RECREATE")
            outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")
        else:
            outputFileName = "output_{}.root".format(number)
            outputFile = r.TFile(outputDir + "/" + outputFileName, "RECREATE")

        eventID = 0
        events = getEvents(t, eventID, doUnblind)

        ### Histograms
        # Significance (inclusive region)
        h_sig_same = r.TH1D("significance_same", ";Significance", 200, 0., 1000.)
        h_sig_mixed = r.TH1D("significance_mixed", ";Significance", 200, 0., 1000.)
        h_sig4_same = r.TH1D("sig4_same", ";Significance", 200, 0., 1000.)
        h_sig4_mixed = r.TH1D("sig4_mixed", ";Significance", 200, 0., 1000.)
        h_sig5_same = r.TH1D("sig5_same", ";Significance", 200, 0., 1000.)
        h_sig5_mixed = r.TH1D("sig5_mixed", ";Significance", 200, 0., 1000.)
        h_sig6_same = r.TH1D("sig6_same", ";Significance", 200, 0., 1000.)
        h_sig6_mixed = r.TH1D("sig6_mixed", ";Significance", 200, 0., 1000.)
        h_distance_same = r.TH1D("distance_same", ";r_{3D} [mm]", 300, 0., 300.)
        h_distance_mixed = r.TH1D("distance_mixed", ";r_{3D} [mm]", 300, 0., 300.)
        # region separated
        h_sig4_same_region = [r.TH1D("sig_4_same_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_sig4_mixed_region = [r.TH1D("sig_4_mixed_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_sig5_same_region = [r.TH1D("sig_5_same_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_sig5_mixed_region = [r.TH1D("sig_5_mixed_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_sig6_same_region = [r.TH1D("sig_6_same_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_sig6_mixed_region = [r.TH1D("sig_6_mixed_"+regions[i], ";Significance", 200, 0., 1000.) for i in regions]
        h_distance_same_region = [r.TH1D("distance_same_"+regions[i], ";r_{3D} [mm]", 300, 0., 300.) for i in regions]
        h_distance_mixed_region = [r.TH1D("distance_mixed_"+regions[i], ";r_{3D} [mm]", 300, 0., 300.) for i in regions]

        # Merged mass
        h_mergedMass4_same = r.TH1D("mergedMass4_same", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_same = r.TH1D("mergedMass5_same", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_same = r.TH1D("mergedMass6_same", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_mixed = r.TH1D("mergedMass4_mixed", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_mixed = r.TH1D("mergedMass5_mixed", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_mixed = r.TH1D("mergedMass6_mixed", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_sig100Cut = r.TH1D("mergedMass4_sig100Cut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_sig100Cut = r.TH1D("mergedMass5_sig100Cut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_sig100Cut = r.TH1D("mergedMass6_sig100Cut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_region = [r.TH1D("mergedMass4_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_region = [r.TH1D("mergedMass5_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_region = [r.TH1D("mergedMass6_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass4_sig100Cut_region = [r.TH1D("mergedMass4_sig100Cut_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_sig100Cut_region = [r.TH1D("mergedMass5_sig100Cut_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_sig100Cut_region = [r.TH1D("mergedMass6_sig100Cut_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        # apply weight
        h_mergedMass4_sigWeight = r.TH1D("mergedMass4_sigWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_sigWeight = r.TH1D("mergedMass5_sigWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_sigWeight = r.TH1D("mergedMass6_sigWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_dRWeight = r.TH1D("mergedMass4_dRWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_dRWeight = r.TH1D("mergedMass5_dRWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_dRWeight = r.TH1D("mergedMass6_dRWeight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_weight = r.TH1D("mergedMass4_weight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_weight = r.TH1D("mergedMass5_weight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_weight = r.TH1D("mergedMass6_weight", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_sigWeight_region = [r.TH1D("mergedMass4_sigWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_sigWeight_region = [r.TH1D("mergedMass5_sigWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_sigWeight_region = [r.TH1D("mergedMass6_sigWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass4_dRWeight_region = [r.TH1D("mergedMass4_dRWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_dRWeight_region = [r.TH1D("mergedMass5_dRWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_dRWeight_region = [r.TH1D("mergedMass6_dRWeight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass4_weight_region = [r.TH1D("mergedMass4_weight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_weight_region = [r.TH1D("mergedMass5_weight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_weight_region = [r.TH1D("mergedMass6_weight_"+regions[i], ";Merged mass [GeV]", 1000, 0., 100.) for i in regions]

        # apply weight, with no significance cut
        h_mergedMass4_sigWeight_noSigCut = r.TH1D("mergedMass4_sigWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_sigWeight_noSigCut = r.TH1D("mergedMass5_sigWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_sigWeight_noSigCut = r.TH1D("mergedMass6_sigWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_dRWeight_noSigCut = r.TH1D("mergedMass4_dRWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_dRWeight_noSigCut = r.TH1D("mergedMass5_dRWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_dRWeight_noSigCut = r.TH1D("mergedMass6_dRWeight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_weight_noSigCut = r.TH1D("mergedMass4_weight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass5_weight_noSigCut = r.TH1D("mergedMass5_weight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass6_weight_noSigCut = r.TH1D("mergedMass6_weight_noSigCut", ";Merged mass [GeV]", 1000, 0., 100.)
        h_mergedMass4_sigWeight_noSigCut_region = [r.TH1D("mergedMass4_sigWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_sigWeight_noSigCut_region = [r.TH1D("mergedMass5_sigWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_sigWeight_noSigCut_region = [r.TH1D("mergedMass6_sigWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass4_dRWeight_noSigCut_region = [r.TH1D("mergedMass4_dRWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_dRWeight_noSigCut_region = [r.TH1D("mergedMass5_dRWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_dRWeight_noSigCut_region = [r.TH1D("mergedMass6_dRWeight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass4_weight_noSigCut_region = [r.TH1D("mergedMass4_weight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass5_weight_noSigCut_region = [r.TH1D("mergedMass5_weight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        h_mergedMass6_weight_noSigCut_region = [r.TH1D("mergedMass6_weight_noSigCut_" + regions[i], "Merged mass [GeV]", 1000, 0., 100.) for i in regions]
        
        
        # DV-jet
        h_dR_jetDV_same = r.TH1D("dR_jetDV_same", "dR(ClosestJet_{DV_{1}}), DV_{cm}", 120, 0., 6.)
        h_dR_jetDV_mixed = r.TH1D("dR_jetDV_mixed", "dR(ClosestJet_{DV_{1}}), DV_{cm}", 120, 0., 6.)
        h_dR_jetDV1_same = r.TH1D("dR_jetDV1_same", "dR(ClosestJet_{DV_{1}}), DV_{1}", 120, 0., 6.)
        h_dR_jetDV1_mixed = r.TH1D("dR_jetDV1_mixed", "dR(ClosestJet_{DV_{1}}), DV_{1}", 120, 0., 6.)
        h_dR_jetDV2_same = r.TH1D("dR_jetDV2_same", "dR(ClosestJet_{DV_{1}}), DV_{2}", 120, 0., 6.)
        h_dR_jetDV2_mixed = r.TH1D("dR_jetDV2_mixed", "dR(ClosestJet_{DV_{1}}), DV_{2}", 120, 0., 6.)
        h_dR_jetDV_same_region = [r.TH1D("dR_jetDV_same_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{cm})", 120, 0., 6.) for i in regions]
        h_dR_jetDV_mixed_region = [r.TH1D("dR_jetDV_mixed_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{cm})", 120, 0., 6.) for i in regions]
        h_dR_jetDV1_same_region = [r.TH1D("dR_jetDV1_same_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{1})", 120, 0., 6.) for i in regions]
        h_dR_jetDV1_mixed_region = [r.TH1D("dR_jetDV1_mixed_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{1})", 120, 0., 6.) for i in regions]
        h_dR_jetDV2_same_region = [r.TH1D("dR_jetDV2_same_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{2})", 120, 0., 6.) for i in regions]
        h_dR_jetDV2_mixed_region = [r.TH1D("dR_jetDV2_mixed_"+regions[i], ";dR(ClosestJet_{DV_{1}}, DV_{2})", 120, 0., 6.) for i in regions]
        #DV-DV
        h_dR_DVDV_same = r.TH1D("dR_DVDV_same", ";dR(DV_{1}, DV_{2})", 120, 0., 6.)
        h_dR_DVDV_mixed = r.TH1D("dR_DVDV_mixed", ";dR(DV_{1}, DV_{2})", 120, 0., 6.)
        h_dPhi_DVDV_same = r.TH1D("dPhi_DVDV_same", ";d#phi(DV_{1}, DV_{2})", 640, -3.2, 3.2)
        h_dPhi_DVDV_mixed = r.TH1D("dPhi_DVDV_mixed", ";d#phi(DV_{1}, DV_{2})", 640, -3.2, 3.2)
        h_dR_DVDV_same_sig100Cut = r.TH1D("dR_DVDV_same_sig100Cut", ";dR(DV_{1}, DV_{2})", 120, 0., 6.)
        h_dR_DVDV_mixed_sig100Cut = r.TH1D("dR_DVDV_mixed_sig100Cut", ";dR(DV_{1}, DV_{2})", 120, 0., 6.)
        h_dPhi_DVDV_same_sig100Cut = r.TH1D("dPhi_DVDV_same_sig100Cut", ";d#phi(DV_{1}, DV_{2})", 640, -3.2, 3.2)
        h_dPhi_DVDV_mixed_sig100Cut = r.TH1D("dPhi_DVDV_mixed_sig100Cut", ";d#phi(DV_{1}, DV_{2})", 640, -3.2, 3.2)
        h_dR_DVDV_same_region = [r.TH1D("dR_DVDV_same_"+regions[i], ";dR(DV_{1}, DV_{2})", 120, 0., 6.) for i in regions]
        h_dR_DVDV_mixed_region = [r.TH1D("dR_DVDV_mixed_"+regions[i], ";dR(DV_{1}, DV_{2})", 120, 0., 6.) for i in regions]
        h_dPhi_DVDV_same_region = [r.TH1D("dPhi_DVDV_same_"+regions[i], ";dPhi(DV_{1}, DV_{2})", 120, 0., 6.) for i in regions]
        h_dPhi_DVDV_mixed_region = [r.TH1D("dPhi_DVDV_mixed_"+regions[i], ";dPhi(DV_{1}, DV_{2})", 120, 0., 6.) for i in regions]
        # DV mass
        h_DV_m = r.TH1D("DV_m", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_DV_m_2track = r.TH1D("DV_m_2track", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_DV_m_3track = r.TH1D("DV_m_3track", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_DV_m_4track = r.TH1D("DV_m_4track", ";m_{DV} [GeV]", 250, 0., 25.)
        h_DV_m_5track = r.TH1D("DV_m_5track", ";m_{DV} [GeV]", 200, 0., 20.)
        h_DV_m_6track = r.TH1D("DV_m_6track", ";m_{DV} [GeV]", 200, 0., 20.)
        h_DV_m_7track = r.TH1D("DV_m_7track", ";m_{DV} [GeV]", 200, 0., 20.)

        h_DV_m_region = [r.TH1D("DV_m_"+regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_DV_m_2track_region = [r.TH1D("DV_m_2track_"+regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_DV_m_3track_region = [r.TH1D("DV_m_3track_"+regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_DV_m_4track_region = [r.TH1D("DV_m_4track_"+regions[i], ";m_{DV} [GeV]", 250, 0., 25.) for i in regions]
        h_DV_m_5track_region = [r.TH1D("DV_m_5track_"+regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]
        h_DV_m_6track_region = [r.TH1D("DV_m_6track_"+regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]
        h_DV_m_7track_region = [r.TH1D("DV_m_7track_"+regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]

        h_recoDV_m = r.TH1D("recoDV_m", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_recoDV_m_2track = r.TH1D("recoDV_m_2track", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_recoDV_m_3track = r.TH1D("recoDV_m_3track", ";m_{DV} [GeV]", 5000, 0., 500.)
        h_recoDV_m_4track = r.TH1D("recoDV_m_4track", ";m_{DV} [GeV]", 250, 0., 25.)
        h_recoDV_m_5track = r.TH1D("recoDV_m_5track", ";m_{DV} [GeV]", 200, 0., 20.)
        h_recoDV_m_6track = r.TH1D("recoDV_m_6track", ";m_{DV} [GeV]", 200, 0., 20.)
        h_recoDV_m_7track = r.TH1D("recoDV_m_7track", ";m_{DV} [GeV]", 200, 0., 20.)
        h_recoDV_m_region = [r.TH1D("recoDV_m_" + regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_recoDV_m_2track_region = [r.TH1D("recoDV_m_2track_" + regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_recoDV_m_3track_region = [r.TH1D("recoDV_m_3track_" + regions[i], ";m_{DV} [GeV]", 5000, 0., 500.) for i in regions]
        h_recoDV_m_4track_region = [r.TH1D("recoDV_m_4track_" + regions[i], ";m_{DV} [GeV]", 250, 0., 25.) for i in regions]
        h_recoDV_m_5track_region = [r.TH1D("recoDV_m_5track_" + regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]
        h_recoDV_m_6track_region = [r.TH1D("recoDV_m_6track_" + regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]
        h_recoDV_m_7track_region = [r.TH1D("recoDV_m_7track_" + regions[i], ";m_{DV} [GeV]", 200, 0., 20.) for i in regions]
        
        h_mergedMass4_sigWeight.Sumw2()
        h_mergedMass5_sigWeight.Sumw2()
        h_mergedMass6_sigWeight.Sumw2()
        h_mergedMass4_dRWeight.Sumw2()
        h_mergedMass5_dRWeight.Sumw2()
        h_mergedMass6_dRWeight.Sumw2()
        h_mergedMass4_weight.Sumw2()
        h_mergedMass5_weight.Sumw2()
        h_mergedMass6_weight.Sumw2()
        
        print ("Looping for same-event")
        for iEvent in range(len(events)):
            dvs = events[iEvent][1]
            if (len(dvs) < 2):
                continue
            dvtracks = events[iEvent][2]
            cov = events[iEvent][3]
            jets = events[iEvent][4]

            for idv in range(len(dvs)-1):
                for jdv in range(idv+1, len(dvs)):
                    dv1, dv2 = getDVMatrix(dvs[idv]), getDVMatrix(dvs[jdv])
                    cov1, cov2 = getCovarianceMatrix(cov[idv]), getCovarianceMatrix(cov[jdv])
                    distance = getDistance(dv1, dv2)
                    sig = getSignificance(dv1, dv2, cov1, cov2)

                    dv_rxy1 = dvs[idv][4]
                    dv_rxy2 = dvs[jdv][4]
                    region1 = getRegion(dv_rxy1)
                    region2 = getRegion(dv_rxy2)
                    tracks1, nTracks_dv1, nTracksSel_dv1 = getDVTracks(dvtracks[idv])
                    tracks2, nTracks_dv2, nTracksSel_dv2 = getDVTracks(dvtracks[jdv])
                    
                    nTracks = nTracks_dv1 + nTracks_dv2
                    mergedDV = tracks1 + tracks2
                    mergedMass = mergedDV.M()
                    
                    closestJet = getClosestJet(dvs[idv], jets)
                    dR_jetDV = closestJet.DeltaR(mergedDV)
                    dR_DVDV = tracks1.DeltaR(tracks2)
                    dPhi_DVDV = tracks1.DeltaPhi(tracks2)
                    dR_jetDV1 = closestJet.DeltaR(tracks1)
                    dR_jetDV2 = closestJet.DeltaR(tracks2)

                    h_sig_same.Fill(sig)
                    h_distance_same.Fill(distance)
                    h_dR_jetDV_same.Fill(dR_jetDV)
                    h_dR_jetDV1_same.Fill(dR_jetDV1)
                    h_dR_jetDV2_same.Fill(dR_jetDV2)
                    h_dR_DVDV_same.Fill(dR_DVDV)
                    h_dPhi_DVDV_same.Fill(dPhi_DVDV)
                    # region
                    h_dR_jetDV_same_region[region1].Fill(dR_jetDV)
                    h_dR_jetDV1_same_region[region1].Fill(dR_jetDV1)
                    h_dR_jetDV2_same_region[region2].Fill(dR_jetDV2)
                    h_dR_DVDV_same_region[region1].Fill(dR_DVDV)
                    h_dPhi_DVDV_same_region[region1].Fill(dPhi_DVDV)
                    h_distance_same_region[region1].Fill(distance)

                    if (sig < 100):
                        h_dR_DVDV_same_sig100Cut.Fill(dR_DVDV)
                        h_dPhi_DVDV_same_sig100Cut.Fill(dPhi_DVDV)
                    if (nTracks == 4):
                        h_sig4_same.Fill(sig)
                        h_mergedMass4_same.Fill(mergedMass)
                        h_sig4_same_region[region1].Fill(sig)
                    if (nTracks == 5):
                        h_sig5_same.Fill(sig)
                        h_mergedMass5_same.Fill(mergedMass)
                        h_sig5_same_region[region1].Fill(sig)
                    if (nTracks == 6):
                        h_sig6_same.Fill(sig)
                        h_mergedMass6_same.Fill(mergedMass)
                        h_sig6_same_region[region1].Fill(sig)
                    
        print("Looping for mixed-event")
        for iEvent in range(len(events)-1):
            if (len(events) < 3):
                continue
            dvs1 = events[iEvent][1]
            dvtracks1 = events[iEvent][2]
            covs1 = events[iEvent][3]
            
            dvs2 = events[iEvent+1][1]
            dvtracks2 = events[iEvent+1][2]
            covs2 = events[iEvent+1][3]
            
            eventList = [i for i in range(len(events))]
            isSame = True
            i = -1
            while isSame:
                i = random.choice(eventList)
                if (i != iEvent and i != iEvent+1):
                    isSame = False
            jets = events[i][4]
            for idv in range(len(dvs1)):
                for jdv in range(len(dvs2)):
                    dv1, dv2 = getDVMatrix(dvs1[idv]), getDVMatrix(dvs2[jdv])
                    cov1, cov2 = getCovarianceMatrix(covs1[idv]), getCovarianceMatrix(covs2[jdv])
                    distance = getDistance(dv1, dv2)
                    sig = getSignificance(dv1, dv2, cov1, cov2)

                    dv_rxy1 = dvs1[idv][4]
                    dv_rxy2 = dvs2[jdv][4]
                    region1 = getRegion(dv_rxy1)
                    region2 = getRegion(dv_rxy2)
                    tracks1, nTracks_dv1, nTracksSel_dv1 = getDVTracks(dvtracks1[idv])
                    tracks2, nTracks_dv2, nTracksSel_dv2 = getDVTracks(dvtracks2[jdv])

                    nTracks = nTracks_dv1 + nTracks_dv2
                    mergedDV = tracks1 + tracks2
                    mergedMass = mergedDV.M()

                    closestJet = getClosestJet(dvs1[idv], jets)
                    dR_jetDV = closestJet.DeltaR(mergedDV)
                    dR_DVDV = tracks1.DeltaR(tracks2)
                    dPhi_DVDV = tracks1.DeltaPhi(tracks2)
                    dR_jetDV1 = closestJet.DeltaR(tracks1)
                    dR_jetDV2 = closestJet.DeltaR(tracks2)

                    h_sig_mixed.Fill(sig)
                    h_distance_mixed.Fill(distance)
                    h_dR_jetDV_mixed.Fill(dR_jetDV)
                    h_dR_jetDV1_mixed.Fill(dR_jetDV1)
                    h_dR_jetDV2_mixed.Fill(dR_jetDV2)
                    h_dR_DVDV_mixed.Fill(dR_DVDV)
                    h_dPhi_DVDV_mixed.Fill(dPhi_DVDV)
                    # region
                    h_dR_jetDV_mixed_region[region1].Fill(dR_jetDV)
                    h_dR_jetDV1_mixed_region[region1].Fill(dR_jetDV1)
                    h_dR_jetDV2_mixed_region[region1].Fill(dR_jetDV2)
                    h_dR_DVDV_mixed_region[region1].Fill(dR_DVDV)
                    h_dPhi_DVDV_mixed_region[region1].Fill(dPhi_DVDV)
                    h_distance_mixed_region[region1].Fill(distance)

                    # Weight
                    if (doWeight):
                        if region1 == -1:
                            continue
                        ratioFile = r.TFile("ratio_insideMaterial.root", "READ")
                        sig4Ratio = ratioFile.Get("sig4_ratio")
                        sig4Ratio_region = ratioFile.Get("sig_4_{}_ratio".format(regions[region1]))
                        sig5Ratio = ratioFile.Get("sig5_ratio")
                        sig5Ratio_region = ratioFile.Get("sig_5_{}_ratio".format(regions[region1]))
                        sig6Ratio = ratioFile.Get("sig6_ratio")
                        sig6Ratio_region = ratioFile.Get("sig_6_{}_ratio".format(regions[region1]))
                        
                        dRRatio = ratioFile.Get("dR_jetDV2_ratio")
                        dRRatio_region = ratioFile.Get("dR_jetDV2_{}_ratio".format(regions[region1]))
                        sigBin = h_sig_mixed.FindBin(sig)
                        #if (sigBin < bin1):
                        if (sig < 100.):
                            sig4Weight = 1 - sig4Ratio.GetBinContent(sigBin)
                            sig4Weight_region = 1 - sig4Ratio_region.GetBinContent(sigBin)
                            sig5Weight = 1 - sig5Ratio.GetBinContent(sigBin)
                            sig5Weight_region = 1 - sig6Ratio_region.GetBinContent(sigBin)
                            sig6Weight = 1 - sig6Ratio.GetBinContent(sigBin)
                            sig6Weight_region = 1 - sig6Ratio_region.GetBinContent(sigBin)
                            if (sig4Weight < 0):
                                sig4Weight = 0
                            if (sig5Weight < 0):
                                sig5Weight = 0
                            if (sig6Weight < 0):
                                sig6Weight = 0
                            if (sig4Weight_region < 0):
                                sig4Weight_region = 0
                            if (sig5Weight_region < 0):
                                sig5Weight_region = 0
                            if (sig6Weight_region < 0):
                                sig6Weight_region = 0
                        else:
                            sig4Weight = 0
                            sig4Weight_region = 0
                            sig5Weight = 0
                            sig5Weight_region = 0
                            sig6Weight = 0
                            sig6Weight_region = 0
                        drBin = h_dR_jetDV2_mixed.FindBin(dR_jetDV2)
                        drWeight = dRRatio.GetBinContent(drBin)
                        drWeight_region = dRRatio_region.GetBinContent(drBin)
                        weight4 = sig4Weight * drWeight
                        weight4_region = sig4Weight_region * drWeight_region
                        weight5 = sig5Weight * drWeight
                        weight5_region = sig5Weight_region * drWeight_region
                        weight6 = sig6Weight * drWeight
                        weight6_region = sig6Weight_region * drWeight_region

                    if (nTracks == 4):
                        h_sig4_mixed.Fill(sig)
                        h_mergedMass4_mixed.Fill(mergedMass)
                        h_sig4_mixed_region[region1].Fill(sig)
                        h_mergedMass4_region[region1].Fill(mergedMass)

                        if (doWeight):
                            h_mergedMass4_sigWeight_noSigCut.Fill(mergedMass, sig4Weight)
                            h_mergedMass4_sigWeight_noSigCut_region[region1].Fill(mergedMass, sig4Weight_region)
                            h_mergedMass4_dRWeight_noSigCut.Fill(mergedMass, drWeight)
                            h_mergedMass4_dRWeight_noSigCut_region[region1].Fill(mergedMass, drWeight_region)
                            h_mergedMass4_weight_noSigCut.Fill(mergedMass, weight4)
                            h_mergedMass4_weight_noSigCut_region[region1].Fill(mergedMass, weight4_region)
                        if (sig < 100.):
                            h_mergedMass4_sig100Cut.Fill(mergedMass)
                            h_mergedMass4_sig100Cut_region[region1].Fill(mergedMass)
                            if (doWeight):
                                h_mergedMass4_sigWeight.Fill(mergedMass, sig4Weight)
                                h_mergedMass4_dRWeight.Fill(mergedMass, drWeight)
                                h_mergedMass4_weight.Fill(mergedMass, weight4)
                                h_mergedMass4_sigWeight_region[region1].Fill(mergedMass, sig4Weight_region)
                                h_mergedMass4_dRWeight_region[region1].Fill(mergedMass, drWeight_region)
                                h_mergedMass4_weight_region[region1].Fill(mergedMass, weight4_region)
                    if (nTracks == 5):
                        h_sig5_mixed.Fill(sig)
                        h_mergedMass5_mixed.Fill(mergedMass)
                        h_sig5_mixed_region[region1].Fill(sig)
                        h_mergedMass5_region[region1].Fill(mergedMass)
                        if (doWeight):
                            h_mergedMass5_sigWeight_noSigCut.Fill(mergedMass, sig5Weight)
                            h_mergedMass5_sigWeight_noSigCut_region[region1].Fill(mergedMass, sig5Weight_region)
                            h_mergedMass5_dRWeight_noSigCut.Fill(mergedMass, drWeight)
                            h_mergedMass5_dRWeight_noSigCut_region[region1].Fill(mergedMass, drWeight_region)
                            h_mergedMass5_weight_noSigCut.Fill(mergedMass, weight5)
                            h_mergedMass5_weight_noSigCut_region[region1].Fill(mergedMass, weight5_region)
                        if (sig < 100.):
                            h_mergedMass5_sig100Cut.Fill(mergedMass)
                            h_mergedMass5_sig100Cut_region[region1].Fill(mergedMass)
                            if (doWeight):
                                h_mergedMass5_sigWeight.Fill(mergedMass, sig5Weight)
                                h_mergedMass5_dRWeight.Fill(mergedMass, drWeight)
                                h_mergedMass5_weight.Fill(mergedMass, weight5)
                                h_mergedMass5_sigWeight_region[region1].Fill(mergedMass, sig5Weight_region)
                                h_mergedMass5_dRWeight_region[region1].Fill(mergedMass, drWeight_region)
                                h_mergedMass5_weight_region[region1].Fill(mergedMass, weight5_region)
                    if (nTracks == 6):
                        h_sig6_mixed.Fill(sig)
                        h_mergedMass6_mixed.Fill(mergedMass)
                        h_sig6_mixed_region[region1].Fill(sig)
                        h_mergedMass6_region[region1].Fill(mergedMass)
                        if (doWeight):
                            h_mergedMass6_sigWeight_noSigCut.Fill(mergedMass, sig6Weight)
                            h_mergedMass6_sigWeight_noSigCut_region[region1].Fill(mergedMass, sig6Weight_region)
                            h_mergedMass6_dRWeight_noSigCut.Fill(mergedMass, drWeight)
                            h_mergedMass6_dRWeight_noSigCut_region[region1].Fill(mergedMass, drWeight_region)
                            h_mergedMass6_weight_noSigCut.Fill(mergedMass, weight6)
                            h_mergedMass6_weight_noSigCut_region[region1].Fill(mergedMass, weight6_region)
                        if (sig < 100.):
                            h_mergedMass6_sig100Cut.Fill(mergedMass)
                            h_mergedMass6_sig100Cut_region[region1].Fill(mergedMass)
                            if (doWeight):
                                h_mergedMass6_sigWeight.Fill(mergedMass, sig6Weight)
                                h_mergedMass6_dRWeight.Fill(mergedMass, drWeight)
                                h_mergedMass6_weight.Fill(mergedMass, weight6)
                                h_mergedMass6_sigWeight_region[region1].Fill(mergedMass, sig6Weight_region)
                                h_mergedMass6_dRWeight_region[region1].Fill(mergedMass, drWeight_region)
                                h_mergedMass6_weight_region[region1].Fill(mergedMass, weight6_region)
                            
        print("Looping for DV mass calculation")
        for iEvent in range(len(events)):
            dvs = events[iEvent][1]
            dvtracks = events[iEvent][2]
            for idv in range(len(dvs)):
                tracks, nTracks, nTracksSel= getDVTracks(dvtracks[idv])
                dv_m = tracks.M()
                dv_rxy = dvs[idv][4]
                region = getRegion(dv_rxy)
                
                h_DV_m.Fill(dv_m)
                h_DV_m_region[region].Fill(dv_m)
                h_recoDV_m.Fill(dvs[idv][3])
                h_recoDV_m_region[region].Fill(dvs[idv][3])
                if (nTracks == 2):
                    h_DV_m_2track.Fill(dv_m)
                    h_DV_m_2track_region[region].Fill(dv_m)
                    h_recoDV_m_2track.Fill(dvs[idv][3])
                    h_recoDV_m_2track_region[region].Fill(dvs[idv][3])
                if (nTracks == 3):
                    h_DV_m_3track.Fill(dv_m)
                    h_DV_m_3track_region[region].Fill(dv_m)
                    h_recoDV_m_3track.Fill(dvs[idv][3])
                    h_recoDV_m_3track_region[region].Fill(dvs[idv][3])
                if (nTracks == 4):
                    h_DV_m_4track.Fill(dv_m)
                    h_DV_m_4track_region[region].Fill(dv_m)
                    h_recoDV_m_4track.Fill(dvs[idv][3])
                    h_recoDV_m_4track_region[region].Fill(dvs[idv][3])
                if (nTracks == 5):
                    h_DV_m_5track.Fill(dv_m)
                    h_DV_m_5track_region[region].Fill(dv_m)
                    h_recoDV_m_5track.Fill(dvs[idv][3])
                    h_recoDV_m_5track_region[region].Fill(dvs[idv][3])
                if (nTracks == 6):
                    h_DV_m_6track.Fill(dv_m)
                    h_DV_m_6track_region[region].Fill(dv_m)
                    h_recoDV_m_6track.Fill(dvs[idv][3])
                    h_recoDV_m_6track_region[region].Fill(dvs[idv][3])
                if (nTracks == 7):
                    h_DV_m_7track.Fill(dv_m)
                    h_DV_m_7track_region[region].Fill(dv_m)
                    h_recoDV_m_7track.Fill(dvs[idv][3])
                    h_recoDV_m_7track_region[region].Fill(dvs[idv][3])
                    

        outputFile.Write()
        outputFile.Close()
        nFile += 1
    else:
        break

import os, datetime
import ROOT as r
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from plotHelper import *

r.gROOT.SetBatch()
SetAtlasStyle()

label = "Work in Progress"

c1 = r.TCanvas("c1", "c1", 800, 600)
inputFile = r.TFile("run2_full_weighted.root", "READ")
oldFile = r.TFile("recoMass_run2Full.root", "READ")

date = str(datetime.date.today())
directory = str(os.getcwd()) + "/plots/" + date + "/mass"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

outputFile = r.TFile("massHists.root", "RECREATE")

# Get mass histograms
h_recoMass4, h_dvmass4, h_mergedMass4, h_mergedMass4_reweight, h_mergedMass4_sigWeight = getMassHist(inputFile, 4, 5)
h_recoMass5, h_dvmass5, h_mergedMass5, h_mergedMass5_reweight, h_mergedMass5_sigWeight = getMassHist(inputFile, 5, 5)
h_recoMass6, h_dvmass6, h_mergedMass6, h_mergedMass6_reweight, h_mergedMass6_sigWeight = getMassHist(inputFile, 6, 5)
# Get mass from old ntuple
h_oldMass4 = oldFile.Get("mass4").Rebin(5)
h_oldMass4_inside_BP = oldFile.Get("mass4_inside_BP").Rebin(5)
h_oldMass4_inside_IBL = oldFile.Get("mass4_inside_IBL").Rebin(5)
h_oldMass4_PIX = oldFile.Get("mass4_PIX").Rebin(5)
h_oldMass4_inside_SCT = oldFile.Get("mass4_inside_SCT").Rebin(5)
oldHists_region = [h_oldMass4_inside_BP, h_oldMass4_inside_IBL, h_oldMass4_PIX, h_oldMass4_inside_SCT]

h_recoMass4.Write()
h_recoMass5.Write()
h_recoMass6.Write()
h_dvmass4.Write()
h_dvmass5.Write()
h_dvmass6.Write()

recoAndReweight = [h_recoMass4, h_dvmass4, h_mergedMass4_sigWeight, h_mergedMass4_reweight]
legList = ["Reconstructed", "calculated", "Weighted with sig", "Weighted with sig #times dR"]
MassHists(c1, recoAndReweight, legList, directory, "recoAndReweight4_logy", label, logy=True)
MassHists(c1, recoAndReweight, legList, directory, "recoAndReweight4", label, logy=False)

recoAndReweight.append(h_oldMass4)
legList.append("old ntuple")

oldAndNew = [h_recoMass4, h_dvmass4, h_oldMass4]
legOldAndNew = ["Reconstructed", "Calculated", "Reconstructed (old ntuple)"]
MassHists(c1, oldAndNew, legOldAndNew, directory, "oldAndNew_logy", label, logy=True)

regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]

recoMass4_region = []
dvmass4_region = []
mergedMass4_region = []
mergedMass4_reweight_region = []
mergedMass4_sigWeight_region = []
for i in range(len(regions)):
    recoMass4_region.append(inputFile.Get("recoDV_m_4track_{}".format(regions[i])).Rebin(5))
    dvmass4_region.append(inputFile.Get("DV_m_4track_{}".format(regions[i])).Rebin(5))
    mergedMass4_region.append(inputFile.Get("mergedMass4_{}".format(regions[i])).Rebin(5))
    mergedMass4_reweight_region.append(inputFile.Get("mergedMass4_weight_{}".format(regions[i])).Rebin(5))
    mergedMass4_sigWeight_region.append(inputFile.Get("mergedMass4_sigWeight_{}".format(regions[i])).Rebin(5))

for i in range(len(recoMass4_region)):
    bin1 = h_recoMass4.FindBin(100)
    recoMass4_region[i].GetXaxis().SetRange(0, bin1)
    dvmass4_region[i].GetXaxis().SetRange(0, bin1)
    histList = [recoMass4_region[i], dvmass4_region[i], mergedMass4_reweight_region[i], mergedMass4_sigWeight_region[i], oldHists_region[i]]
    MassHists(c1, histList, legList, directory, "recoAndReweight4_{}_logy".format(regions[i]), label, logy=True)
    massList = [recoMass4_region[i], dvmass4_region[i], oldHists_region[i]]
    MassHists(c1, massList, legOldAndNew, directory, "oldAndNew_{}_logy".format(regions[i]), label, logy=True)

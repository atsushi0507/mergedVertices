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

date = str(datetime.date.today())
directory = str(os.getcwd()) + "/plots/" + date + "/mass"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

outputFile = r.TFile("massHists.root", "RECREATE")

# Get mass histograms
h_recoMass4, h_dvmass4, h_mergedMass4, h_mergedMass4_reweight, h_mergedMass4_sigWeight = getMassHist(inputFile, 4, 20)
h_recoMass5, h_dvmass5, h_mergedMass5, h_mergedMass5_reweight, h_mergedMass5_sigWeight = getMassHist(inputFile, 5, 20)
h_recoMass6, h_dvmass6, h_mergedMass6, h_mergedMass6_reweight, h_mergedMass6_sigWeight = getMassHist(inputFile, 6, 20)

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

regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]

recoMass4_region = []
dvmass4_region = []
mergedMass4_region = []
mergedMass4_reweight_region = []
mergedMass4_sigWeight_region = []
for i in range(len(regions)):
    recoMass4_region.append(inputFile.Get("recoDV_m_4track_{}".format(regions[i])).Rebin(20))
    dvmass4_region.append(inputFile.Get("DV_m_4track_{}".format(regions[i])).Rebin(20))
    mergedMass4_region.append(inputFile.Get("mergedMass4_{}".format(regions[i])).Rebin(20))
    mergedMass4_reweight_region.append(inputFile.Get("mergedMass4_weight_{}".format(regions[i])).Rebin(20))
    mergedMass4_sigWeight_region.append(inputFile.Get("mergedMass4_sigWeight_{}".format(regions[i])).Rebin(20))

for i in range(len(recoMass4_region)):
    bin1 = h_recoMass4.FindBin(100)
    recoMass4_region[i].GetXaxis().SetRange(0, bin1)
    dvmass4_region[i].GetXaxis().SetRange(0, bin1)
    histList = [recoMass4_region[i], dvmass4_region[i], mergedMass4_reweight_region[i], mergedMass4_sigWeight_region[i]]
    MassHists(c1, histList, legList, directory, "recoAndReweight4_{}_logy".format(regions[i]), label, logy=True)

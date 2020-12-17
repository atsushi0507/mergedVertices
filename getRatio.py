import ROOT as r
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from plotHelper import *
import argparse
import datetime, os

r.gROOT.SetBatch()
SetAtlasStyle()

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFileName", help="Choose inputFile", default="run2_full.root")
args = p.parse_args()

inputFile = args.inputFileName
inFile = r.TFile(inputFile, "READ")

date = str(datetime.date.today())
directory = str(os.getcwd()) + "/plots/" + date + "/ratio"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

label = "Work in Progress"

outputFile = r.TFile("ratio.root", "RECREATE")
c = r.TCanvas("c", "c", 800, 600)
sig4_same, sig4 = getHists(inFile, "sig4")
bin1 = sig4.FindBin(100)
bin2 = sig4.GetNbinsX() + 1
sf4trk = getSF(sig4_same, sig4, bin1, bin2)
sig4.Sumw2()
sig4.Scale(sf4trk)
h_ratio4track = getRatio(sig4_same, sig4)
ratioPlot(sig4_same, sig4, directory, "ratio4track", label)
# Zoomed
sig4_same_zoomed = sig4_same.Clone("same_zoomed")
sig4_zoomed = sig4.Clone("mixed_zoomed")
sig4_same_zoomed.GetXaxis().SetRange(1, bin1)
sig4_zoomed.GetXaxis().SetRange(1, bin1+1)
h_ratio4track_zoomed = getRatio(sig4_same_zoomed, sig4_zoomed)
ratioPlot(sig4_same_zoomed, sig4_zoomed, directory, "ratio4track_zoomed", label)

# Region definition
regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]

sig4_same_region = []
sig4_region = []
for region in regions:
    sig4_same_region.append(inFile.Get("sig_4_same_{}".format(region)))
    sig4_region.append(inFile.Get("sig_4_mixed_{}".format(region)))
    
h_ratio_region = []
for i in range(len(sig4_region)):
    sf = sig4_same_region[i].Integral(bin1, bin2) / sig4_region[i].Integral(bin1, bin2)
    sig4_region[i].Sumw2()
    sig4_region[i].Scale(sf)
    h_ratio_region.append(getRatio(sig4_same_region[i], sig4_region[i]))
    ratioPlot(sig4_same_region[i], sig4_region[i], directory, "ratio4track_{}".format(regions[i]), label)

for ratio in h_ratio_region:
    ratio.Write()

# DV-Jet
h_dRJetDV1_same, h_dRJetDV1_mixed = getHists(inFile, "dR_jetDV1")
h_dRJetDV1_same.Sumw2()
h_dRJetDV1_same.Scale(1./h_dRJetDV1_same.Integral())
h_dRJetDV1_mixed.Sumw2()
h_dRJetDV1_mixed.Scale(1./h_dRJetDV1_mixed.Integral())
dRJetDV1_ratio = getRatio(h_dRJetDV1_same, h_dRJetDV1_mixed)
ratioPlot(h_dRJetDV1_same, h_dRJetDV1_mixed, directory, "dRJetDV1_ratio", label)

h_dRJetDV2_same, h_dRJetDV2_mixed = getHists(inFile, "dR_jetDV2")
h_dRJetDV2_same.Sumw2()
h_dRJetDV2_same.Scale(1./h_dRJetDV2_same.Integral())
h_dRJetDV2_mixed.Sumw2()
h_dRJetDV2_mixed.Scale(1./h_dRJetDV2_mixed.Integral())
dRJetDV2_ratio = getRatio(h_dRJetDV2_same, h_dRJetDV2_mixed)
ratioPlot(h_dRJetDV2_same, h_dRJetDV2_mixed, directory, "dRJetDV2_ratio", label)

h_dRJetDV_same, h_dRJetDV_mixed = getHists(inFile, "dR_jetDV")
h_dRJetDV_same.Sumw2()
h_dRJetDV_same.Scale(1./h_dRJetDV_same.Integral())
h_dRJetDV_mixed.Sumw2()
h_dRJetDV_mixed.Scale(1./h_dRJetDV_mixed.Integral())
dRJetDV_ratio = getRatio(h_dRJetDV_same, h_dRJetDV_mixed)
ratioPlot(h_dRJetDV_same, h_dRJetDV_mixed, directory, "dRJetDV_ratio", label)

dR_jetDV1_same_region = []
dR_jetDV1_region = []
dR_jetDV2_same_region = []
dR_jetDV2_region = []
dR_jetDV_same_region = []
dR_jetDV_region = []
for region in regions:
    dR_jetDV1_same_region.append(inFile.Get("dR_jetDV1_same_{}".format(region)))
    dR_jetDV1_region.append(inFile.Get("dR_jetDV1_mixed_{}".format(region)))
    dR_jetDV2_same_region.append(inFile.Get("dR_jetDV2_same_{}".format(region)))
    dR_jetDV2_region.append(inFile.Get("dR_jetDV2_mixed_{}".format(region)))
    dR_jetDV_same_region.append(inFile.Get("dR_jetDV_same_{}".format(region)))
    dR_jetDV_region.append(inFile.Get("dR_jetDV_mixed_{}".format(region)))

h_dR_jetDV1_ratio_region = []
h_dR_jetDV2_ratio_region = []
h_dR_jetDV_ratio_region = []
for i in range(len(dR_jetDV1_region)):
    dR_jetDV1_same_region[i].Sumw2()
    dR_jetDV1_region[i].Sumw2()
    dR_jetDV2_same_region[i].Sumw2()
    dR_jetDV2_region[i].Sumw2()
    dR_jetDV_same_region[i].Sumw2()
    dR_jetDV_region[i].Sumw2()
    
    dR_jetDV1_same_region[i].Scale(1./dR_jetDV1_same_region[i].Integral())
    dR_jetDV1_region[i].Scale(1./dR_jetDV1_region[i].Integral())
    dR_jetDV2_same_region[i].Scale(1./dR_jetDV2_same_region[i].Integral())
    dR_jetDV2_region[i].Scale(1./dR_jetDV2_region[i].Integral())
    dR_jetDV_same_region[i].Scale(1./dR_jetDV_same_region[i].Integral())
    dR_jetDV_region[i].Scale(1./dR_jetDV_region[i].Integral())
    h_dR_jetDV1_ratio_region.append(getRatio(dR_jetDV1_same_region[i], dR_jetDV1_region[i]))
    h_dR_jetDV2_ratio_region.append(getRatio(dR_jetDV2_same_region[i], dR_jetDV2_region[i]))
    h_dR_jetDV_ratio_region.append(getRatio(dR_jetDV_same_region[i], dR_jetDV_region[i]))
    
    ratioPlot(dR_jetDV1_same_region[i], dR_jetDV1_region[i], directory, "dRjetDV1_ratio_{}".format(regions[i]), label)
    ratioPlot(dR_jetDV2_same_region[i], dR_jetDV2_region[i], directory, "dRjetDV2_ratio_{}".format(regions[i]), label)
    ratioPlot(dR_jetDV_same_region[i], dR_jetDV_region[i], directory, "dRjetDV_ratio_{}".format(regions[i]), label)

for i in range(len(h_dR_jetDV1_ratio_region)):
    h_dR_jetDV1_ratio_region[i].Write()
    h_dR_jetDV2_ratio_region[i].Write()
    h_dR_jetDV_ratio_region[i].Write()
    
h_ratio4track.Write()
dRJetDV1_ratio.Write()
dRJetDV2_ratio.Write()
dRJetDV_ratio.Write()

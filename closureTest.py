import ROOT as r
import os, datetime

# For AM's environment
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
SetAtlasStyle()

r.gROOT.SetBatch()

label = "Internal"
date = str(datetime.date.today())
directory = "plots/" + date + "/" + "closure"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("run2_full_weighted.root", "READ")
regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]
colors = [r.kBlack, r.kRed, r.kBlue, r.kOrange, r.kGreen, r.kMagenta, r.kCyan]

bin = 5

def getSF(h_same, h_mixed, bin1, bin2):
    sf = []
    for i in range(len(h_same)):
        try:
            scaleFactor = h_same[i].Integral(bin1, bin2) / h_mixed[i].Integral(bin1, bin2)
            sf.append(scaleFactor)
        except ZeroDivisionError:
            print("ZeroDivisionError: Scale Factor is set to 0.")
            scaleFactor = 0.
            sf.append(scaleFactor)
    return sf

def getHists(inputFile, nTracks, bin):
    h_same = []
    h_mixed = []
    h_same.append(inputFile.Get("sig{}_same".format(nTracks)).Rebin(bin))
    h_mixed.append(inputFile.Get("sig{}_mixed".format(nTracks)).Rebin(bin))
    for region in regions:
        h_same.append(inputFile.Get("sig_{}_same_{}".format(nTracks, region)).Rebin(bin))
        h_mixed.append(inputFile.Get("sig_{}_mixed_{}".format(nTracks, region)).Rebin(bin))
    return h_same, h_mixed

def getClonedHists(h_mixed):
    h_predictMV = []
    h_samePredict = []
    h_diff = []
    for hist in h_mixed:
        name = hist.GetName()
        h_predictMV.append(hist.Clone(name + "_predictMV"))
        h_samePredict.append(hist.Clone(name + "_samePredict"))
        h_diff.append(hist.Clone(name + "_diff"))
    return [h_predictMV, h_samePredict, h_diff]

def getRatio(h_same, h_mixed):
    h_ratios = []
    for i in range(len(h_same)):
        h_ratio = h_same[i].Clone("{}_ratio".format(h_same[i].GetName()))
        h_ratio.Divide(h_mixed[i])
        h_ratios.append(h_ratio)
    return h_ratios

def calc(h_same, histList, h_ratio):
    h_predictMVs = []
    h_samePredicts = []
    h_diffs = []
    for i in range(len(h_same)):
        h_predictMV = histList[0][i].Clone("{}_predictMV".format(histList[0][i].GetName()))
        h_samePredict = histList[1][i].Clone("{}_samePredict".format(histList[1][i].GetName()))
        h_diff = histList[2][i].Clone("{}_diff".format(histList[2][i].GetName()))

        h_samePredict.Multiply(h_ratio[i])
        h_diff.Add(h_same[i], -1)
        h_predictMV.Add(h_samePredict, -1)

        """
        print(histList[0][i].GetName())
        print(h_diff.Integral(1, bin1), h_diff.Integral(bin1, bin2))
        print(h_predictMV.Integral(1, bin1), h_predictMV.Integral(bin1, bin2))
        """

        h_predictMVs.append(h_predictMV)
        h_samePredicts.append(h_samePredict)
        h_diffs.append(h_diff)
    return h_samePredicts, h_diffs, h_predictMVs

def DrawHists(hists, legs, bin1, bin2, outputName):
    leg = r.TLegend(0.65, 0.65, 0.85, 0.88)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    c1 = r.TCanvas("c1", "c1", 800, 600)
    c1.SetTopMargin(0.075)

    maximum = -1e8
    minimum = 1e8
    for i in range(len(hists)):
        tmpMax = hists[i].GetMaximum()
        tmpMin = hists[i].GetMinimum()
        if (tmpMax > maximum):
            maximum = tmpMax
        if (tmpMin < minimum):
            minimum = tmpMin
        hists[i].SetLineColor(colors[i])
        leg.AddEntry(hists[i], legs[i], "l")
    hists[0].SetMaximum(maximum * 1.1)
    hists[0].SetMinimum(minimum * 1.1)
    hists[0].Draw("axis")
    for i in range(len(hists)):
        hists[i].Draw("hist same")
    leg.Draw()
    ATLASLabel(0.205, 0.945, label)
    c1.Print("{}/{}.pdf".format(directory, outputName))


### Main program start here ###
c = r.TCanvas("c", "c", 800, 600)

h_same4, h_mixed4 = getHists(inputFile, 4, bin)
h_same5, h_mixed5 = getHists(inputFile, 5, bin)
h_same6, h_mixed6 = getHists(inputFile, 6, bin)
bin1 = h_same4[0].FindBin(100.)
bin2 = h_same4[0].GetNbinsX()
sf4 = getSF(h_same4, h_mixed4, bin1, bin2)
sf5 = getSF(h_same5, h_mixed5, bin1, bin2)
sf6 = getSF(h_same6, h_mixed6, bin1, bin2)
for i in range(len(h_mixed4)):
    h_mixed4[i].Scale(sf4[i])
    h_mixed5[i].Scale(sf5[i])
    h_mixed6[i].Scale(sf6[i])

ratios4 = getRatio(h_same4, h_mixed4)

histList4 = getClonedHists(h_mixed4)
histList5 = getClonedHists(h_mixed5)
histList6 = getClonedHists(h_mixed6)
h_samePredicts4, h_diffs4, h_predictMVs4 = calc(h_same4, histList4, ratios4)
h_samePredicts5, h_diffs5, h_predictMVs5 = calc(h_same5, histList5, ratios4)
h_samePredicts6, h_diffs6, h_predictMVs6 = calc(h_same6, histList6, ratios4)

legList = ["same", "mixed", "predicted same"]
legList_full = ["same", "mixed", "samePredicted", "mixed - same", "mixed - samePredicted"]
outputNameList = ["", "_inside_BP", "_inside_IBL", "_PIX", "_inside_SCT"]

for i in range(len(h_same4)):
    hists4 = [h_same4[i], h_mixed4[i], h_samePredicts4[i]]
    hists5 = [h_same5[i], h_mixed5[i], h_samePredicts5[i], h_diffs5[i], h_predictMVs5[i]]
    hists6 = [h_same6[i], h_mixed6[i], h_samePredicts6[i], h_diffs6[i], h_predictMVs6[i]]
    DrawHists(hists4, legList, bin1, bin2, "sig4"+outputNameList[i])
    DrawHists(hists5, legList_full, bin1, bin2, "sig5"+outputNameList[i])
    DrawHists(hists6, legList_full, bin1, bin2, "sig6"+outputNameList[i])

### 2021.01.21, add new idea about samePredict
ratio4 = ratios4[0]

h_same5 = inputFile.Get("sig5_same")
h_mixed5 = inputFile.Get("sig5_mixed")

h_samePredicted5 = h_mixed5.Clone("samePredicted5")
h_samePredicted5.Multiply(ratio4)

h_mixed5.SetLineColor(r.kRed)
h_samePredicted5.SetLineColor(r.kBlue)

h_same5.Draw("hist")
h_mixed5.Draw("same hist")
h_samePredicted5.Draw("same hist")
c.Print("{}/samePredicted5.pdf".format(directory))

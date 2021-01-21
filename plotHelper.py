import ROOT as r
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasLabel import *
from AtlasStyle import *

def getHists(dataFile, histName):
    h_same = dataFile.Get(histName + "_same")
    h_mixed = dataFile.Get(histName + "_mixed")
    return h_same, h_mixed

def getSF(h_same, h_mixed, bin1, bin2):
    try:
        scaleFactor = h_same.Integral(bin1, bin2) / h_mixed.Integral(bin1, bin2)
    except ZeroDivisionError:
        print("ZeroDivisionError: Scale factor is set to 0.")
        scaleFactor = 0.
    return scaleFactor

def getRatio(h_same, h_mixed):
    h_ratio = h_same.Clone("{}_ratio".format((h_same.GetName()).replace("_same", "")))
    h_ratio.Divide(h_mixed)
    return h_ratio

def ratioPlot(h_same, h_mixed, directory, outputName, label):
    c1 = r.TCanvas("c1", "c1", 800, 600)
    h_mixed.SetLineColor(r.kRed)

    leg = r.TLegend(0.75, 0.70, 0.88, 0.80)
    leg.AddEntry(h_same, "Same", "l")
    leg.AddEntry(h_mixed, "Mixed", "l")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    maximum = -999
    if (h_same.GetMaximum() > h_mixed.GetMaximum()):
        maximum = h_same.GetMaximum() * 1.1
    else:
        maximum = h_mixed.GetMaximum() * 1.1

    h_same.SetMaximum(maximum)
    h_same.SetMinimum(0.0)

    rp = r.TRatioPlot(h_same, h_mixed)
    rp.SetH2DrawOpt("hist")
    rp.Draw()
    rp.GetLowerRefGraph().SetMaximum(3.0)
    rp.GetLowerRefGraph().SetMinimum(0.0)
    rp.GetLowYaxis().SetNdivisions(4)

    rp.GetLowerRefYaxis().SetTitle("#frac{Same}{Mixed}")
    rp.SetSeparationMargin(0.02)
    rp.SetLeftMargin(0.1575)
    rp.SetLowBottomMargin(0.50)

    c1.SetTicks(0,0)
    leg.Draw()
    ATLASLabel(0.175, 0.945, label)
    c1.Update()
    c1.Print("{}/{}.pdf".format(directory, outputName))

def getMassHist(inFile, nTracks=4, rebin=1):
    h_reco = inFile.Get("recoDV_m_{}track".format(nTracks)).Rebin(rebin)
    h_dvmass = inFile.Get("DV_m_{}track".format(nTracks)).Rebin(rebin)
    h_mergedMass = inFile.Get("mergedMass{}_mixed".format(nTracks)).Rebin(rebin)
    h_mergedMass_reweight = inFile.Get("mergedMass{}_weight".format(nTracks)).Rebin(rebin)
    h_mergedMass_sigWeight = inFile.Get("mergedMass{}_sigWeight".format(nTracks)).Rebin(rebin)

    bin = h_reco.FindBin(99)
    h_reco.GetXaxis().SetRange(0, bin)
    h_dvmass.GetXaxis().SetRange(0, bin)
    return h_reco, h_dvmass, h_mergedMass, h_mergedMass_reweight, h_mergedMass_sigWeight

def MassHists(c1, massHists, legs, directory, outputName, label, logy=True):
    colors = [r.kBlack, r.kRed, r.kBlue, r.kOrange, r.kGreen, r.kMagenta, r.kCyan]

    leg = r.TLegend(0.55, 0.65, 0.85, 0.85)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    maximum = -1e10
    minimum = 1e10
    if (logy):
        r.gPad.SetLogy(1)
    else:
        r.gPad.SetLogy(0)
    for i in range(len(massHists)):
        tmpMax = massHists[i].GetMaximum()
        tmpMin = massHists[i].GetMinimum()
        if (tmpMax > maximum):
            maximum = tmpMax
        if (tmpMin < minimum):
            minimum = tmpMin
        massHists[i].SetLineColor(colors[i])
        massHists[i].SetMarkerColor(colors[i])
        leg.AddEntry(massHists[i], legs[i], "l")
    massHists[0].SetMaximum(maximum*1.1)
    massHists[0].Draw("axis")
    for i in range(len(massHists)):
        massHists[i].Draw("hist same")
    leg.Draw()
    ATLASLabel(0.175, 0.945, label)
    c1.Print("{}/{}.pdf".format(directory, outputName))
        

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
    ATLASLabel(0.50, 0.85, label)
    c1.Update()
    c1.Print("{}/{}.pdf".format(directory, outputName))

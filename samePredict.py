import ROOT as r
import os, datetime
import sys
#sys.path.append("/Users/amizukam/DVJets/atlasstyle")
sys.path.append("/Users/atsushi/mvstudy_dv")
from AtlasStyle import *
from AtlasLabel import *
SetAtlasStyle()

r.gROOT.SetBatch()

label = "Internal"
date = str(datetime.date.today())
directory = "plots/" + date + "/test"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("run2_full_weighted.root", "READ")
c1 = r.TCanvas("c1", "c1", 800, 600)

rebin = 2
h_same4 = inputFile.Get("sig4_same").Rebin(rebin)
h_mixed4 = inputFile.Get("sig4_mixed").Rebin(rebin)
h_same5 = inputFile.Get("sig5_same").Rebin(rebin)
h_mixed5 = inputFile.Get("sig5_mixed").Rebin(rebin)

h_mixed4.Sumw2()
h_mixed5.Sumw2()

bin1 = h_same4.FindBin(100.)
bin2 = h_same4.GetNbinsX()+1

sf4 = h_same4.Integral(bin1, bin2) / h_mixed4.Integral(bin1, bin2)
sf5 = h_same5.Integral(bin1, bin2) / h_mixed5.Integral(bin1, bin2)

h_mixed4.Scale(sf4)

h_ratio4 = h_same4.Clone("ratio4")
h_ratio4.Divide(h_mixed4)

h_samePredict4 = h_mixed4.Clone("h_samePredict4")
h_samePredict4.Multiply(h_ratio4)

h_mixed4.SetLineColor(r.kRed)
h_samePredict4.SetLineColor(r.kBlue)
h_samePredict4.SetMarkerColor(r.kBlue)

h_same4.Draw("hist")
h_mixed4.Draw("hist same")
h_samePredict4.Draw("hist same e0")
c1.Print("{}/hist4.pdf".format(directory))

h_mixed5_scaled = h_mixed5.Clone("h_mixed5_scaled")
h_mixed5_scaled.Scale(sf5)
h_samePredict5_scaled = h_mixed5_scaled.Clone("h_samePredict5_scaled")
h_samePredict5_scaled.Multiply(h_ratio4)
h_samePredict5 = h_mixed5.Clone("h_samePredict5")
h_samePredict5.Multiply(h_ratio4)

h_mixed5_scaled.SetLineColor(r.kRed)
h_samePredict5_scaled.SetLineColor(r.kBlue)
h_samePredict5_scaled.SetMarkerColor(r.kBlue)

h_same5.Draw("hist")
h_mixed5_scaled.Draw("hist same")
h_samePredict5_scaled.Draw("hist same e0")
c1.Print("{}/hist5.pdf".format(directory))

h_ratio5 = h_same5.Clone("h_ratio5")
h_ratio5_predicted = h_samePredict5.Clone("h_ratio5_predicted")
h_ratio5.Divide(h_mixed5_scaled)
h_ratio5_predicted.Divide(h_mixed5)

h_ratio5_predicted.SetLineColor(r.kRed)
h_ratio5_predicted.SetMarkerColor(r.kRed)

h_ratio5.Draw("hist e0")
h_ratio5_predicted.Draw("hist e0 same")
c1.Print("{}/ratio5.pdf".format(directory))

h_samePredict5.SetLineColor(r.kBlue)
h_samePredict5.SetMarkerColor(r.kBlue)

h_mixed5.Draw("hist ")
h_samePredict5.Draw("hist same e0")
c1.Print("{}/mixed_samePredict_5track.pdf".format(directory))

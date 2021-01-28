import ROOT as r
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
#sys.path.append("/Users/atsushi/mvstudy_dv")
import os, datetime
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()

label = "Internal"

inputFile = r.TFile("run2_full_weighted.root", "READ")

date = str(datetime.date.today())
directory = os.getcwd() + "/plots/" + date + "/mergedMass"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

c1 = r.TCanvas("c1", "c1", 800, 600)

colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen+2, r.kCyan]

rebin = 20

mv4_noCut = inputFile.Get("mergedMass4_mixed").Rebin(rebin)
mv4_sigCut = inputFile.Get("mergedMass4_sig100Cut").Rebin(rebin)
mv4_sigWeight = inputFile.Get("mergedMass4_sigWeight").Rebin(rebin)
mv4_dRWeight = inputFile.Get("mergedMass4_dRWeight").Rebin(rebin)
mv4_weight = inputFile.Get("mergedMass4_weight").Rebin(rebin)

mv4 = [mv4_noCut, mv4_sigCut, mv4_sigWeight, mv4_dRWeight, mv4_weight]
legs = ["No cut and weight applied", "S < 100", "Significance weight", "dR weight", "Weight = sig #times dR"]

r.gPad.SetLogy()
l1 = r.TLegend(0.60, 0.65, 0.88, 0.88)
l1.SetFillStyle(0)
l1.SetBorderSize(0)
l1.SetTextSize(0.03)
l1.SetTextFont(42)
for i in range(len(mv4)):
    mv4[i].SetLineColor(colors[i])
    mv4[i].SetMarkerColor(colors[i])
    l1.AddEntry(mv4[i], legs[i], "l")
    if i == 0:
        mv4[i].DrawNormalized("hist")
    else:
        mv4[i].DrawNormalized("hist same")
    l1.Draw()
    ATLASLabel(0.175, 0.955, label)
c1.Print("{}/mv4.pdf".format(directory))

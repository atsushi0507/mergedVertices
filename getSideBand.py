import ROOT as r
import os, datetime
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle/")
from AtlasStyle import *
from AtlasLabel import *
label = "Internal"

SetAtlasStyle()
r.gROOT.SetBatch()

#inputFile = r.TFile("ks.root", "READ")
inputFile = r.TFile("combination.root", "READ")
date = str(datetime.date.today())
outputDir = "plots/" + date + "/ksFit/"
if (not os.path.isdir(outputDir)):
    os.makedirs(outputDir)

h_mDV_2from4 = inputFile.Get("mDV_2from4")

c1 = r.TCanvas("c1", "c1", 800, 600)

mygaus = r.TF1("mygaus", "gaus", 0.4, 0.6)
mygaus.SetLineColor(r.kRed)
h_mDV_2from4.Draw()
h_mDV_2from4.Fit("mygaus", "", "", 0.4, 0.6)
const = mygaus.GetParameter(0)
mean = mygaus.GetParameter(1)
sigma = mygaus.GetParameter(2)
print(const, mean, sigma)


c1.Print("{}/fit.pdf".format(outputDir))

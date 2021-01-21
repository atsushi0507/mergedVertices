import ROOT as r
import os, datetime
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
SetAtlasStyle()
label = "Internal"

m_kshort = 497.11 * 0.001

r.gROOT.SetBatch()

date = str(datetime.date.today())
directory = "plots/" + date + "/plots/"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("combination.root", "READ")

h_3track_2comb = inputFile.Get("ditrack_3track")
h_4track_2comb = inputFile.Get("ditrack_4track")

c1 = r.TCanvas("c1", "c1", 800, 600)

h_3track_2comb.Draw()
ATLASLabel(0.175, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_3track_2comb.GetName()))

h_4track_2comb.Draw()
ATLASLabel(0.175, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_4track_2comb.GetName()))

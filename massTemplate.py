import ROOT as r
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
#sys.path.append("/Users/atsushi/mvstudy_dv")
import os, datetime
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()

label = "Work in Progress"

inputFile = r.TFile("run2_full_weighted.root", "READ")
outputFile = r.TFile("mergedVertices_massTemplate.root", "RECREATE")

date = str(datetime.date.today())
directory = os.getcwd() + "/plots/" + date + "/mergedMass"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

c1 = r.TCanvas("c1", "c1", 800, 600)

DV_m_4track = inputFile.Get("DV_m_4track").Rebin(10)
mergedMass4 = inputFile.Get("mergedMass4_mixed").Rebin(10)
mergedMass4_sigWeight = inputFile.Get("mergedMass4_sigWeight").Rebin(10)

bin1 = DV_m_4track.FindBin(100)
DV_m_4track.GetXaxis().SetRange(1, bin1)

### Color setting
DV_m_4track.SetLineColor(r.kBlack)
mergedMass4.SetLineColor(r.kRed)
mergedMass4.SetMarkerColor(r.kRed)
mergedMass4_sigWeight.SetLineColor(r.kBlue)
mergedMass4_sigWeight.SetMarkerColor(r.kBlue)

sf = DV_m_4track.Integral() / mergedMass4.Integral()

leg = r.TLegend(0.65, 0.65, 0.88, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.03)

r.gPad.SetLogy()

mergedMass4.Scale(sf)
mergedMass4_sigWeight.Scale(sf)
DV_m_4track.Draw("e")
mergedMass4.Draw("same hist e0")
mergedMass4_sigWeight.Draw("same hist e0")
leg.AddEntry(DV_m_4track, "Data", "l")
leg.AddEntry(mergedMass4, "100% merged", "l")
leg.AddEntry(mergedMass4_sigWeight, "apply merge rate", "l")
leg.Draw()
ATLASLabel(0.4, 0.88, label)
c1.Print("{}/{}.pdf".format(directory, "mergedMass4_logy"))

mergedMass4_sigWeight.Draw("hist e0")
ATLASLabel(0.4, 0.88, label)
c1.Print("{}/{}.pdf".format(directory, "mergedMass4_sigWeight_logy"))
mergedMass4_sigWeight.Write()

r.gPad.SetLogy(0)
DV_m_4track.Draw("p")
mergedMass4.Draw("same hist e0")
mergedMass4_sigWeight.Draw("same hist e0")
leg.Draw()
ATLASLabel(0.4, 0.88, label)
c1.Print("{}/{}.pdf".format(directory, "mergedMass4"))

mergedMass4_sigWeight.Draw("hist e0")
ATLASLabel(0.4, 0.88, label)
c1.Print("{}/{}.pdf".format(directory, "mergedMass4_sigWeight"))

bin10 = mergedMass4_sigWeight.FindBin(10)
binMax = mergedMass4_sigWeight.GetNbinsX()
print(mergedMass4_sigWeight.Integral(bin10, binMax))

r.gPad.SetLogy()

regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]
DV_m_region = []
mergedMass4_region = []
mergedMass4_sigWeight_region = []
for region in regions:
    DV_m_region.append(inputFile.Get("DV_m_4track_{}".format(region)).Rebin(10))
    mergedMass4_region.append(inputFile.Get("mergedMass4_{}".format(region)).Rebin(10))
    mergedMass4_sigWeight_region.append(inputFile.Get("mergedMass4_sigWeight_{}".format(region)).Rebin(10))

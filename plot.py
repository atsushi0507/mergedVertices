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
templateFile = r.TFile("/Users/amizukam/DVJets/mergedVertices/run2_full_weighted.root", "READ")
hiTemp = r.TFile("/Users/amizukam/DVJets/hadronicInteractions/HI_Templates/HI_Templates_Small_Bins.root", "READ")

# Validate method
rebin = 5
h_ditrackMass_2from3 = inputFile.Get("mDV_2from3").Rebin(rebin)
h_ditrackMass_2from4 = inputFile.Get("mDV_2from4").Rebin(rebin)
h_ditrackMass_2from4_noSel = inputFile.Get("mDV_2from4_noSel").Rebin(rebin)
h_mDV_2track = inputFile.Get("mDV_2track").Rebin(rebin)
h_mv_4track = inputFile.Get("mv_4track")#.Rebin(rebin)
h_mv_4track_passTC = inputFile.Get("mv_4track_passTrackCleaning")#.Rebin(rebin)

h_ditrackMass_2from4_noSel_zoomed = h_ditrackMass_2from4_noSel.Clone("zoomed")
h_ditrackMass_2from4_noSel_zoomed.GetXaxis().SetRange(1, h_ditrackMass_2from4_noSel_zoomed.FindBin(1.))

# Tested template
h_mergedMass4_weighted = templateFile.Get("mergedMass4_weight").Rebin(rebin)
#h_mergedMass4_weighted.GetXaxis().SetRange(1, h_mergedMass4_weighted.FindBin(22.))

# HI template
h_4trk = hiTemp.Get("4trk")

hi_4trk = r.TH1D("hi_4trk", ";m_{DV} [GeV]", 100, 0., 50.)
for i in range(hi_4trk.GetNbinsX()+1):
    hi_4trk.SetBinContent(i, h_4trk.GetBinContent(i))


c1 = r.TCanvas("c1", "c1", 800, 600)

h_ditrackMass_2from3.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_ditrackMass_2from3.GetName()))

h_ditrackMass_2from4.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_ditrackMass_2from4.GetName()))

h_ditrackMass_2from4_noSel.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_ditrackMass_2from4_noSel.GetName()))

h_ditrackMass_2from4_noSel_zoomed.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_ditrackMass_2from4_noSel_zoomed.GetName()))

h_mv_4track.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_mv_4track.GetName()))

# Plots with log scale
r.gPad.SetLogy()
h_mDV_2track.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, h_mDV_2track.GetName()))

# HI
hi_4trk.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, hi_4trk.GetName()))

# Template with normalized
leg = r.TLegend(0.70, 0.70, 0.88, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)
leg.SetTextFont(42)
h_mergedMass4_weighted.SetLineColor(r.kRed)
hi_4trk.SetLineColor(r.kBlue)
h_mv_4track.DrawNormalized()
h_mergedMass4_weighted.DrawNormalized("same hist")
hi_4trk.DrawNormalized("same hist")
leg.AddEntry(h_mv_4track, "New method", "l")
leg.AddEntry(h_mergedMass4_weighted, "MV template", "l")
leg.AddEntry(hi_4trk, "HI Template", "l")
leg.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "normalized"))

bin5 = h_mv_4track.FindBin(5)
bin10 = h_mv_4track.FindBin(10)

hi_4trk_noSel = hi_4trk.Clone("noSel_HI")
h_mv4_noSel = h_mergedMass4_weighted.Clone("noSel_MV")

hi_4trk_TC = hi_4trk.Clone("forTC_HI")
h_mv4_TC = h_mergedMass4_weighted.Clone("forTC_MV")

norm_HI = h_mv_4track.Integral(1, bin5) / hi_4trk_noSel.Integral(1, bin5)
norm_MV = h_mv_4track.Integral(bin5, bin10) / h_mv4_noSel.Integral(bin5, bin10)

hi_4trk.Scale(norm_HI)
h_mv4_noSel.Scale(norm_MV)

h_mv_4track.Draw()
h_mv4_noSel.Draw("same hist")
hi_4trk.Draw("same hist")
leg.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "scaled"))


norm_HI_TC = h_mv_4track_passTC.Integral(1, bin5) / hi_4trk_TC.Integral(1, bin5)
norm_MV_TC = h_mv_4track_passTC.Integral(bin5, bin10) / h_mv4_TC.Integral(bin5, bin10)

hi_4trk_TC.Scale(norm_HI_TC)
h_mv4_TC.Scale(norm_MV_TC)

h_mv_4track_passTC.Draw()
h_mv4_TC.Draw("same hist")
hi_4trk_TC.Draw("same hist")
leg.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "TC"))


h_mv_4track_passTC.SetLineColor(r.kRed)
h_mv_4track.DrawNormalized()
h_mv_4track_passTC.DrawNormalized("same")
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "compare"))

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

inputFile = r.TFile("ks.root", "READ") # from validationStudy.py, files are in newMethod/, same-event 
mvFile = r.TFile("combination.root", "READ") # from trackCombination.py, files are in kshort/, mixed-event
templateFile = r.TFile("/Users/amizukam/DVJets/mergedVertices/run2_full_weighted.root", "READ")
hiTemp = r.TFile("/Users/amizukam/DVJets/hadronicInteractions/HI_Templates/HI_Templates_Small_Bins.root", "READ")

# Validate method
rebin = 5
h_ditrackMass_2from3 = inputFile.Get("mDV_2from3").Rebin(rebin)
h_ditrackMass_2from4 = inputFile.Get("mDV_2from4").Rebin(rebin)
h_ditrackMass_2from4_noSel = inputFile.Get("mDV_2from4_noSel").Rebin(rebin)
h_mDV_2track = inputFile.Get("mDV_2track").Rebin(rebin)
h_mv_4track = inputFile.Get("mv_4track").Rebin(rebin)
h_mv_4track_passTC = inputFile.Get("mv_4track_passTrackCleaning")#.Rebin(rebin)
#h_mv_4track_passTC = inputFile.Get("mv_4track_combination")#.Rebin(rebin)
h_mergedMass4_dv1_vs_dv2 = mvFile.Get("mergedMass4_dv1_vs_dv2").Rebin2D(5, 5)

h_ditrackMass_2from4_noSel_zoomed = h_ditrackMass_2from4_noSel.Clone("zoomed")
h_ditrackMass_2from4_noSel_zoomed.GetXaxis().SetRange(1, h_ditrackMass_2from4_noSel_zoomed.FindBin(1.))

# Tested template
h_mergedMass4_weighted = templateFile.Get("mergedMass4_weight").Rebin(rebin)
h_mv4_fromMixed = mvFile.Get("mergedMass4_sig100Cut_ks").Rebin(rebin)

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
leg = r.TLegend(0.55, 0.70, 0.85, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)
leg.SetTextFont(42)
h_mergedMass4_weighted.SetLineColor(r.kRed)
h_mergedMass4_weighted.SetMarkerColor(r.kRed)
hi_4trk.SetLineColor(r.kBlue)
hi_4trk.SetMarkerColor(r.kBlue)
h_mv_4track.DrawNormalized()
h_mergedMass4_weighted.DrawNormalized("same hist")
hi_4trk.DrawNormalized("same hist")
leg.AddEntry(h_mv_4track, "Ks from same-event", "l")
#leg.AddEntry(h_mergedMass4_weighted, "MV template", "l")
leg.AddEntry(h_mv4_fromMixed, "Ks from mixed-event", "l")
leg.AddEntry(hi_4trk, "HI Template", "l")
leg.Draw()
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "normalized"))

h_mv_4track.Rebin(2)
h_mv4_fromMixed.Rebin(2)
bin3 = h_mv_4track.FindBin(3)
bin5 = h_mv_4track.FindBin(5)
bin10 = h_mv_4track.FindBin(10)

hi_4trk_noSel = hi_4trk.Clone("noSel_HI")
h_mv4_noSel = h_mergedMass4_weighted.Clone("noSel_MV")

hi_4trk_TC = hi_4trk.Clone("forTC_HI")
h_mv4_TC = h_mergedMass4_weighted.Clone("forTC_MV")

h_mv4_fromMixed.SetLineColor(r.kGreen + 2)
h_mv4_fromMixed.SetMarkerColor(r.kGreen + 2)

norm_HI = h_mv_4track.Integral(1, bin3) / hi_4trk_noSel.Integral(1, bin3)
norm_MV = h_mv_4track.Integral(bin5, bin10) / h_mv4_noSel.Integral(bin5, bin10)
norm_mixed = h_mv_4track.Integral(bin5, bin10) / h_mv4_fromMixed.Integral(bin5, bin10)

hi_4trk.Scale(norm_HI)
h_mv4_noSel.Scale(norm_MV)
h_mv4_fromMixed.Scale(norm_mixed)

h_mv_4track.Draw("e0")
#h_mv4_noSel.Draw("same hist e0")
h_mv4_fromMixed.Draw("same hist e0")
hi_4trk.Draw("same hist")
leg.Draw()
ATLASLabel(0.150, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "scaled"))

h_mv_4track.Rebin(2)
h_mv4_fromMixed.Rebin(2)
leg2 = r.TLegend(0.55, 0.70, 0.85, 0.88)
leg2.SetBorderSize(0)
leg2.SetFillColor(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.03)
leg2.AddEntry(h_mv_4track, "Ks from same-event", "l")
leg2.AddEntry(h_mv4_fromMixed, "Ks from mixed-event", "l")
rp = r.TRatioPlot(h_mv_4track, h_mv4_fromMixed)
rp.SetH1DrawOpt("e0")
rp.SetH2DrawOpt("hist e0")
rp.Draw()
rp.GetLowerRefGraph().SetMaximum(2.0)
rp.GetLowerRefGraph().SetMinimum(0.0)
rp.GetLowYaxis().SetNdivisions(4)

rp.GetLowerRefYaxis().SetTitle("#frac{same}{mixed}")
rp.SetSeparationMargin(0.02)
rp.SetLeftMargin(0.1575)
rp.SetLowBottomMargin(0.50)
leg2.Draw()
ATLASLabel(0.150, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "mv_ratio"))

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

r.gPad.SetLogy(0)
r.gPad.SetLogz()
h_mergedMass4_dv1_vs_dv2.Draw("colz")
ATLASLabel(0.250, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "mv4_dv1_vs_dv2"))

# sideband
r.gPad.SetLogz(0)
h_sideband_same = inputFile.Get("mv_4track_sideband").Rebin(20*2)
h_sideband_mixed = mvFile.Get("mv4_sideband").Rebin(20*2)
h_sideband_mixed.SetLineColor(r.kRed)
h_sideband_mixed.SetMarkerColor(r.kRed)

bin1 = h_sideband_same.FindBin(5.)
bin2 = h_sideband_same.FindBin(10.)

sf = h_sideband_same.Integral(bin1, bin2) / h_sideband_mixed.Integral(bin1, bin2)
h_sideband_mixed.Sumw2()
h_sideband_mixed.Scale(sf)

r.gPad.SetLogy()
leg3 = r.TLegend(0.70, 0.65, 0.80, 0.85)
leg3.SetFillStyle(0)
leg3.SetBorderSize(0)
leg3.SetTextSize(0.03)
leg3.SetTextFont(42)

leg3.AddEntry(h_sideband_same, "Same", "l")
leg3.AddEntry(h_sideband_mixed, "Mixed", "l")

h_sideband_same.Draw("e0 hist")
h_sideband_mixed.Draw("same e0 hist")
leg3.Draw()
ATLASLabel(0.150, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "sideband"))

rp_side = r.TRatioPlot(h_sideband_same, h_sideband_mixed)
rp_side.SetH1DrawOpt("e0")
rp_side.SetH2DrawOpt("hist e0")
rp_side.Draw()
rp_side.GetLowerRefGraph().SetMaximum(2.0)
rp_side.GetLowerRefGraph().SetMinimum(0.0)
rp_side.GetLowYaxis().SetNdivisions(4)
rp_side.SetSeparationMargin(0.02)
rp_side.SetLeftMargin(0.1575)
rp_side.SetLowBottomMargin(0.50)
leg3.Draw()
ATLASLabel(0.150, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "sideband_ratio"))

# using ks mass as track mass
ksFile = r.TFile("validStudy-ks.root", "READ")
ksFile_hoge = r.TFile("hoge-ks.root", "READ")
infile = r.TFile("ks.root", "READ")
bothFile = r.TFile("validStudy-both.root", "READ")

mv_pion = infile.Get("mv_4track").Rebin(10)
mv_ks = ksFile.Get("mv_4track").Rebin(10)
mv_both = bothFile.Get("mv_4track").Rebin(10)
mv_ks.SetLineColor(r.kRed)
mv_both.SetLineColor(r.kBlue)
#mv_mixed = ksFile_hoge.Get("")

leg4 = r.TLegend(0.65, 0.65, 0.80, 0.80)
leg4.SetBorderSize(0)
leg4.SetFillStyle(0)
leg4.SetTextSize(0.03)
leg4.SetTextFont(42)
leg4.AddEntry(mv_pion, "Used pion mass", "l")
leg4.AddEntry(mv_ks, "Used kshort mass", "l")
leg4.AddEntry(mv_both, "Used pion and kshort mass", "l")
mv_pion.DrawNormalized()
mv_ks.DrawNormalized("same")
mv_both.DrawNormalized("same")
leg4.Draw()
ATLASLabel(0.150, 0.955, label)
c1.Print("{}/{}.pdf".format(directory, "kstrack"))

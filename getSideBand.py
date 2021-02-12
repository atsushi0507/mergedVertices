import ROOT as r
import os, datetime
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle/")
from AtlasStyle import *
from AtlasLabel import *
label = "Internal"

SetAtlasStyle()
r.gROOT.SetBatch()

def flatBackground(x, par):
    return par[0] + par[1]*x[0]

def expBackground(x, par):
    return r.TMath.Exp(par[0] + par[1]*x[0])

def secondGaus(x, par):
    return par[0]*r.TMath.Exp(-0.5*pow(x[0]-par[1]/par[2]))

def lorentzianPeak(x, par):
    return (0.5*par[0]*par[1]/r.TMath.Pi()) / r.Math.Max(1.e-10, (x[0]-par[2])*(x[0]-par[2]) + 0.25*par[1]*par[1])

def signal(x, par):
    return par[0]*r.TMath.Exp(-0.5*pow((x[0]-par[1])/par[2], 2))

def totalFit2trk(x, par):
    return expBackground(x, par) + signal(x, par[2:])

def totalFit(x, par):
    #flatBackground = par[0] + par[1]*x[0]
    flatBackground = r.TMath.Exp(par[0] + par[1]*x[0])
    signal = par[2]*r.TMath.Exp(-0.5*pow((x[0]-par[3])/par[4], 2))
    return flatBackground + signal


inputFile = r.TFile("ks.root", "READ")
date = str(datetime.date.today())
outputDir = "plots/" + date + "/ksFit/"
if (not os.path.isdir(outputDir)):
    os.makedirs(outputDir)

h_mDV_2from4 = inputFile.Get("mDV_2from4")

c1 = r.TCanvas("c1", "c1", 800, 600)

# Prepare to fit
y1 = h_mDV_2from4.GetBinContent(h_mDV_2from4.FindBin(0.4))
y2 = h_mDV_2from4.GetBinContent(h_mDV_2from4.FindBin(0.6))
gradient = (y2 - y1)/0.2
yIntercept = y1 - (gradient*0.4)
peakHeight = h_mDV_2from4.GetBinContent(h_mDV_2from4.FindBin(0.498))

print("Starting parameters: y1 = {}, y2 = {}".format(y1, y2))
print("yIntercept, p[0] = {}, gradient, p[1] = {}".format(yIntercept, gradient))
print("peakHeight, p[2] = {}".format(peakHeight))

# Find FWHM to set sigma of gauss fit
binLow = h_mDV_2from4.FindBin(0.4)
binHigh = h_mDV_2from4.FindBin(0.6)
set_xLow = False
set_xHigh = False
xLow = 0.
xHigh = 0.

for i in range(binLow, binHigh):
    if (not set_xLow):
        if (h_mDV_2from4.GetBinContent(i) >= peakHeight/2.):
            xLow = h_mDV_2from4.GetBinCenter(i-1)
            set_xLow = True
            continue
    else:
            if (h_mDV_2from4.GetBinContent(i) < peakHeight/2.):
                xHigh = h_mDV_2from4.GetBinCenter(i)
                break

FWHM = (xHigh - xLow)
sigma = FWHM / (2.*r.TMath.Sqrt(2*r.TMath.Log(2)))
print("Half-max = {}".format(peakHeight/2.))
print("xLow = {}, xHigh = {}, FWHM = {}".format(xLow, xHigh, FWHM))
print("sigma, p[4] = {}".format(sigma))

# Fit to mDV_2from4
fit_xLower = 0.4
fit_xUpper = 0.6
nPars = 5

f_total = r.TF1("f_total", totalFit, fit_xLower, fit_xUpper, nPars)
f_total.SetNpx(500)
f_total.SetLineWidth(2)
f_total.SetLineColor(r.kRed)

# Set up starting parameters for fit
f_total.SetParameter(0, yIntercept) # Expo offset
f_total.SetParameter(1, gradient) # Expo gradient
f_total.SetParameter(2, peakHeight) # Signal peak height
f_total.SetParameter(3, 0.498) # Signal peak mean: Ksh mass
f_total.SetParameter(4, sigma) # Signal peak width
### To be deleted. Just for test
r.gPad.SetLogy()
h_mDV_2from4.Draw()
h_mDV_2from4.Fit("f_total", "RM")
c1.Print("{}/{}.pdf".format(outputDir, "testFit"))

r.gPad.SetLogy(0)

f_gaus_2from4 = r.TF1("f_gaus_2from4", "gaus", fit_xLower, fit_xUpper)
f_flat_2from4 = r.TF1("f_flat_2from4", "pol1", fit_xLower, fit_xUpper)

f_gaus_2from4.SetLineColor(r.kBlue)
f_flat_2from4.SetLineColor(r.kGreen+2)

par = f_total.GetParameters()
par0, par1, par2, par3, par4 = par[0], par[1], par[2], par[3], par[4]
f_flat_2from4.SetParameters(par0, par1)
f_gaus_2from4.SetParameters(par2, par3, par4)

h_mDV_2from4.Draw("hist")
f_gaus_2from4.Draw("same")
f_flat_2from4.Draw("same")
f_total.Draw("same")

c1.Modified()
c1.Update()
c1.Print("{}/{}.pdf".format(outputDir, "fitToData"))

##############################
## Subtract fitted background
##############################

# Now make a new histogram that has the exponential background subtracted
h_sub = h_mDV_2from4.Clone("h_sub")
h_final = h_mDV_2from4.Clone("h_final")

low  = 0.46
high = 0.54
binLow  = h_sub.FindBin(low)
binHigh = h_sub.FindBin(high)
num_beforeFit = h_sub.Integral(binLow, binHigh)
print("Before background subtraction: {}".format(num_beforeFit))

h_sub.Add(f_flat_2from4, -1.)
h_final.SetLineColor(r.kBlue)
h_sub.SetLineColor(r.kRed)
h_sub.SetLineWidth(2)
h_final.Draw("hist")
h_sub.Draw("same")
c1.Modified()
c1.Update()
c1.Print("{}/{}.pdf".format(outputDir, "subtracted"))

for l in range(h_sub.GetXaxis().GetNbins()):
    if (h_sub.GetBinContent(l) < 0.):
        h_sub.SetBinContent(l, 0.)
h_sub.Draw()
c1.Modified()
c1.Update()
c1.Print("{}/{}.pdf".format(outputDir, "modified"))

###############
## Integrate
###############
num = h_sub.Integral(binLow, binHigh)
print("Before background subtraction: {}".format(num_beforeFit))
print("Integrated from bin: {} to {} = {}".format(binLow, binHigh, num))

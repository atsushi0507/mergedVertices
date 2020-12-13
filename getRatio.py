import ROOT as r
import sys
sys.path.append("/Users/atsushi/mvstudy_dv")
from AtlasStyle import *
from AtlasLabel import *
from plotHelper import *
import argparse
import datetime, os

r.gROOT.SetBatch()
SetAtlasStyle()

p = argparse.ArgumentParser()
p.add_argument("-i", "--inputFileName", help="Choose inputFile", default="run2_full.root")
args = p.parse_args()

inputFile = args.inputFileName
inFile = r.TFile(inputFile, "READ")

date = str(datetime.date.today())
directory = str(os.getcwd()) + "/plots/" + date + "/ratio"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

label = "Work in Progress"

outputFile = r.TFile("ratio.root", "RECREATE")

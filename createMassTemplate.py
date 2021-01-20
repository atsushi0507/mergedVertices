import ROOT as r

r.gROOT.SetBatch()

inputFile = r.TFile("run2_full_weighted.root", "READ")
outputFile = r.TFile("mergedVertices_massTemplate.root", "RECREATE")

regions = ["inside_BP", "inside_IBL", "PIX", "inside_SCT"]

rebin = 5
mergedMass4 = inputFile.Get("mergedMass4_weight").Rebin(rebin)
mergedMass5 = inputFile.Get("mergedMass5_weight").Rebin(rebin)
mergedMass6 = inputFile.Get("mergedMass6_weight").Rebin(rebin)

mv4 = []
mv5 = []
mv6 = []
for region in regions:
    mv4.append(inputFile.Get("mergedMass4_weight_{}".format(region)).Rebin(rebin))
    mv5.append(inputFile.Get("mergedMass5_weight_{}".format(region)).Rebin(rebin))
    mv6.append(inputFile.Get("mergedMass6_weight_{}".format(region)).Rebin(rebin))

bin1 = 1
bin2 = mergedMass4.FindBin(50.)

mergedMass4.GetXaxis().SetRange(bin1, bin2)
mergedMass5.GetXaxis().SetRange(bin1, bin2)
mergedMass6.GetXaxis().SetRange(bin1, bin2)

for i in range(len(mv4)):
    mv4[i].GetXaxis().SetRange(bin1, bin2)
    mv5[i].GetXaxis().SetRange(bin1, bin2)
    mv6[i].GetXaxis().SetRange(bin1, bin2)

    mv4[i].Write()
    mv5[i].Write()
    mv6[i].Write()

mergedMass4.Write()
mergedMass5.Write()
mergedMass6.Write()

outputFile.Write()
outputFile.Close()

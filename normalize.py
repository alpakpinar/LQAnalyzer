#Script for normalizing the leptoquark histograms

import ROOT

filename = 'LQRootFiles/LQ_1_4TeV_1_histOut_all.root'
infile = ROOT.TFile.Open(filename, 'UPDATE')
mydir = infile.plots

cross_section = 0.01542
luminosity = 35900
num_events_gen = 49500

norm_weight = cross_section*luminosity/num_events_gen

mydir.cd()

#MET Histogram
canv2 = ROOT.TCanvas('canv2', 'canv2')
METHist = mydir.Get('MET')
for i in range(METHist.GetNbinsX()):
    original_cont = METHist.GetBinContent(i+1)
    bin_width = METHist.GetBinWidth(i+1)
    METHist.SetBinContent(i+1, original_cont/bin_width)

METHist.Scale(norm_weight)
METHist.GetYaxis().SetTitle('Number of Events')
METHist.Draw("Hist")
canv2.Print("MET_1_4TeV_1.png")
METHist.Write()

#Eta Difference Between Jets
canv3 = ROOT.TCanvas('canv3', 'canv3')
EtaHist = mydir.Get('etaDiffGenJets')
bin_widthEta = EtaHist.GetBinWidth(1)
EtaHist.Scale(norm_weight/bin_widthEta)
EtaHist.Draw("Hist")
canv3.Print("etaDiffGenJets_1_4TeV_1.png")
EtaHist.Write()

#Phi Difference Between Jets
canv4 = ROOT.TCanvas('canv4','canv4')
PhiHist = mydir.Get('phiDiffGenJets')
bin_widthPhi = PhiHist.GetBinWidth(1)
PhiHist.Scale(norm_weight/bin_widthPhi)
PhiHist.Draw("Hist")
canv4.Print("phiDiffGenJets_1_4TeV_1.png")
PhiHist.Write()

#Jet-MET Phi Difference
canv5 = ROOT.TCanvas('canv5', 'canv5')
jetMET_hist = mydir.Get('jetMETPhi')
bin_width_jetMET = jetMET_hist.GetBinWidth(1)
jetMET_hist.Scale(norm_weight/bin_width_jetMET)
jetMET_hist.Draw("Hist")
canv5.Print("jetMETPhi_1_4TeV_1.png")
jetMET_hist.Write()

#Number of b-jets
canv6 = ROOT.TCanvas('canv6', 'canv6')
numbJets_hist = mydir.Get('numbJets')
numbJets_hist.Scale(norm_weight)
numbJets_hist.Draw("Hist")
canv6.Print("numbJets_1_4TeV_1.png")
numbJets_hist.Write()

#Number of Leptoquarks
canv7 = ROOT.TCanvas('canv7', 'canv7')
numLQ_hist = mydir.Get('numLQ')
numLQ_hist.Scale(norm_weight)
numLQ_hist.Draw("Hist")
canv7.Print("numLQ_1_4TeV_1.png")
numLQ_hist.Write()

#Number of u Jets
canv8 = ROOT.TCanvas('canv8', 'canv8')
num_uJets_hist = mydir.Get('num_uJets')
num_uJets_hist.Scale(norm_weight)
num_uJets_hist.Draw("Hist")
canv8.Print("num_uJets_1_4TeV_1.png")
num_uJets_hist.Write()





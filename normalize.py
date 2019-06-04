#Script for normalizing and plotting the leptoquark histograms

import ROOT

filename = 'LQRootFiles/LQ_1_4TeV_1_histOut_all.root'
infile = ROOT.TFile.Open(filename, 'UPDATE')
mydir = infile.plots

#No stat box
ROOT.gStyle.SetOptStat(0)

#Thicker lines
ROOT.gStyle.SetHistLineWidth(2)

cross_section = 0.01542
luminosity = 35900
num_events_gen = 49500

norm_weight = cross_section*luminosity/num_events_gen

mydir.cd()

#MET Histogram
canv2 = ROOT.TCanvas('canv2', 'canv2')
canv2.SetGrid()

avgBinWidth = 0
METHist = mydir.Get('MET;1')

for i in range(METHist.GetNbinsX()):
    original_cont = METHist.GetBinContent(i+1)
    bin_width = METHist.GetBinWidth(i+1)
    avgBinWidth += bin_width
    METHist.SetBinContent(i+1, original_cont/bin_width)

avgBinWidth /= METHist.GetNbinsX()
METHist.Scale(norm_weight)
METHist.GetYaxis().SetTitle('Number of Events / GeV')

#METHist.SetFillStyle(1001)
#METHist.SetFillColor(ROOT.kRed)
METHist.SetLineColor(ROOT.kBlue)

METHist.Draw("Hist")
canv2.Print("MET_1_4TeV_1.png")
METHist.Write()

#Eta Difference Between Jets
canv3 = ROOT.TCanvas('canv3', 'canv3')
canv3.SetGrid()

EtaHist = mydir.Get('etaDiffGenJets;1')
#bin_widthEta = EtaHist.GetBinWidth(1)
EtaHist.Scale(norm_weight)
EtaHist.GetYaxis().SetTitle('Number of Events')

#EtaHist.SetFillStyle(1001)
#EtaHist.SetFillColor(ROOT.kRed)
EtaHist.SetLineColor(ROOT.kBlue)

EtaHist.Draw("Hist")
canv3.Print("etaDiffGenJets_1_4TeV_1.png")
EtaHist.Write()

#Phi Difference Between Jets
canv4 = ROOT.TCanvas('canv4','canv4')
canv4.SetGrid()

PhiHist = mydir.Get('phiDiffGenJets;1')
#bin_widthPhi = PhiHist.GetBinWidth(1)
PhiHist.Scale(norm_weight)
PhiHist.GetYaxis().SetTitle('Number of Events')

#PhiHist.SetFillStyle(1001)
#PhiHist.SetFillColor(ROOT.kRed)
PhiHist.SetLineColor(ROOT.kBlue)

#Changing x-axis labels
axis = PhiHist.GetXaxis()
axis.SetNdivisions(504, ROOT.kFALSE)
axis.ChangeLabel(2, -1, -1, -1, -1, -1, "#pi/4")
axis.ChangeLabel(3, -1, -1, -1, -1, -1, "#pi/2")
axis.ChangeLabel(4, -1, -1, -1, -1, -1, "3#pi/4")
axis.ChangeLabel(5, -1, -1, -1, -1, -1, "#pi")

PhiHist.Draw("Hist")
canv4.Print("phiDiffGenJets_1_4TeV_1.png")
PhiHist.Write()

#Jet-MET Phi Difference
canv5 = ROOT.TCanvas('canv5', 'canv5')
canv5.SetGrid()

jetMET_hist = mydir.Get('jetMETPhi;1')
#bin_width_jetMET = jetMET_hist.GetBinWidth(1)
jetMET_hist.Scale(norm_weight)
jetMET_hist.GetYaxis().SetTitle('Number of Events')

#jetMET_hist.SetFillStyle(1001)
#jetMET_hist.SetFillColor(ROOT.kRed)
jetMET_hist.SetLineColor(ROOT.kBlue)

#Changing x-axis labels
axis = jetMET_hist.GetXaxis()
axis.SetNdivisions(504, ROOT.kFALSE)
axis.ChangeLabel(2, -1, -1, -1, -1, -1, "#pi/4")
axis.ChangeLabel(3, -1, -1, -1, -1, -1, "#pi/2")
axis.ChangeLabel(4, -1, -1, -1, -1, -1, "3#pi/4")
axis.ChangeLabel(5, -1, -1, -1, -1, -1, "#pi")

jetMET_hist.Draw("Hist")
canv5.Print("jetMETPhi_1_4TeV_1.png")
jetMET_hist.Write()

#Number of b-jets
canv6 = ROOT.TCanvas('canv6', 'canv6')
canv6.SetGrid()

numbJets_hist = mydir.Get('numbJets;1')
numbJets_hist.Scale(norm_weight)

#numbJets_hist.SetFillStyle(1001)
#numbJets_hist.SetFillColor(ROOT.kRed)
numbJets_hist.SetLineColor(ROOT.kBlue)

numbJets_hist.Draw("Hist")
canv6.Print("numbJets_1_4TeV_1.png")
numbJets_hist.Write()

#Number of Leptoquarks
canv7 = ROOT.TCanvas('canv7', 'canv7')
canv7.SetGrid()

numLQ_hist = mydir.Get('numLQ;1')
numLQ_hist.Scale(norm_weight)

#numLQ_hist.SetFillStyle(1001)
#numLQ_hist.SetFillColor(ROOT.kRed)
numLQ_hist.SetLineColor(ROOT.kBlue)

numLQ_hist.GetXaxis().SetNdivisions(505, ROOT.kFALSE)

numLQ_hist.Draw("Hist")
canv7.Print("numLQ_1_4TeV_1.png")
numLQ_hist.Write()

#Number of u Jets
canv8 = ROOT.TCanvas('canv8', 'canv8')
canv8.SetGrid()

num_uJets_hist = mydir.Get('num_uJets;1')
num_uJets_hist.Scale(norm_weight)

#num_uJets_hist.SetFillStyle(1001)
#num_uJets_hist.SetFillColor(ROOT.kRed)
num_uJets_hist.SetLineColor(ROOT.kBlue)

num_uJets_hist.Draw("Hist")
canv8.Print("num_uJets_1_4TeV_1.png")
num_uJets_hist.Write()

#Leading Jet Pt
canv9 = ROOT.TCanvas('canv9', 'canv9')
canv9.SetGrid()

leadingJetPt_hist = mydir.Get('leadingJetPt;1')
leadingJetPt_hist.Scale(norm_weight)

leadingJetPt_hist.SetLineColor(ROOT.kBlue)

leadingJetPt_hist.Draw("Hist")
canv9.Print("leadingJetPt_1_4TeV_1.png")
leadingJetPt_hist.Write()





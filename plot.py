import ROOT
import os
from numpy import arange

filename = 'LQ_1_4TeV_1_histOut_all.root'
infile = ROOT.TFile.Open(filename, 'UPDATE')
mydir = infile.plots
#mydir.cd()

evtCountsGraph = mydir.Get('evtCounts')
cut_names = ['No Cut', 'HLT', 'Filters', 'MET', 'LJ_pT,eta', 'LJ_CHF,NHF', 'CaloMET-PFMET', 'Loose Ph', 'Loose El', 'Loose Mu', 'Loose Tau', 'Jet-MET Phi', 'b-jet'] 
x = arange(evtCountsGraph.GetN())

num_events = evtCountsGraph.GetY()[0]
#print(evtCountsGraph.GetN())

for i in range(evtCountsGraph.GetN()):
    evtCountsGraph.SetPoint(i, x[i], evtCountsGraph.GetY()[i]/num_events)      

x_ax = evtCountsGraph.GetXaxis()
x_ax.Set(13,0,12)

for i in range(len(cut_names)):
    x_ax.SetBinLabel(i+1, cut_names[i])

#Event Counts
canv1 = ROOT.TCanvas("canv1","canv1")
canv1.SetGrid()

evtCountsGraph.Draw("AP")
#canv1.Print("evtCounts_1_4TeV_1.png")
evtCountsGraph.Write()

#MET Histogram
canv2 = ROOT.TCanvas('canv2', 'canv2')
METHist = mydir.Get('MET')
METHist.Scale(0.000653/52.2727)
METHist.GetYaxis().SetTitle('Number of Events / 52.2727')
METHist.Draw("Hist")
#canv2.Print("MET_1_4TeV_1.png")
METHist.Write()

#Eta Difference Between Jets
canv3 = ROOT.TCanvas('canv3', 'canv3')
EtaHist = mydir.Get('etaDiffGenJets')
bin_widthEta = EtaHist.GetBinWidth(1)
EtaHist.Scale(0.000653/bin_widthEta)
EtaHist.Draw("Hist")
#canv3.Print("etaDiffGenJets_1_4TeV_1.png")
EtaHist.Write()

#Phi Difference Between Jets
canv4 = ROOT.TCanvas('canv4','canv4')
PhiHist = mydir.Get('phiDiffGenJets')
bin_widthPhi = PhiHist.GetBinWidth(1)
PhiHist.Scale(0.000653/bin_widthPhi)
PhiHist.Draw("Hist")
#canv4.Print("phiDiffGenJets_1_4TeV_1.png")
PhiHist.Write()

#Jet-MET Phi Difference
canv5 = ROOT.TCanvas('canv5', 'canv5')
jetMET_hist = mydir.Get('jetMETPhi')
bin_width_jetMET = jetMET_hist.GetBinWidth(1)
jetMET_hist.Scale(0.000653/bin_width_jetMET)
jetMET_hist.Draw("Hist")
#canv5.Print("jetMETPhi_1_4TeV_1.png")
jetMET_hist.Write()

#Number of b-jets
canv6 = ROOT.TCanvas('canv6', 'canv6')
numbJets_hist = mydir.Get('numbJets')
bin_width_numbJets = numbJets_hist.GetBinWidth(1)
numbJets_hist.Scale(0.000653/bin_width_numbJets)
numbJets_hist.Draw("Hist")
#canv6.Print("numbJets_1_4TeV_1.png")
numbJets_hist.Write()



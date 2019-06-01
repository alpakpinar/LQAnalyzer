#Script for drawing the event yield graph for Higgs samples

import ROOT
from numpy import arange

#filename = 'LQ_1_4TeV_1_histOut_all.root'
filename = 'higgsRootFiles/Higgs2017_noHLTMET100_histOut_all.root' 
infile = ROOT.TFile.Open(filename, 'UPDATE')
mydir = infile.plots
mydir.cd()

evtCountsGraph = mydir.Get('evtCounts')
cut_names = ['No Cut', 'Filters', 'MET', 'LJ_pT,eta', 'LJ_CHF,NHF', 'CaloMET-PFMET', 'Loose Ph', 'Loose El', 'Loose Mu', 'Loose Tau', 'Jet-MET Phi', 'b-jet'] 
x = arange(evtCountsGraph.GetN())

evtCountsGraph.SetMarkerStyle(21)
num_events = evtCountsGraph.GetY()[0]
#print(evtCountsGraph.GetN())

for i in range(evtCountsGraph.GetN()):
    evtCountsGraph.SetPoint(i, x[i], evtCountsGraph.GetY()[i]/num_events)      

x_ax = evtCountsGraph.GetXaxis()
x_ax.Set(12,0,11)

for i in range(len(cut_names)):
    x_ax.SetBinLabel(i+1, cut_names[i])

#Event Counts
canv1 = ROOT.TCanvas("canv1","canv1")
canv1.SetGrid()

evtCountsGraph.Draw("AP")
canv1.Print("evtCounts_Higgs_noHLTMET100.png")
evtCountsGraph.Write()


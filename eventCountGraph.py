#Script for drawing the event yield graph for LQ samples

import ROOT
from numpy import arange

filename = 'LQRootFiles/LQ_1_4TeV_1_histOut_all.root'
infile = ROOT.TFile.Open(filename, 'UPDATE')
mydir = infile.plots
mydir.cd()

evtCountsGraph = mydir.Get('evtCounts;1')
cut_names = ['No Cut', 'HLT', 'Filters', 'Loose Mu', 'Loose El', 'Loose Ph', 'Loose Tau', 'MET', 'LJ_pT,eta', 'LJ_CHF,NHF', 'CaloMET-PFMET', 'Jet-MET Phi', 'b-jet'] 
x = arange(evtCountsGraph.GetN())

evtCountsGraph.SetMarkerStyle(21)

num_events = evtCountsGraph.GetY()[0]
#print(evtCountsGraph.GetN())

for i in range(evtCountsGraph.GetN()):
    evtCountsGraph.SetPoint(i, x[i], evtCountsGraph.GetY()[i]*100/num_events)      

x_ax = evtCountsGraph.GetXaxis()
x_ax.Set(13,0,13)

for i in range(len(cut_names)):
    x_ax.SetBinLabel(i+1, cut_names[i])

#x_ax.CenterLabels()
x_ax.LabelsOption("v")
x_ax.SetTitle('Cuts')
x_ax.SetTitleOffset(1.4)
x_ax.SetLabelSize(0.03)


evtCountsGraph.GetYaxis().SetTitle('% Events Passing')

canv1 = ROOT.TCanvas("canv1","canv1", 800, 600)
canv1.SetGrid()
canv1.SetBottomMargin(0.20)

evtCountsGraph.Draw("AP")
canv1.Print("evtCounts_LQ_1_4TeV_1.png")
evtCountsGraph.Write()


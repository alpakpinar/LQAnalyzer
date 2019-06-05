#Script for drawing three leading jet pt histograms (on the same canvas) for three different mass and coupling points

import ROOT

#Three mass points

labels = ['0_5TeV_1', '1TeV_1', '1_4TeV_1']
colors = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed]
legend_labels = ['M_{LQ} = 0.5 TeV', 'M_{LQ} = 1 TeV', 'M_{LQ} = 1.4 TeV']
histos = {}

#No stat box
ROOT.gStyle.SetOptStat(0)

canv = ROOT.TCanvas('canv', 'canv', 800, 600)

legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.041)
legend.SetTextFont(42)

for j, label in enumerate(labels):

    infile = ROOT.TFile('LQRootFiles/LQ_' + label + '_histOut_all.root')
    plotdir = infile.plots
    plotdir.cd()
    
    print('Inside the file %s' % infile.GetName())

    histos[label] = plotdir.Get('leadingJetPt;1')

    print('Got the histogram')

    histos[label].SetDirectory(0) #To decouple the hist from the open file directory!

    infile.Close()
    
    histos[label].GetYaxis().SetTitle('Number of Events (Normalized)') 
    histos[label].SetLineColor(colors[j])
    histos[label].SetTitle('Leading Jet p_{T}, #lambda = 1.0')
    
    if j == 0:
        histos[label].DrawNormalized()
    else:
        histos[label].DrawNormalized('same')
   
    legend.AddEntry(histos[label], legend_labels[j], 'L')

legend.Draw()
canv.Print("savedPlots/comparisonPlots/LeadingJetPtPlot_mass.png")

#########################

#Three coupling points

labels = ['1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5']
colors = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed]
legend_labels = ['#lambda = 0.7', '#lambda = 1.0', '#lambda = 1.5']
histos = {}

canv2 = ROOT.TCanvas('canv2', 'canv2', 800, 600)

legend2 = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
legend2.SetFillStyle(0)
legend2.SetBorderSize(0)
legend2.SetTextSize(0.041)
legend2.SetTextFont(42)

for j, label in enumerate(labels):
    infile = ROOT.TFile('LQRootFiles/LQ_' + label + '_histOut_all.root')
    plotdir = infile.plots
    plotdir.cd()

    print('Inside the file %s' % infile.GetName())

    histos[label] = plotdir.Get('leadingJetPt;1')

    print('Got the histogram')

    histos[label].SetDirectory(0) #To decouple the hist from open file directory!

    infile.Close()

    histos[label].GetYaxis().SetTitle('Number of Events (Normalized)')
    histos[label].SetLineColor(colors[j])
    histos[label].SetTitle('Leading Jet p_{T}, M_{LQ} = 1.4 TeV')

    if j == 0:
        histos[label].DrawNormalized()
    else:
        histos[label].DrawNormalized('same')

    legend2.AddEntry(histos[label], legend_labels[j], 'L')

legend2.Draw()
canv2.Print("savedPlots/comparisonPlots/LeadingJetPtPlot_coupling.png")



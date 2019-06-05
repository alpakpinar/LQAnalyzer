#Script for drawing three MET histograms (on the same canvas) for three different mass and coupling points

import ROOT

#Three mass points

labels = ['0_5TeV_1', '1TeV_1', '1_4TeV_1']
colors = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed]
legend_labels = ['M_{LQ} = 0.5 TeV', 'M_{LQ} = 1 TeV', 'M_{LQ} = 1.4 TeV']
METhistos = {}

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

    METhistos[label] = plotdir.Get('MET;1')
    
    print('Got the histogram')

    METhistos[label].SetDirectory(0) #To decouple the hist from the open file directory!

    infile.Close()
    
    for i in range(METhistos[label].GetNbinsX()):
        original_cont = METhistos[label].GetBinContent(i+1)
        bin_width = METhistos[label].GetBinWidth(i+1)
      
        METhistos[label].SetBinContent(i+1, original_cont/bin_width)
    
    print('Bin width division complete')

    METhistos[label].GetYaxis().SetTitle('Number of Events / GeV (Normalized)') 
    METhistos[label].SetLineColor(colors[j])
    METhistos[label].SetTitle('Missing Transverse Energy, #lambda = 1.0')
    
    #Drawing MET histograms, normalized to 1

    if j == 0:
        METhistos[label].DrawNormalized()
    else:
        METhistos[label].DrawNormalized('same')
   
    legend.AddEntry(METhistos[label], legend_labels[j], 'L')

legend.Draw()
canv.Print("savedPlots/comparisonPlots/METPlot_mass.png")

#########################

#Three coupling points

labels = ['1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5']
colors = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed]
legend_labels = ['#lambda = 0.7', '#lambda = 1.0', '#lambda = 1.5']
METhistos = {}

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

    METhistos[label] = plotdir.Get('MET;1')

    print('Got the histogram')

    METhistos[label].SetDirectory(0) #To decouple the hist from open file directory!

    infile.Close()

    for i in range(METhistos[label].GetNbinsX()):
        original_cont = METhistos[label].GetBinContent(i+1)
        bin_width = METhistos[label].GetBinWidth(i+1)

        METhistos[label].SetBinContent(i+1, original_cont/bin_width)

    print('Bin width division complete')

    METhistos[label].GetYaxis().SetTitle('Number of Events / GeV (Normalized)')
    METhistos[label].SetLineColor(colors[j])
    METhistos[label].SetTitle('Missing Transverse Energy, M_{LQ} = 1.4 TeV')

    if j == 0:
        METhistos[label].DrawNormalized()
    else:
        METhistos[label].DrawNormalized('same')

    legend2.AddEntry(METhistos[label], legend_labels[j], 'L')

legend2.Draw()
canv2.Print("savedPlots/comparisonPlots/METPlot_coupling.png")



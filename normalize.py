#Module for normalizing and plotting the leptoquark histograms

import ROOT
import os

def drawHist(filename, LQParams, fillHist=False, saveHistToROOT=True): 
    
    #No stat box
    ROOT.gStyle.SetOptStat(0)

    #Thicker lines
    ROOT.gStyle.SetHistLineWidth(2)

    #Creating PNG directory if not created before
    pngDir = 'savedPlots/normalizedPlots/' + LQParams
	
    if not os.path.exists(pngDir):

        os.mkdir(pngDir) 
 
    labels = ['1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5', '0_5TeV_1', '1TeV_1', '2TeV_1']
    xsections = [0.003762, 0.007397, 0.01542, 0.04106, 2.294, 0.09211, 0.001973]
    numEvents = [50000, 50000, 49500, 50000, 49750, 50000, 49750]    

    crossSections = {}
    num_events_gen = {}    

    for i, label in enumerate(labels):
        crossSections[label] = xsections[i]
        num_events_gen[label] = numEvents[i]

    cross_section = crossSections[LQParams]
    num_events = num_events_gen[LQParams]
    luminosity = 35900
    norm_weight = cross_section*luminosity/num_events

    print('Cross section: %f, Number of events generated: %d' % (cross_section, num_events))

    infile = ROOT.TFile.Open(filename, 'UPDATE')
    mydir = infile.plots
    mydir.cd()

    print('Inside the file %s' % filename)
    print('Working on MET histogram...')

    canv = ROOT.TCanvas('canv', 'canv')

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

    if fillHist:
        METHist.SetFillStyle(1001)
        METHist.SetFillColor(ROOT.kRed)
        METHist.SetLineColor(ROOT.kBlack)
    
    else:
        METHist.SetLineColor(ROOT.kBlue)

    METHist.Draw("Hist")
    canv.Print(os.path.join(pngDir, "MET_" + LQParams + ".png"))

    if saveHistToROOT:
        METHist.Write()

    print('Working on jet-MET phi histogram...')

    canv2 = ROOT.TCanvas('canv2', 'canv2')

    jetMET_hist = mydir.Get('jetMETPhi;1')
    jetMET_hist.Scale(norm_weight)
    jetMET_hist.GetYaxis().SetTitle('Number of Events')

    if fillHist:
        jetMET_hist.SetFillStyle(1001)
        jetMET_hist.SetFillColor(ROOT.kRed)
        jetMET_hist.SetLineColor(ROOT.kBlack)    

    else:
        jetMET_hist.SetLineColor(ROOT.kBlue)

    #Changing x-axis labels
    axis = jetMET_hist.GetXaxis()
    axis.SetNdivisions(504, ROOT.kFALSE)
    axis.ChangeLabel(2, -1, -1, -1, -1, -1, "#pi/4")
    axis.ChangeLabel(3, -1, -1, -1, -1, -1, "#pi/2")
    axis.ChangeLabel(4, -1, -1, -1, -1, -1, "3#pi/4")
    axis.ChangeLabel(5, -1, -1, -1, -1, -1, "#pi")

    jetMET_hist.Draw("Hist")
    canv2.Print(os.path.join(pngDir, "jetMETPhi_" + LQParams + ".png"))
    
    if saveHistToROOT:
        jetMET_hist.Write()

    print('Working on num-bJets histogram...')

    canv3 = ROOT.TCanvas('canv3', 'canv3')

    numbJets_hist = mydir.Get('numbJets;1')
    numbJets_hist.Scale(norm_weight)

    if fillHist:
        numbJets_hist.SetFillStyle(1001)
        numbJets_hist.SetFillColor(ROOT.kRed)
        numbJets_hist.SetLineColor(ROOT.kBlack)

    else:    
        numbJets_hist.SetLineColor(ROOT.kBlue)

    numbJets_hist.GetXaxis().SetNdivisions(504, ROOT.kFALSE)

    numbJets_hist.Draw("Hist")
    canv3.Print(os.path.join(pngDir, "numbJets_" + LQParams + ".png"))
    
    if saveHistToROOT:
        numbJets_hist.Write()

    print('Working on numLQ histogram...')

    canv4 = ROOT.TCanvas('canv4', 'canv4')

    numLQ_hist = mydir.Get('numLQ;1')
    numLQ_hist.Scale(norm_weight)

    if fillHist:
        numLQ_hist.SetFillStyle(1001)
        numLQ_hist.SetFillColor(ROOT.kRed)
        numLQ_hist.SetLineColor(ROOT.kBlack)
    
    else:
        numLQ_hist.SetLineColor(ROOT.kBlue)

    numLQ_hist.GetXaxis().SetNdivisions(505, ROOT.kFALSE)

    numLQ_hist.Draw("Hist")
    canv4.Print(os.path.join(pngDir, "numLQ_" + LQParams + ".png"))
    
    if saveHistToROOT:
        numLQ_hist.Write()

    print('Working on leading jet Pt histogram...')

    canv5 = ROOT.TCanvas('canv5', 'canv5')

    leadingJetPt_hist = mydir.Get('leadingJetPt;1')
    leadingJetPt_hist.Scale(norm_weight)

    if fillHist:
        leadingJetPt_hist.SetFillStyle(1001)
        leadingJetPt_hist.SetFillColor(ROOT.kRed)
        leadingJetPt_hist.SetLineColor(ROOT.kBlack)

    else:    
        leadingJetPt_hist.SetLineColor(ROOT.kBlue)

    leadingJetPt_hist.Draw("Hist")
    canv5.Print(os.path.join(pngDir, "leadingJetPt_" + LQParams + ".png"))
   
    if saveHistToROOT:
         leadingJetPt_hist.Write()

    print('*****Job finished*****')






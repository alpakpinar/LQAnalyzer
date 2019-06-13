#Module for drawing Brazilian plot for different mass points

import ROOT
import numpy as np

def cmsText(pad):
    cmsText = 'CMS'
    cmsTextFont = 61
    
    extraText   = "Preliminary"
    extraTextFont = 52 
 
    lumiTextSize     = 0.6
    lumiTextOffset   = 0.2
 
    cmsTextSize      = 0.75
    cmsTextOffset    = 0.1
 
    relPosX    = 0.045
    relPosY    = 0.035
    relExtraDY = 1.2
 
    extraOverCmsTextSize  = 0.76
 
    #lumi_13TeV = "35.9 fb^{-1}"
    lumi_13TeV = "137 fb^{-1}"

    align_ = 13

    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025

    pad.cd()

    lumi_text = lumi_13TeV + ' (13 TeV)'

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)

    extraTextSize = extraOverCmsTextSize*cmsTextSize
 
    latex.SetTextFont(42)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    
 
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumi_text)

    pad.cd()

    posX_ =   l + relPosX*(1-l-r)   # left aligned
    posY_ = 1-t - relPosY*(1-t-b)
    
    latex.SetTextFont(cmsTextFont)
    latex.SetTextSize(cmsTextSize*t)
    latex.SetTextAlign(align_)
    latex.DrawLatex(posX_, posY_, cmsText)
  
    pad.Update()

def plotLimits(values, upperbounds95, upperbounds68, median_exclusion, lowerbounds68, lowerbounds95):
    
    N = len(values)
    yellow = ROOT.TGraph(2*N)
    green = ROOT.TGraph(2*N)
    median = ROOT.TGraph(N)
    boundLine = ROOT.TGraph(N)

    for i in range(N):
	yellow.SetPoint(i, values[i], upperbounds95[i]) #+2 sigma
	green.SetPoint(i, values[i], upperbounds68[i]) #+1 sigma
	median.SetPoint(i, values[i], median_exclusion[i]) #Median
	green.SetPoint(2*N-i-1, values[i], lowerbounds68[i]) #-1 sigma
	yellow.SetPoint(2*N-i-1, values[i], lowerbounds95[i]) #-2 sigma
	boundLine.SetPoint(i, values[i], 1) #constant line at 1

    W = 800
    H = 600
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W
    
    c = ROOT.TCanvas('c', 'c', 100, 100, W, H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    c.SetGrid()
    c.cd()

    frame = c.DrawFrame(1.4, 0.001, 4.1, 10)
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(0.9)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetYaxis().CenterTitle(True)
    frame.GetYaxis().SetTitle("Upper limit on #sigma / #sigma_{th}") 
    frame.GetXaxis().SetTitle("LQ Mass [GeV]")
    frame.SetMinimum(0)
    frame.SetMaximum(max(upperbounds95)*1.05)
    frame.GetXaxis().SetLimits(min(values),max(values))
 
    yellow.SetFillColor(ROOT.kOrange)
    yellow.SetLineColor(ROOT.kOrange)
    yellow.SetFillStyle(1001)
    yellow.Draw('F')
 
    green.SetFillColor(ROOT.kGreen+1)
    green.SetLineColor(ROOT.kGreen+1)
    green.SetFillStyle(1001)
    green.Draw('Fsame')
 
    median.SetLineColor(1)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.Draw('Lsame')

    boundLine.SetLineColor(ROOT.kRed)
    boundLine.SetLineWidth(2)
    boundLine.SetLineStyle(2)
    boundLine.Draw('Lsame')

    ROOT.gPad.SetTicks(1,1)
    frame.Draw('sameaxis')

    x1 = 0.15
    x2 = x1 + 0.24
    y2 = 0.76
    y1 = 0.60
    legend = ROOT.TLegend(x1,y1,x2,y2)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.041)
    legend.SetTextFont(42)
    legend.AddEntry(median, "50% CL_{s} expected" , 'L')
    legend.AddEntry(green, "#pm 1 std. deviation" , 'f')
    legend.AddEntry(yellow, "#pm 2 std. deviation", 'f')
    legend.Draw()

    cmsText(c)
	
    print("Done!")
    c.SaveAs("LQBraPlot_mass.png")
    c.Close()


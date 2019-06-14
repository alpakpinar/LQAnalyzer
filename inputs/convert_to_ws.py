import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from HiggsAnalysis.CombinedLimit.ModelTools import *

cat  = "monojet"

th1name = "hQCD_MonoJ"

fdir = ROOT.TFile('LQ_1_4TeV_0_5_histOut_all.root','READ')
#fdir = ROOT.TFile.Open('LQ_1_4TeV_1_histOut_all.root','READ')

wsin_combine = ROOT.RooWorkspace("monoxLQ","monoxLQ")
wsin_combine._import = SafeWorkspaceImporter(wsin_combine)#getattr(wsin_combine,"import")

#obj = fdir.plots.Get("MET")
obj = fdir.Get("plots/MET;2") 
nbins = obj.GetNbinsX()
varl = ROOT.RooRealVar("met_"+cat,"met_"+cat,0,100000);

print obj.GetName(), obj.GetTitle(), type(obj)
if type(obj)!=type(ROOT.TH1F()): 
  print "Histogram is not TH1F type!"
title = obj.GetTitle()
name = obj.GetName()
if not obj.Integral() > 0 : obj.SetBinContent(1,0.0001) # otherwise Combine will complain! 
print "Creating Data Hist for ", name
dhist = ROOT.RooDataHist("%s_signal_leptoquark"%(cat),"Dataset for leptoquark in monojet SR",ROOT.RooArgList(varl),obj)
wsin_combine._import(dhist)
wsin_combine.writeToFile("%s_lq.root"%(cat))


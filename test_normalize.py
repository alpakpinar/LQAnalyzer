import ROOT

filename = 'LQ_1_4TeV_1_histOut_all.root'
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
    print("Bin Width %d is %d" %(i+1, bin_width))
    print("Multiplying bin %d by %f" %(i+1, norm_weight/bin_width))
    METHist.SetBinContent(i+1, original_cont/bin_width)

METHist.Scale(norm_weight)
METHist.GetYaxis().SetTitle('Number of Events')
METHist.Draw("Hist")
canv2.Print("MET_1_4TeV_1.png")
METHist.Write()

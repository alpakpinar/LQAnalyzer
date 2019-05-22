import ROOT

luminosity = 35900
ggHcross_section = 43.92
numHiggsEvents = 994000
normWeight = ggHcross_section*luminosity/numHiggsEvents

filename = 'fitDiagnostics.root'

second_file = 'Higgs2017_histOut_all.root'

infile = ROOT.TFile.Open(filename)
my_dir = infile.shapes_prefit.GetDirectory('ch1')
histo = my_dir.Get('ggH_hinv')
histo.GetXaxis().SetTitle('MET (GeV)')

canv = ROOT.TCanvas('canv', 'canv')

histo.Draw()

new_file = ROOT.TFile.Open(second_file, 'UPDATE')
plotsdir = new_file.plots
plotsdir.cd()

METHist = plotsdir.Get('MET')

for i in range(METHist.GetNbinsX()):
    original_cont = METHist.GetBinContent(i+1)
    bin_width = METHist.GetBinWidth(i+1)
    METHist.SetBinContent(i+1, original_cont/bin_width) 

METHist.Scale(normWeight)
METHist.Draw("hist same")
METHist.Write()

canv.Print('EventYields_Higgs2017.png')



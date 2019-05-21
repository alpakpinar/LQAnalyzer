import ROOT

luminosity = 35900
ggHcross_section = 43.92
numHiggsEvents = 994000
normWeight = ggHcross_section*luminosity/numHiggsEvents

filename = 'Higgs2017_histOut_all.root'

infile = ROOT.TFile.Open(filename, 'UPDATE')
plotsdir = infile.plots

plotsdir.cd()

canv = ROOT.TCanvas('canv', 'canv')
METHist = plotsdir.Get('MET')
METHist.Scale(normWeight/52.2727)
METHist.GetYaxis().SetTitle('Number of Events / 52.2727')
METHist.GetYaxis().SetTitleOffset(1.5)
METHist.SetTitle('MET Distribution')
METHist.Draw("hist")
METHist.Write()

second_file = 'fitDiagnostics.root'

new_file = ROOT.TFile.Open(second_file)
my_dir = new_file.shapes_prefit.GetDirectory('ch1')
histo = my_dir.Get('ggH_hinv')
histo.Draw("same")

canv.Print('EventYields_Higgs2017.png')



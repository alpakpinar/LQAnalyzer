import ROOT
import os

#FWLite python libraries
from DataFormats.FWLite import Handle, Events

#FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

ROOT.gStyle.SetOptStat(0)

LQParams = '2TeV_1_5'

MET_bounds = [150, 250, 350]

#Defining output file
fout = ROOT.TFile('GENSIM_MET_' + LQParams +  'numLQcomparisonPlot_50METCut.root', "RECREATE")

LQMass = '2 TeV'
LQCoupling = '1.5'

#Prepare the MET histogram
MET_hist=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + LQMass + ' #lambda = ' + LQCoupling, 27, 50, 1400)
MET_hist.GetXaxis().SetTitle('MET (GeV)')
MET_hist.GetYaxis().SetTitle('Number of Events')

#Prepare the numLQ histogram
numLQ_hist1=ROOT.TH1F('numLQ1', 'Number of Leptoquarks', 4, 0, 4)
numLQ_hist1.GetXaxis().SetTitle('Number of Leptoquarks')
numLQ_hist1.GetYaxis().SetTitle('Number of Events')

numLQ_hist2=ROOT.TH1F('numLQ2', 'Number of Leptoquarks', 4, 0, 4)

numLQ_hist3=ROOT.TH1F('numLQ3', 'Number of Leptoquarks', 4, 0, 4)

mets, metLabel = Handle("std::vector<reco::GenMET>"), "genMetTrue" 
genParticles, genParticleLabel = Handle("std::vector<reco::GenParticle>"), "genParticles"

#inputFile = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/SLQ_1_4TeV_1_noGenCut_RunIIFall17wmLHEGS-00007_1.root'
#inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/' #No cuts
#inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/shape_study/SLQ_2TeV_0_5/SLQ_2TeV_0_5_LHEGS/190525_193828/0000'
inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/shape_study/SLQ_2TeV_1_5/SLQ_2TeV_1_5_LHEGS/190524_033135/0000' #2 TeV, 1.5 coupling

file_count = 0

print('Starting analyzing files in %s' % inputDir)

for inputFile in os.listdir(inputDir):
    
    if file_count == 25: break #For quick tests

    if 'inLHE' not in inputFile:
	inFile = os.path.join(inputDir,inputFile)
        file_count += 1
        events = Events(inFile)
        nevents = int(events.size())
        if file_count % 10 == 0:
	    print("Analyzing file # %d" % file_count)
        #print("Number of events: %d" % nevents)

        for event in events:

            event.getByLabel(metLabel, mets)
	    event.getByLabel(genParticleLabel, genParticles)

            MET_hist.Fill(mets.product()[0].pt())

	    numLQ = [0, 0, 0]

	    if mets.product()[0].pt() < MET_bounds[0]:

	        for particle in genParticles.product():
		 	    
		    if abs(particle.pdgId()) == 1104 and particle.status() == 22:

	    	        numLQ[0] += 1	

	    numLQ_hist1.Fill(numLQ[0])

	    if mets.product()[0].pt() < MET_bounds[1]:

	        for particle in genParticles.product():
		 	    
		    if abs(particle.pdgId()) == 1104 and particle.status() == 22:

	    	        numLQ[1] += 1	

	    numLQ_hist2.Fill(numLQ[1])

	    if mets.product()[0].pt() < MET_bounds[2]:

	        for particle in genParticles.product():
		 	    
		    if abs(particle.pdgId()) == 1104 and particle.status() == 22:

	    	        numLQ[2] += 1	

	    numLQ_hist3.Fill(numLQ[2])


print('Normalizing MET histogram...')

cross_section = 0.005347 #2 TeV, 1.5 coupling
#cross_section = 0.06559 #for the no-cut sample
#cross_section = 0.0004373
luminosity = 35900
num_events = 50000
normWeight = cross_section*luminosity/num_events

MET_hist.Scale(normWeight)

print('Normalizing numLQ histograms...')

numLQ_hist1.Scale(normWeight)
numLQ_hist1.SetNdivisions(505)
numLQ_hist1.SetLineColor(ROOT.kBlue)

numLQ_hist2.Scale(normWeight)
numLQ_hist2.SetNdivisions(505)
numLQ_hist2.SetLineColor(ROOT.kBlack)

numLQ_hist3.Scale(normWeight)
numLQ_hist3.SetNdivisions(505)
numLQ_hist3.SetLineColor(ROOT.kRed)

#Creating a legend
print('Writing the legend...')

legend = ROOT.TLegend(0.55, 0.55, 0.8, 0.8)
legend.SetBorderSize(0)
legend.AddEntry(numLQ_hist1, 'MET < ' + str(MET_bounds[0]) + ' GeV', 'L')
legend.AddEntry(numLQ_hist2, 'MET < ' + str(MET_bounds[1]) + ' GeV', 'L')
legend.AddEntry(numLQ_hist3, 'MET < ' + str(MET_bounds[2]) + ' GeV', 'L')

print('Drawing the histograms and saving the ROOT file...')
canv = ROOT.TCanvas('canv', 'canv')
MET_hist.Draw("hist")
canv.Print('savedPlots/METPlots/GENSIM_METPlots/GENSIM_MET_' + LQParams + 'newTrial_noMETCut.png')

canv2 = ROOT.TCanvas('canv2', 'canv2')
numLQ_hist1.Draw("hist")
numLQ_hist2.Draw("histsame")
numLQ_hist3.Draw("histsame")
legend.Draw("same")

canv2.Print("savedPlots/METPlots/GENSIM_METPlots/GENSIM_numLQ_" + LQParams + 'comparison_50METCut.png') 

fout.Write()



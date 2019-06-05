import ROOT
import os

#FWLite python libraries
from DataFormats.FWLite import Handle, Events

#FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

LQParams = '1_4TeV_1'

#Defining output file
fout = ROOT.TFile('GENSIM_MET_' + LQParams +  '_50METCut.root', "RECREATE")

LQMass = '1.4 TeV'
LQCoupling = '1.0'

#Prepare the MET histogram
MET_hist=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + LQMass + ' #lambda = ' + LQCoupling, 27, 0, 1400)
MET_hist.GetXaxis().SetTitle('MET (GeV)')
MET_hist.GetYaxis().SetTitle('Number of Events')

#Prepare the numLQ histogram
numLQ_hist=ROOT.TH1F('numLQ', 'Number of Leptoquarks, MET < 50 GeV', 4, 0, 4)
numLQ_hist.GetXaxis().SetTitle('Number of Leptoquarks')
numLQ_hist.GetYaxis().SetTitle('Number of Events')

mets, metLabel = Handle("std::vector<reco::GenMET>"), "genMetTrue" 
genParticles, genParticleLabel = Handle("std::vector<reco::GenParticle>"), "genParticles"

#inputFile = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/SLQ_1_4TeV_1_noGenCut_RunIIFall17wmLHEGS-00007_1.root'
inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/' #No cuts
#inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/shape_study/SLQ_2TeV_0_5/SLQ_2TeV_0_5_LHEGS/190525_193828/0000'

file_count = 0

print('Starting analyzing files in %s' % inputDir)

for inputFile in os.listdir(inputDir):
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

	    numLQ = 0

	    if mets.product()[0].pt() < 50:

	        for particle in genParticles.product():
		 	    
		    if abs(particle.pdgId()) == 1104 and particle.status() == 22:

	    	        numLQ += 1

	    numLQ_hist.Fill(numLQ)

print('Normalizing MET histogram...')

cross_section = 0.06559 #for the no-cut sample
#cross_section = 0.0004373
luminosity = 35900
num_events = 50000
normWeight = cross_section*luminosity/num_events

MET_hist.Scale(normWeight)

print('Normalizing numLQ histogram...')

numLQ_hist.Scale(normWeight)
numLQ_hist.SetNdivisions(505)

print('Drawing the histograms and saving the ROOT file...')
canv = ROOT.TCanvas('canv', 'canv')
MET_hist.Draw("hist")
canv.Print('savedPlots/METPlots/GENSIM_METPlots/GENSIM_MET_' + LQParams + '_noMETCut.png')

canv2 = ROOT.TCanvas('canv2', 'canv2')
numLQ_hist.Draw("hist")
canv2.Print("savedPlots/METPlots/GENSIM_METPlots/GENSIM_numLQ_" + LQParams + '_noMETCut.png') 

fout.Write()



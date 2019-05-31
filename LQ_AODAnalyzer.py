import ROOT
import os

#FWLite python libraries
from DataFormats.FWLite import Handle, Events

#FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

LQParams = '0_5TeV_0_7'

#Defining output file
fout = ROOT.TFile('GENSIM_MET_' + LQParams +  '_50METCut.root', "RECREATE")

LQMass = LQParams[0] + '.' + LQParams[2] + ' ' + LQParams[3:6]
LQCoupling = LQParams[-3] + '.' + LQParams[-1]

#Prepare the MET histogram
MET_hist=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + LQMass + ' #lambda = ' + LQCoupling, 27, 50, 1400)
MET_hist.GetXaxis().SetTitle('MET (GeV)')
MET_hist.GetYaxis().SetTitle('Number of Events')

mets, metLabel = Handle("std::vector<reco::GenMET>"), "genMetTrue" 

#inputFile = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/SLQ_1_4TeV_1_noGenCut_RunIIFall17wmLHEGS-00007_1.root'
#inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1_noGenCut/SLQ_1_4TeV_1_LHEGS_noGenCut/190530_160018/0000/' #No cuts
inputDir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/shape_study/SLQ_0_5TeV_0_7/SLQ_0_5TeV_0_7_LHEGS/190526_233645/0000'

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
            MET_hist.Fill(mets.product()[0].pt())

print('Normalizing MET histogram...')
cross_section = 1.162
luminosity = 35900
num_events = 50000
normWeight = cross_section*luminosity/num_events

MET_hist.Scale(normWeight)

print('Drawing the histogram and saving the ROOT file...')
canv = ROOT.TCanvas('canv', 'canv')
MET_hist.Draw("hist")
canv.Print('savedPlots/METPlots/GENSIM_METPlots/GENSIM_MET_' + LQParams + '_50METCut.png')

fout.Write()



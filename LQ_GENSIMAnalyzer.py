import ROOT
import os
import argparse
from numpy import array

#FWLite python libraries
from DataFormats.FWLite import Handle, Events

#FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mass', help = 'Mass of the LQ sample in TeV (Enter with an underscore)')
parser.add_argument('-c', '--coupling', help = 'Coupling of the LQ sample (Enter with an underscore)')
parser.add_argument('-s', '--short', help = 'Run over first 25 files', action = 'store_true')
parser.add_argument('--genCut', help = 'Run over files with genCut MET > 50 GeV', action = 'store_true')
parser.add_argument('--LQhist', help = 'Draw the numLQ comparison histograms for three cases', action = 'store_true')

args = parser.parse_args()

LQParams = args.mass + 'TeV_' + args.coupling

#Arranging parameters for the graph titles

if '_' in args.mass:
    index = args.mass.find('_')
    LQMass = args.mass[:index] + '.' + args.mass[index+1:] + ' TeV' 

else:

    LQMass = args.mass + ' TeV'

if '_' in args.coupling:
    index = args.coupling.find('_')
    LQCoupling = args.coupling[:index] + '.' + args.coupling[index+1:]

else:
    LQCoupling = args.coupling

print('LQ Mass: %s, LQ Coupling: %s' % (LQMass, LQCoupling))
print('MET > 50 GeV cut: %s' % args.genCut)
print('Drawing numLQ histograms: %s' % args.LQhist)
print('Running in short mode: %s' % args.short)

##########################
#Choosing the cross-section

labels_genCut = ['0_5TeV_0_5', '0_5TeV_0_7', '0_5TeV_1', '0_5TeV_1_5', '1TeV_0_5', '1TeV_0_7', '1TeV_1', '1TeV_1_5', '1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5', '2TeV_0_5', '2TeV_0_7', '2TeV_1', '2TeV_1_5', '2_25TeV_1', '2_5TeV_1_2', '1_75TeV_0_8', '1_5TeV_0_6', '1_25TeV_0_4']

xsections_genCut = [0.6892, 1.162, 2.294, 5.779, 0.02342, 0.04379, 0.09211, 0.239, 0.003762, 0.007397, 0.01542, 0.04106, 0.0004373, 0.0008746, 0.001973, 0.005347, 0.0009407, 0.0007549, 0.002705, 0.003682, 0.00469]

crossSections_genCut = {}

for i, label in enumerate(labels_genCut):
    crossSections_genCut[label] = xsections_genCut[i]

labels_nogenCut = ['0_5TeV_1_5', '1_4TeV_1', '2TeV_1_5']

xsections_nogenCut = [19.37, 0.06559, 0.06647]  

crossSections_nogenCut = {}

for i, label in enumerate(labels_nogenCut):
    crossSections_nogenCut[label] = xsections_nogenCut[i]  

if args.genCut:
    print('Samples with cut MET > 50 GeV will be analyzed')
    cross_section = crossSections_genCut[LQParams] 
    print('Cross section of the process: %f pb' % cross_section)

else:
    print('Samples with NO generator level cuts will be analyzed')
    cross_section = crossSections_nogenCut[LQParams]
    print('Cross section of the process: %f pb' % cross_section)

#########################

MET_bounds = [150, 250, 350]

#Defining output file
if args.LQhist and args.genCut:
    fout = ROOT.TFile('GENSIM_MET_' + LQParams +  'numLQcomparisonPlot_50METCut.root', "RECREATE")

elif args.LQhist and not args.genCut:
    fout = ROOT.TFile('GENSIM_MET_' + LQParams +  'numLQcomparisonPlot_noMETCut.root', "RECREATE")

elif not args.LQhist and args.genCut:
    fout = ROOT.TFile('GENSIM_MET_' + LQParams +  '_50METCut.root', "RECREATE")

elif not args.LQhist and not args.genCut:
    fout = ROOT.TFile('GENSIM_MET_' + LQParams +  '_noMETCut.root', "RECREATE")

#Prepare the MET histogram

edges = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0] 
MET_hist=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + LQMass + ' #lambda = ' + str(LQCoupling), 22, array(edges))

#MET_hist=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + LQMass + ' #lambda = ' + LQCoupling, 20, 0, 100)
MET_hist.GetXaxis().SetTitle('MET (GeV)')
MET_hist.GetYaxis().SetTitle('Number of Events')

#Prepare the numLQ histogram
numLQ_hist1=ROOT.TH1F('numLQ1', 'Number of Leptoquarks, M = ' + LQMass + ' #lambda = ' + LQCoupling, 4, 0, 4)
numLQ_hist1.GetXaxis().SetTitle('Number of Leptoquarks')
numLQ_hist1.GetYaxis().SetTitle('Number of Events')

numLQ_hist2=ROOT.TH1F('numLQ2', 'Number of Leptoquarks', 4, 0, 4)

numLQ_hist3=ROOT.TH1F('numLQ3', 'Number of Leptoquarks', 4, 0, 4)

mets, metLabel = Handle("std::vector<reco::GenMET>"), "genMetTrue" 
genParticles, genParticleLabel = Handle("std::vector<reco::GenParticle>"), "genParticles"

if args.genCut: #Files with MET > 50 GeV
    shape_study_dir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/shape_study/SLQ_' + LQParams
    sample_dir = 'SLQ_' + LQParams + '_LHEGS'
    inputDir = os.path.join(shape_study_dir, sample_dir)
    inputDir += '/' + os.listdir(inputDir)[0] + '/0000'

else: #Files with no genCut
    prod_dir = '/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_' + LQParams + '_noGenCut'
    sample_dir = 'SLQ_' + LQParams + '_LHEGS_noGenCut'
    inputDir = os.path.join(prod_dir, sample_dir)
    inputDir += '/' + os.listdir(inputDir)[0] + '/0000'

file_count = 0

print('Starting analyzing files in %s' % inputDir)

for inputFile in os.listdir(inputDir):
    
    if args.short:
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

	    if args.LQhist:

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

#####################

print('Normalizing MET histogram...')

luminosity = 35900
num_events = 50000
normWeight = cross_section*luminosity/num_events

MET_hist.Scale(normWeight)

if args.LQhist:

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
    
    canv2 = ROOT.TCanvas('canv2', 'canv2')
    numLQ_hist1.Draw("hist")
    numLQ_hist2.Draw("histsame")
    numLQ_hist3.Draw("histsame")
    legend.Draw("same")

    if args.genCut:
	canv2.Print("savedPlots/METPlots/GENSIM_METPlots/GENSIM_numLQ_" + LQParams + 'comparison_50METCut.png') 

    else:
	canv2.Print("savedPlots/METPlots/GENSIM_METPlots/GENSIM_numLQ_" + LQParams + 'comparison_noMETCut.png') 
	

print('Drawing the histograms and saving the ROOT file...')
canv = ROOT.TCanvas('canv', 'canv')
MET_hist.Draw("hist")

if args.genCut:
    canv.Print('savedPlots/METPlots/GENSIM_METPlots/GENSIM_MET_' + LQParams + '_50METCut.png')

else:
    canv.Print('savedPlots/METPlots/GENSIM_METPlots/GENSIM_MET_' + LQParams + '_noMETCut.png')

fout.Write()



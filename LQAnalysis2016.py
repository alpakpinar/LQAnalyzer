#!/usr/bin/env python
import os, sys
import ROOT
import glob
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from numpy import arange, zeros, array

class LQAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
	
	self.leadingJetPt=ROOT.TH1F('leadingJetPt', 'Leading Jet Pt', 50, 0, 1500) 
	self.addObject(self.leadingJetPt)
	self.leadingJetPt.GetXaxis().SetTitle('Leading Jet Pt (GeV)')
	self.leadingJetPt.GetYaxis().SetTitle('Number of Events')

	self.num_bJets=ROOT.TH1F('numbJets', 'Number of b-jets', 4, 0, 4)
	self.addObject(self.num_bJets)
	self.num_bJets.GetXaxis().SetTitle('Number of b-jets')
	self.num_bJets.GetYaxis().SetTitle('Number of Events')	

	self.edges = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
	self.MET=ROOT.TH1F('MET', 'Missing Transverse Energy', 22, array(self.edges))
	self.addObject(self.MET) 
	self.MET.GetXaxis().SetTitle('MET (GeV)')
	self.MET.GetYaxis().SetTitle('Number of Events')

	self.jetMETPhi=ROOT.TH1F('jetMETPhi', 'Minimum #Delta #phi Between 4 Leading Jets and MET', 15, 0, math.pi)
	self.addObject(self.jetMETPhi)
	self.jetMETPhi.GetXaxis().SetTitle('#Delta #phi')
	self.jetMETPhi.GetYaxis().SetTitle('Number of Events')	
	
	self.eventCountGraph=ROOT.TGraph(13)
	self.addObject(self.eventCountGraph)

	self.eventCounts = zeros(9)

    def deltaR(self,prt1,prt2):
	eta1, eta2 = prt1.eta, prt2.eta
	phi1, phi2 = prt1.phi, prt2.phi
	eta_diff = eta1 - eta2
	phi_diff = phi1 - phi2
	return math.sqrt((eta_diff)**2 + (phi_diff)**2) 	

    def analyze(self,event):
	self.nLoosePhotons=0
	self.nLooseElectrons=0
	self.nLooseMuons=0
	self.nLooseTaus=0
	
	electrons = Collection(event, 'Electron')
	muons = Collection(event, 'Muon')
	jets = Collection(event, 'Jet')
	photons = Collection(event, 'Photon')
	taus = Collection(event, 'Tau')
	genParticles = Collection(event, 'GenPart')
	genJets = Collection(event, 'GenJet')
	eventSum = ROOT.TLorentzVector()

	self.eventCounts[0] += 1
	
	#AK4 jet requirements
	self.ak4Jets = [jet for jet in jets if (abs(jet.eta) < 2.5 and jet.pt > 30)]
	
	#Taking the non-overlapping leptons/photons
	self.non_ovr_electrons = [el for el in electrons for jet in self.ak4Jets if self.deltaR(jet,el) > 0.4]
	self.non_ovr_muons = [mu for mu in muons for jet in self.ak4Jets if self.deltaR(jet,mu) > 0.4]
	self.non_ovr_taus = [tau for tau in taus for jet in self.ak4Jets if self.deltaR(jet,tau) > 0.4]
	self.non_ovr_photons = [ph for ph in photons for jet in self.ak4Jets if self.deltaR(jet,ph) > 0.4]	

	#Calculate the number of loose electrons	
	for el in self.non_ovr_electrons:
	    if (el.cutBased > 1) and (el.pt > 10) and (abs(el.eta) < 2.5):
	        self.nLooseElectrons += 1

	#Calculate the number of loose muons
	for mu in self.non_ovr_muons:
	    if ((mu.isGlobal == 1) or (mu.isTracker == 1)) and (mu.isPFcand == 1) and (mu.pfRelIso04_all < 0.25):		
	    	self.nLooseMuons += 1

	#Calculate the number of loose taus
	for tau in self.non_ovr_taus:
	    if (tau.pt > 18) and (abs(tau.eta) < 2.3) and (tau.idDecayModeNewDMs == 1) and (tau.idMVAnewDM2017v2 & 4 > 0): 
		self.nLooseTaus += 1	    

	#Calculate the number of loose photons
	for ph in self.non_ovr_photons:
	    if abs(ph.eta) < 2.5 and ph.pt > 15 and ph.cutBased17Bitmap > 0: #for the 2016 dataset
		self.nLoosePhotons += 1
	

	#############
	#Vetoing events with loose leptons or photons
	if self.nLooseMuons != 0: return False
	self.eventCounts[1] += 1 
	if self.nLooseElectrons != 0: return False
	self.eventCounts[2] += 1
	if self.nLoosePhotons != 0: return False
	self.eventCounts[3] += 1
	if self.nLooseTaus != 0: return False
	self.eventCounts[4] += 1 
	#############	

	###############
	self.num_bjets = 0
	for jet in self.ak4Jets:
	    if abs(jet.eta) < 2.4 and jet.pt > 20 and jet.btagCSVV2 > 0.8484: #2016 criteria
		self.num_bjets += 1
	
	self.num_bJets.Fill(self.num_bjets)

	#b-jet veto
	if self.num_bjets != 0: return False

	self.eventCounts[5] += 1

	##############

	if len(jets) > 1:
	    if not (jets[0].pt > 80 and jets[1].pt > 40): return False #For comparison with MIT and UCSD official sync results

	self.eventCounts[6] += 1

	if event.MET_pt <= 200: return False #MET larger than 200 GeV 

	self.eventCounts[7] += 1

	#Delta-phi requirement for first four leading AK4 jets
	self.phiDiff = []
	if 0 < len(self.ak4Jets) <= 4:
	    for jet in self.ak4Jets:
		phi_difference = abs(jet.phi - event.MET_phi)
		if phi_difference <= math.pi:
	            self.phiDiff.append(phi_difference)
		else:
		    self.phiDiff.append(2*math.pi - phi_difference)
	    
	    self.jetMETPhi.Fill(min(self.phiDiff))
	    if min(self.phiDiff) < 0.5: return False

	if len(self.ak4Jets) > 4:
	    for i in range(4):
		phi_difference = abs(jets[i].phi - event.MET_phi)
		if phi_difference <= math.pi:
		    self.phiDiff.append(phi_difference)
	  	else:
		    self.phiDiff.append(2*math.pi - phi_difference)
	    
	    self.jetMETPhi.Fill(min(self.phiDiff))
            if min(self.phiDiff) < 0.5: return False

	self.eventCounts[8] += 1
	
	###################	

	x = arange(len(self.eventCounts))

	self.eventCountGraph.SetNameTitle('evtCounts', 'Event Counts After Each Cut')	

	for i in range(len(self.eventCounts)):
	    self.eventCountGraph.SetPoint(i, x[i], self.eventCounts[i])    
		
	self.leadingJetPt.Fill(jets[0].pt)	
     	 	
	self.MET.Fill(event.MET_pt)

	return True

#preselection='Jet_pt[0] > 100'

ZnnFiles = ['/store/mc/RunIISummer16NanoAODv4/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext2-v1/260000/F2F31654-10E9-9D41-AFCC-DDE40C930347.root', '/store/mc/RunIISummer16NanoAODv4/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext2-v1/260000/6F26C788-BF65-F847-B3D9-51ECCBC107FC.root', '/store/mc/RunIISummer16NanoAODv4/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext2-v1/260000/577F1F8C-25E5-974F-A1B9-1A4DDD0A5AA5.root', '/store/mc/RunIISummer16NanoAODv4/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext2-v1/260000/0FDC56A3-0ADF-2744-A6D6-645F4DF0C905.root']

for i in range(len(ZnnFiles)):
    ZnnFiles[i] = 'root://cmsxrootd.fnal.gov//' + ZnnFiles[i]

p=PostProcessor(".",ZnnFiles,branchsel=None,modules=[LQAnalysis()],noOut=True,histFileName="syncTrial_Znn.root",histDirName="plots")
p.run()
		    

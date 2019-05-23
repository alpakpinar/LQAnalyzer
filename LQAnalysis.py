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
	
	self.LQMass = '1.4 TeV'
	self.LQCoupling = 1.0

	self.leadingJetPt=ROOT.TH1F('leadingJetPt', 'Leading Jet Pt, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling) , 50, 0, 1500) 
	self.addObject(self.leadingJetPt)
	self.leadingJetPt.GetXaxis().SetTitle('Leading Jet Pt (GeV)')
	self.leadingJetPt.GetYaxis().SetTitle('Number of Events')

	self.num_bJets=ROOT.TH1F('numbJets', 'Number of b-jets, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 4, 0, 4)
	self.addObject(self.num_bJets)
	self.num_bJets.GetXaxis().SetTitle('Number of b-jets')
	self.num_bJets.GetYaxis().SetTitle('Number of Events')	

	self.edges = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
	self.MET=ROOT.TH1F('MET', 'Missing Transverse Energy, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 22, array(self.edges))
	self.addObject(self.MET) 
	self.MET.GetXaxis().SetTitle('MET (GeV)')
	self.MET.GetYaxis().SetTitle('Number of Events')

	self.phiDiffGenJets=ROOT.TH1F('phiDiffGenJets', '#Delta #phi Between Two GenJets Coming From u Quark, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 15, 0, math.pi)
	self.addObject(self.phiDiffGenJets)
	self.phiDiffGenJets.GetXaxis().SetTitle('#Delta #phi')
	self.phiDiffGenJets.GetYaxis().SetTitle('Number of Events')

	self.etaDiffGenJets=ROOT.TH1F('etaDiffGenJets', '#Delta #eta Between Two GenJets Coming From u Quark, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 30, -3, 3)
	self.addObject(self.etaDiffGenJets)
	self.etaDiffGenJets.GetXaxis().SetTitle('#Delta #eta')
	self.etaDiffGenJets.GetYaxis().SetTitle('Number of Events')

	self.num_uJets=ROOT.TH1F('num_uJets', 'Number of GenJets Coming From u Quark, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 5, 0, 5)
	self.addObject(self.num_uJets)
	self.num_uJets.GetXaxis().SetTitle('Number of u Jets')
	self.num_uJets.GetYaxis().SetTitle('Number of Events')
	
	self.numLQ=ROOT.TH1F('numLQ', 'Number of Leptoquarks, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 5, 0, 5)
	self.addObject(self.numLQ)
	self.numLQ.GetXaxis().SetTitle('Number of Leptoquarks')
	self.numLQ.GetYaxis().SetTitle('Number of Events')

	self.deltaR_prtJet=ROOT.TH1F('deltaR_prtJet', 'deltaR Between GenParticle and GenJet, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling), 20, 0, 5)
	self.addObject(self.deltaR_prtJet)

	self.jetMETPhi=ROOT.TH1F('jetMETPhi', 'Minimum #Delta #phi Between 4 Leading Jets and MET', 15, 0, math.pi)
	self.addObject(self.jetMETPhi)
	self.jetMETPhi.GetXaxis().SetTitle('#Delta #phi')
	self.jetMETPhi.GetYaxis().SetTitle('Number of Events')	

	self.eventCountGraph=ROOT.TGraph(13)
	self.addObject(self.eventCountGraph)

	self.eventCounts = zeros(13)
	self.cutNames = []

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

	#ET_miss Triggers
	trigger_pass = (event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight == 1) or (event.HLT_PFMETNoMu130_PFMHTNoMu130_IDTight == 1) or (event.HLT_PFMETNoMu140_PFMHTNoMu140_IDTight == 1)

	if not trigger_pass: return False

	self.eventCounts[1] += 1
	
	#############

	#Filters
	if event.Flag_goodVertices != 1: return False
	if event.Flag_globalSuperTightHalo2016Filter != 1: return False
	if event.Flag_HBHENoiseFilter != 1: return False
	if event.Flag_HBHENoiseIsoFilter != 1: return False
	if event.Flag_EcalDeadCellTriggerPrimitiveFilter != 1: return False
	if event.Flag_BadPFMuonFilter != 1: return False
	self.eventCounts[2] += 1

	############

	if event.MET_pt <= 250: return False #MET larger than 250 GeV 

	self.eventCounts[3] += 1

        if len(jets) != 0:
	    if not (jets[0].pt > 100 and abs(jets[0].eta) < 2.5): return False #Leading jet requirements
            self.eventCounts[4] += 1
	    if not (jets[0].chHEF > 0.1 and jets[0].neHEF < 0.8): return False
	    self.eventCounts[5] += 1 
	if abs(event.CaloMET_sumEt - event.MET_sumEt)/event.CaloMET_sumEt >= 0.5: return False #check if the PF MET is correct!	
	
	self.eventCounts[6] += 1	

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
	
	#For Higgs 2017 sample
	#for mu in self.non_ovr_muons:
	#    if (mu.softId == 1) and (mu.isPFcand == 1) and (mu.pfRelIso04_all < 0.25): 
        #	self.nLooseMuons += 1

	#Calculate the number of loose taus
	for tau in self.non_ovr_taus:
	    if (tau.pt > 18) and (abs(tau.eta) < 2.3) and (tau.idDecayModeNewDMs == 1) and (tau.idMVAnewDM2017v2 & 4 > 0): 
		self.nLooseTaus += 1	    

	#Calculate the number of loose photons
	for ph in self.non_ovr_photons:
	    if abs(ph.eta) < 2.5 and ph.pt > 15 and ph.cutBasedBitmap > 0:
		self.nLoosePhotons += 1
	

	#############
	#Vetoing events with loose leptons or photons
	if self.nLoosePhotons != 0: return False
	self.eventCounts[7] += 1 
	if self.nLooseElectrons != 0: return False
	self.eventCounts[8] += 1
	if self.nLooseMuons != 0: return False
	self.eventCounts[9] += 1
	if self.nLooseTaus != 0: return False
	self.eventCounts[10] += 1 
	#############	


	#Delta-phi requirement for first four leading AK4 jets
	self.phiDiff = []
	if len(self.ak4Jets) <= 4:
	    for jet in self.ak4Jets:
		phi_difference = abs(jet.phi - event.MET_phi)
		if phi_difference <= math.pi:
	            self.phiDiff.append(phi_difference)
		else:
		    self.phiDiff.append(2*math.pi - phi_difference)
	    
	    self.jetMETPhi.Fill(min(self.phiDiff))
	    if min(self.phiDiff) < 0.5: return False

	else:
	    for i in range(4):
		phi_difference = abs(jets[i].phi - event.MET_phi)
		if phi_difference <= math.pi:
		    self.phiDiff.append(phi_difference)
	  	else:
		    self.phiDiff.append(2*math.pi - phi_difference)
	    
	    self.jetMETPhi.Fill(min(self.phiDiff))
            if min(self.phiDiff) < 0.5: return False

	self.eventCounts[11] += 1
	
	###############
	self.num_bjets = 0
	for jet in self.ak4Jets:
	    if abs(jet.eta) < 2.4 and jet.pt > 20 and jet.btagCSVV2 > 0.8484:
		self.num_bjets += 1
	
	self.num_bJets.Fill(self.num_bjets)

	#b-jet veto
	if self.num_bjets != 0: return False

	self.eventCounts[12] += 1

	##############
	
	x = arange(len(self.eventCounts))

	self.eventCountGraph.SetNameTitle('evtCounts', 'Event Counts After Each Cut, M = ' + self.LQMass + ' #lambda = ' + str(self.LQCoupling))	

	for i in range(len(self.eventCounts)):
	    self.eventCountGraph.SetPoint(i, x[i], self.eventCounts[i])    
		
	self.leadingJetPt.Fill(jets[0].pt)	
     	 	
	self.MET.Fill(event.MET_pt)

	#Phi difference and eta difference plots for pair production of leptoquarks
	self.nLeptoquarks = 0
	for i in range(len(genParticles)):
	    if (genParticles[i].pdgId == 1104 or genParticles[i].pdgId == -1104) and genParticles[i].status == 22:
		self.nLeptoquarks += 1

	self.genJetsFromU = []
	self.numLQ.Fill(self.nLeptoquarks)	
	
	if self.nLeptoquarks == 2: #pair production
	    for jet in genJets:
		for particle in genParticles:
		    self.deltaR_prtJet.Fill(self.deltaR(jet,particle))
		    if particle.genPartIdxMother == -1: continue
		    if self.deltaR(jet, particle) < 0.3 and (particle.pdgId == 2 or particle.pdgId == -2) and (abs(genParticles[particle.genPartIdxMother].pdgId) == 1104):
			self.genJetsFromU.append(jet)
	
	self.num_uJets.Fill(len(self.genJetsFromU))	

	if len(self.genJetsFromU) == 2: #Filling the histograms for pair production modes
	    self.phiDiff_genJets = abs(self.genJetsFromU[1].phi - self.genJetsFromU[0].phi)
	    if self.phiDiff_genJets <= math.pi:
	        self.phiDiffGenJets.Fill(self.phiDiff_genJets)
	    else:
		self.phiDiffGenJets.Fill(2*math.pi - self.phiDiff_genJets)

	    self.etaDiff_genJets = self.genJetsFromU[1].eta - self.genJetsFromU[0].eta
	    self.etaDiffGenJets.Fill(self.etaDiff_genJets)
		
	return True

#preselection='Jet_pt[0] > 100'

higgsfile = ['root://cmsxrootd.fnal.gov///store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/866B463C-D124-E911-B9F3-0CC47A1E0748.root']

Higgs2017Files = ['/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/866B463C-D124-E911-B9F3-0CC47A1E0748.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/AC59921F-CF24-E911-9390-008CFAF7174A.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/AA678DF5-9125-E911-B693-5065F3818271.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/9AD9EDBF-AB24-E911-87F7-AC1F6BAC815A.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/AE21A571-0425-E911-A9C0-0025905D1CB4.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/DEEA87BD-AA24-E911-940C-1866DA890700.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/30000/20C4D3A3-F928-E911-9B0D-AC1F6B0DE2A2.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/30000/D2F3FEAA-F928-E911-8F98-0242AC1C0502.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/30000/C82464B5-9028-E911-B6D9-001E6750489D.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/30000/9E9C6F17-CB28-E911-A76D-008CFA197C1C.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/2671FB83-AC24-E911-BB24-48D539F38882.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/28C15088-3225-E911-A8A4-001E67E6F8B9.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/705C9948-9125-E911-8058-246E96D10CBC.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/7AFEFCCE-AB24-E911-AB02-C0BFC0E56846.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/7ABE5247-1F1E-E911-883E-20040FE9DE50.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/00EF24C5-C624-E911-A8EA-0242AC1C0501.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/0603DE57-B624-E911-8420-AC1F6B5676BA.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/086D358B-D91E-E911-87B9-0CC47AA989C6.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/1011C8A1-AB24-E911-92C7-0CC47A5FC61D.root', '/store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/280000/402D5A55-AB24-E911-BE79-002590E2DA08.root']

for i in range(len(Higgs2017Files)):
    Higgs2017Files[i] = 'root://cmsxrootd.fnal.gov//' + Higgs2017Files[i]

#files=glob.glob("root://cmsxrootd.fnal.gov///store/mc/RunIIFall17NanoAOD/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/*")
#files=["root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAOD/GluGlu_HToInvisible_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/70FE44FE-C912-E811-9525-0CC47A7C3424.root", "root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAOD/GluGlu_HToInvisible_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/E2817A05-CA12-E811-9FAA-0025905B8612.root"]
trial_file=["/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1TeV_0_1/SLQ_NanoAOD_new/190425_205837/0000/SLQ_1TeV_0_1_RunIIFall17NanoAOD-00027_trial_1.root"]

#1TeV_0_1_Files=glob.glob("/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1TeV_0_1/SLQ_NanoAOD_new/190425_205837/0000/SLQ_1TeV_0_1_RunIIFall17NanoAOD-00027_trial_*")

files=glob.glob("/eos/uscms/store/user/aakpinar/SLQ_MCProduction/SLQ_1_4TeV_1/SLQ_1_4TeV_1_NanoAOD_new/190523_034946/0000/SLQ_1_4TeV_1_RunIIFall17NanoAOD-00027_*")

p=PostProcessor(".",files,branchsel=None,modules=[LQAnalysis()],noOut=True,histFileName="LQ_1_4TeV_1_histOut_all.root",histDirName="plots")
p.run()
		    

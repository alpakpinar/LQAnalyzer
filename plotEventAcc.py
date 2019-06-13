#####################
#Script for plotting total event acceptance graph, data taken from file EventAcceptances.txt
#####################

import ROOT
import os
import numpy as np

f = open('EventAcceptances.txt', 'r')

finalDir = 'savedPlots/eventAcceptancePlots'

lines = f.readlines()
labels = []
acceptances = []

for i, line in enumerate(lines):
    if i > 2:

	paramList = lines[i][:-1].split()
	#print(paramList)
	labels.append(paramList[0])
	acceptances.append(paramList[-1])

#print(labels)
#print(acceptances)

acc = {}
for i, label in enumerate(labels):
    acc[label] = acceptances[i]

#Selecting samples with coupling 1
masses = []
acc_coupling1 = [] #Accetances for samples with coupling 1

for label in labels:
    if '_1' in label and '_1_' not in label:
	if '_' in label[:3]:
	    masses.append(float(label[:3].split('_')[0] + '.' + label[:3].split('_')[1])) 
	    acc_coupling1.append(float(acc[label]))
	else:
	    masses.append(float(label[0]))
	    acc_coupling1.append(float(acc[label]))

#print(masses)
#print(acc_coupling1)

canv = ROOT.TCanvas('canv', 'canv')
canv.SetGrid()

n = len(masses)
graph = ROOT.TGraph(n)

for i in range(n):
    graph.SetPoint(i, masses[i], acc_coupling1[i])

graph.SetMarkerStyle(20)
graph.GetXaxis().SetTitle('LQ Mass (TeV)')
graph.GetYaxis().SetTitle('% Events Passing')
graph.SetTitle('Event Acceptances, #lambda = 1.0')

graph.Draw('AP')
canv.Print(os.path.join(finalDir, 'EventAcc_Coupling1.png')) 

########################
#Selecting samples with mass 1.4 TeV
couplings = []
acc_mass14 = [] #Acceptances for samples with mass 1.4 TeV

for label in labels:
    if '1_4TeV' in label:
	if '_' in label[-3:] and 'V' not in label[-3:]:
	    couplings.append(float(label[-3:].split('_')[0] + '.' + label[-3:].split('_')[1]))
	    acc_mass14.append(float(acc[label]))
	else:
	    couplings.append(float(label[-1]))
	    acc_mass14.append(float(acc[label]))

canv2 = ROOT.TCanvas('canv2', 'canv2')
canv2.SetGrid()

m = len(couplings)
graph2 = ROOT.TGraph(m)

for i in range(m):
    graph2.SetPoint(i, couplings[i], acc_mass14[i])

graph2.SetMarkerStyle(20)
graph2.GetXaxis().SetTitle('LQ Coupling, #lambda')
graph2.GetXaxis().SetNdivisions(212)
graph2.GetYaxis().SetTitle('% Events Passing')
graph2.SetTitle('Event Acceptances, M_{LQ} = 1.4 TeV')

graph2.Draw('AP')
canv2.Print(os.path.join(finalDir, 'EventAcc_Mass1_4.png'))












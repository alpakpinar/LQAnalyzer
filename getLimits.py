########################
#Script for getting the exclusion limits and plotting the results
########################

import ROOT
import os
import argparse
import subprocess

import brazilPlot_coup, brazilPlot_mass

def lineReplace(file_path, subst, lineIndex=8):
    with open(file_path, 'r') as f:
	lines = f.readlines()

    params = ['0_5TeV_0_5', '0_5TeV_1', '1TeV_1', '2TeV_1', '2TeV_1_5', '1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1_5', '1_4TeV_1']

    for param in params:
	if param in lines[lineIndex] and param != subst:

	    lines[lineIndex] = lines[lineIndex].split(param)[0] + subst + lines[lineIndex].split(param)[1] #Changing the relevant line

    with open(file_path, 'w') as f:
	f.writelines(lines)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--const_mass', help = 'Calculate the limits for a constant mass of 1.4 TeV', action ='store_true')
parser.add_argument('-c', '--const_coupling', help = 'Calculate the limits for a constant coupling of 1', action = 'store_true')
parser.add_argument('--data2016', help = 'Run combine over 2016 data only', action = 'store_true')
args = parser.parse_args()

def getLimits(LQParams, data2016=False):

    file_path = 'inputs/convert_to_ws.py'

    #Modifying convert_to_ws.py file
    lineReplace(file_path, LQParams)

    os.chdir('inputs')

    #Running convert_to_ws.py file
    print('Running convert_to_ws.py for ' + LQParams)

    command = 'python convert_to_ws.py'
    subprocess.call(command.split())

    os.chdir('../')

    ################
    #Running combine on the modified LQ file

    if data2016:
	
	print('##################')
	print('Running combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=1.0 --freezeParameter lumiscale for ' + LQParams)
	print('##################')

	command = 'combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=1.0 --freezeParameter lumiscale'
	p = subprocess.Popen(command.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
	out = p.communicate()[0]

	output = out.split('\n')

	for i in range(-10, -2):
	    print(output[i])

	return output[-10:-2]

    else:

	print('##################')
	print('Running combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=3.8 --freezeParameter lumiscale for ' + LQParams)
	print('##################')

	command = 'combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=3.8 --freezeParameter lumiscale'
	p = subprocess.Popen(command.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
	out = p.communicate()[0]

	output = out.split('\n')

	for i in range(-10, -2):
	    print(output[i])

	return output[-10:-2]


def drawLimits(params, constMass, constCoupling, data2016=False):
    
    upperbounds95 = []
    upperbounds68 = []
    lowerbounds68 = []
    lowerbounds95 = []
    median_exclusion = []
    mass_points = [500, 1000, 1400, 2000]
    coupling_points = [0.5, 0.7, 1, 1.5]

    for param in params:
	output = getLimits(param, data2016)

	upperbounds95.append(float(output[-2].split()[-1]))
	upperbounds68.append(float(output[-3].split()[-1]))
	median_exclusion.append(float(output[-4].split()[-1]))
	lowerbounds68.append(float(output[-5].split()[-1]))
	lowerbounds95.append(float(output[-6].split()[-1]))

	print(upperbounds95)
	print(upperbounds68)
	print(median_exclusion)
	print(lowerbounds68)
	print(lowerbounds95)

    if constMass:
	brazilPlot_coup.plotLimits(coupling_points, upperbounds95, upperbounds68, median_exclusion, lowerbounds68, lowerbounds95) #Change the function!

    elif constCoupling:
	brazilPlot_mass.plotLimits(mass_points, upperbounds95, upperbounds68, median_exclusion, lowerbounds68, lowerbounds95) #Change the function!


###################

if args.const_mass:
    if args.data2016:
	print('Running combine over 2016 data only!')
	print('Working on samples with M = 1.4 TeV')
	params = ['1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5']
	drawLimits(params, constMass=True, constCoupling=False, data2016=True)

    else:
	print('Working on samples with M = 1.4 TeV')
	params = ['1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1', '1_4TeV_1_5']
	drawLimits(params, constMass=True, constCoupling=False)


elif args.const_coupling: 
    if args.data2016:
	print('Running combine over 2016 data only!')
	print('Working on samples with coupling 1')
	params = ['0_5TeV_1', '1TeV_1', '1_4TeV_1', '2TeV_1']
	drawLimits(params, constMass=False, constCoupling=True, data2016=True)

    else:
	print('Working on samples with coupling 1')
	params = ['0_5TeV_1', '1TeV_1', '1_4TeV_1', '2TeV_1']
	drawLimits(params, constMass=False, constCoupling=True) 










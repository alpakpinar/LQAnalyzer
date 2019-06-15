#####################
#Script for getting the exclusion limits for a single sample
#####################

import ROOT
import os
import argparse
import subprocess

def lineReplace(file_path, subst, lineIndex=8):
    with open(file_path, 'r') as f:
	lines = f.readlines()

    params = ['0_5TeV_0_5', '0_5TeV_1', '1TeV_1', '2TeV_1_5', '2TeV_1', '1_4TeV_0_5', '1_4TeV_0_7', '1_4TeV_1_5', '1_4TeV_1', '2_25TeV_1', '2_5TeV_1_2', '1_75TeV_0_8', '1_5TeV_0_6', '1_25TeV_0_4']

    for param in params:
	if param in lines[lineIndex]:

	    lines[lineIndex] = lines[lineIndex].split(param)[0] + subst + lines[lineIndex].split(param)[1] #Changing the relevant line
	    break

    with open(file_path, 'w') as f:
	f.writelines(lines)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mass', help = 'Mass of the LQ sample to be analyzed (Enter with an underscore)')
parser.add_argument('-c', '--coupling', help = 'Coupling of the LQ sample to be analyzed (Enter with an underscore)')
parser.add_argument('--data2016', help = 'Run combine over 2016 data only', action = 'store_true')
parser.add_argument('--genLevel', help = 'Running over gen-level samples', action = 'store_true')

args = parser.parse_args()

LQParams = args.mass + 'TeV_' + args.coupling

os.chdir('inputs')

#Running convert_to_ws.py file

if args.genLevel:
    file_path = 'convert_to_ws_GEN.py'
    #Modifying convert_to_ws.py file
    lineReplace(file_path, LQParams)

    print('Running convert_to_ws_GEN.py')
    command = 'python convert_to_ws_GEN.py'
    
else:
    file_path = 'convert_to_ws.py'
    #Modifying convert_to_ws.py file
    lineReplace(file_path, LQParams)

    print('Running convert_to_ws.py')
    command = 'python convert_to_ws.py'

subprocess.call(command.split())

os.chdir('../')

################
#Running combine on the modified LQ file

if args.data2016:

    print('##################')
    print('Running combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=1.0 --freezeParameter lumiscale for ' + LQParams)
    print('##################')

    command = 'combine -M AsymptoticLimits monojet_card.txt -t -1 --setParameters lumiscale=1.0 --freezeParameter lumiscale'
    p = subprocess.Popen(command.split(), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
    out = p.communicate()[0]

    output = out.split('\n')

    for i in range(-10, -2):
	print(output[i])

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









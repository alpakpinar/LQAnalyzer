import ROOT
import os

fileDir = 'GENSIM_RootFiles'
os.chdir(fileDir)

print("In the directory %s" % fileDir)

W = 1500
H = 1500

canv = ROOT.TCanvas('canv', 'canv', W, H)
canv.Divide(4,4)

files={}

for filename in os.listdir(os.getcwd()):
    files[filename] = ROOT.TFile(filename)

os.chdir('../')

#Create a tmp file so that script stays in this dir
tmpFile=ROOT.TFile("newtmpfile.root","recreate")
tmpFile.cd()

for i, filename in enumerate(os.listdir(fileDir),1):
    canv.cd(i)
    inFile = os.path.join(fileDir, filename)
    print('Getting histogram from file %s...' % inFile)
    MET_hist = files[filename].Get("MET")
    MET_hist.Draw("hist")


canv.Print('gridPlot_big.png')





import ROOT
import os

#Defining the plot style
ROOT.gStyle.SetTitleY(0.99)
ROOT.gStyle.SetTitleW(0.85)
ROOT.gStyle.SetTitleH(0.08)

ROOT.gStyle.SetOptStat(0) #no stat box

#x-axis labels
ROOT.gStyle.SetLabelSize(0.05)
ROOT.gStyle.SetLabelOffset(1.15)

#y-axis labels
ROOT.gStyle.SetLabelSize(0.05, "Y")
ROOT.gStyle.SetLabelOffset(1.35, "Y")

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
    MET_hist.SetFillStyle(1001)
    MET_hist.SetFillColor(602)
    MET_hist.Draw("hist")


canv.Print('gridPlot_big_colored.png')





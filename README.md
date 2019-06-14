# LQAnalyzer

In this repo, the scripts for analyzing leptoquark gen-level and NanoAOD samples are located. The samples to be analyzed are in the directory /eos/uscms/store/user/aakpinar/SLQ\_MCProduction/shape\_study.

## Analyzing LQ NanoAOD Files

### Applying Monojet Cuts and Getting the Histograms

For analyzing NanoAOD files, LQ\_NANOAnalyzer.py should be used. This script takes the relevant LQ files, specified by -m (mass) and -c (coupling) arguments provided to the script, and performs monojet selection on these files, then draws the event yield graphs and relevant kinematic distributions like MET or leading jet pt.

LQ\_NANOAnalyzer.py takes multiple arguments:

-m and -c arguments provide the script with the mass and coupling values of the sample that is to be analyzed. If either of these values contain a decimal, it should be written with an underscore. For example, to analyze the LQ samples with mass of 1.4 TeV and coupling 1, enter:

```
python LQ_NANOAnalyzer.py -m 1_4 -c 1
```

If the program is to be run only on one trial file, -t or --trial option should be used.

If -w or --writeToTxt option is used, the program will write the total event acceptance results to EventAcceptances.txt. Using the data in EventAcceptances.txt, a plot can be drawn using the script plotEventAcc.py.

By default, the program draws histograms that are not bin-width divided, due to compatibility issues with the combine command, to be used later. However, if the program is to draw a MET histogram and divide the contents by the bin widths, -b or --binWidthDivide option should be used.

### Running Combine and Getting The Limits

To get the exclusion limits, combine command should be run on the modified output of LQ\_NANOAnalyzer.py. The modification of the output and running combine can be done at the same time by running one of two scripts: getLimits.py and getLimits\_single.py 

To get the exclusion limits for a single case, getLimits\_single.py should be used, providing the mass and the coupling with options -m and -c. 

If the combine command is to be run on multiple files and the exclusion plots are to be drawn, getLimits.py should be used for this purpose. If this program is called with an option -m or --const\_mass, it will calculate the limits and draw the histograms for 4 different samples with 1.4 TeV mass. If it is called with an option -c or --const\_coupling, it will do the same job for 4 different samples with a coupling of 1.

By default, both getLimits\_single.py and getLimits.py calculate the limits on the whole Run 2 data taken by CMS (2016-2018). If only 2016 data is to be used, --data2016 option should be specified. So, the following program will calculate the exclusion limits for a mass of 2 TeV and coupling 1, using only the data taken at 2016:

```
python getLimits_single.py -m 2 -c 1 --data2016
```
 
## Analyzing LQ Gen-Level Samples

For analyzing Gen-Level samples, LQ\_GENSIMAnalyzer.py should be used. Similar to LQ\_NANOAnalyzer.py, this script takes arguments -m and -c that specifies the mass and the coupling of the samples to be analyzed, and draws MET and numLQ histograms.
 
This program does not put any additional cuts on the samples. It operates on two kinds of samples: Samples with MET > 50 GeV cut, samples with no MET cut 

To operate on the former, --genCut option must be specified. If this option is not specified, program will run on samples with no MET cut.

To obtain the numLQ (number of leptoquarks) histogram in addition to MET histogram, --LQhist option must also be used. 

The program also has an option -s or --short, such that if specified, the program will run only on first 25 files in the relevant directory.

As an example, if the program is to run over LQ samples with mass 1 TeV and coupling 1.5, which have the MET > 50 GeV cut, and if the output is to contain numLQ histograms, enter:

```
python LQ_GENSIMAnalyzer.py -m 1 -c 1_5 --genCut --LQhist
``` 


 

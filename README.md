# LQAnalyzer

In this repo, the scripts for analyzing leptoquark gen-level and NanoAOD samples are located. The samples to be analyzed are in the directory /eos/uscms/store/user/aakpinar/SLQ\_MCProduction/shape\_study.

## Analyzing LQ NanoAOD Files

For analyzing NanoAOD files, LQ\_NANOAnalyzer.py should be used. This script takes the relevant LQ files, specified by -m (mass) and -c (coupling) arguments provided to the script, and performs monojet selection on these files, then draws the event yield graphs and relevant kinematic distributions like MET or leading jet pt.

LQ\_NANOAnalyzer.py takes multiple arguments:

-m and -c arguments provide the script with the mass and coupling values of the sample that is to be analyzed. If either of these values contain a decimal, it should be written with an underscore. For example, to analyze the LQ samples with mass of 1.4 TeV and coupling 1, enter:

```
python LQ\_NANOAnalyzer.py -m 1\_4 -c 1

```

If the program is to be run only on one trial file, -t or --trial option should be used.

If -w or --writeToTxt option is used, the program will write the total event acceptance results to EventAcceptances.txt.

By default, the program draws histograms that are not bin-width divided, due to compatibility issues with the combine command, to be used later. However, if the program is to draw a MET histogram and divide the contents by the bin widths, -b or --binWidthDivide option should be used.


 

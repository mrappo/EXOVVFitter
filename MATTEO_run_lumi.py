import os,commands
import sys
from optparse import OptionParser
import subprocess
from subprocess import Popen, PIPE, STDOUT


luminosity=[0.25,0.75,1.0,1.25,1.75,2.0,2.25];

lumi=0.0;
for lumi in luminosity:
    pd1 = subprocess.Popen(['python','MATTEO_run_all.py','--lumi',str(lumi)]);
    pd1.wait();



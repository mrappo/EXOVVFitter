import os,commands
import sys
from optparse import OptionParser
import subprocess
from subprocess import Popen, PIPE, STDOUT
import glob
import math
import array
import ROOT
import ntpath
import sys
from optparse import OptionParser
#import CMS_lumi, tdrstyle
from array import array
from datetime import datetime


from ROOT import TColor, gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite, gPad
parser = OptionParser()

parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="em")
parser.add_option('--ntuple', action="store",type="string",dest="ntuple",default="WWTree_22sep_jecV7_lowmass")
parser.add_option('--category', action="store",type="string",dest="category",default="HP")
parser.add_option('--type', action="store",type="string",dest="type",default="")
parser.add_option('--jetalgo', action="store",type="string",dest="jetalgo",default="jet_mass_pr")
parser.add_option('--interpolate', action="store_true",dest="interpolate",default=False)
parser.add_option('--batchMode', action="store_true",dest="batchMode",default=True)
parser.add_option('--vbf', action="store_true",dest="VBF_process",default=True)
parser.add_option('--pseudodata', action="store_true",dest="pseudodata",default=False)
parser.add_option('--lumi', action="store",type="float",dest="lumi",default=2300.0)
parser.add_option('--CrossCuts', action="store_true",dest="CrosCuts",default=True)
parser.add_option('--UnBlind', action="store_true",dest="UnBlind",default=True)
parser.add_option('--LogFile', action="store_true",dest="LogFile",default=False)
(options, args) = parser.parse_args()

currentDir = os.getcwd();
devnull = open(os.devnull, 'w');
samples=["BulkGraviton","Higgs"];
lumi_str=str("%.0f"%options.lumi);
# DEta cut
#DEta_values=[0.0,1.0,1.5,2.0,2.5];

# Mjj Cut
#DMjj_values=[0.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0,450.0,500.0];

## DeltaEta Cut
#DEta_values=[0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.0];
#DEta_values=[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0];
DEta_values=[2.0];
# Mjj Cut
#DMjj_values=[0.0,25.0,50.0,75.0,100.0,125.0,150.0,175.0,200.0,225.0,250.0,275.0,300.0,325.0];
#Mjj_values=[0.0,20.0,40.0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,220.0,240.0,260.0,280.0,300.0,320.0,340.0];
Mjj_values=[200.0];

#DEta_values=[0.0,0.2,0.4];
#Mjj_values=[0.0,20.0,40.0];


   
########################################################
#### Function Definition
########################################################

def set_palette(name,ncontours):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        '''
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]
        '''
        stops = [0.00, 0.34, 0.61, 0.84, 0.90]
        red   = [0.35, 0.00, 0.87, 1.00, 0.61]
        green = [0.10, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]
    
    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)
    
def GetDataFromFile(filename):
    
    f = open(filename,'r');
    lines=f.readlines();
    
    i=j=0;
    for i in lines:
        j=j+1;
    
    out=[int(j),lines]
    return out;  
    


def GetIndex(mjj_in,deta_in):
    print mjj_in
    print deta_in
    m=e=0;
    epsilon = 0.5

    i=j=0;
    
    for i in Mjj_values:#range(len(Mjj_values)):
        '''
        print "in: %f    vector: %f"%(mjj_in,Mjj_values[i])
        if (TMath.Abs(mjj_in - Mjj_values[i]))>epsilon:
        
           print "ciao"
        else:
           print "trovato"
           m=i;
           print m
        '''
        if mjj_in==i:
           m=j;
        j=j+1;
           
        
    i=j=0;
    
    for i in DEta_values:
        
        if deta_in==i:
           e=j;
        j=j+1;   
     
    index=[m,e];
    print index
    return index;

def print_lined_string_File(in_string_vector,out_file):
    
    offset=3;

    s_number=0;
    for t in in_string_vector:
        s_number=s_number+1;
    
    lenght=0;
    for i in in_string_vector:
        tmp_lenght=len(i);
        if tmp_lenght>lenght:
           lenght=tmp_lenght;
    total_lenght=int(lenght*1.40)
    if total_lenght > 120:
       total_lenght=120;


        
    line_empty="\n";
    line_zero=""
    for k in range(offset):
        line_zero=line_zero+" ";
    

    out_file.write("\n"+line_empty);
    out_file.write("\n"+line_empty);
    print line_empty
    print line_empty
    z=0;
    for i in in_string_vector:
        if z:
          
           print_string=line_zero+i;
           out_file.write("\n"+print_string);
           print print_string
        else:
           tmp_len=len(i);
           pos=int((total_lenght-tmp_len)/2);
           tmp_final_space="";
           for k in range(pos):
               tmp_final_space=tmp_final_space+"-";
           
           if not i==" ":
               print_string=tmp_final_space+" "+i+" "+tmp_final_space;
           else:
               print_string=tmp_final_space+"---"+tmp_final_space;
           out_file.write("\n"+line_empty);
           out_file.write("\n"+line_empty);
           out_file.write("\n"+print_string);
           out_file.write("\n"+line_empty);
           
           print line_empty
           print line_empty
           print print_string
           print line_empty
           
           z=1;
    
        
    out_file.write("\n"+line_empty);
    print line_empty
    
    final_line="";
    for k in range(total_lenght+1):
        final_line=final_line+"-";
    
    out_file.write("\n"+final_line);
    out_file.write("\n"+line_empty);
    
    print final_line
    print line_empty









def print_boxed_string_File(in_string_vector,out_file_name):
    
    offset_1=3;
    offset_2=4;
    s_number=0;
    t=0;
    for t in in_string_vector:
        s_number=s_number+1;
    
    lenght=0;
    i=0;
    for i in in_string_vector:
        tmp_lenght=len(i);
        if tmp_lenght>lenght:
           lenght=tmp_lenght;
    total_lenght=int(lenght*1.40)
    if total_lenght > 120:
       total_lenght=120;
    line_ext="";
    line_in="";
    zero_space="";
    i=0;
    for i in range(offset_1):
        line_ext=line_ext+" ";
        line_in=line_in+" ";
    i=0;
    for i in range(offset_2):
        zero_space=zero_space+" ";
    line_ext=line_ext+" ";
    
    i=0;
    for i in range(total_lenght):
        line_ext=line_ext+"-";
        
    line_empty=line_in+"|";
    for i in range(total_lenght):
        line_empty=line_empty+" ";
    line_empty=line_empty+"|";
    
    out_file=open(out_file_name,'a');
    out_file.write("\n");
    out_file.write("\n");
    out_file.write("\n");
    out_file.write("\n"+line_ext);
    out_file.write("\n"+line_empty);
    
    print "\n\n"
    print line_ext
    print line_empty
    
    z=0;
    for i in in_string_vector:
        if z:
           tmp_len=len(i);
           tmp_final_space=""
           for k in range(total_lenght-offset_2-tmp_len):
               tmp_final_space=tmp_final_space+" ";
           print_string=line_in+"|"+zero_space+i+tmp_final_space+"|"
           out_file.write("\n"+print_string);
           print print_string
         
        else:
           tmp_len=len(i);
           tmp_final_space=""
           add=int((total_lenght-tmp_len)/2)
           for k in range(add):
               tmp_final_space=tmp_final_space+" ";
           add_line="";
           if (2*add+tmp_len)<total_lenght:
              add_line=" ";
         
           print_string=line_in+"|"+tmp_final_space+i+tmp_final_space+add_line+"|"
           #out_file.write("\n"+line_empty
           out_file.write("\n"+print_string);
           out_file.write("\n"+line_empty);
           
           print print_string
           print line_empty
           
           z=1;
    
    if (s_number-1): 
       out_file.write("\n"+line_empty);
       print line_empty
    out_file.write("\n"+line_ext);
    out_file.write("\n");
    out_file.write("\n");
    out_file.close();
    print line_ext
    print "\n\n"





   
########################################################
#### Main Code
########################################################
if __name__ == '__main__':
    

    ## Make Directory for DataCards
    Ntuple_dir="Ntuple_%s"%(options.ntuple);
   
    if options.pseudodata:
       Data_dir=Ntuple_dir+"/pseudoData";
          
    else:
       Data_dir=Ntuple_dir+"/trueData";
     
    
    # Make VBF process
    if options.VBF_process:
       
       
       # Make VBF Directory and CutsFile
       Lumi_dir_VBF=Data_dir+"/Lumi_%s_VBF"%lumi_str;
                
       Channel_dir=Lumi_dir_VBF+"/%s_Channel"%options.channel;
       
       
       if options.UnBlind:
          blind_dir=Channel_dir+"/UnBlind";
       
       else:
          blind_dir=Channel_dir+"/Blind";
        
      
       
      
    
       # Count number of DeltaEtajj Cuts
       n_eta=0;
       i=0;
       for i in DEta_values:
           n_eta=n_eta+1;
           print "Deta: %f \t\t n_eta: %.0f"%(i,n_eta)
       
       n_eta=int(n_eta);
       
       
         
    
       # Count number of Mjj Cuts
       n_mjj=0;
       i=0;
       for i in Mjj_values:
           n_mjj=n_mjj+1;
           print "DMjj: %f \t\t n_mjj: %.0f"%(i,n_mjj)
        
       n_mjj=int(n_mjj);
       
       
       
       
       
       
       
       
       # Store all cuts in a Vector: index 0 -> DEltaEta Cut
       #                             index 1 -> Mjj Cut
       if options.CrosCuts:
          print "\nCROSS CUTS\n"
          i=j=0;
          range_value=int((n_mjj*n_eta));
          print range_value
          VBF_cut_values=[0.0 for i in range(range_value)];
          i=j=k=0;
          tmp_signal_values=[0.0 for i in range(range_value)];
          i=j=k=0;
          signal_values=[[[0.0 for k in range(7)] for j in range(range_value) ] for i in range(5)];
          i=j=0;
          for i in range(n_mjj):
                 j=0;
                 for j in range(n_eta):
                     tmp=(i*(n_eta)+j);
                     VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.0f"%Mjj_values[i])];

           
           
      

       
       
       

       

       # Check the CutsVector
       i=0;
       print "\n\nVector of Cut Values:\n"
       print "Total CutsNumber: %.0f"%range_value
       print "\n"
       for i in range(range_value):
           i=int(i);
           tmp=VBF_cut_values[i];
           DEta_tmp=tmp[0];
           Mjj_tmp=tmp[1];
           DEta_local=float(DEta_tmp);
           Mjj_local=float(Mjj_tmp);
           print " %.0f)  DEta: %1.3f \t\t Mjj: %.1f\n"%((i+1),DEta_local,Mjj_local)
        

    
    
    
    
    
    outputFileName=open("Plots.txt",'w+');
    outputFileName.close(); 
    
    sample_counter=int(0.0);
    
    # Make Datacard and Plots
    for sample in samples:

        if sample.find('BulkGraviton') !=-1:
           masses=["600","800","1000"];
       
       
        if sample.find('Higgs') !=-1:
           masses=["650","1000"];
    
        for m in masses:
            i=0;
            counter=0;
            for i in range(range_value):
                
                
                 
                   i=int(i);
                   tmp=VBF_cut_values[i];
                   DEta_local=float("%1.3f"%tmp[0]);
                   Mjj_local=float("%.1f"%tmp[1]);
                   TTB_SF=float(tmp[0]);
                   Sigma_TTB_SF=float(tmp[1]);
                   
                   tmp_string=["Sample: %s%s"%(sample,m),
                               " ",
                               "DEta: %f"%(DEta_local),
                               " ",
                               "Mjj: %f"%(Mjj_local)];
                               
                   print_boxed_string_File(tmp_string,"Plots.txt");
                   
                   
                   Cut_dir=blind_dir+"/DEta%1.3f_Mjj_%.0f"%(DEta_local,Mjj_local);    
  
                   datacardFileName=Cut_dir+"/cards_em_HP_VBF/%s/wwlvj_"%(sample)+sample+m+"_em_HP_lumi_2300_unbin.txt";
                   datacardFile=open(datacardFileName,'r');
                   newdatacardFileName=Cut_dir+"/cards_em_HP_VBF/%s/wwlvj_"%(sample)+sample+m+"_MATTEO.txt";
                   newdatacardFile=open(newdatacardFileName,'w+');
                   
                   
                   for line in datacardFile.readlines():
                        
                        #print line
                        if sample=="BulkGraviton":
                           if m=="600":
                              if line.find('CMS_xww_XS_BulkGraviton_13TeV lnN 1.170 - - - -') !=-1:
                                 new_line="CMS_xww_XS_BulkGraviton_13TeV lnN 1.080 - - - -";
                                 newdatacardFile.write(new_line+"\n");
                                 
                              else:
                                 newdatacardFile.write(line);
                           
                           if m=="800":
                              if line.find('CMS_xww_XS_BulkGraviton_13TeV lnN 1.170 - - - -') !=-1:
                                 old_line="CMS_xww_XS_BulkGraviton_13TeV lnN 1.170 - - - -";
                                 new_line="CMS_xww_XS_BulkGraviton_13TeV lnN 1.110 - - - -";
                                 newdatacardFile.write(new_line+"\n");
                                 
                              else:
                                 newdatacardFile.write(line);
                           
                           if m=="1000":
                              if line.find('CMS_xww_XS_BulkGraviton_13TeV lnN 1.170 - - - -') !=-1:
                                 old_line="CMS_xww_XS_BulkGraviton_13TeV lnN 1.170 - - - -";
                                 new_line="CMS_xww_XS_BulkGraviton_13TeV lnN 1.130 - - - -";
                                 newdatacardFile.write(new_line+"\n");
                                 
                              else:
                                 newdatacardFile.write(line);
                              
                        else:
                           if m=="650":
                              if line.find('CMS_xww_XS_sig_13TeV lnN 1.170 - - - -') !=-1:
                                 old_line="CMS_xww_XS_sig_13TeV lnN 1.170 - - - -";
                                 new_line="CMS_xww_XS_sig_13TeV lnN 1.021 - - - -";
                                 newdatacardFile.write(new_line+"\n");
                                 
                              else:
                                 newdatacardFile.write(line);
                           
                           if m=="1000":
                              if line.find('CMS_xww_XS_sig_13TeV lnN 1.170 - - - -') !=-1:
                                 old_line="CMS_xww_XS_sig_13TeV lnN 1.170 - - - -";
                                 new_line="CMS_xww_XS_sig_13TeV lnN 1.025 - - - -";
                                 newdatacardFile.write(new_line+"\n");
                                 
                              else:
                                 newdatacardFile.write(line);
                   datacardFile.close();
                   newdatacardFile.close();

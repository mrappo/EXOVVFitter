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
DEta_values=[0.0];
# Mjj Cut
#DMjj_values=[0.0,25.0,50.0,75.0,100.0,125.0,150.0,175.0,200.0,225.0,250.0,275.0,300.0,325.0];
Mjj_values=[0.0,20.0,40.0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,220.0,240.0,260.0,280.0,300.0,320.0,340.0,360.0,380.0,400.0,420.0,440.0,460.0,480.0];
#Mjj_values=[0.0,20.0,40.0,60.0,80.0];


   
########################################################
#### Function Definition
########################################################


    
def GetDataFromFile(filename):
    
    f = open(filename,'r');
    lines=f.readlines();
    
    i=j=0;
    for i in lines:
        j=j+1;
    
    out=[int(j),lines]
    return out;  
    




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
          tmp_signal_values=[0.0 for i in range(range_value)];
          i=j=k=0;
          signal_values=[[[0.0 for k in range(5)] for j in range(range_value) ] for i in range(5)];
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
            #/Ntuple_WWTree_22sep_jecV7_lowmass/trueData/Lumi_2300_VBF/em_Channel/UnBlind/DEta0.200_Mjj_200/cards_em_HP_VBF/BulkGraviton/wwlvj_BulkGraviton800_em_HP_lumi_2300_unbin.txt


                   datacardFileName=Cut_dir+"/cards_em_HP_VBF/%s/wwlvj_"%(sample)+sample+m+"_em_HP_lumi_2300_unbin.txt";
                   datacardFile=open(datacardFileName,'r');
            
                   for line in datacardFile.readlines():
                        #print line
                        if line.find('rate ') !=-1:
                           #print line
                           signal=float(line.split(" ")[1]);
                           WJ=float(line.split(" ")[2]);
                           TTB=float(line.split(" ")[3]);
                           STop=float(line.split(" ")[4]);
                           VV=float(line.split(" ")[5]);
                           #print signal
                           #print WJ
                           #print TTB
                           #print STop
                           #print VV
                           signal_values[sample_counter][counter][0]=signal;
                           signal_values[sample_counter][counter][1]=WJ;
                           signal_values[sample_counter][counter][2]=TTB;
                           signal_values[sample_counter][counter][3]=STop;
                           signal_values[sample_counter][counter][4]=VV;
                           #tmp_data=[signal,WJ,TTB,STop,VV];
                           #print tmp_data[0]
                   #tmp_signal_values[counter]=tmp_data;
                   counter=counter+1;
            #signal_values[sample_counter]=tmp_signal_values;
            #print tmp_signal_values
            #print signal_values[sample_counter]
            #print sample_counter 
            sample_counter=sample_counter+1;
           
            
    i=j=0;
    for i in DEta_values:
        j=j+1;
    
    Total_bin_deta=j;
    
    i=j=0;
    for i in Mjj_values:
        j=j+1;
    
    Total_bin_mjj=j;
    
    print "N_eta: %.0f \t N_Mjj: %.0f"%(Total_bin_deta,Total_bin_mjj)
    
    blind_dir=blind_dir+"/RatePlotsMjj";
    if not os.path.isdir(blind_dir):
              pd3 = subprocess.Popen(['mkdir',blind_dir]);
              pd3.wait();
    
    i=j=sm=0;
    sample_counter=int(0.0);
    for sm in samples:
         
        if sm=="BulkGraviton":
           masses=[600.0,800.0,1000.0];
        else:
           masses=[650.0,1000.0];
        
        for m in masses:
            
            tmp_graph_signal=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_wj=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_ttb=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_stop=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_vv=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_efficiency_signal=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            tmp_graph_efficiency_bkg=ROOT.TH1D("graph_val","graph_val",Total_bin_mjj,Mjj_values[0],Mjj_values[Total_bin_mjj-1]);
            
            #signal_values[sample][Mjj][value]
            tmp_signal_zero=signal_values[sample_counter][0][0];
            tmp_wj_zero=signal_values[sample_counter][0][1];
            tmp_ttb_zero=signal_values[sample_counter][0][2];
            tmp_stop_zero=signal_values[sample_counter][0][3];
            tmp_vv_zero=signal_values[sample_counter][0][4];
            tmp_total_bkg_zero=tmp_wj_zero+tmp_ttb_zero+tmp_stop_zero+tmp_vv_zero;
   
            for i in range(range_value):
                

                
                tmp_signal=signal_values[sample_counter][i][0];
                tmp_wj=signal_values[sample_counter][i][1];
                tmp_ttb=signal_values[sample_counter][i][2];
                tmp_stop=signal_values[sample_counter][i][3];
                tmp_vv=signal_values[sample_counter][i][4];
                tmp_total_bkg=tmp_wj+tmp_ttb+tmp_stop+tmp_vv;
                
                tmp_efficiency_signal=tmp_signal/tmp_signal_zero;
                tmp_efficiency_bkg=tmp_total_bkg/tmp_total_bkg_zero;
                
                tmp_string=["Sample: %s%.0f"%(sm,m),
                               " ",
                               "Mjj: %f"%(Mjj_values[i]),
                               " ",
                               "Signal: %f"%tmp_signal,
                               " ",
                               "W+Jets: %f"%tmp_wj,
                               " ",
                               "TTBar: %f"%tmp_ttb,
                               " ",
                               "STop: %f"%tmp_stop,
                               " ",
                               "VV: %f"%tmp_vv,
                               " ",                                                         
                               "Signal efficiency: %f"%(tmp_efficiency_signal),
                               " ",
                               "Bkg Efficiency: %f"%(tmp_efficiency_bkg)];
                               
                print_boxed_string_File(tmp_string,"Plots.txt");
                
            
                tmp_graph_signal.SetBinContent(i+1,tmp_signal);
                tmp_graph_wj.SetBinContent(i+1,tmp_wj);
                tmp_graph_ttb.SetBinContent(i+1,tmp_ttb);
                tmp_graph_stop.SetBinContent(i+1,tmp_stop);
                tmp_graph_vv.SetBinContent(i+1,tmp_vv);
                tmp_graph_efficiency_signal.SetBinContent(i+1,tmp_efficiency_signal);
                tmp_graph_efficiency_bkg.SetBinContent(i+1,tmp_efficiency_bkg);
                
                tmp_graph_signal.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_wj.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_ttb.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_stop.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_vv.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_efficiency_signal.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                tmp_graph_efficiency_bkg.GetXaxis().SetBinLabel(i+1,str("%.0f"%(Mjj_values[i])));
                
            
            
            
            tmp_canvas11=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas11.SetLogy();
            tmp_canvas11.SetGrid();
            titleGraph="Signal %s%.0f"%(sm,m);
            tmp_graph_signal.SetTitle(titleGraph);
            tmp_graph_signal.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_signal.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_signal.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_signal.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_signal.SetFillColor(kAzure+2);
            tmp_graph_signal.SetBarWidth(0.8);
            tmp_graph_signal.SetBarOffset(0.1);
            gStyle.SetOptStat(0);
            #tmp_graph_signal.SetMinimum(-0.05);
            #tmp_graph_signal.SetMaximum(0.3);
            tmp_graph_signal.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_Signal";
            tmp_canvas11.SaveAs(canvasFileName+".pdf");
            tmp_canvas11.SaveAs(canvasFileName+".root");
            #raw_input('Press Enter to exit')
            
            
            
            
            tmp_canvas12=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas12.SetLogy();
            tmp_canvas12.SetGrid();
            titleGraph="W+Jets %s%.0f"%(sm,m);
            tmp_graph_wj.SetTitle(titleGraph);
            tmp_graph_wj.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_wj.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_wj.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_wj.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_wj.SetFillColor(kAzure+2);
            tmp_graph_wj.SetBarWidth(0.8);
            tmp_graph_wj.SetBarOffset(0.1);
            gStyle.SetOptStat(0);
            #tmp_graph_wj.SetMinimum(-0.05);
            #tmp_graph_wj.SetMaximum(0.3);
            tmp_graph_wj.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_WJets";
            tmp_canvas12.SaveAs(canvasFileName+".pdf");
            tmp_canvas12.SaveAs(canvasFileName+".root");
            
            tmp_canvas13=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas13.SetLogy();
            tmp_canvas13.SetGrid();
            titleGraph="TTBar %s%.0f"%(sm,m);
            tmp_graph_ttb.SetTitle(titleGraph);
            tmp_graph_ttb.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_ttb.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_ttb.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_ttb.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_ttb.SetFillColor(kAzure+2);
            tmp_graph_ttb.SetBarWidth(0.8);
            tmp_graph_ttb.SetBarOffset(0.1);
            gStyle.SetOptStat(0);
            #tmp_graph_ttb.SetMinimum(-0.05);
            #tmp_graph_ttb.SetMaximum(0.3);
            tmp_graph_ttb.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_TTB";
            tmp_canvas13.SaveAs(canvasFileName+".pdf");
            tmp_canvas13.SaveAs(canvasFileName+".root");
            
            tmp_canvas14=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas14.SetLogy();
            tmp_canvas14.SetGrid();
            titleGraph="STop %s%.0f"%(sm,m);
            tmp_graph_stop.SetTitle(titleGraph);
            tmp_graph_stop.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_stop.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_stop.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_stop.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_stop.SetFillColor(kAzure+2);
            tmp_graph_stop.SetBarWidth(0.8);
            tmp_graph_stop.SetBarOffset(0.1);
            gStyle.SetOptStat(0);
            #tmp_graph_stop.SetMinimum(-0.05);
            #tmp_graph_stop.SetMaximum(0.3);
            tmp_graph_stop.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_STop";
            tmp_canvas14.SaveAs(canvasFileName+".pdf");
            tmp_canvas14.SaveAs(canvasFileName+".root");
            
            tmp_canvas15=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas15.SetLogy();
            tmp_canvas15.SetGrid();
            titleGraph="VV %s%.0f"%(sm,m);
            tmp_graph_vv.SetTitle(titleGraph);
            tmp_graph_vv.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_vv.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_vv.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_vv.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_vv.SetFillColor(kAzure+2);
            tmp_graph_vv.SetBarWidth(0.8);
            tmp_graph_vv.SetBarOffset(0.1);
            gStyle.SetOptStat(0);
            #tmp_graph_vv.SetMinimum(-0.05);
            #tmp_graph_vv.SetMaximum(0.3);
            tmp_graph_vv.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_VV";
            tmp_canvas15.SaveAs(canvasFileName+".pdf");
            tmp_canvas15.SaveAs(canvasFileName+".root");
            
            tmp_canvas16=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas16.SetLogy();
            tmp_canvas16.SetGrid();
            titleGraph="Signal Efficiency %s%.0f"%(sm,m);
            tmp_graph_efficiency_signal.SetTitle(titleGraph);
            tmp_graph_efficiency_signal.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_efficiency_signal.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_efficiency_signal.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_efficiency_signal.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_efficiency_signal.SetFillColor(kAzure+2);
            tmp_graph_efficiency_signal.SetBarWidth(0.8);
            tmp_graph_efficiency_signal.SetBarOffset(0.1);
            #tmp_graph_efficiency_signal.SetMinimum(-0.05);
            #tmp_graph_efficiency_signal.SetMaximum(0.3);
            tmp_graph_efficiency_signal.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_EffSignal";
            tmp_canvas16.SaveAs(canvasFileName+".pdf");
            tmp_canvas16.SaveAs(canvasFileName+".root");
            
            tmp_canvas17=TCanvas ("Plot","Plot", 1000,600);
            #tmp_canvas17.SetLogy();
            tmp_canvas17.SetGrid();
            titleGraph="Bkg Efficiency %s%.0f"%(sm,m);
            tmp_graph_efficiency_bkg.SetTitle(titleGraph);
            tmp_graph_efficiency_bkg.GetXaxis().SetNdivisions(5,kFALSE);
            tmp_graph_efficiency_bkg.GetXaxis().SetTitle("M_{jj}");
            tmp_graph_efficiency_bkg.GetXaxis().CenterTitle(kTRUE);
            #tmp_graph_efficiency_bkg.GetXaxis().SetTitleOffset(1.5);
            tmp_graph_efficiency_bkg.SetFillColor(kAzure+2);
            tmp_graph_efficiency_bkg.SetBarWidth(0.8);
            tmp_graph_efficiency_bkg.SetBarOffset(0.1);
            #tmp_graph_efficiency_bkg.SetMinimum(-0.05);
            #tmp_graph_efficiency_bkg.SetMaximum(0.3);
            tmp_graph_efficiency_bkg.Draw("b");
            canvasFileName=blind_dir+"/"+sm+"%.0f"%(m)+"_Effbkg";
            tmp_canvas17.SaveAs(canvasFileName+".pdf");
            tmp_canvas17.SaveAs(canvasFileName+".root");
            
            #raw_input('Press Enter to exit')
            sample_counter=int(sample_counter+1);
                
            
            
            
            
            


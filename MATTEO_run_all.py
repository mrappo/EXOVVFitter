import os,commands
import sys
from optparse import OptionParser
import subprocess
from subprocess import Popen, PIPE, STDOUT

parser = OptionParser()

parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="em")
parser.add_option('--ntuple', action="store",type="string",dest="ntuple",default="WWTree_22sep_jecV7_lowmass")
parser.add_option('--category', action="store",type="string",dest="category",default="HP")
parser.add_option('--type', action="store",type="string",dest="type",default="")
parser.add_option('--jetalgo', action="store",type="string",dest="jetalgo",default="jet_mass_pr")
parser.add_option('--interpolate', action="store_true",dest="interpolate",default=False)
parser.add_option('--batchMode', action="store_true",dest="batchMode",default=False)
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
DEta_values=[0.0,1.0,1.5,2.0,2.5];

# Mjj Cut
DMjj_values=[0.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0,450.0,500.0];





   
########################################################
#### Function Definition
########################################################

def get_ScaleFactor(Deta,mjj,ControlP_Dir_2_gs,outputFileName_gs):
           
        DEta_local=float("%1.3f"%Deta);
        Mjj_local=float("%.1f"%mjj);
        
        if (DEta_local==0.0 and Mjj_local==0.0):
           nJetsCut_value=0.0;
        else:
           nJetsCut_value=1.0;
        
        ControlP_Dir_3=ControlP_Dir_2+"/Deta%1.3f_Mjj%.0f_NJ%.0f"%(DEta_local,Mjj_local,nJetsCut_value);
        
        #print ControlP_Dir_3
        tmp_in_FileName=ControlP_Dir_3+"/Summary_CP_for_datacard.txt";
        error_value=[0.0001,0.0001,DEta_local,Mjj_local];
        
        control2=0;
        
        control1=os.path.isfile(tmp_in_FileName);
        
        if control1:
           control2=os.path.getsize(tmp_in_FileName);
        
        else:
           control2=0;
        if control2:
           
           tmp_Cut_Value_Vector=GetDataFromFile(tmp_in_FileName);
           print tmp_Cut_Value_Vector
        
        
           if tmp_Cut_Value_Vector[0]<15:
              ScaleFactorVector=error_value;
        
           else:
              tmp_CutVector=tmp_Cut_Value_Vector[1];
        
              tmp_TTB_SF=tmp_CutVector[14];
              tmp_TTB_SF_Sigma=tmp_CutVector[15];
        
              if (((tmp_TTB_SF).find('nan') != -1) or  (tmp_TTB_SF < 0.0)):
                 ScaleFactorVector=error_value;
           
              elif (((tmp_TTB_SF_Sigma).find('nan') != -1) or (tmp_TTB_SF_Sigma < 0.0)):
                 ScaleFactorVector=error_value;
           
                     
              else:
                 ScaleFactorVector=[float(tmp_TTB_SF),float(tmp_TTB_SF_Sigma),DEta_local,Mjj_local];
           
              tmp_print_string=["READED TTB Value form File",
                                " ",
                                "file: %s"%ControlP_Dir_3,
                                " ",
                                "TTB ScaleFactor: %f"%ScaleFactorVector[0],
                                " ",
                                "Sigma TTB SF: %f"%ScaleFactorVector[1]];
           
              print_boxed_string_File(tmp_print_string,outputFileName_gs);
        else:
           ScaleFactorVector=error_value
         
        print ScaleFactorVector
        return ScaleFactorVector;
    
    
   

def readVBFCutsFile(in_VBFCutsFile):
    '''
    textName="VBF_CutListFile.txt";
    if options.pseudodata:
       
       if options.vbf:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/pseudoData/Lumi_%s_VBF/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
       else:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/pseudoData/Lumi_%s/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
    
    else:
       if options.vbf:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/trueData/Lumi_%s_VBF/"%(options.ntuple,str("%.0f"%options.lumi))+textName;
       else:
          in_VBFCutsFile="../../../CMSSW_5_3_13/src/EXOVVFitter/Ntuple_%s/trueData/Lumi_%s/"%(options.ntuple,str("%.0f"%options.lumi))+textName;    
    '''
    tmp_VBFCutsFile=open(in_VBFCutsFile, 'r');
    
    readedLines=tmp_VBFCutsFile.readlines();
    
    i=j=0;
    for i in readedLines:
        j=j+1;
    
    totalLineNumber=j;
    
    i=j=0;
    
    tmp_Cuts_Vector= [0 for i in range(totalLineNumber)];
    i=j=0;
    
    for i in range(totalLineNumber):
        tmp_Cuts_Vector[i]=[float((readedLines[i]).split(" ")[0]),float((readedLines[i]).split(" ")[1])];
        print tmp_Cuts_Vector[i]
    
    

    tmp_VBFCutsFile.close(); 
    return [totalLineNumber,tmp_Cuts_Vector];
    
    
    
    
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
    if total_lenght > 140:
       total_lenght=140;


        
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
    total_lenght=int(lenght*1.30)
    if total_lenght > 140:
       total_lenght=140;
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
    
    # Check TTBar ScaleFactor input Directory
    Ntuple_Dir_control="../../../CMSSW_7_1_5/src/CVS/VBFHWWlnuJ/output/Ntuple_%s"%(options.ntuple);
    if not os.path.isdir(Ntuple_Dir_control):
           print "\nError!!! Missing directory:%s \n EXIT"%Ntuple_Dircontrol
           sys.exit();


    Lumi_Dir_control=Ntuple_Dir_control+"/Lumi_%.0f"%(options.lumi);
    if not os.path.isdir(Lumi_Dir_control):
           print "\nError!!! Missing directory:%s \n EXIT"%Lumi_Dir_control
           sys.exit();
       

    ControlP_Dir_1=Lumi_Dir_control+"/ControlPlots";
    if not os.path.isdir(ControlP_Dir_1):
           print "\nError!!! Missing directory:%s \n EXIT"%ControlP_Dir_1
           sys.exit();
    
    
    
    ControlP_Dir_2=ControlP_Dir_1+"/%s_Channel"%options.channel;
    if not os.path.isdir(ControlP_Dir_2):
           print "\nError!!! Missing directory:%s \n EXIT"%ControlP_Dir_2
           sys.exit();
    
    ## Make Directory for DataCards
    Ntuple_dir="Ntuple_%s"%(options.ntuple);
    if not os.path.isdir(Ntuple_dir):
           pd1 = subprocess.Popen(['mkdir',Ntuple_dir]);
           pd1.wait();
           #os.system("mkdir "+Ntuple_dir);

    if options.pseudodata:
       Data_dir=Ntuple_dir+"/pseudoData";
       if not os.path.isdir(Data_dir):
              pd2 = subprocess.Popen(['mkdir',Data_dir]);
              pd2.wait()
       
          
    else:
       Data_dir=Ntuple_dir+"/trueData";
       if not os.path.isdir(Data_dir):
              pd3 = subprocess.Popen(['mkdir',Data_dir]);
              pd3.wait();
    

    
    # Make VBF process
    if options.VBF_process:
       
       
       # Make VBF Directory and CutsFile
       Lumi_dir_VBF=Data_dir+"/Lumi_%s_VBF"%lumi_str;
       if not os.path.isdir(Lumi_dir_VBF):
              pd4 = subprocess.Popen(['mkdir',Lumi_dir_VBF]);
              pd4.wait();
              
       Channel_dir=Lumi_dir_VBF+"/%s_Channel"%options.channel;
       if not os.path.isdir(Channel_dir):
              pd5 = subprocess.Popen(['mkdir',Channel_dir]);
              pd5.wait();
       
       
       if options.UnBlind:
          blind_dir=Channel_dir+"/UnBlind";
          if not os.path.isdir(blind_dir):
                 pd6a = subprocess.Popen(['mkdir',blind_dir]);
                 pd6a.wait();
       else:
          blind_dir=Channel_dir+"/Blind";
          if not os.path.isdir(blind_dir):
                 pd6b = subprocess.Popen(['mkdir',blind_dir]);
                 pd6b.wait();
              
       # Store the readed TTB SF in this File      
       outputFileName=blind_dir+"/Total_TTB_SF_Value.txt";
       outputFile=open(outputFileName,'w');
       outputFile.write("\nTTBar Scale Factor Total");
       outputFile.close();
       

       
       
      
    
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
       for i in DMjj_values:
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
                    
          i=j=0;
          for i in range(n_mjj):
                 j=0;
                 for j in range(n_eta):
                     tmp=(i*(n_eta)+j);
                     tmp_TTB_SF=get_ScaleFactor(float("%1.3f"%DEta_values[j]),float("%.0f"%DMjj_values[i]),ControlP_Dir_2,outputFileName);
                     VBF_cut_values[tmp]=tmp_TTB_SF;

           
           
      
              
       else:
          print "\nSINGLE CUTS\n"
          i=j=0;

          range_value=int(n_mjj+n_eta-1);
          VBF_cut_values=[0.0 for i in range(range_value)];          

          i=j=0;
          for i in range(n_eta):
              tmp_TTB_SF=get_ScaleFactor(float("%1.3f"%DEta_values[i]),0.0,ControlP_Dir_2,outputFileName);
              print "\n"
              print tmp_TTB_SF
              VBF_cut_values[i]=[float("%1.3f"%DEta_values[i]),0.0,float(tmp_TTB_SF[0]),float(tmp_TTB_SF[1])];
          
          for j in range(n_mjj-1):
              tmp_TTB_SF=get_ScaleFactor(0.0,float("%.0f"%DMjj_values[j+1]),ControlP_Dir_2,outputFileName);
              print "\n"
              print tmp_TTB_SF
              VBF_cut_values[n_eta+j]=[0.0,float("%.0f"%DMjj_values[j+1]),float(tmp_TTB_SF[0]),float(tmp_TTB_SF[1])];
       
       
       

       

       # Check the CutsVector
       i=0;
       print "\n\nVector of Cut Values:\n"
       print "Total CutsNumber: %.0f"%range_value
       print "\n"
       for i in range(range_value):
           i=int(i);
           tmp=VBF_cut_values[i];
           DEta_tmp=tmp[2];
           Mjj_tmp=tmp[3];
           DEta_local=float(DEta_tmp);
           Mjj_local=float(Mjj_tmp);
           print " %.0f)  DEta: %1.3f \t\t Mjj: %.1f\n"%((i+1),DEta_local,Mjj_local)
        

    
    
    
    
       
       # Store the done Cuts in a file (to be readed for make the ExclusionLimit)
       VBF_CutListFileName = blind_dir+"/VBF_CutListFile.txt";
       VBF_CutListFile = open(VBF_CutListFileName, 'w');
       
       i=0;
       for i in range(range_value):
           i=int(i);
           tmp=VBF_cut_values[i];
           DEta_local=float("%1.3f"%tmp[2]);
           Mjj_local=float("%.1f"%tmp[3]);
           VBF_CutListFile.write("%f %f\n"%(DEta_local,Mjj_local));
    
       VBF_CutListFile.close();
    
    
    
    
    # Normal Process (NO VBF)
    else:
       Lumi_dir=Data_dir+"/Lumi_%s"%lumi_str;
       if not os.path.isdir(Lumi_dir):
              pd7 = subprocess.Popen(['mkdir',Lumi_dir]);
              pd7.wait();
              
       Channel_dir=Lumi_dir+"/%s_Channel"%options.channel;
       if not os.path.isdir(Channel_dir):
              pd8 = subprocess.Popen(['mkdir',Channel_dir]);
              pd8.wait();
       
       
       if options.UnBlind:
          blind_dir=Channel_dir+"/UnBlind";
          if not os.path.isdir(blind_dir):
                 pd9a = subprocess.Popen(['mkdir',blind_dir]);
                 pd9a.wait();
       else:
          blind_dir=Channel_dir+"/Blind";
          if not os.path.isdir(blind_dir):
                 pd9b = subprocess.Popen(['mkdir',blind_dir]);
                 pd9b.wait();
    
    
    
    # Make Datacard and Plots
    for sample in samples:

        if sample.find('BulkGraviton') !=-1:
           masses=[600.0,800.0,1000.0]
       
       
        if sample.find('Higgs') !=-1:
           masses=[650.0,1000.0]
    
        for m in masses:
            
            #### VBF PROCESS
            if options.VBF_process:
               i=0;
               for i in range(range_value):
                   i=int(i);
                   tmp=VBF_cut_values[i];
                   DEta_local=float("%1.3f"%tmp[2]);
                   Mjj_local=float("%.1f"%tmp[3]);
                   TTB_SF=float(tmp[0]);
                   Sigma_TTB_SF=float(tmp[1]);
                   
                   tmp_string=["Sample: %s%.0f"%(sample,m),
                               " ",
                               "DEta: %f"%(DEta_local),
                               " ",
                               "Mjj: %f"%(Mjj_local),
                               " ",
                               "TTB_SF: %f"%(TTB_SF),
                               " ",
                               "Sigma: %f"%(Sigma_TTB_SF)];
                               
                   print_boxed_string_File(tmp_string,outputFileName);
                   
                   
                   Cut_dir=blind_dir+"/DEta%1.3f_Mjj_%.0f"%(DEta_local,Mjj_local);               
                   if not os.path.isdir(Cut_dir):
                          pd10 = subprocess.Popen(['mkdir',Cut_dir]);
                          pd10.wait();
                              
                   log_dir=Cut_dir+"/log_VBF";
                   if not os.path.isdir(log_dir):
                          pd11 = subprocess.Popen(['mkdir',log_dir]);
                          pd11.wait();
               
               
                   log_file=log_dir+"/log_VBF_%s_M%.0f_%s_%s.log"%(sample,m,options.channel,options.category);
                   
    
                   ## BatchMode
                   if (options.interpolate==False and options.batchMode==True):
              
                      job_dir=Cut_dir+"/Job_VBF";
                      if not os.path.isdir(job_dir):
                             pd12 = subprocess.Popen(['mkdir',job_dir]);
                             pd12.wait();
                             
                             
                      fn = job_dir+"/job_VBF_%s_%s_%s_%.0f"%(options.channel,options.category,sample,m)
                      outScript = open(fn+".sh","w");
 
                      outScript.write('#!/bin/bash');
                      outScript.write("\n"+'cd '+currentDir);
                      outScript.write("\n"+'eval `scram runtime -sh`');
                      outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
                      outScript.write("\n"+'echo ${PATH}');
                      outScript.write("\n"+'ls');
                      
                      if options.LogFile:
                         
                         if options.UnBlind:
                          
                            cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s --TTBSF %f --sigmaTTBSF %f --UnBlind > "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir,TTB_SF,Sigma_TTB_SF);
                         else:
                            cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s --TTBSF %f --sigmaTTBSF %f > "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir,TTB_SF,Sigma_TTB_SF);
                         
                         cmd= cmd_tmp+log_file;
                      
                      
                      
                      else:
                      
                         if options.UnBlind:
                            cmd = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s --TTBSF %f --sigmaTTBSF %f --UnBlind True"%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir,TTB_SF,Sigma_TTB_SF);
                         else:
                            cmd = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s --TTBSF %f --sigmaTTBSF %f"%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir,TTB_SF,Sigma_TTB_SF);
                         
                         
                      
                      outScript.write("\n"+cmd);
                      #outScript.write("\n"+'rm *.out');
                      outScript.close();
                      
                      
                      cmd_to_execute = currentDir+"/"+fn+".sh";
                      
                      pd13 = subprocess.Popen(['chmod','777',cmd_to_execute]);
                      pd13.wait();
                      
                     
                      pd14 = subprocess.Popen(['bsub','-q','cmscaf1nd','-cwd',currentDir,cmd_to_execute]);
                      pd14.wait();
                      
                      #os.system("chmod 777 "+currentDir+"/"+fn+".sh");
                      #os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");


                   
                   
                   ## BatchMode and Interpolate
                   elif (options.interpolate==True and not options.batchMode==True):
                      
                      if options.LogFile:
                         cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True --vbf True %s --DEta %f --DMjj %f --CDir %s > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,pd_option,DEta_local,Mjj_local,Cut_dir);
                         cmd=cmd_tmp+log_file;
                      else:
                         cmd = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True --vbf True %s --DEta %f --DMjj %f --CDir %s " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,pd_option,DEta_local,Mjj_local,Cut_dir);
                      
                      print cmd
                      os.system(cmd);

                   ## Normal executing way
                   else:   
                      
                      if options.LogFile:   
                      
                         output_logFileName=log_dir+"/StdOut_LogFile.log"
                         output_log_errorFileName=log_dir+"/StdErr_LogFile.log"
                         output_log = open(output_logFileName,'w');
                         output_log_error=open(output_log_errorFileName,'w');
                         
                         if options.UnBlind:
                            pd15a = subprocess.Popen(['python','MATTEO_g1_exo_doFit_class_new.py','-b','-c',options.channel,'--ntuple',options.ntuple,'--mass',str(m),'--category',options.category,'--sample',sample,'--jetalgo',options.jetalgo,'--luminosity',str(options.lumi),'--vbf','True','--DEta',str(DEta_local),'--DMjj',str(Mjj_local),'--CDir',Cut_dir,'--TTBSF',str(TTB_SF),'--sigmaTTBSF',str(Sigma_TTB_SF),'--UnBlind','True'],stdout=output_log,stderr=output_log_error);
                            pd15a.wait();
                         
                         else:
                            pd15a = subprocess.Popen(['python','MATTEO_g1_exo_doFit_class_new.py','-b','-c',options.channel,'--ntuple',options.ntuple,'--mass',str(m),'--category',options.category,'--sample',sample,'--jetalgo',options.jetalgo,'--luminosity',str(options.lumi),'--vbf','True','--DEta',str(DEta_local),'--DMjj',str(Mjj_local),'--CDir',Cut_dir,'--TTBSF',str(TTB_SF),'--sigmaTTBSF',str(Sigma_TTB_SF)],stdout=output_log,stderr=output_log_error);
                            pd15a.wait();
                         
                         output_log_error.close();
                         output_log.close();
                         
                      else:
                         
                         #cmd = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s --TTBSF %f --sigmaTTBSF %f "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir,TTB_SF,Sigma_TTB_SF);
                         #print cmd                     
                         
                         if options.UnBlind:
                            with open(os.devnull, "w") as fnull:
                                 pd15b = subprocess.Popen(['python','MATTEO_g1_exo_doFit_class_new.py','-b','-c',options.channel,'--ntuple',options.ntuple,'--mass',str(m),'--category',options.category,'--sample',sample,'--jetalgo',options.jetalgo,'--luminosity',str(options.lumi),'--vbf','True','--DEta',str(DEta_local),'--DMjj',str(Mjj_local),'--CDir',Cut_dir,'--TTBSF',str(TTB_SF),'--sigmaTTBSF',str(Sigma_TTB_SF),'--UnBlind','True'],stdout=fnull);
                                 pd15b.wait();
                         
                         
                         else:
                            with open(os.devnull, "w") as fnull:
                                 pd15b = subprocess.Popen(['python','MATTEO_g1_exo_doFit_class_new.py','-b','-c',options.channel,'--ntuple',options.ntuple,'--mass',str(m),'--category',options.category,'--sample',sample,'--jetalgo',options.jetalgo,'--luminosity',str(options.lumi),'--vbf','True','--DEta',str(DEta_local),'--DMjj',str(Mjj_local),'--CDir',Cut_dir,'--TTBSF',str(TTB_SF),'--sigmaTTBSF',str(Sigma_TTB_SF)],stdout=fnull);
                                 pd15b.wait();
                        
                        #os.system(cmd);
                
                
        
#python MATTEO_g1_exo_doFit_class_new.py -b -c em --ntuple WWTree_22sep_jecV7_lowmass --mass 800 --category HP --sample BulkGraviton --jetalgo jet_mass_pr --luminosity 2300 --vbf True --DEta 2.0 --DMjj 200 --CDir Ntuple_WWTree_22sep_jecV7_lowmass/trueData/Lumi_2300_VBF/em_Channel/DEta2.000_Mjj_200/ --TTBSF 0.75 --sigmaTTBSF 0.2       

        
        
        
            #### No VBF               
            else:
        
               
               Lumi_dir=Data_dir+"/Lumi_%s"%lumi_str
               if not os.path.isdir(Lumi_dir):
                      os.system("mkdir "+Lumi_dir);               
               
                              
               log_dir=Lumi_dir+"/log"
               if not os.path.isdir(log_dir):
                      os.system("mkdir "+log_dir);
               
               
               log_file=log_dir+"/log_%s_M%i_%s_%s_lumi%s.log"%(sample,m,options.channel,options.category,lumi_str)
               if (options.interpolate==False and options.batchMode==True):
              
                  job_dir=Data_dir+"/Job_lumi_%s"%(lumi_str)
                  if not os.path.isdir(job_dir):
                         os.system("mkdir "+job_dir);
            
                  fn = job_dir+"/job_%s_%s_%s_%d"%(options.channel,options.category,sample,m)
                  outScript = open(fn+".sh","w");
 
                  outScript.write('#!/bin/bash');
                  outScript.write("\n"+'cd '+currentDir);
                  outScript.write("\n"+'eval `scram runtime -sh`');
                  outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
                  outScript.write("\n"+'echo ${PATH}');
                  outScript.write("\n"+'ls');
#           cmd = "python g1_exo_doFit_class.py -b -c %s --mass %i --category %s --sample %s_lvjj --jetalgo %s --interpolate True > log/%s_M%i_%s_%s.log" %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,sample,m,options.channel,options.category)
                  cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f  > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value)
                  cmd= cmd_tmp+log_file;
                  outScript.write("\n"+cmd);
#      outScript.write("\n"+'rm *.out');
                  outScript.close();

                  os.system("chmod 777 "+currentDir+"/"+fn+".sh");
                  os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");

               elif (options.interpolate==True and not options.batchMode==True):
                    cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True %s > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option)
                    cmd=cmd_tmp+log_file
                    print cmd
                    os.system(cmd)

               else:   
                    cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f %s > "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option)
                    cmd=cmd_tmp+log_file;
                    print cmd
                    os.system(cmd)
               
               
            
               
     
               
               
              
               
               
               
               
               
               
               
               
               
               
               
               
                
               
               
               
               
                   
                
        
               
               
               
    
  
#python run-all.py --channel mu -s Wprime_WZ --jetalgo Mjsoftdrop --category HP
#python run-all.py -c mu -s BulkG_WW --category HPW

import os,commands
import sys
from optparse import OptionParser
import subprocess

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
parser.add_option('--CrossCuts', action="store_true",dest="CrosCuts",default=False)
#parser.add_option('--SignleCuts', action="store_true",dest="SingleCuts",default=False)
#parser.add_option('--MultipleCuts', action="store_true",dest="MultipleCuts",default=False)
(options, args) = parser.parse_args()

currentDir = os.getcwd();

samples=["BulkGraviton","Higgs"];
lumi_str=str("%.0f"%options.lumi);
########################################################
#### Main Code
########################################################
if __name__ == '__main__':
    
    # Make Global Directory
    Ntuple_dir="Ntuple_%s"%(options.ntuple);
    if not os.path.isdir(Ntuple_dir):
           os.system("mkdir "+Ntuple_dir);

    if options.pseudodata:
       Data_dir=Ntuple_dir+"/pseudoData";
       if not os.path.isdir(Data_dir):
              os.system("mkdir "+Data_dir);
       pd_option="--pseudodata True ";
          
    else:
       Data_dir=Ntuple_dir+"/trueData";
       if not os.path.isdir(Data_dir):
              os.system("mkdir "+Data_dir);
              pd_option=" ";



    # Make VBF process
    if options.VBF_process:
       
       ## DeltaEta Cut
       DEta_values=[0.0,1.0,1.5,2.0,2.2,2.4,2.5,2.7,3.0,3.5,4.0,4.5,5.0];
     
       # Mjj Cut
       DMjj_values=[0.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0];
       
       n_eta=0;
       n_mjj=0;
    
       # Count number of DeltaEtajj Cuts
       i=0;
       for i in DEta_values:
           n_eta=n_eta+1;
           print "Deta: %f \t\t n_eta: %.0f"%(i,n_eta)
    
    
       # Count number of Mjj Cuts
       i=0;
       for i in DMjj_values:
           n_mjj=n_mjj+1;
           print "DMjj: %f \t\t n_mjj: %.0f"%(i,n_mjj)
    
    
       n_mjj=int(n_mjj);
       n_eta=int(n_eta);
       
       
       
       # Store all cuts in a Vector: index 0 -> DEltaEta Cut
       #                             index 1 -> Mjj Cut
       if options.CrosCuts:
          print "\nCROSS CUTS\n"
          i=j=0;
          range_value=int((n_mjj*n_eta));
          print range_value
          VBF_cut_values=[0.0 for i in range(range_value)];
          
          i=j=0;
          if (n_eta<n_mjj):
             for i in range(n_eta):
                 for j in range(n_mjj):
                     i=int(i);
                     j=int(j);
                     tmp=int(i*(n_eta+1)+j);
                     #print VBF_cut_values[tmp]
                     #print tmp
                     VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[i]),float("%.1f"%DMjj_values[j])];
                     #print VBF_cut_values[tmp]
          
          elif (n_eta>n_mjj):
             for i in range(n_mjj):
                 for j in range(n_eta):
                     i=int(i);
                     j=int(j);
                     tmp=int(i*(n_mjj+1)+j);
                     #print VBF_cut_values[tmp]
                     #print "tmp: %.0f\ti: %.0f\tj: %.0f"%(tmp,i,j) 
                     VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.1f"%DMjj_values[i])];
                     #print VBF_cut_values[tmp]
          else:
             for i in range(n_mjj):
                 for j in range(n_eta):
                     i=int(i);
                     j=int(j);
                     tmp=int(i*(n_mjj)+j);
                     #print VBF_cut_values[tmp]
                     #print "tmp: %.0f\ti: %.0f\tj: %.0f"%(tmp,i,j) 
                     VBF_cut_values[tmp]=[float("%1.3f"%DEta_values[j]),float("%.1f"%DMjj_values[i])];
           
           
           
      
              
       else:
          print "\nSINGLE CUTS\n"
          i=j=0;

          range_value=int(n_mjj+n_eta-1);
          VBF_cut_values=[0.0 for i in range(range_value)];          

          i=j=0;
          for i in range(n_eta):
              VBF_cut_values[i]=[float("%1.3f"%DEta_values[i]),0.0];
          
          for j in range(n_mjj-1):
              VBF_cut_values[n_eta+j]=[0.0,float("%.1f"%DMjj_values[j+1])];
       
       
       

       

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
        

    
    
    

       # Make VBF Directory and CutsFile
       Lumi_dir_VBF=Data_dir+"/Lumi_%s_VBF"%lumi_str;
       if not os.path.isdir(Lumi_dir_VBF):
              os.system("mkdir "+Lumi_dir_VBF);
       
       VBF_CutListFileName = Lumi_dir_VBF+"/VBF_CutListFile.txt";
       VBF_CutListFile = open(VBF_CutListFileName, 'w');
       
       i=0;
       for i in range(range_value):
           i=int(i);
           tmp=VBF_cut_values[i];
           DEta_local=float("%1.3f"%tmp[0]);
           Mjj_local=float("%.1f"%tmp[1]);
           VBF_CutListFile.write("%f %f\n"%(DEta_local,Mjj_local));
    
       VBF_CutListFile.close();
    
    
    
    
    # Normal Process (NO VBF)
    else:
       Lumi_dir=Data_dir+"/Lumi_%s"%lumi_str;
       if not os.path.isdir(Lumi_dir):
              os.system("mkdir "+Lumi_dir);
    
    
    
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
                   DEta_local=float("%1.3f"%tmp[0]);
                   Mjj_local=float("%.1f"%tmp[1]);
       
                   Cut_dir=Lumi_dir_VBF+"/DEta%1.3f_Mjj_%.0f"%(DEta_local,Mjj_local);               
                   if not os.path.isdir(Cut_dir):
                          os.system("mkdir "+Cut_dir);
                   
                              
                   log_dir=Cut_dir+"/log_VBF";
                   if not os.path.isdir(log_dir):
                          os.system("mkdir "+log_dir);
               
               
                   log_file=log_dir+"/log_VBF_%s_M%.0f_%s_%s.log"%(sample,m,options.channel,options.category);
                   
    
                   ## BatchMode
                   if (options.interpolate==False and options.batchMode==True):
              
                      job_dir=Cut_dir+"/Job_VBF";
                      if not os.path.isdir(job_dir):
                             os.system("mkdir "+job_dir);
            
                      fn = job_dir+"/job_VBF_%s_%s_%s_%.0f"%(options.channel,options.category,sample,m)
                      outScript = open(fn+".sh","w");
 
                      outScript.write('#!/bin/bash');
                      outScript.write("\n"+'cd '+currentDir);
                      outScript.write("\n"+'eval `scram runtime -sh`');
                      outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
                      outScript.write("\n"+'echo ${PATH}');
                      outScript.write("\n"+'ls');

                      cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir);
                      cmd= cmd_tmp;#p+log_file;
                      outScript.write("\n"+cmd);
                      #outScript.write("\n"+'rm *.out');
                      outScript.close();

                      os.system("chmod 777 "+currentDir+"/"+fn+".sh");
                      os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");


                   ## BatchMode and Interpolate
                   elif (options.interpolate==True and not options.batchMode==True):
                        cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True --vbf True %s --DEta %f --DMjj %f --CDir %s " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,pd_option,DEta_local,Mjj_local,Cut_dir);
                        cmd=cmd_tmp;#+log_file;
                        print cmd
                        os.system(cmd);

                   ## Normal executing way
                   else:   
                        cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %f --category %s --sample %s --jetalgo %s --luminosity %f --vbf True --DEta %f --DMjj %f --CDir %s "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,options.lumi,DEta_local,Mjj_local,Cut_dir);
                        cmd=cmd_tmp;#+log_file;
                        print cmd
                        os.system(cmd);
                
                
        
        
        
        
        
        
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
                  cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f %s > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option)
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

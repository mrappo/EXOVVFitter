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
parser.add_option('--batchMode', action="store_true",dest="batchMode",default=False)
parser.add_option('--vbf', action="store_true",dest="VBF_process",default=True)
parser.add_option('--pseudodata', action="store_true",dest="pseudodata",default=False)
(options, args) = parser.parse_args()

currentDir = os.getcwd();


Ntuple_dir="Ntuple_%s"%(options.ntuple)

if not os.path.isdir(Ntuple_dir):
       os.system("mkdir "+Ntuple_dir);

if options.pseudodata:
   
   Data_dir=Ntuple_dir+"/pseudoData"
   if not os.path.isdir(Data_dir):
          os.system("mkdir "+Data_dir);
   pd_option="--pseudodata True ";
          
else:
   
   Data_dir=Ntuple_dir+"/trueData"
   if not os.path.isdir(Data_dir):
          os.system("mkdir "+Data_dir);
   pd_option=" ";

#Ntuple_Path_lxplus="/afs/cern.ch/user/l/lbrianza/work/public/%s/"%options.ntuple
samples=["BulkGraviton"]#,"Higgs"]
lumi_float_true=2300;
#lumi_float_true=2197.96#*1.023;
luminosities=[lumi_float_true]

#luminosities = [lumi_float_true,5000,10000]

#DEta_values=[1.0,1.5,2.0,2.5];
#DMjj_values=[100,150,200,250,300];

DEta_values=[1.0];
DMjj_values=[250];


n_eta=0;
n_mjj=0;

i=0;
for i in DEta_values:
    n_eta=n_eta+1;
    print "Deta: %f \t\t n_eta: %.0f"%(i,n_eta)
    

i=0;
for i in DMjj_values:
    
    n_mjj=n_mjj+1;
    print "DMjj: %f \t\t n_mjj: %.0f"%(i,n_mjj)

i=j=0;
VBF_cut_values=[0 for i in range(n_mjj+n_eta) ];

i=j=0;
for i in range(n_eta):
    VBF_cut_values[i]=[DEta_values[i],0];

for j in range(n_mjj):
    VBF_cut_values[j+n_eta]=[0,DMjj_values[j]];


i=0;
for i in range(n_mjj+n_eta):
    print VBF_cut_values[i]
    
VBF_cut=[0,0];




VBF_cut=[0,0];

for lumi_float_value in luminosities:
    
    lumi_str=str("%.0f"%lumi_float_value);
    #log_file=Lumi_dir+"/log_VBF_%s_M%i_%s_%s_lumi%s.log"%sample,m,options.channel,options.category,lumi_str
    
    if options.VBF_process:
       Lumi_dir_VBF=Data_dir+"/Lumi_%s_VBF"%lumi_str;
       if not os.path.isdir(Lumi_dir_VBF):
              os.system("mkdir "+Lumi_dir_VBF);
       
       VBF_CutListFileName = Lumi_dir_VBF+"/VBF_CutListFile.txt";
       VBF_CutListFile = open(VBF_CutListFileName, 'w');
       for VBF_cut in VBF_cut_values:
           VBF_CutListFile.write("%f %f\n"%(VBF_cut[0],VBF_cut[1]));
    
       VBF_CutListFile.close();
    
    
    
    
    
    for sample in samples:

        if sample.find('BulkGraviton') !=-1:
           masses=[600]#,800,1000]
       
       
        if sample.find('Higgs') !=-1:
           masses=[650,1000]
    
    
    
    
    
        for m in masses:
          
          
        
        
        
            #### VBF PROCESS
            if options.VBF_process:
               for VBF_cut in VBF_cut_values:
                            
                   
                   
                   Cut_dir=Lumi_dir_VBF+"/DEta%1.1f_Mjj_%.0f"%(VBF_cut[0],VBF_cut[1]);               
                   if not os.path.isdir(Cut_dir):
                          os.system("mkdir "+Cut_dir);
                   
                              
                   log_dir=Cut_dir+"/log_VBF";
                   if not os.path.isdir(log_dir):
                          os.system("mkdir "+log_dir);
               
               
                   log_file=log_dir+"/log_VBF_%s_M%i_%s_%s_lumi%s.log"%(sample,m,options.channel,options.category,lumi_str);
                   if (options.interpolate==False and options.batchMode==True):
              
                      job_dir=Cut_dir+"/Job_VBF_lumi_%s"%(lumi_str)
                      if not os.path.isdir(job_dir):
                             os.system("mkdir "+job_dir);
            
                      fn = job_dir+"/job_VBF_%s_%s_%s_%d"%(options.channel,options.category,sample,m)
                      outScript = open(fn+".sh","w");
 
                      outScript.write('#!/bin/bash');
                      outScript.write("\n"+'cd '+currentDir);
                      outScript.write("\n"+'eval `scram runtime -sh`');
                      outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
                      outScript.write("\n"+'echo ${PATH}');
                      outScript.write("\n"+'ls');
#           cmd = "python g1_exo_doFit_class.py -b -c %s --mass %i --category %s --sample %s_lvjj --jetalgo %s --interpolate True > log/%s_M%i_%s_%s.log" %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,sample,m,options.channel,options.category)
                      cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f --vbf True %s --DEta %f --DMjj %f > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option,VBF_cut[0],VBF_cut[1]);
                      cmd= cmd_tmp+log_file;
                      outScript.write("\n"+cmd);
#      outScript.write("\n"+'rm *.out');
                      outScript.close();

                      os.system("chmod 777 "+currentDir+"/"+fn+".sh");
                      os.system("bsub -q 8nm -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");

                   elif (options.interpolate==True and not options.batchMode==True):
                        cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True --vbf True %s --DEta %f --DMjj %f> " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option,VBF_cut[0],VBF_cut[1]);
                        cmd=cmd_tmp+log_file;
                        print cmd
                        os.system(cmd);

                   else:   
                        cmd_tmp = "python MATTEO_g1_exo_doFit_class_new.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f --vbf True %s --DEta %f --DMjj %f > "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value,pd_option,VBF_cut[0],VBF_cut[1]);
                        cmd=cmd_tmp+log_file;
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
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               '''
               Ntuple_dir_name_lumi=Ntuple_dir_name+"/Lumi_%s"%lumi_str
               if not os.path.isdir(Ntuple_dir_name_lumi):
                      os.system("mkdir "+Ntuple_dir_name_lumi);
               
               log_dir_name=Ntuple_dir_name_lumi+"/log"
               if not os.path.isdir(log_dir_name):
                      os.system("mkdir "+log_dir_name);
               
               plots_dir_name=Ntuple_dir_name_lumi+"/plots_%s_%s" %(options.channel,options.category) 
               if not os.path.isdir(plots_dir_name):
                      os.system("mkdir "+plots_dir_name);
               
               plots_dir_name2=Ntuple_dir_name_lumi+"/plots_%s_%s/%s" %(options.channel,options.category,sample) 
               if not os.path.isdir(plots_dir_name2):
                      os.system("mkdir "+plots_dir_name2);
               
               cards_dir_name=Ntuple_dir_name_lumi+"/cards_%s_%s" %(options.channel,options.category) 
               if not os.path.isdir(cards_dir_name):
                      os.system("mkdir "+cards_dir_name);
                      
               cards_dir_name2=Ntuple_dir_name_lumi+"/cards_%s_%s/%s" %(options.channel,options.category,sample) 
               if not os.path.isdir(cards_dir_name2):
                      os.system("mkdir "+cards_dir_name2);  
               
               
                     
                      
               
               
               #log_dir=Ntuple_dir_name_lumi+"/log"
               mass=str(m);
               log_file=log_dir_name+"/log_%s_%s_%s_%s.log"%(sample,mass,options.channel,options.category)
               
               if (options.interpolate==False and options.batchMode==True):
              
                  if not os.path.isdir("Job_lumi_%s"%(lumi_str)):
                         os.system("mkdir Job_lumi_%s"%(lumi_str));
                
                  fn = "Job_lumi_%s/job_%s_%s_lumi%s_%d"%(lumi_str,options.channel,options.category,lumi_str,m)
                  outScript = open(fn+".sh","w");
 
                  outScript.write('#!/bin/bash');
                  outScript.write("\n"+'cd '+currentDir);
                  outScript.write("\n"+'eval `scram runtime -sh`');
                  outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
                  outScript.write("\n"+'echo ${PATH}');
                  outScript.write("\n"+'ls');
#           cmd = "python g1_exo_doFit_class.py -b -c %s --mass %i --category %s --sample %s_lvjj --jetalgo %s --interpolate True > log/%s_M%i_%s_%s.log" %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,sample,m,options.channel,options.category)
                  cmd_tmp = "python MATTEO_g1_exo_doFit_class_new3.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value)
                  cmd=cmd_tmp+log_file;
                  outScript.write("\n"+cmd);
#      outScript.write("\n"+'rm *.out');
                  outScript.close();

                  os.system("chmod 777 "+currentDir+"/"+fn+".sh");
                  os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+currentDir+"/"+fn+".sh");

               elif (options.interpolate==True and not options.batchMode==True):
                    cmd_tmp = "python MATTEO_g1_exo_doFit_class_new3.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f --interpolate True > " %(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value)
                    cmd=cmd_tmp+log_file
                    print cmd
                    os.system(cmd)
           
           

               else:   
                    cmd_tmp = "python MATTEO_g1_exo_doFit_class_new3.py -b -c %s --ntuple %s --mass %i --category %s --sample %s --jetalgo %s --luminosity %f > "%(options.channel,options.ntuple,m,options.category,sample,options.jetalgo,lumi_float_value)
                    cmd=cmd_tmp+log_file
                    print cmd
                    os.system(cmd)

               '''



######################################################
###    Move the output in the Ntuple directory
######################################################


'''
if not options.batchMode==True:
   for lumi in luminosities:
     
       lumi_str_value=str("%.0f"%lumi);
     
       if options.VBF_process:
          tmp_vbf_name="_VBF_";
          Ntuple_dir_name_lumi_for_cp=Ntuple_dir_name+"/Lumi_%s_VBF"%lumi_str_value
          if not os.path.isdir(Ntuple_dir_name_lumi_for_cp):
                 os.system("mkdir "+Ntuple_dir_name_lumi_for_cp);
	
       else:
          tmp_vbf_name="_";
          Ntuple_dir_name_lumi_for_cp=Ntuple_dir_name+"/Lumi_%s"%lumi_str_value
          if not os.path.isdir(Ntuple_dir_name_lumi_for_cp):
                 os.system("mkdir "+Ntuple_dir_name_lumi_for_cp);
     
     
     
     
     
     
     
     
       plots_dir_in="plots%s%s_%s_lumi_%s/" %(tmp_vbf_name,options.channel,options.category,lumi_str_value)
       plots_dir_out=Ntuple_dir_name_lumi_for_cp+"/"+"plots%s%s_%s/" %(tmp_vbf_name,options.channel,options.category)
     
       datacards_dir_in="cards%s%s_%s_lumi_%s/"%(tmp_vbf_name,options.channel,options.category,lumi_str_value)
       datacards_dir_out=Ntuple_dir_name_lumi_for_cp+"/"+"cards%s%s_%s/"%(tmp_vbf_name,options.channel,options.category)
        
       log_dir_in="log%slumi_%s"%(tmp_vbf_name,lumi_str)
       log_dir_out=Ntuple_dir_name_lumi_for_cp+"/"+"Log%s%s_%s/"%(tmp_vbf_name,options.channel,options.category)
     
       p1 = subprocess.Popen(['cp','-r',plots_dir_in,plots_dir_out])
       p1.wait()
     
       p3 = subprocess.Popen(['cp','-r',datacards_dir_in,datacards_dir_out])
       p3.wait()
     
     
       p7 = subprocess.Popen(['cp','-r',log_dir_in,log_dir_out])
       p7.wait()
     
             
       p4 = subprocess.Popen(['rm','-r',datacards_dir_in])
       p4.wait()
     
       p5 = subprocess.Popen(['rm','-r',plots_dir_in])
       p5.wait()
     
       p8 = subprocess.Popen(['rm','-r',log_dir_in])
       p8.wait()
     
      
     
     
     
           
    
'''    
#python run-all.py --channel mu -s Wprime_WZ --jetalgo Mjsoftdrop --category HP
#python run-all.py -c mu -s BulkG_WW --category HPW

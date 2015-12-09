import json
from ggplot import *
import pandas as pd

my_file = open('/Users/Xinyue_star/Desktop/Final_Proj/connectivity_results.txt', 'r')
connectivity_results = json.load(my_file)
connectivity_results['003']['con'].keys()
#within network
data_in_scz = []
dic_scz = connectivity_results['003']['scz']
data_in_scz.append(np.ravel(dic_scz['Default']))
data_in_scz.append(np.ravel(dic_scz['Cingulo-Opercular']))
data_in_scz.append(np.ravel(dic_scz['Fronto-Parietal']))
data_in_scz.append(np.ravel(dic_scz['Cerebellar']))



data_in_con = connectivity_results['003']['con']
data_in_con = []
dic_con = connectivity_results['003']['con']
data_in_con.append(np.ravel(dic_scz['Default']))
data_in_con.append(np.ravel(dic_scz['Cingulo-Opercular']))
data_in_con.append(np.ravel(dic_scz['Fronto-Parietal']))
data_in_con.append(np.ravel(dic_scz['Cerebellar']))

#CREAT A DICTIONAY TO FIND THE TARGET NETWORK. It is like a rename.
find_nw = {}
find_nw['Default-Cerebellar']='bDMN-CER'
find_nw['Cerebellar-Cingulo-Opercular']='bCO-CER'
find_nw['Default-Cingulo-Opercular']='bDMN-CO'
find_nw['Default']='wDMN'
find_nw['Fronto-Parietal-Cerebellar']='bFP-CER'
find_nw['Cingulo-Opercular']='wCO'
find_nw['Default-Fronto-Parietal']='bDMN-FP'
find_nw['Fronto-Parietal']='wFP'
find_nw['Cerebellar']='wCER'
find_nw['Fronto-Parietal-Cingulo-Opercular']='bFP-CO'
between_namelist = ['Default-Cerebellar','Cerebellar-Cingulo-Opercular','Default-Cingulo-Opercular'
,'Fronto-Parietal-Cerebellar','Default-Fronto-Parietal','Fronto-Parietal-Cingulo-Opercular']



# dic = connectivity_results
def create_f (task, dic, namelist):
	con_group = "con"
	scz_group = 'scz'

	sub_dic_con = dic[task][con_group]
	sub_dic_scz = dic[task][scz_group]
	corrs = np.array([])
	network = np.array([])
	for name in namelist:
		corrs = np.append(corrs, np.ravel(sub_dic_con[name]))
	 	network =np.append(network, [find_nw[name] + ",con"]*len(np.ravel(sub_dic_con[name])))
	 	corrs = np.append(corrs, np.ravel(sub_dic_scz[name]))
	 	network =np.append(network, [find_nw[name] + ",scz"]*len(np.ravel(sub_dic_scz[name])))
	data_f = pd.DataFrame(corrs)
	data_f['networks']=network
	data_f.columns = ['corrs','networks']
	return data_f

within_namelist = ['Default','Fronto-Parietal','Cerebellar','Cingulo-Opercular']
f_within = create_f ('003', connectivity_results, within_namelist)
ggplot(f_within, aes(x='corrs', y='networks')) +\
    geom_boxplot()+\
    ggtitle("Within-Network Correlations in CON and SCZ Group")+\
    xlab("Correlation")+\
    ylab("networks")+\
    scale_x_continuous(limits=(-1.0, 1.0))

between_namelist = ['Default-Cerebellar','Cerebellar-Cingulo-Opercular','Default-Cingulo-Opercular'
,'Fronto-Parietal-Cerebellar','Default-Fronto-Parietal','Fronto-Parietal-Cingulo-Opercular']
f_between = create_f ('003', connectivity_results, between_namelist)
ggplot(f_between, aes(x='corrs', y='networks')) +\
    geom_boxplot()+\
    ggtitle("Between-Network Correlations in CON and SCZ Group")+\
    xlab("Correlation")+\
    ylab("networks")+\
    scale_x_continuous(limits=(-1.0, 1.0))

'''
APPENDIX A
DETAILED DESCRIPTION OF THE
RUN-TIME INPUT FOR STANDARD RUNS

PDF: p. 110.
'''

#%%
def create_batchrun_file(Id, Tag, Comment, CHL, CDOM, NAP, S_CDOM, spf_ff_bb_b_nap, spf_ff_bb_b_chl, suntheta, sunphi, cloud, windspeed):

    # Crea el archivo en el formato de HL.
    
    S = '' # string vací­o donde se van guardando los datos.
    
    #RECORD 1: Default Parameters
    Record = {}
    
    Record[1] = '0, 400, 700, 0.02, 488, 0.00026, 1, 5.3'
    
    ########################################
    #RECORD 2: Run Title
    # This record gives the descriptive title for the run. The title can be up to 120 characters long.
    
    Record[2] = Comment # Comentarios opcionales.
    
    ########################################
    #RECORD 3: Rootname
    
    Record[3] = '%04d_%s'%(Id, Tag)
    
    ########################################
    #RECORD 4a: output options
    
    Record_4a = '0, 1, 0, 0, 0, 1'
    
    #RECORD 4b: model options
    
    Record_4b = '2, 1, 0, 2, 3, 0'
    # Si tarda varios segundos por cada long. de onda y los resultados no tienen sentido, puede ser un error en el record 4b.
    
    Record[4] = Record_4a + '\n' + Record_4b
    
    del Record_4a, Record_4b
    
    ########################################
    R5 = {} # Record 5.
    
    #RECORD 5a: Number of IOP components
    
    R5['a'] = '4, 4' # H2O, CHL, CDOM, NAP.

    #RECORD 5b: Concentration options
    
    R5['b'] = '0, %g, %g, %g'%(CHL, CDOM, NAP) # Concentraciones.
    
    #RECORD 5c: Absorption parameters
    Record_5c_H20 = '0, 0, 0, 0, 0'#'0, -999, -999, -999, -999' # leer archivo
    Record_5c_CHL = '0, 0, 0, 0, 0'#'0, -999, -999, -999, -999' # leer archivo
    Record_5c_CDOM = '0, 4, 443, 1, %g'%(-S_CDOM) #'3, 4, 443, 1, 0.0176' # exponencial para CDOM
    Record_5c_NAP = '0, 0, 0, 0, 0'#'0, -999, -999, -999, -999' # leer archivo
    
    R5['c'] = Record_5c_H20 + '\n' + Record_5c_CHL + '\n' + Record_5c_CDOM + '\n' + Record_5c_NAP
    
    del Record_5c_H20, Record_5c_CHL, Record_5c_CDOM, Record_5c_NAP

    #RECORD 5d: Absorption data files
    Record_5d_H20 = '/home/santiago/Documents/HE60/data/H2OabCCRR.txt'
    Record_5d_CHL = '/home/santiago/Documents/HE60/data/DATA_SS/%04d_astar_CHL.txt'%(Id)
    Record_5d_CDOM = 'dummyastar.txt'
    Record_5d_NAP = '/home/santiago/Documents/HE60/data/DATA_SS/%04d_astar_NAP.txt'%(Id)
       
    R5['d'] = Record_5d_H20 + '\n' + Record_5d_CHL + '\n' + Record_5d_CDOM + '\n' + Record_5d_NAP
    
    del Record_5d_H20, Record_5d_CHL, Record_5d_CDOM, Record_5d_NAP

    #RECORD 5e: Scattering parameters
    Record_5e_H20 = '0, -999, -999, -999, -999, -999'
    Record_5e_CHL = '0, -999, -999, -999, -999, -999'
    Record_5e_CDOM = '-1, -999, 0, -999, -999, -999'
    Record_5e_NAP = '0, -999, -999, -999, -999, -999'
    
    R5['e'] = Record_5e_H20 + '\n' + Record_5e_CHL + '\n' + Record_5e_CDOM + '\n' + Record_5e_NAP
    
    del Record_5e_H20, Record_5e_CHL, Record_5e_CDOM, Record_5e_NAP
    
    #RECORD 5f: Scattering data files
    Record_5f_H20 = 'bstarDummy.txt'
    Record_5f_CHL = '/home/santiago/Documents/HE60/data/DATA_SS/%04d_bstar_CHL.txt'%(Id)
    Record_5f_CDOM = 'dummybstar.txt'
    Record_5f_NAP = '/home/santiago/Documents/HE60/data/DATA_SS/%04d_bstar_NAP.txt'%(Id)
    
    R5['f'] = Record_5f_H20 + '\n' + Record_5f_CHL + '\n' + Record_5f_CDOM + '\n' + Record_5f_NAP
    
    del Record_5f_H20, Record_5f_CHL, Record_5f_CDOM, Record_5f_NAP
    
    #RECORD 5g: Conc & phase func params
    Record_5g_H20 = '0,0,550,0.01,0'
    Record_5g_CHL = '0,0,550,0.01,0'
    Record_5g_CDOM = '0,0,550,0.01,0'
    Record_5g_NAP = '0,0,550,0.01,0'
    
    R5['g'] = Record_5g_H20 + '\n' + Record_5g_CHL + '\n' + Record_5g_CDOM + '\n' + Record_5g_NAP
    
    del Record_5g_H20, Record_5g_CHL, Record_5g_CDOM, Record_5g_NAP
    
    #RECORD 5h: Phase function files
    
    # W:
    Record_5h_H20 = 'dpf_pure_H2O.txt'
    
    # CHL:
    if spf_ff_bb_b_chl=='Petzold':
        Record_5h_CHL = 'dpf_Petzold_avg_particle.txt'
    else:
        Record_5h_CHL = 'dpf_FF_bb%03d.txt'%(spf_ff_bb_b_chl*1000)
    
    # CDOM:
    Record_5h_CDOM = 'dpf_Petzold_avg_particle.txt'
    
    # NAP:
    if spf_ff_bb_b_nap=='Petzold':
        Record_5h_NAP = 'dpf_Petzold_avg_particle.txt'
    else:
        Record_5h_NAP = 'dpf_FF_bb%03d.txt'%(spf_ff_bb_b_nap*1000)

    R5['h'] = Record_5h_H20 + '\n' + Record_5h_CHL + '\n' + Record_5h_CDOM + '\n' + Record_5h_NAP
        
    Record[5] = '\n'.join(R5.values())

    del R5
     
    ########################################
    
    # Para generar las longitudes de onda:
    #import numpy as np
    #x = np.arange(350-1.25, 957.5-1.25, 2.5)
    #print(x)

    R6 = {}
    
    # Para pruebas:
    # np.linspace(350, 950, 6)
    #R6['a'] = '5'
    #R6['b'] = '350.0, 470.0, 590.0, 710.0, 830.0, 950.0'

    # np.linspace(350, 950, 11)
    #R6['a'] = '10'
    #R6['b'] = '350.0, 410.0, 470.0, 530.0, 590.0, 650.0, 710.0, 770.0, 830.0, 890.0, 950.0'
    
    #RECORD 6a: number of wavelength bands
    R6['a'] = '241'
    #RECORD 6b: Wavelength band boundaries
    R6['b'] = '348.75 351.25 353.75 356.25 358.75 361.25 363.75 366.25 368.75 371.25  373.75 376.25 378.75 381.25 383.75 386.25 388.75 391.25 393.75 396.25 398.75 401.25 403.75 406.25 408.75 411.25 413.75 416.25 418.75 421.25 423.75 426.25 428.75 431.25 433.75 436.25 438.75 441.25 443.75 446.25 448.75 451.25 453.75 456.25 458.75 461.25 463.75 466.25 468.75 471.25 473.75 476.25 478.75 481.25 483.75 486.25 488.75 491.25 493.75 496.25 498.75 501.25 503.75 506.25 508.75 511.25 513.75 516.25 518.75 521.25 523.75 526.25 528.75 531.25 533.75 536.25 538.75 541.25 543.75 546.25 548.75 551.25 553.75 556.25 558.75 561.25 563.75 566.25 568.75 571.25 573.75 576.25 578.75 581.25 583.75 586.25 588.75 591.25 593.75 596.25 598.75 601.25 603.75 606.25 608.75 611.25 613.75 616.25 618.75 621.25 623.75 626.25 628.75 631.25 633.75 636.25 638.75 641.25 643.75 646.25 648.75 651.25 653.75 656.25 658.75 661.25 663.75 666.25 668.75 671.25 673.75 676.25 678.75 681.25 683.75 686.25 688.75 691.25 693.75 696.25 698.75 701.25 703.75 706.25 708.75 711.25 713.75 716.25 718.75 721.25 723.75 726.25 728.75 731.25 733.75 736.25 738.75 741.25 743.75 746.25 748.75 751.25 753.75 756.25 758.75 761.25 763.75 766.25 768.75 771.25 773.75 776.25 778.75 781.25 783.75 786.25 788.75 791.25 793.75 796.25 798.75 801.25 803.75 806.25 808.75 811.25 813.75 816.25 818.75 821.25 823.75 826.25 828.75 831.25 833.75 836.25 838.75 841.25 843.75 846.25 848.75 851.25 853.75 856.25 858.75 861.25 863.75 866.25 868.75 871.25 873.75 876.25 878.75 881.25 883.75 886.25 888.75 891.25 893.75 896.25 898.75 901.25 903.75 906.25 908.75 911.25 913.75 916.25 918.75 921.25 923.75 926.25 928.75 931.25 933.75 936.25 938.75 941.25 943.75 946.25 948.75 951.25 953.75'
     
    Record[6] = '\n'.join(R6.values())
    
    del R6
    ########################################
    
    #RECORD 7: Inelastic scattering parameters
    Record[7] = '0, 1, 0, 0, 2'
    
    ########################################
    
    #RECORD 8a: Sky model parameters
    R8_a = '2, 3, %g, %g, %g'%(suntheta, sunphi, cloud)
    
    #RECORD 8b: Atmospheric parameters
    R8_b = '-1, 0, 0, 29.92, 1, 80, 2.5, 15, 5, 300'
    
    Record[8] = R8_a + '\n' + R8_b
    
    del R8_a, R8_b
    
    ########################################
    
    #RECORD 9: Sea surface parameters
    Record[9] = '%g, 1.34, 20, 35, 3'%(windspeed)
    
    ########################################
    
    #RECORD 10: Bottom parameters
    Record[10] = '0, 0'
    
    ########################################
    
    #RECORD 11: Output depths
    Record[11] = '0, 1, 0'
    
    ########################################
    R12 = {} # Record 12.
    
    #RECORD 12a: Data file for water IOPs
    R12['1'] = '/home/santiago/Documents/HE60/data/H2OabCCRR.txt'
    
    #RECORD 12b: Numbre of ac-x files
    R12['2'] = '1'
    
    #RECORD 12c: Unfiltered ac-x file
    R12['3'] = 'dummyac9.txt'
    
    #RECORD 12d: Filtered ac-x file
    R12['4'] = 'dummyFilteredAc9.txt'
    
    #RECORD 12e: Backscatter file
    R12['5'] = 'dummyHscat.txt'
    
    #RECORD 12f: Chlorophyll concentration file
    R12['6'] = 'dummyCHLdata.txt'
    
    #RECORD 12g: CDOM data file
    R12['7'] = 'dummyCDOMdata.txt'
    
    #RECORD 12h: Bottom reflectance file
    R12['8'] = 'dummyR.bot'
    
    #RECORD 12i: Component concentration file
    R12['9'] = 'dummyComp.txt\ndummyComp.txt\ndummyComp.txt\ndummyComp.txt'
    # ATENCION: Si tira "WARNING:  only [n] component datafiles were read." es porque faltan acá. Es un dummy por cada componente.
    
    #RECORD 12j: Sky irradiance data file
    R12['10'] = 'DummyIrrad.txt'
    
    #RECORD 12k: Bioluminiscence source file
    R12['11'] = '../data/examples/So_biolum_user_data.txt'
    
    #RECORD 12l: Sky radiance data file
    R12['12'] = 'DummyRad.txt'
    
    Record[12] = '\n'.join(R12.values())
    ########################################
    
    #RECORD 13: Names of user defined components
    Record[13] = ''
    
    
    S = '\n'.join(Record.values())
    
    ########################################
    
    with open("batchruns/I%s_%04d.txt"%(Tag, Id), "w") as output:
        output.write(S)

#%%

if __name__ == "__main__":

    # Valores de prueba:
    
    Id = 12345
    Tag = 'TAG'
    Comment = 'COMMENT'
    spf_ff_bb_b_nap = 0.018
    spf_ff_bb_b_chl = 0.006
    
    CHL = 1
    NAP = 1
    CDOM = 1
    
    S_CDOM = -0.0149
    
    suntheta = 40
    sunphi = 0
    cloud = 0
    windspeed = 5
    
    create_batchrun_file(Id, Tag, Comment, CHL, CDOM, NAP, S_CDOM, spf_ff_bb_b_nap, spf_ff_bb_b_chl, suntheta, sunphi, cloud, windspeed)
    
#!/usr/bin/env python
# import modules
import pika
import numpy as np
import pandas as pd
import time
import msgpack
import uproot # for reading .root files
import awkward as ak # to represent nested data in columnar format
import vector # for 4-momentum calculations
import time # to measure time to analyse
import math # for mathematical functions such as square root
import numpy as np # for numerical calculations such as histogramming
import pickle

# create important variables
lumi = 10 # fb-1 # data_A,data_B,data_C,data_D
MeV = 0.001
GeV = 1.0
fraction = 1.0 # reduce this is if you want the code to run quicker                                                                                                                
#tuple_path = "Input/4lep/" # local 
tuple_path = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/" # web address

"""Dict with DSID, # events, reduction efficiency, sum of weights, cross-section for each MC"""
infos = {

    # ZPrime -> ee

    'ZPrime2000_ee': {'DSID'    : 301215,
                      'events'  : 19800,
                      'red_eff' :1,
                      'sumw'    :19800,
                      'xsec'    :0.0088432},

    'ZPrime3000_ee': {'DSID'    : 301216,
                      'events'  : 19600,
                      'red_eff' :1,
                      'sumw'    :19600,
                      'xsec'    :0.00080617},

    'ZPrime4000_ee': {'DSID'    : 301217,
                      'events'  : 19800,
                      'red_eff' :1,
                      'sumw'    :19800,
                      'xsec'    :0.00010351},

    'ZPrime5000_ee': {'DSID'    : 301218,
                      'events'  : 18000,
                      'red_eff' :1,
                      'sumw'    :18000,
                      'xsec'    :0.000018319},


    # ZPrime -> mumu 2lep

    'ZPrime2000_mumu': {'DSID'    : 301220,
                        'events'  : 983000,
                        'red_eff' :1,
                        'sumw'    :983000,
                        'xsec'    :0.0088801},

    'ZPrime3000_mumu': {'DSID'    : 301221,
                        'events'  : 988000,
                        'red_eff' :1,
                        'sumw'    :988000,
                        'xsec'    :0.00080295},

    'ZPrime4000_mumu': {'DSID'    : 301222,
                        'events'  : 986000,
                        'red_eff' :1,
                        'sumw'    :986000,
                        'xsec'    :0.00010332},

    'ZPrime5000_mumu': {'DSID'    : 1,
                        'events'  : 999000,
                        'red_eff' :1,
                        'sumw'    :999000,
                        'xsec'    :0.000018334},


    # ZPrime -> tt

    'ZPrime400_tt': {'DSID'    : 301322,
                     'events'  : 199200,
                     'red_eff' : 1,
                     'sumw'    : 199200,
                     'xsec'    : 8.9857},

    'ZPrime500_tt': {'DSID'    : 301323,
                     'events'  : 199600,
                     'red_eff' : 1,
                     'sumw'    : 199600,
                     'xsec'    : 8.7385},

    'ZPrime750_tt': {'DSID'    : 301324,
                     'events'  : 199000,
                     'red_eff' : 1,
                     'sumw'    : 199000,
                     'xsec'    : 3.1201},

    'ZPrime1000_tt': {'DSID'    : 301325,
                      'events'  : 199800,
                      'red_eff' : 1,
                      'sumw'    : 199800,
                      'xsec'    : 1.1261},

    'ZPrime1250_tt': {'DSID'    : 301326,
                      'events'  : 199200,
                      'red_eff' : 1,
                      'sumw'    : 199200,
                      'xsec'    : 0.45981},

    'ZPrime1500_tt': {'DSID'    : 301327,
                      'events'  : 198800,
                      'red_eff' : 1,
                      'sumw'    : 198800,
                      'xsec'    : 0.20685},

    'ZPrime1750_tt': {'DSID'    : 301328,
                      'events'  : 199800,
                      'red_eff' : 1,
                      'sumw'    : 199800,
                      'xsec'    : 0.10016},

    'ZPrime2000_tt': {'DSID'    : 301329,
                      'events'  : 199800,
                      'red_eff' : 1,
                      'sumw'    : 199800,
                      'xsec'    : 0.051346},

    'ZPrime2250_tt': {'DSID'    : 301330,
                      'events'  : 199200,
                      'red_eff' : 1,
                      'sumw'    : 199200,
                      'xsec'    : 0.027481},

    'ZPrime2500_tt': {'DSID'    : 301331,
                      'events'  : 198200,
                      'red_eff' : 1,
                      'sumw'    : 198200,
                      'xsec'    : 0.015226},

    'ZPrime2750_tt': {'DSID'    : 301332,
                      'events'  : 199800,
                      'red_eff' : 1,
                      'sumw'    : 199800,
                      'xsec'    : 0.0086884},

    'ZPrime3000_tt': {'DSID'    : 301333,
                      'events'  : 195800,
                      'red_eff' : 1,
                      'sumw'    : 195800,
                      'xsec'    : 0.0050843},


    # Graviton

    'RS_G_ZZ_llll_c10_m0200': {'DSID'    : 307431,
                               'events'  : 29000,
                               'red_eff' : 1,
                               'sumw'    : 29000,
                               'xsec'    : 1.86},

    'RS_G_ZZ_llll_c10_m0500': {'DSID'    : 307434,
                               'events'  : 27000,
                               'red_eff' : 1,
                               'sumw'    : 27000,
                               'xsec'    : 0.02373},

    'RS_G_ZZ_llll_c10_m1000': {'DSID'    : 303329,
                               'events'  : 3000,
                               'red_eff' : 1,
                               'sumw'    : 3000,
                               'xsec'    : 0.0004122},

    'RS_G_ZZ_llll_c10_m1500': {'DSID'    : 307439,
                               'events'  : 30000,
                               'red_eff' : 1,
                               'sumw'    : 30000,
                               'xsec'    : 0.00003702},

    'RS_G_ZZ_llll_c10_m2000': {'DSID'    : 303334,
                               'events'  : 5000,
                               'red_eff' : 1,
                               'sumw'    : 5000,
                               'xsec'    : 0.0000057},


    # Mono Z

    'dmV_Zll_MET40_DM1_MM10': {'DSID'    : 303511,
                               'events'  : 10000,
                               'red_eff' : 1,
                               'sumw'    : 10000,
                               'xsec'    : 11.55},

    'dmV_Zll_MET40_DM1_MM100': {'DSID'    : 303512,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.4682},

    'dmV_Zll_MET40_DM1_MM200': {'DSID'    : 306085,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.1424},

    'dmV_Zll_MET40_DM1_MM300': {'DSID'    : 303513,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.063965},

    'dmV_Zll_MET40_DM1_MM400': {'DSID'    : 306093,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.031865},

    'dmV_Zll_MET40_DM1_MM500': {'DSID'    : 305710,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.018275},

    'dmV_Zll_MET40_DM1_MM600': {'DSID'    : 306103,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.01136},

    'dmV_Zll_MET40_DM1_MM700': {'DSID'    : 305711,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.007416},

    'dmV_Zll_MET40_DM1_MM800': {'DSID'    : 306109,
                                'events'  : 10000,
                                'red_eff' : 1,
                                'sumw'    : 10000,
                                'xsec'    : 0.005016},

    'dmV_Zll_MET40_DM1_MM2000': {'DSID'    : 303514,
                                 'events'  : 10000,
                                 'red_eff' : 1,
                                 'sumw'    : 10000,
                                 'xsec'    : 0.0001636},


    # gluino-gluino -> stop-stop -> tttt + DM

    'GG_ttn1_1200_5000_1': {'DSID'    : 370114,
                            'events'  : 100000,
                            'red_eff' : 1,
                            'sumw'    : 101591.347734,
                            'xsec'    : 0.057037},

    'GG_ttn1_1200_5000_600': {'DSID'    : 370118,
                              'events'  : 100000,
                              'red_eff' : 1,
                              'sumw'    : 101591.282303,
                              'xsec'    : 0.057002},

    'GG_ttn1_1400_5000_1': {'DSID'    : 370129,
                            'events'  : 100000,
                            'red_eff' : 1,
                            'sumw'    : 101197.830825,
                            'xsec'    : 0.015756},

    'GG_ttn1_1600_5000_1': {'DSID'    : 370144,
                            'events'  : 99000,
                            'red_eff' : 1,
                            'sumw'    : 99850.3055654,
                            'xsec'    : 0.004747},


    # stop-stop -> tt + DM

    'TT_directTT_450_1': {'DSID'    : 388240,
                          'events'  : 50000,
                          'red_eff' : 1,
                          'sumw'    : 52247.301193,
                          'xsec'    : 0.88424},

    'TT_directTT_500_1': {'DSID'    : 387154,
                          'events'  : 20000,
                          'red_eff' : 1,
                          'sumw'    : 20793.7352104,
                          'xsec'    : 0.46603},

    'TT_directTT_500_200': {'DSID'    : 387157,
                            'events'  : 50000,
                            'red_eff' : 1,
                            'sumw'    : 51998.4134001,
                            'xsec'    : 0.46702},

    'TT_directTT_600_1': {'DSID'    : 387163,
                          'events'  : 49000,
                          'red_eff' : 1,
                          'sumw'    : 50709.6451392,
                          'xsec'    : 0.15518},


    # chargino-neutralino -> WZ(->lvll)

    'C1N2_WZ_100p0_0p0_3L_2L7': {'DSID'    : 392226,
                                 'events'  : 20000,
                                 'red_eff' : 1,
                                 'sumw'    : 21798.5046117,
                                 'xsec'    : 15.82879625},

    'C1N2_WZ_350p0_0p0_3L_2L7': {'DSID'    : 392220,
                                 'events'  : 10000,
                                 'red_eff' : 1,
                                 'sumw'    : 10346.0705611,
                                 'xsec'    : 0.1418528975},

    'C1N2_WZ_400p0_0p0_3L_2L7': {'DSID'    : 392217,
                                 'events'  : 10000,
                                 'red_eff' : 1,
                                 'sumw'    : 10327.8154224,
                                 'xsec'    : 0.080689712},

    'C1N2_WZ_500p0_0p0_3L_2L7': {'DSID'    : 392223,
                                 'events'  : 5000,
                                 'red_eff' : 1,
                                 'sumw'    : 5130.27250254,
                                 'xsec'    : 0.0301334215},


    # chargino-neutralino -> WZ(->qqll)

    'C1N2_WZ_500p0_100p0_2L2J_2L7': {'DSID'    : 392302,
                                     'events'  : 5000,
                                     'red_eff' : 1,
                                     'sumw'    : 5123.94193453,
                                     'xsec'    : 0.025481788},

    'C1N2_WZ_300p0_100p0_2L2J_2L7': {'DSID'    : 392304,
                                     'events'  : 10000,
                                     'red_eff' : 1,
                                     'sumw'    : 10419.6442093,
                                     'xsec'    : 0.2182152585},

    'C1N2_WZ_300p0_200p0_2L2J_2L7': {'DSID'    : 392308,
                                     'events'  : 10000,
                                     'red_eff' : 1,
                                     'sumw'    : 10414.1419529,
                                     'xsec'    : 0.218912097},

    'C1N2_WZ_400p0_0p0_2L2J_2L7': {'DSID'    : 392317,
                                   'events'  : 10000,
                                   'red_eff' : 1,
                                   'sumw'    : 10324.0226582,
                                   'xsec'    : 0.068632923},

    'C1N2_WZ_500p0_0p0_2L2J_2L7': {'DSID'    : 392323,
                                   'events'  : 5000,
                                   'red_eff' : 1,
                                   'sumw'    : 5135.2308228,
                                   'xsec'    : 0.0257187712},

    'C1N2_WZ_400p0_300p0_2L2J_2L7': {'DSID'    : 392324,
                                     'events'  : 10000,
                                     'red_eff' : 1,
                                     'sumw'    : 10318.5426682,
                                     'xsec'    : 0.067068856},

    'C1N2_WZ_100p0_0p0_2L2J_2L7': {'DSID'    : 392326,
                                   'events'  : 20000,
                                   'red_eff' : 1,
                                   'sumw'    : 21807.0756063,
                                   'xsec'    : 12.3557577},

    'C1N2_WZ_200p0_100p0_2L2J_2L7': {'DSID'    : 392330,
                                     'events'  : 20000,
                                     'red_eff' : 1,
                                     'sumw'    : 21100.6583921,
                                     'xsec'    : 0.3120280476},

    'C1N2_WZ_500p0_300p0_2L2J_2L7': {'DSID'    : 392332,
                                     'events'  : 5000,
                                     'red_eff' : 1,
                                     'sumw'    : 5136.04743809,
                                     'xsec'    : 0.0255630137},

    'C1N2_WZ_600_100_2L2J_2L7': {'DSID'    : 392354,
                                 'events'  : 5000,
                                 'red_eff' : 1,
                                 'sumw'    : 5130.17177922,
                                 'xsec'    : 0.0110981746},

    'C1N2_WZ_600_0_2L2J_2L7': {'DSID'    : 392356,
                               'events'  : 5000,
                               'red_eff' : 1,
                               'sumw'    : 5115.96802914,
                               'xsec'    : 0.01106208},

    'C1N2_WZ_700_400_2L2J_2L7': {'DSID'    : 392361,
                                 'events'  : 4000,
                                 'red_eff' : 1,
                                 'sumw'    : 4069.40415132,
                                 'xsec'    : 0.00518059472},

    'C1N2_WZ_700_100_2L2J_2L7': {'DSID'    : 392364,
                                 'events'  : 5000,
                                 'red_eff' : 1,
                                 'sumw'    : 5093.62593496,
                                 'xsec'    : 0.00511756038},

    'C1N2_WZ_700_0_2L2J_2L7': {'DSID'    : 392365,
                               'events'  : 5000,
                               'red_eff' : 1,
                               'sumw'    : 5100.51524758,
                               'xsec'    : 0.0052089336},


    # chargino-chargino

    'C1C1_SlepSnu_x0p50_200p0_100p0_2L8': {'DSID'    : 392501,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 26095.2892522,
                                           'xsec'    : 0.438382903},

    'C1C1_SlepSnu_x0p50_200p0_150p0_2L8': {'DSID'    : 392502,
                                           'events'  : 14000,
                                           'red_eff' : 1,
                                           'sumw'    : 14610.1961992,
                                           'xsec'    : 0.3788318576},

    'C1C1_SlepSnu_x0p50_300p0_100p0_2L8': {'DSID'    : 392504,
                                           'events'  : 24000,
                                           'red_eff' : 1,
                                           'sumw'    : 24769.4974021,
                                           'xsec'    : 0.0999784056},

    'C1C1_SlepSnu_x0p50_300p0_250p0_2L8': {'DSID'    : 392506,
                                           'events'  : 14000,
                                           'red_eff' : 1,
                                           'sumw'    : 14461.581905,
                                           'xsec'    : 0.080525632},

    'C1C1_SlepSnu_x0p50_400p0_100p0_2L8': {'DSID'    : 392507,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 25655.2504594,
                                           'xsec'    : 0.0311401198},

    'C1C1_SlepSnu_x0p50_400p0_300p0_2L8': {'DSID'    : 392509,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 25632.581066,
                                           'xsec'    : 0.0285856272},

    'C1C1_SlepSnu_x0p50_500p0_300p0_2L8': {'DSID'    : 392513,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 25567.3058318,
                                           'xsec'    : 0.0114399795},

    'C1C1_SlepSnu_x0p50_600p0_300p0_2L8': {'DSID'    : 392517,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 25472.8026792,
                                           'xsec'    : 0.004885755904},

    'C1C1_SlepSnu_x0p50_700p0_1p0_2L8': {'DSID'    : 392518,
                                         'events'  : 25000,
                                         'red_eff' : 1,
                                         'sumw'    : 25410.7097093,
                                         'xsec'    : 0.00231816666},

    'C1C1_SlepSnu_x0p50_700p0_300p0_2L8': {'DSID'    : 392521,
                                           'events'  : 25000,
                                           'red_eff' : 1,
                                           'sumw'    : 25397.7880948,
                                           'xsec'    : 0.002285652872},


    # slepton

    'SlepSlep_direct_100p5_1p0_2L8': {'DSID'    : 392916,
                                      'events'  : 10000,
                                      'red_eff' : 1,
                                      'sumw'    : 12744.8491732,
                                      'xsec'    : 0.806723},

    'SlepSlep_direct_200p5_1p0_2L8': {'DSID'    : 392918,
                                      'events'  : 8000,
                                      'red_eff' : 1,
                                      'sumw'    : 9384.14328927,
                                      'xsec'    : 0.06466635},

    'SlepSlep_direct_300p5_1p0_2L8': {'DSID'    : 392920,
                                      'events'  : 10000,
                                      'red_eff' : 1,
                                      'sumw'    : 11199.5583518,
                                      'xsec'    : 0.01244275305},

    'SlepSlep_direct_500p5_1p0_2L8': {'DSID'    : 392924,
                                      'events'  : 9000,
                                      'red_eff' : 1,
                                      'sumw'    : 9692.91836751,
                                      'xsec'    : 0.001223162955},

    'SlepSlep_direct_100p0_50p0_2L8': {'DSID'    : 392925,
                                       'events'  : 10000,
                                       'red_eff' : 1,
                                       'sumw'    : 12817.7130976,
                                       'xsec'    : 0.81656133},

    'SlepSlep_direct_200p0_100p0_2L8': {'DSID'    : 392936,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 11683.0100918,
                                        'xsec'    : 0.064644393},

    'SlepSlep_direct_500p0_100p0_2L8': {'DSID'    : 392942,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 10774.6592166,
                                        'xsec'    : 0.001229322225},

    'SlepSlep_direct_300p0_200p0_2L8': {'DSID'    : 392951,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 11237.8868441,
                                        'xsec'    : 0.01243520595},

    'SlepSlep_direct_400p0_300p0_2L8': {'DSID'    : 392962,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 10944.9245315,
                                        'xsec'    : 0.0034380269},

    'SlepSlep_direct_500p0_300p0_2L8': {'DSID'    : 392964,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 10772.8356151,
                                        'xsec'    : 0.00121170732},

    'SlepSlep_direct_600p0_1p0_2L8': {'DSID'    : 392982,
                                      'events'  : 10000,
                                      'red_eff' : 1,
                                      'sumw'    : 10448.2514935,
                                      'xsec'    : 0.0004647888015},

    'SlepSlep_direct_600p0_300p0_2L8': {'DSID'    : 392985,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 10457.5703245,
                                        'xsec'    : 0.000464769511},

    'SlepSlep_direct_700p0_1p0_2L8': {'DSID'    : 392996,
                                      'events'  : 10000,
                                      'red_eff' : 1,
                                      'sumw'    : 10367.2338168,
                                      'xsec'    : 0.000204735222},

    'SlepSlep_direct_700p0_300p0_2L8': {'DSID'    : 392999,
                                        'events'  : 10000,
                                        'red_eff' : 1,
                                        'sumw'    : 10370.1994236,
                                        'xsec'    : 0.000204884372},

    'ttH125_gamgam': {'DSID'    : 341081,
                      'events'  : 927400,
                      'red_eff' : 1,
                      'sumw'    : 485440,
                      'xsec'    : 0.0000026433864},

    'ggH125_gamgam': {'DSID'    : 343981,
                      'events'  : 1976000,
                      'red_eff' : 1,
                      'sumw'    : 55922617.6297,
                      'xsec'    : 0.102},

    'VBFH125_gamgam': {'DSID'    : 345041,
                       'events'  : 921000,
                       'red_eff' : 1,
                       'sumw'    : 3441426.13711,
                       'xsec'    : 0.008518764},

    'WpH125J_Wincl_gamgam': {'DSID'    : 345318,
                             'events'  : 248000,
                             'red_eff' : 1,
                             'sumw'    : 213799.958463,
                             'xsec'    : 0.0019654512},

    'ZH125J_Zincl_gamgam': {'DSID'    : 345319,
                            'events'  : 471000,
                            'red_eff' : 1,
                            'sumw'    : 358401.082034,
                            'xsec'    : 0.0017347836},

    'ggH125_tautaull':{'DSID':341122,
                       'events':1522300,
                       'red_eff':1,
                       'sumw':20207228.675,
                       'xsec':0.3407921994},

    'VBFH125_tautaull':{'DSID':341155,
                        'events':2078800,
                        'red_eff':1,
                        'sumw':2078800,
                        'xsec':0.02906767389},

    'ggH125_tautaulh': {'DSID'    : 341123,
                        'events'  : 1446900,
                        'red_eff' : 1,
                        'sumw'    : 46547831.1387,
                        'xsec'    : 1.262373851},

    'VBFH125_tautaulh': {'DSID'    : 341156,
                         'events'  : 2087900,
                         'red_eff' : 1,
                         'sumw'    : 2087900,
                         'xsec'    : 0.1078731107},

    'ZH125_ZZ4lep':{'DSID':341947,
                    'events':150000,
                    'red_eff':1,
                    'sumw':150000,
                    'xsec':0.0000021424784},

    'WH125_ZZ4lep':{'DSID':341964,
                    'events':149400,
                    'red_eff':1,
                    'sumw':149400,
                    'xsec':0.0003769},

    'VBFH125_ZZ4lep':{'DSID':344235,
                      'events':985000,
                      'red_eff':1,
                      'sumw':3680490.83243,
                      'xsec':0.0004633012},

    'ggH125_ZZ4lep':{'DSID':345060,
                     'events':985000,
                     'red_eff':1,
                     'sumw':27881776.6536,
                     'xsec':0.0060239},

    'VBFH125_WW2lep':{'DSID':345323,
                      'events':1175000,
                      'red_eff':1,
                      'sumw':4389990.08913,
                      'xsec':0.02020229148},

    'ggH125_WW2lep':{'DSID':345324,
                     'events':1972000,
                     'red_eff':1,
                     'sumw':55832659.6908,
                     'xsec':0.1481173588},

    'WpH125J_qqWW2lep':{'DSID':345325,
                        'events':246000,
                        'red_eff':1,
                        'sumw':212083.006669,
                        'xsec':0.009137412},

    'WpH125J_lvWW2lep':{'DSID':345327,
                        'events':99000,
                        'red_eff':1,
                        'sumw':27654.9427524,
                        'xsec':0.002953584},

    'ZH125J_qqWW2lep':{'DSID':345336,
                       'events':245000,
                       'red_eff':1,
                       'sumw':186418.164907,
                       'xsec':0.008065858},

    'ZH125J_llWW2lep':{'DSID':345337,
                       'events':297000,
                       'red_eff':1,
                       'sumw':22685.3119437,
                       'xsec':0.0008078684},

    'ZH125J_vvWW2lep':{'DSID':345445,
                       'events':198000,
                       'red_eff':1,
                       'sumw':29701.769871,
                       'xsec':0.00159106},

    'Zee_PTV0_70_CVetoBVeto': {'DSID'    : 364114,
                               'events'  :7900000,
                               'red_eff' :1,
                               'sumw'    :5307644.52827,
                               'xsec'    :1587.021595},

    'Zee_PTV0_70_CFilterBVeto': {'DSID'    : 364115,
                                 'events'  :4940500,
                                 'red_eff' :1,
                                 'sumw'    :2839137.81561,
                                 'xsec'    :219.9958116},

    'Zee_PTV0_70_BFilter': {'DSID'    : 364116,
                            'events'  :7883600,
                            'red_eff' :1,
                            'sumw'    :4053053.52848,
                            'xsec'    :127.0857614},

    'Zee_PTV70_140_CVetoBVeto': {'DSID'    : 364117,
                                 'events'  :5885000,
                                 'red_eff' :1,
                                 'sumw'    :2149611.09271,
                                 'xsec'    :74.90381742},

    'Zee_PTV70_140_CFilterBVeto': {'DSID'    : 364118,
                                   'events'  :1972600,
                                   'red_eff' :1,
                                   'sumw'    :715162.089738,
                                   'xsec'    :20.3159891},

    'Zee_PTV70_140_BFilter': {'DSID'    : 364119,
                              'events'  :5855000,
                              'red_eff' :1,
                              'sumw'    :2043192.28295,
                              'xsec'    :12.73880801},

    'Zee_PTV140_280_CVetoBVeto': {'DSID'    : 364120,
                                  'events'  :4949000,
                                  'red_eff' :1,
                                  'sumw'    :2966342.61469,
                                  'xsec'    :24.44184978},

    'Zee_PTV140_280_CFilterBVeto': {'DSID'    : 364121,
                                    'events'  :2922600,
                                    'red_eff' :1,
                                    'sumw'    :1949820.29674,
                                    'xsec'    :9.237605979},

    'Zee_PTV140_280_BFilter': {'DSID'    : 364122,
                               'events'  :12010900,
                               'red_eff' :1,
                               'sumw'    :8328729.48708,
                               'xsec'    :6.081254464},

    'Zee_PTV280_500_CVetoBVeto': {'DSID'    : 364123,
                                  'events'  :1932800,
                                  'red_eff' :1,
                                  'sumw'    :1665734.2346,
                                  'xsec'    :4.796836771},

    'Zee_PTV280_500_CFilterBVeto': {'DSID'    : 364124,
                                    'events'  :988900,
                                    'red_eff' :1,
                                    'sumw'    :908261.497964,
                                    'xsec'    :2.249186051},

    'Zee_PTV280_500_BFilter': {'DSID'    : 364125,
                               'events'  :1976850,
                               'red_eff' :1,
                               'sumw'    :1854184.55614,
                               'xsec'    :1.49219843},

    'Zee_PTV500_1000': {'DSID'    : 364126,
                        'events'  :2973000,
                        'red_eff' :1,
                        'sumw'    :2942740.91362,
                        'xsec'    :1.76415092},

    'Zee_PTV1000_E_CMS': {'DSID'    : 364127,
                          'events'  :988000,
                          'red_eff' :1,
                          'sumw'    :1004312.18015,
                          'xsec'    :0.145046125},

    'Zmumu_PTV0_70_CVetoBVeto': {'DSID'    : 364100,
                                 'events'  :7891000,
                                 'red_eff' :1,
                                 'sumw'    :5319367.44387,
                                 'xsec'    :1588.474174},

    'Zmumu_PTV0_70_CFilterBVeto': {'DSID'    : 364101,
                                   'events'  :4917000,
                                   'red_eff' :1,
                                   'sumw'    :2834664.0856,
                                   'xsec'    :219.4826028},

    'Zmumu_PTV0_70_BFilter': {'DSID'    : 364102,
                              'events'  :7902000,
                              'red_eff' :1,
                              'sumw'    :4078710.85229,
                              'xsec'    :127.1303743},

    'Zmumu_PTV70_140_CVetoBVeto': {'DSID'    : 364103,
                                   'events'  :5917000,
                                   'red_eff' :1,
                                   'sumw'    :2143575.01278,
                                   'xsec'    :73.36940289},

    'Zmumu_PTV70_140_CFilterBVeto': {'DSID'    : 364104,
                                     'events'  :1969800,
                                     'red_eff' :1,
                                     'sumw'    :722736.703003,
                                     'xsec'    :20.90606833},

    'Zmumu_PTV70_140_BFilter': {'DSID'    : 364105,
                                'events'  :5900600,
                                'red_eff' :1,
                                'sumw'    :2053470.59226,
                                'xsec'    :12.50542972},

    'Zmumu_PTV140_280_CVetoBVeto': {'DSID'    : 364106,
                                    'events'  :4943000,
                                    'red_eff' :1,
                                    'sumw'    :2940060.231,
                                    'xsec'    :23.43735064},

    'Zmumu_PTV140_280_CFilterBVeto': {'DSID'    : 364107,
                                      'events'  :2954400,
                                      'red_eff' :1,
                                      'sumw'    :1961708.95573,
                                      'xsec'    :9.145130781},

    'Zmumu_PTV140_280_BFilter': {'DSID'    : 364108,
                                 'events'  :11924400,
                                 'red_eff' :1,
                                 'sumw'    :8276965.60895,
                                 'xsec'    :6.076989874},

    'Zmumu_PTV280_500_CVetoBVeto': {'DSID'    : 364109,
                                    'events'  :1973000,
                                    'red_eff' :1,
                                    'sumw'    :1705022.00352,
                                    'xsec'    :4.657367095},

    'Zmumu_PTV280_500_CFilterBVeto': {'DSID'    : 364110,
                                      'events'  :986000,
                                      'red_eff' :1,
                                      'sumw'    :906361.047826,
                                      'xsec'    :2.214827532},

    'Zmumu_PTV280_500_BFilter': {'DSID'    : 364111,
                                 'events'  :1971400,
                                 'red_eff' :1,
                                 'sumw'    :1854208.83636,
                                 'xsec'    :1.468357812},

    'Zmumu_PTV500_1000': {'DSID'    : 364112,
                          'events'  :2960500,
                          'red_eff' :1,
                          'sumw'    :2944710.97814,
                          'xsec'    :1.74260121},

    'Zmumu_PTV1000_E_CMS': {'DSID'    : 364113,
                            'events'  :988000,
                            'red_eff' :1,
                            'sumw'    :1007977.7298,
                            'xsec'    :0.14392476},

    'Ztautau_PTV0_70_CVetoBVeto': {'DSID'    : 364128,
                                   'events'  :7907000,
                                   'red_eff' :1,
                                   'sumw'    :5322698.33479,
                                   'xsec'    :1612.531483},

    'Ztautau_PTV0_70_CFilterBVeto': {'DSID'    : 364129,
                                     'events'  :4941000,
                                     'red_eff' :1,
                                     'sumw'    :2848153.01809,
                                     'xsec'    :211.7088872},

    'Ztautau_PTV0_70_BFilter': {'DSID'    : 364130,
                                'events'  :7890600,
                                'red_eff' :1,
                                'sumw'    :4060541.5209,
                                'xsec'    :127.0915597},

    'Ztautau_PTV70_140_CVetoBVeto': {'DSID'    : 364131,
                                     'events'  :5935500,
                                     'red_eff' :1,
                                     'sumw'    :2168444.60741,
                                     'xsec'    :74.70740605},

    'Ztautau_PTV70_140_CFilterBVeto': {'DSID'    : 364132,
                                       'events'  :1961200,
                                       'red_eff' :1,
                                       'sumw'    :717613.996532,
                                       'xsec'    :20.50813626},

    'Ztautau_PTV70_140_BFilter': {'DSID'    : 364133,
                                  'events'  :5912550,
                                  'red_eff' :1,
                                  'sumw'    :2071490.99782,
                                  'xsec'    :11.96510571},

    'Ztautau_PTV140_280_CVetoBVeto': {'DSID'    : 364134,
                                      'events'  :4956000,
                                      'red_eff' :1,
                                      'sumw'    :2969289.71879,
                                      'xsec'    :24.57266372},

    'Ztautau_PTV140_280_CFilterBVeto': {'DSID'    : 364135,
                                        'events'  :2973000,
                                        'red_eff' :1,
                                        'sumw'    :1983172.64602,
                                        'xsec'    :9.301821784},

    'Ztautau_PTV140_280_BFilter': {'DSID'    : 364136,
                                   'events'  :4932950,
                                   'red_eff' :1,
                                   'sumw'    :3430451.22731,
                                   'xsec'    :6.192971739},

    'Ztautau_PTV280_500_CVetoBVeto': {'DSID'    : 364137,
                                      'events'  :1923000,
                                      'red_eff' :1,
                                      'sumw'    :1613067.78257,
                                      'xsec'    :4.759698353},

    'Ztautau_PTV280_500_CFilterBVeto': {'DSID'    : 364138,
                                        'events'  :986000,
                                        'red_eff' :1,
                                        'sumw'    :905387.206237,
                                        'xsec'    :2.236223236},

    'Ztautau_PTV280_500_BFilter': {'DSID'    : 364139,
                                   'events'  :1974950,
                                   'red_eff' :1,
                                   'sumw'    :1853029.9701,
                                   'xsec'    :1.491840072},

    'Ztautau_PTV500_1000': {'DSID'    : 364140,
                            'events'  :2744800,
                            'red_eff' :1,
                            'sumw'    :2725664.32001,
                            'xsec'    :1.76249325},

    'Ztautau_PTV1000_E_CMS':{'DSID'    : 364141,
                             'events'  :980000,
                             'red_eff' :1,
                             'sumw'    :997974.838867,
                             'xsec'    :0.144568326},

    'ZqqZll' : {'DSID'             : 363356,
                'events'           : 5317000,
                'red_eff'          : 1,
                'sumw'             : 3439266.11559,
                'xsec'             : 2.20355112},

    'WqqZll' : {'DSID':363358,
                'events':5124000,
                'red_eff'          : 1,
                'sumw'             : 241438.72705,
                'xsec'             : 3.4328},

    'WpqqWmlv' : {'DSID':363359,
                  'events':6673000,
                  'red_eff'          : 1,
                  'sumw'             : 998250.783475,
                  'xsec'             : 24.708},

    'WplvWmqq' : {'DSID':363360,
                  'events':7115000,
                  'red_eff'          : 1,
                  'sumw'             : 1069526.41899,
                  'xsec'             : 24.724},

    'WlvZqq' : {'DSID':363489,
                'events':7100000,
                'red_eff'          : 1,
                'sumw'             : 1111991.15979,
                'xsec'             : 11.42},

    'llll' : {'DSID':363490,
              'events':17825300,
              'red_eff'          : 1,
              'sumw'             : 7538705.8077,
              'xsec'             : 1.2578},

    'lllv' : {'DSID':363491,
              'events':15772084,
              'red_eff'          : 1,
              'sumw'             : 5441475.00407,
              'xsec'             : 4.6049},

    'llvv' : {'DSID':363492,
              'events':14803000,
              'red_eff'            : 1,
              'sumw'               : 5039259.9696,
              'xsec'               : 12.466},

    'lvvv' : {'DSID':363493,
              'events':5922600,
              'red_eff'          : 1,
              'sumw'             : 1727991.07441,
              'xsec'             : 3.2286},

    'single_top_tchan': {'DSID'    : 410011,
                         'events'  : 4986200,
                         'red_eff' : 1,
                         'sumw'    : 0.218165148808,
                         'xsec'    : 44.152},

    'single_antitop_tchan': {'DSID'    : 410012,
                             'events'  : 4989800,
                             'red_eff' : 1,
                             'sumw'    : 0.128694693283,
                             'xsec'    : 26.276},

    'single_top_schan': {'DSID'    : 410025,
                         'events'  : 997800,
                         'red_eff' : 1,
                         'sumw'    : 0.00204856751068,
                         'xsec'    : 2.06121},

    'single_antitop_schan': {'DSID'    : 410026,
                             'events'  : 995400,
                             'red_eff' : 1,
                             'sumw'    : 0.00125651986173,
                             'xsec'    : 1.288662},

    'single_top_wtchan': {'DSID'    : 410013,
                          'events'  : 4985800,
                          'red_eff' : 1,
                          'sumw'    : 4865800,
                          'xsec'    : 35.845486},

    'single_antitop_wtchan': {'DSID'    : 410014,
                              'events'  : 4985600,
                              'red_eff' : 1,
                              'sumw'    : 4945600,
                              'xsec'    : 35.824406},

    'ttbar_lep': {'DSID'    : 410000,
                  'events'  : 49386600,
                  'red_eff' : 1,
                  'sumw'    : 49386600,
                  'xsec'    : 452.693559},

    'ttW':{'DSID':410155,
           'red_eff' : 1,
           'sumw':4075279.75386,
           'xsec':0.60084912},

    'ttee':{'DSID':410218,
            'red_eff': 1,
            'sumw':51968.9384584,
            'xsec':0.0412888},

    'ttmumu':{'DSID':410219,
              'red_eff':1,
              'sumw':52007.5311319,
              'xsec':0.04129216},

    # Inclusive MC
    'Wplusenu': {'DSID' : 361100,
                 'events':41870000,
                 'red_eff' : 1,
                 'sumw' : 473389396815,
                 'xsec' : 11500.4632},

    'Wplusmunu': {'DSID' : 361101,
                  'events' : 39493600,
                  'red_eff': 1,
                  'sumw' : 446507925520,
                  'xsec' : 11500.4632},

    'Wplustaunu': {'DSID' : 361102,
                   'events' : 59343600,
                   'red_eff': 1,
                   'sumw' : 670928468875,
                   'xsec' : 11500.4632},

    'Wminusenu': {'DSID' : 361103,
                  'events' : 29886000,
                  'red_eff': 1,
                  'sumw' : 247538642447,
                  'xsec' : 8579.63498},

    'Wminusmunu': {'DSID' : 361104,
                   'events' : 31915400,
                   'red_eff': 1,
                   'sumw' : 264338188182,
                   'xsec' : 8579.63498},

    'Wminustaunu': {'DSID' : 361105,
                    'events' : 19945400,
                    'red_eff': 1,
                    'sumw' : 165195850954,
                    'xsec' : 8579.63498},

    'Zee': {'DSID'    : 361106,
            'events'  : 79045597,
            'red_eff' : 1,
            'sumw'    : 150277594200,
            'xsec'    : 1950.5295},

    'Zmumu': {'DSID'    : 361107,
              'events'  : 77497800,
              'red_eff' : 1,
              'sumw'    : 147334691090,
              'xsec'    : 1950.6321},

    'Ztautau': {'DSID'    : 361108,
                'events'  : 29546000,
                'red_eff' : 1,
                'sumw'    : 56171652547.3,
                'xsec'    : 1950.6321},

    'Wenu_PTV0_70_BFilter': {'DSID'    : 364172,
                             'events'  : 17242400,
                             'red_eff' : 1,
                             'sumw'    : 10407897.8772,
                             'xsec'    : 832.203758},

    'Wenu_PTV0_70_CFilterBVeto': {'DSID'    : 364171,
                                  'events'  : 9853500,
                                  'red_eff' : 1,
                                  'sumw'    : 5647044.71225,
                                  'xsec'    : 2430.656322},

    'Wenu_PTV0_70_CVetoBVeto': {'DSID'   : 364170,
                                'events' : 24740000,
                                'red_eff': 1,
                                'sumw'   : 16615214.8608,
                                'xsec'   : 15324.216356},

    'Wenu_PTV70_140_BFilter': {'DSID'    : 364175,
                               'events'  : 9801900,
                               'red_eff' : 1,
                               'sumw'    : 3980401.78673,
                               'xsec'    : 94.875534},

    'Wenu_PTV70_140_CFilterBVeto': {'DSID'    : 364174,
                                    'events'  : 9813400,
                                    'red_eff' : 1,
                                    'sumw'    : 3714792.41865,
                                    'xsec'    : 223.63946},

    'Wenu_PTV70_140_CVetoBVeto': {'DSID'   : 364173,
                                  'events' : 14660500,
                                  'red_eff': 1,
                                  'sumw'   : 5359689.22316,
                                  'xsec'   : 618.6882},

    'Wenu_PTV140_280_BFilter': {'DSID'    : 364178,
                                'events'  : 24677800,
                                'red_eff' : 1,
                                'sumw'    : 18298138.5816,
                                'xsec'    : 35.917295},

    'Wenu_PTV140_280_CFilterBVeto': {'DSID'    : 364177,
                                     'events'  : 7410000,
                                     'red_eff' : 1,
                                     'sumw'    : 5263243.42582,
                                     'xsec'    : 96.277568},

    'Wenu_PTV140_280_CVetoBVeto': {'DSID'   : 364176,
                                   'events' : 9879000,
                                   'red_eff': 1,
                                   'sumw'   : 6159276.028,
                                   'xsec'   : 197.343129},

    'Wenu_PTV280_500_BFilter': {'DSID'    : 364181,
                                'events'  : 2958000,
                                'red_eff' : 1,
                                'sumw'    : 2835314.68179,
                                'xsec'    : 9.586345},

    'Wenu_PTV280_500_CFilterBVeto': {'DSID'    : 364180,
                                     'events'  : 2963400,
                                     'red_eff' : 1,
                                     'sumw'    : 2778654.28759,
                                     'xsec'    : 22.36999},

    'Wenu_PTV280_500_CVetoBVeto': {'DSID'   : 364179,
                                   'events' : 4923800,
                                   'red_eff': 1,
                                   'sumw'   : 4312357.01458,
                                   'xsec'   : 38.340533},

    'Wenu_PTV500_1000': {'DSID'    : 364182,
                         'events'  : 5911800,
                         'red_eff' : 1,
                         'sumw'    : 6003269.52809,
                         'xsec'    : 14.598599},

    'Wenu_PTV1000_E_CMS': {'DSID'    : 364183,
                           'events'  : 3947000,
                           'red_eff' : 1,
                           'sumw'    : 4075236.23897,
                           'xsec'    : 1.197518},

    'Wmunu_PTV0_70_BFilter': {'DSID'    : 364158,
                              'events'  : 17226200,
                              'red_eff' : 1,
                              'sumw'    : 10403012.6599,
                              'xsec'    : 828.465384},

    'Wmunu_PTV0_70_CFilterBVeto': {'DSID'    : 364157,
                                   'events'  : 9847000,
                                   'red_eff' : 1,
                                   'sumw'    : 5643599.11526,
                                   'xsec'    : 2431.204019},

    'Wmunu_PTV0_70_CVetoBVeto': {'DSID'    : 364156,
                                 'events'  : 24723000,
                                 'red_eff' : 1,
                                 'sumw'    : 16619290.3298,
                                 'xsec'    : 15317.171239},

    'Wmunu_PTV70_140_BFilter': {'DSID'    : 364161,
                                'events'  : 19639000,
                                'red_eff' : 1,
                                'sumw'    : 7990084.35926,
                                'xsec'    : 76.213179},

    'Wmunu_PTV70_140_CFilterBVeto': {'DSID'    : 364160,
                                     'events'  : 9853800,
                                     'red_eff' : 1,
                                     'sumw'    : 3693885.78953,
                                     'xsec'    : 225.006704},

    'Wmunu_PTV70_140_CVetoBVeto': {'DSID'    : 364159,
                                   'events'  : 14788000,
                                   'red_eff' : 1,
                                   'sumw'    : 5418398.88082,
                                   'xsec'    : 617.439593},

    'Wmunu_PTV140_280_BFilter': {'DSID'    : 364164,
                                 'events'  : 24585000,
                                 'red_eff' : 1,
                                 'sumw'    : 18222434.0789,
                                 'xsec'    : 36.348467},

    'Wmunu_PTV140_280_CFilterBVeto': {'DSID'    : 364163,
                                      'events'  : 7408000,
                                      'red_eff' : 1,
                                      'sumw'    : 5260811.17463,
                                      'xsec'    : 96.233222},

    'Wmunu_PTV140_280_CVetoBVeto': {'DSID'    : 364162,
                                    'events'  : 9882000,
                                    'red_eff' : 1,
                                    'sumw'    : 6155495.28527,
                                    'xsec'    : 198.635592},

    'Wmunu_PTV280_500_BFilter': {'DSID'    : 364167,
                                 'events'  : 2959500,
                                 'red_eff' : 1,
                                 'sumw'    : 2835707.22044,
                                 'xsec'    : 8.768196},

    'Wmunu_PTV280_500_CFilterBVeto': {'DSID'    : 364166,
                                      'events'  : 2958000,
                                      'red_eff' : 1,
                                      'sumw'    : 2783968.68238,
                                      'xsec'    : 22.395647},

    'Wmunu_PTV280_500_CVetoBVeto': {'DSID'    : 364165,
                                    'events'  : 4940000,
                                    'red_eff' : 1,
                                    'sumw'    : 4325283.67358,
                                    'xsec'    : 38.299835},

    'Wmunu_PTV500_1000': {'DSID'    : 364168,
                          'events'  : 5910500,
                          'red_eff' : 1,
                          'sumw'    : 5941704.99235,
                          'xsec'    : 14.558821},

    'Wmunu_PTV1000_E_CMS': {'DSID'    : 364169,
                            'events'  : 3959000,
                            'red_eff' : 1,
                            'sumw'    : 3882898.99675,
                            'xsec'    : 1.198003},

    'Wtaunu_PTV0_70_BFilter': {'DSID'    : 364186,
                               'events'  : 17273200,
                               'red_eff' : 1,
                               'sumw'    : 10498770.1084,
                               'xsec'    : 837.531038},

    'Wtaunu_PTV0_70_CFilterBVeto': {'DSID'    : 364185,
                                    'events'  : 9865600,
                                    'red_eff' : 1,
                                    'sumw'    : 5671521.55269,
                                    'xsec'    : 2443.425881},

    'Wtaunu_PTV0_70_CVetoBVeto': {'DSID'    : 364184,
                                  'events'  : 24784000,
                                  'red_eff' : 1,
                                  'sumw'    : 16726425.0218,
                                  'xsec'    : 15324.887336},

    'Wtaunu_PTV70_140_BFilter': {'DSID'    : 364189,
                                 'events'  : 9857000,
                                 'red_eff' : 1,
                                 'sumw'    : 3969118.20687,
                                 'xsec'    : 95.365521},

    'Wtaunu_PTV70_140_CFilterBVeto': {'DSID'    : 364188,
                                      'events'  : 9860000,
                                      'red_eff' : 1,
                                      'sumw'    : 3719117.16117,
                                      'xsec'    : 222.595303},

    'Wtaunu_PTV70_140_CVetoBVeto': {'DSID'    : 364187,
                                    'events'  : 14808500,
                                    'red_eff' : 1,
                                    'sumw'    : 5427023.47527,
                                    'xsec'    : 620.166885},

    'Wtaunu_PTV140_280_BFilter': {'DSID'    : 364192,
                                  'events'  : 24595900,
                                  'red_eff' : 1,
                                  'sumw'    : 7291603.73991,
                                  'xsec'    : 34.639523},

    'Wtaunu_PTV140_280_CFilterBVeto': {'DSID'    : 364191,
                                       'events'  : 7415000,
                                       'red_eff' : 1,
                                       'sumw'    : 5184365.13393,
                                       'xsec'    : 93.808553},

    'Wtaunu_PTV140_280_CVetoBVeto': {'DSID'    : 364190,
                                     'events'  : 9899000,
                                     'red_eff' : 1,
                                     'sumw'    : 6166514.76606,
                                     'xsec'    : 197.370776},

    'Wtaunu_PTV280_500_BFilter': {'DSID'    : 364195,
                                  'events'  : 2954100,
                                  'red_eff' : 1,
                                  'sumw'    : 2830341.62344,
                                  'xsec'    : 9.490847},

    'Wtaunu_PTV280_500_CFilterBVeto': {'DSID'    : 364194,
                                       'events'  : 2956400,
                                       'red_eff' : 1,
                                       'sumw'    : 2772305.06916,
                                       'xsec'    : 22.268425},

    'Wtaunu_PTV280_500_CVetoBVeto': {'DSID'    : 364193,
                                     'events'  : 4931200,
                                     'red_eff' : 1,
                                     'sumw'    : 4322848.66983,
                                     'xsec'    : 38.34009},

    'Wtaunu_PTV500_1000': {'DSID'    : 364196,
                           'events'  : 5945000,
                           'red_eff' : 1,
                           'sumw'    : 5389084.10064,
                           'xsec'    : 14.60345},

    'Wtaunu_PTV1000_E_CMS': {'DSID'    : 364197,
                             'events'  : 3946000,
                             'red_eff' : 1,
                             'sumw'    : 4057477.95297,
                             'xsec'    : 1.197324},

    'Wplusenu_1lep1tau':{'DSID':361100,
                         'events':25544800,
                         'red_eff':1,
                         'sumw':288804806460,
                         'xsec':11500.4632},

    'Wplusmunu_1lep1tau':{'DSID':361101,
                          'events':1996000,
                          'red_eff':1,
                          'sumw':22564856148.4,
                          'xsec':11500.4632},

    'Wplustaunu_1lep1tau':{'DSID':361102,
                           'events':1979400,
                           'red_eff':1,
                           'sumw':22377037617.7,
                           'xsec':11500.4632},

    'Wminusenu_1lep1tau':{'DSID':361103,
                          'events':17905400,
                          'red_eff':1,
                          'sumw':148301360014,
                          'xsec':8579.63498},

    'Wminusmunu_1lep1tau':{'DSID':361104,
                           'events':1997000,
                           'red_eff':1,
                           'sumw':16541864239.9,
                           'xsec':8579.63498},

    'Wminustaunu_1lep1tau':{'DSID':361105,
                            'events':1999800,
                            'red_eff':1,
                            'sumw':16563331847,
                            'xsec':8579.63498},

    'Zee_1lep1tau':{'DSID':361106,
                    'events':61106597,
                    'red_eff':1,
                    'sumw':116172063285,
                    'xsec':1950.5295},

    'Zmumu_1lep1tau':{'DSID':361107,
                      'events':1998400,
                      'red_eff':1,
                      'sumw':3799531630.02,
                      'xsec':1950.6321},

    'Ztautau_1lep1tau':{'DSID':361108,
                        'events':29546000,
                        'red_eff':1,
                        'sumw':56171652547.3,
                        'xsec':1950.6321},

    'ttbar_lep_1lep1tau':{'DSID':410000,
                          'events':49296600,
                          'red_eff':1,
                          'sumw':49296600,
                          'xsec':452.693559},

    'single_top_tchan_1lep1tau':{'DSID':410011,
                                 'events':1996600,
                                 'red_eff':1,
                                 'sumw':0.0873624212691,
                                 'xsec':44.152},

    'single_antitop_tchan_1lep1tau':{'DSID':410012,
                                     'events':1994200,
                                     'red_eff':1,
                                     'sumw':0.051427775374,
                                     'xsec':26.276},

    'single_top_wtchan_1lep1tau':{'DSID':410013,
                                  'events':1994200,
                                  'red_eff':1,
                                  'sumw':1994200,
                                  'xsec':35.845486},

    'single_antitop_wtchan_1lep1tau':{'DSID':410014,
                                      'events':1994000,
                                      'red_eff':1,
                                      'sumw':1994000,
                                      'xsec':35.824406},

    'single_top_schan_1lep1tau':{'DSID':410025,
                                 'events':997800,
                                 'red_eff':1,
                                 'sumw':0.00204856751068,
                                 'xsec':2.06111},

    'single_antitop_schan_1lep1tau':{'DSID':410026,
                                     'events':995400,
                                     'red_eff':1,
                                     'sumw':0.00125651986173,
                                     'xsec':1.288662},

    'Zmumu_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364100,
                                         'events':7891000,
                                         'red_eff':1,
                                         'sumw':5319367.44387,
                                         'xsec':1588.474174},

    'Zmumu_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364101,
                                           'events':4917000,
                                           'red_eff':1,
                                           'sumw':2834664.0856,
                                           'xsec':219.4826028},

    'Zmumu_PTV0_70_BFilter_1lep1tau':{'DSID':364102,
                                      'events':7902000,
                                      'red_eff':1,
                                      'sumw':4078710.85229,
                                      'xsec':127.1303743},

    'Zmumu_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364103,
                                           'events':5917000,
                                           'red_eff':1,
                                           'sumw':2143575.01278,
                                           'xsec':73.36940289},

    'Zmumu_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364104,
                                             'events':1969800,
                                             'red_eff':1,
                                             'sumw':722736.703003,
                                             'xsec':20.90606833},

    'Zmumu_PTV70_140_BFilter_1lep1tau':{'DSID':364105,
                                        'events':5900600,
                                        'red_eff':1,
                                        'sumw':2053470.59226,
                                        'xsec':12.50542972},

    'Zmumu_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364106,
                                            'events':4943000,
                                            'red_eff':1,
                                            'sumw':2940060.231,
                                            'xsec':23.43735064},

    'Zmumu_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364107,
                                              'events':2954400,
                                              'red_eff':1,
                                              'sumw':1961708.95573,
                                              'xsec':9.145130781},

    'Zmumu_PTV140_280_BFilter_1lep1tau':{'DSID':364108,
                                         'events':4942300,
                                         'red_eff':1,
                                         'sumw':3441102.46707,
                                         'xsec':6.076989874},

    'Zmumu_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364109,
                                            'events':1973000,
                                            'red_eff':1,
                                            'sumw':1705022.00352,
                                            'xsec':4.657367095},

    'Zmumu_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364110,
                                              'events':986000,
                                              'red_eff':1,
                                              'sumw':906361.047826,
                                              'xsec':2.214827532},

    'Zmumu_PTV280_500_BFilter_1lep1tau':{'DSID':364111,
                                         'events':1971400,
                                         'red_eff':1,
                                         'sumw':1854208.83636,
                                         'xsec':1.468357812},

    'Zmumu_PTV500_1000_1lep1tau':{'DSID':364112,
                                  'events':2960500,
                                  'red_eff':1,
                                  'sumw':2944710.97814,
                                  'xsec':1.74260121},

    'Zmumu_PTV1000_E_CMS_1lep1tau':{'DSID':364113,
                                    'events':988000,
                                    'red_eff':1,
                                    'sumw':1007977.7298,
                                    'xsec':0.14392476},

    'Zee_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364114,
                                       'events':7900000,
                                       'red_eff':1,
                                       'sumw':5307644.52827,
                                       'xsec':1587.021595},
    'Zee_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364115,
                                         'events':4940500,
                                         'red_eff':1,
                                         'sumw':2839137.81561,
                                         'xsec':219.9958116},
    'Zee_PTV0_70_BFilter_1lep1tau':{'DSID':364116,
                                    'events':7883600,
                                    'red_eff':1,
                                    'sumw':4053053.52848,
                                    'xsec':127.0857614},
    'Zee_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364117,
                                         'events':5925000,
                                         'red_eff':1,
                                         'sumw':2164248.98844,
                                         'xsec':74.90381742},
    'Zee_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364118,
                                           'events':1972600,
                                           'red_eff':1,
                                           'sumw':715162.089738,
                                           'xsec':20.3159891},
    'Zee_PTV70_140_BFilter_1lep1tau':{'DSID':364119,
                                      'events':5855000,
                                      'red_eff':1,
                                      'sumw':2043192.28295,
                                      'xsec':12.73880801},
    'Zee_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364120,
                                          'events':4949000,
                                          'red_eff':1,
                                          'sumw':2966342.61469,
                                          'xsec':24.44184978},
    'Zee_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364121,
                                            'events':2962600,
                                            'red_eff':1,
                                            'sumw':1976624.57582,
                                            'xsec':9.237605979},
    'Zee_PTV140_280_BFilter_1lep1tau':{'DSID':364122,
                                       'events':4890000,
                                       'red_eff':1,
                                       'sumw':3396476.98264,
                                       'xsec':6.081254464},
    'Zee_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364123,
                                          'events':1882800,
                                          'red_eff':1,
                                          'sumw':1622207.75969,
                                          'xsec':4.796836771},
    'Zee_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364124,
                                            'events':988900,
                                            'red_eff':1,
                                            'sumw':908261.497964,
                                            'xsec':2.249186051},
    'Zee_PTV280_500_BFilter_1lep1tau':{'DSID':364125,
                                       'events':1976850,
                                       'red_eff':1,
                                       'sumw':1854184.55614,
                                       'xsec':1.49219843},
    'Zee_PTV500_1000_1lep1tau':{'DSID':364126,
                                'events':2973000,
                                'red_eff':1,
                                'sumw':2942740.91362,
                                'xsec':1.76415092},
    'Zee_PTV1000_E_CMS_1lep1tau':{'DSID':364127,
                                  'events':978000,
                                  'red_eff':1,
                                  'sumw':994142.027341,
                                  'xsec':0.145046125},

    'Ztautau_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364128,
                                           'events':7817000,
                                           'red_eff':1,
                                           'sumw':5261983.52635,
                                           'xsec':1612.531483},

    'Ztautau_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364129,
                                             'events':4941000,
                                             'red_eff':1,
                                             'sumw':2848153.01809,
                                             'xsec':211.7088872},

    'Ztautau_PTV0_70_BFilter_1lep1tau':{'DSID':364130,
                                        'events':7890600,
                                        'red_eff':1,
                                        'sumw':4060541.5209,
                                        'xsec':127.0915597},

    'Ztautau_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364131,
                                             'events':5935500,
                                             'red_eff':1,
                                             'sumw':2168444.60741,
                                             'xsec':74.70740605},

    'Ztautau_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364132,
                                               'events':1961200,
                                               'red_eff':1,
                                               'sumw':717613.996532,
                                               'xsec':20.50813626},

    'Ztautau_PTV70_140_BFilter_1lep1tau':{'DSID':364133,
                                          'events':5912550,
                                          'red_eff':1,
                                          'sumw':2071490.99782,
                                          'xsec':11.96510571},

    'Ztautau_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364134,
                                              'events':4956000,
                                              'red_eff':1,
                                              'sumw':2969289.71879,
                                              'xsec':24.57266372},

    'Ztautau_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364135,
                                                'events':2973000,
                                                'red_eff':1,
                                                'sumw':1983172.64602,
                                                'xsec':9.301821784},

    'Ztautau_PTV140_280_BFilter_1lep1tau':{'DSID':364136,
                                           'events':4932950,
                                           'red_eff':1,
                                           'sumw':3430451.22731,
                                           'xsec':6.192971739},

    'Ztautau_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364137,
                                              'events':1973000,
                                              'red_eff':1,
                                              'sumw':1656090.74518,
                                              'xsec':4.759698353},

    'Ztautau_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364138,
                                                'events':986000,
                                                'red_eff':1,
                                                'sumw':905387.206237,
                                                'xsec':2.236223236},

    'Ztautau_PTV280_500_BFilter_1lep1tau':{'DSID':364139,
                                           'events':1974950,
                                           'red_eff':1,
                                           'sumw':1853029.9701,
                                           'xsec':1.491840072},

    'Ztautau_PTV500_1000_1lep1tau':{'DSID':364140,
                                    'events':2944800,
                                    'red_eff':1,
                                    'sumw':2923750.21933,
                                    'xsec':1.76249325},

    'Ztautau_PTV1000_E_CMS_1lep1tau':{'DSID':364141,
                                      'events':980000,
                                      'red_eff':1,
                                      'sumw':997974.838867,
                                      'xsec':0.144568326},

    'Wmunu_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364156,
                                         'events':24723000,
                                         'red_eff':1,
                                         'sumw':16619290.3298,
                                         'xsec':15317.171239},
    'Wmunu_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364157,
                                           'events':9847000,
                                           'red_eff':1,
                                           'sumw':5643599.11526,
                                           'xsec':2431.204019},
    'Wmunu_PTV0_70_BFilter_1lep1tau':{'DSID':364158,
                                      'events':17226200,
                                      'red_eff':1,
                                      'sumw':10403012.6599,
                                      'xsec':828.465384},
    'Wmunu_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364159,
                                           'events':14788000,
                                           'red_eff':1,
                                           'sumw':5418398.88082,
                                           'xsec':617.439593},
    'Wmunu_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364160,
                                             'events':9853800,
                                             'red_eff':1,
                                             'sumw':3693885.78953,
                                             'xsec':225.006704},
    'Wmunu_PTV70_140_BFilter_1lep1tau':{'DSID':364161,
                                        'events':19639000,
                                        'red_eff':1,
                                        'sumw':7990084.35926,
                                        'xsec':76.213179},
    'Wmunu_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364162,
                                            'events':9882000,
                                            'red_eff':1,
                                            'sumw':6155495.28527,
                                            'xsec':198.635592},
    'Wmunu_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364163,
                                              'events':7408000,
                                              'red_eff':1,
                                              'sumw':5260811.17463,
                                              'xsec':96.233222},
    'Wmunu_PTV140_280_BFilter_1lep1tau':{'DSID':364164,
                                         'events':9826000,
                                         'red_eff':1,
                                         'sumw':7271557.26566,
                                         'xsec':36.348467},
    'Wmunu_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364165,
                                            'events':4940000,
                                            'red_eff':1,
                                            'sumw':4325283.67358,
                                            'xsec':38.299835},
    'Wmunu_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364166,
                                              'events':2958000,
                                              'red_eff':1,
                                              'sumw':2783968.68238,
                                              'xsec':22.395647},
    'Wmunu_PTV280_500_BFilter_1lep1tau':{'DSID':364167,
                                         'events':2959500,
                                         'red_eff':1,
                                         'sumw':2835707.22044,
                                         'xsec':8.768196},
    'Wmunu_PTV500_1000_1lep1tau':{'DSID':364168,
                                  'events':5910500,
                                  'red_eff':1,
                                  'sumw':5941704.99235,
                                  'xsec':14.558821},
    'Wmunu_PTV1000_E_CMS_1lep1tau':{'DSID':364169,
                                    'events':3959000,
                                    'red_eff':1,
                                    'sumw':4068015.22447,
                                    'xsec':1.198003},

    'Wenu_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364170,
                                        'events':24740000,
                                        'red_eff':1,
                                        'sumw':16615214.8608,
                                        'xsec':15324.216356},

    'Wenu_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364171,
                                          'events':9853500,
                                          'red_eff':1,
                                          'sumw':5647044.71225,
                                          'xsec':2430.656322},

    'Wenu_PTV0_70_BFilter_1lep1tau':{'DSID':364172,
                                     'events':17242400,
                                     'red_eff':1,
                                     'sumw':10407897.8772,
                                     'xsec':832.203758},

    'Wenu_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364173,
                                          'events':13950500,
                                          'red_eff':1,
                                          'sumw':5098540.19503,
                                          'xsec':618.6882},

    'Wenu_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364174,
                                            'events':9678400,
                                            'red_eff':1,
                                            'sumw':3661915.17878,
                                            'xsec':223.63946},

    'Wenu_PTV70_140_BFilter_1lep1tau':{'DSID':364175,
                                       'events':9801900,
                                       'red_eff':1,
                                       'sumw':3980401.78673,
                                       'xsec':94.875534},

    'Wenu_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364176,
                                           'events':9819000,
                                           'red_eff':1,
                                           'sumw':6121546.03361,
                                           'xsec':197.343129},

    'Wenu_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364177,
                                             'events':7410000,
                                             'red_eff':1,
                                             'sumw':5263243.42582,
                                             'xsec':96.277568},

    'Wenu_PTV140_280_BFilter_1lep1tau':{'DSID':364178,
                                        'events':9880900,
                                        'red_eff':1,
                                        'sumw':7327201.08884,
                                        'xsec':35.917295},

    'Wenu_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364179,
                                           'events':4923800,
                                           'red_eff':1,
                                           'sumw':4312357.01458,
                                           'xsec':38.340533},

    'Wenu_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364180,
                                             'events':2963400,
                                             'red_eff':1,
                                             'sumw':2778654.28759,
                                             'xsec':22.36999},

    'Wenu_PTV280_500_BFilter_1lep1tau':{'DSID':364181,
                                        'events':2958000,
                                        'red_eff':1,
                                        'sumw':2835314.68179,
                                        'xsec':9.586345},

    'Wenu_PTV500_1000_1lep1tau':{'DSID':364182,
                                 'events':5916800,
                                 'red_eff':1,
                                 'sumw':6003269.52809,
                                 'xsec':14.598599},

    'Wenu_PTV1000_E_CMS_1lep1tau':{'DSID':364183,
                                   'events':3947000,
                                   'red_eff':1,
                                   'sumw':4075236.23897,
                                   'xsec':1.197518},

    'Wtaunu_PTV0_70_CVetoBVeto_1lep1tau':{'DSID':364184,
                                          'events':17674000,
                                          'red_eff':1,
                                          'sumw':11929044.1188,
                                          'xsec':15324.887336},

    'Wtaunu_PTV0_70_CFilterBVeto_1lep1tau':{'DSID':364185,
                                            'events':9865600,
                                            'red_eff':1,
                                            'sumw':5671521.55269,
                                            'xsec':2443.425881},

    'Wtaunu_PTV0_70_BFilter_1lep1tau':{'DSID':364186,
                                       'events':17273200,
                                       'red_eff':1,
                                       'sumw':10498770.1084,
                                       'xsec':837.531038},

    'Wtaunu_PTV70_140_CVetoBVeto_1lep1tau':{'DSID':364187,
                                            'events':14808500,
                                            'red_eff':1,
                                            'sumw':5427023.47527,
                                            'xsec':620.166885},

    'Wtaunu_PTV70_140_CFilterBVeto_1lep1tau':{'DSID':364188,
                                              'events':9860000,
                                              'red_eff':1,
                                              'sumw':3719117.16117,
                                              'xsec':222.595303},

    'Wtaunu_PTV70_140_BFilter_1lep1tau':{'DSID':364189,
                                         'events':9857000,
                                         'red_eff':1,
                                         'sumw':3969118.20687,
                                         'xsec':95.365521},

    'Wtaunu_PTV140_280_CVetoBVeto_1lep1tau':{'DSID':364190,
                                             'events':9899000,
                                             'red_eff':1,
                                             'sumw':6166514.76606,
                                             'xsec':197.370776},

    'Wtaunu_PTV140_280_CFilterBVeto_1lep1tau':{'DSID':364191,
                                               'events':7175000,
                                               'red_eff':1,
                                               'sumw':5085280.31607,
                                               'xsec':93.808553},

    'Wtaunu_PTV140_280_BFilter_1lep1tau':{'DSID':364192,
                                          'events':9834000,
                                          'red_eff':1,
                                          'sumw':7291603.73991,
                                          'xsec':34.639523},

    'Wtaunu_PTV280_500_CVetoBVeto_1lep1tau':{'DSID':364193,
                                             'events':4931200,
                                             'red_eff':1,
                                             'sumw':4322848.66983,
                                             'xsec':38.34009},

    'Wtaunu_PTV280_500_CFilterBVeto_1lep1tau':{'DSID':364194,
                                               'events':2956400,
                                               'red_eff':1,
                                               'sumw':2772305.06916,
                                               'xsec':22.268425},

    'Wtaunu_PTV280_500_BFilter_1lep1tau':{'DSID':364195,
                                          'events':2954100,
                                          'red_eff':1,
                                          'sumw':2830341.62344,
                                          'xsec':9.490847},

    'Wtaunu_PTV500_1000_1lep1tau':{'DSID':364196,
                                   'events':5895000,
                                   'red_eff':1,
                                   'sumw':5932750.60186,
                                   'xsec':14.60345},

    'Wtaunu_PTV1000_E_CMS_1lep1tau':{'DSID':364197,
                                     'events':3946000,
                                     'red_eff':1,
                                     'sumw':4057477.95297,
                                     'xsec':1.197324},

    'ttbar_lep_1largeRjet1lep':{'DSID':410000,
                                'events':49386600,
                                'red_eff':1,
                                'sumw':4938660,
                                'xsec':452.693559},

    'single_top_tchan_1largeRjet1lep':{'DSID':410011,
                                       'events':4986200,
                                       'red_eff':1,
                                       'sumw':0.218165148808,
                                       'xsec':44.152},

    'single_antitop_tchan_1largeRjet1lep':{'DSID':410012,
                                           'events':4989800,
                                           'red_eff':1,
                                           'sumw':0.128694693283,
                                           'xsec':26.276},

    'single_top_wtchan_1largeRjet1lep':{'DSID':410013,
                                        'events':4985800,
                                        'red_eff':1,
                                        'sumw':4985800,
                                        'xsec':35.845486},

    'single_antitop_wtchan_1largeRjet1lep':{'DSID':410014,
                                            'events':4985600,
                                            'red_eff':1,
                                            'sumw':4985600,
                                            'xsec':35.824406},

    'single_top_schan_1largeRjet1lep':{'DSID':410025,
                                       'events':997800,
                                       'red_eff':1,
                                       'sumw':0.00204856751068,
                                       'xsec':2.06111},

    'single_antitop_schan_1largeRjet1lep':{'DSID':410026,
                                           'events':220000,
                                           'red_eff':1,
                                           'sumw':0.000277829987565,
                                           'xsec':1.288662},

    'Zmumu0_70CVetoBVeto_1largeRjet1lep':{'DSID':364100,
                                          'events':7891000,
                                          'red_eff':1,
                                          'sumw':5319367.44387,
                                          'xsec':1588.474174},

    'Zmumu0_70CFilterBVeto_1largeRjet1lep':{'DSID':364101,
                                            'events':4917000,
                                            'red_eff':1,
                                            'sumw':2834664.0856,
                                            'xsec':219.4826028},

    'Zmumu0_70BFilter_1largeRjet1lep':{'DSID':364102,
                                       'events':7902000,
                                       'red_eff':1,
                                       'sumw':4078710.85229,
                                       'xsec':127.1303743},

    'Zmumu70_140CVetoBVeto_1largeRjet1lep':{'DSID':364103,
                                            'events':5917000,
                                            'red_eff':1,
                                            'sumw':2143575.01278,
                                            'xsec':73.36940289},

    'Zmumu70_140CFilterBVeto_1largeRjet1lep':{'DSID':364104,
                                              'events':1969800,
                                              'red_eff':1,
                                              'sumw':722736.703003,
                                              'xsec':20.90606833},

    'Zmumu70_140BFilter_1largeRjet1lep':{'DSID':364105,
                                         'events':5900600,
                                         'red_eff':1,
                                         'sumw':2053470.59226,
                                         'xsec':12.50542972},

    'Zmumu140_280CVetoBVeto_1largeRjet1lep':{'DSID':364106,
                                             'events':4943000,
                                             'red_eff':1,
                                             'sumw':2940060.231,
                                             'xsec':23.43735064},

    'Zmumu140_280CFilterBVeto_1largeRjet1lep':{'DSID':364107,
                                               'events':2954400,
                                               'red_eff':1,
                                               'sumw':1961708.95573,
                                               'xsec':9.145130781},

    'Zmumu140_280BFilter_1largeRjet1lep':{'DSID':364108,
                                          'events':12339300,
                                          'red_eff':1,
                                          'sumw':8563701.72954,
                                          'xsec':6.076989874},

    'Zmumu280_500CVetoBVeto_1largeRjet1lep':{'DSID':364109,
                                             'events':1973000,
                                             'red_eff':1,
                                             'sumw':1705022.00352,
                                             'xsec':4.657367095},

    'Zmumu280_500CFilterBVeto_1largeRjet1lep':{'DSID':364110,
                                               'events':986000,
                                               'red_eff':1,
                                               'sumw':906361.047826,
                                               'xsec':2.214827532},

    'Zmumu280_500BFilter_1largeRjet1lep':{'DSID':364111,
                                          'events':1971400,
                                          'red_eff':1,
                                          'sumw':1854208.83636,
                                          'xsec':1.468357812},

    'Zmumu500_1000_1largeRjet1lep':{'DSID':364112,
                                    'events':1,
                                    'red_eff':1,
                                    'sumw':2944710.97814,
                                    'xsec':1.74260121},

    'Zmumu1000_1largeRjet1lep':{'DSID':364113,
                                'events':988000,
                                'red_eff':1,
                                'sumw':1007977.7298,
                                'xsec':0.14392476},

    'Zee_PTV0_70_CVetoBVeto_1largeRjet1lep':{'DSID':364114,
                                             'events':6850000,
                                             'red_eff':1,
                                             'sumw':5307644.52827,
                                             'xsec':1587.021595},
    'Zee_PTV0_70_CFilterBVeto_1largeRjet1lep':{'DSID':364115,
                                               'events':4940500,
                                               'red_eff':1,
                                               'sumw':2839137.81561,
                                               'xsec':219.9958116},
    'Zee_PTV0_70_BFilter_1largeRjet1lep':{'DSID':364116,
                                          'events':7883600,
                                          'red_eff':1,
                                          'sumw':4053053.52848,
                                          'xsec':127.0857614},
    'Zee_PTV70_140_CVetoBVeto_1largeRjet1lep':{'DSID':364117,
                                               'events':5925000,
                                               'red_eff':1,
                                               'sumw':2164248.98844,
                                               'xsec':74.90381742},
    'Zee_PTV70_140_CFilterBVeto_1largeRjet1lep':{'DSID':364118,
                                                 'events':1972600,
                                                 'red_eff':1,
                                                 'sumw':715162.089738,
                                                 'xsec':20.3159891},
    'Zee_PTV70_140_BFilter_1largeRjet1lep':{'DSID':364119,
                                            'events':1,
                                            'red_eff':1,
                                            'sumw':2043192.28295,
                                            'xsec':12.73880801},
    'Zee_PTV140_280_CVetoBVeto_1largeRjet1lep':{'DSID':364120,
                                                'events':4949000,
                                                'red_eff':1,
                                                'sumw':2966342.61469,
                                                'xsec':24.44184978},
    'Zee_PTV140_280_CFilterBVeto_1largeRjet1lep':{'DSID':364121,
                                                  'events':2962600,
                                                  'red_eff':1,
                                                  'sumw':1976624.57582,
                                                  'xsec':9.237605979},
    'Zee_PTV140_280_BFilter_1largeRjet1lep':{'DSID':364122,
                                             'events':4800000,
                                             'red_eff':1,
                                             'sumw':3338606.00232,
                                             'xsec':6.081254464},
    'Zee_PTV280_500_CVetoBVeto_1largeRjet1lep':{'DSID':364123,
                                                'events':1932800,
                                                'red_eff':1,
                                                'sumw':1665734.2346,
                                                'xsec':4.796836771},
    'Zee_PTV280_500_CFilterBVeto_1largeRjet1lep':{'DSID':364124,
                                                  'events':988900,
                                                  'red_eff':1,
                                                  'sumw':908261.497964,
                                                  'xsec':2.249186051},
    'Zee_PTV280_500_BFilter_1largeRjet1lep':{'DSID':364125,
                                             'events':1976850,
                                             'red_eff':1,
                                             'sumw':1854184.55614,
                                             'xsec':1.49219843},
    'Zee_PTV500_1000_1largeRjet1lep':{'DSID':364126,
                                      'events':2973000,
                                      'red_eff':1,
                                      'sumw':2942740.91362,
                                      'xsec':1.76415092},
    'Zee_PTV1000_E_CMS_1largeRjet1lep':{'DSID':364127,
                                        'events':988000,
                                        'red_eff':1,
                                        'sumw':1004312.18015,
                                        'xsec':0.145046125},

    'Ztautau_PTV0_70_CVetoBVeto_1largeRjet1lep':{'DSID':364128,
                                                 'events':7907000,
                                                 'red_eff':1,
                                                 'sumw':5322698.33479,
                                                 'xsec':1612.531483},

    'Ztautau_PTV0_70_CFilterBVeto_1largeRjet1lep':{'DSID':364129,
                                                   'events':4941000,
                                                   'red_eff':1,
                                                   'sumw':2848153.01809,
                                                   'xsec':211.7088872},

    'Ztautau_PTV0_70_BFilter_1largeRjet1lep':{'DSID':364130,
                                              'events':7890600,
                                              'red_eff':1,
                                              'sumw':4060541.5209,
                                              'xsec':127.0915597},

    'Ztautau_PTV70_140_CVetoBVeto_1largeRjet1lep':{'DSID':364131,
                                                   'events':5935500,
                                                   'red_eff':1,
                                                   'sumw':2168444.60741,
                                                   'xsec':74.70740605},

    'Ztautau_PTV70_140_CFilterBVeto_1largeRjet1lep':{'DSID':364132,
                                                     'events':1961200,
                                                     'red_eff':1,
                                                     'sumw':717613.996532,
                                                     'xsec':20.50813626},

    'Ztautau_PTV70_140_BFilter_1largeRjet1lep':{'DSID':364133,
                                                'events':5912550,
                                                'red_eff':1,
                                                'sumw':2071490.99782,
                                                'xsec':11.96510571},

    'Ztautau_PTV140_280_CVetoBVeto_1largeRjet1lep':{'DSID':364134,
                                                    'events':4296000,
                                                    'red_eff':1,
                                                    'sumw':2574043.5746,
                                                    'xsec':24.57266372},

    'Ztautau_PTV140_280_CFilterBVeto_1largeRjet1lep':{'DSID':364135,
                                                      'events':2973000,
                                                      'red_eff':1,
                                                      'sumw':1983172.64602,
                                                      'xsec':9.301821784},

    'Ztautau_PTV140_280_BFilter_1largeRjet1lep':{'DSID':364136,
                                                 'events':4932950,
                                                 'red_eff':1,
                                                 'sumw':3430451.22731,
                                                 'xsec':6.192971739},

    'Ztautau_PTV280_500_CVetoBVeto_1largeRjet1lep':{'DSID':364137,
                                                    'events':1973000,
                                                    'red_eff':1,
                                                    'sumw':1656090.74518,
                                                    'xsec':4.759698353},

    'Ztautau_PTV280_500_CFilterBVeto_1largeRjet1lep':{'DSID':364138,
                                                      'events':986000,
                                                      'red_eff':1,
                                                      'sumw':905387.206237,
                                                      'xsec':2.236223236},

    'Ztautau_PTV280_500_BFilter_1largeRjet1lep':{'DSID':364139,
                                                 'events':1974950,
                                                 'red_eff':1,
                                                 'sumw':1853029.9701,
                                                 'xsec':1.491840072},

    'Ztautau_PTV500_1000_1largeRjet1lep':{'DSID':364140,
                                          'events':2944800,
                                          'red_eff':1,
                                          'sumw':2923750.21933,
                                          'xsec':1.76249325},

    'Ztautau_PTV1000_E_CMS_1largeRjet1lep':{'DSID':364141,
                                            'events':980000,
                                            'red_eff':1,
                                            'sumw':997974.838867,
                                            'xsec':0.144568326},

    'Wmunu_PTV0_70_CVetoBVeto_1largeRjet1lep':{'DSID':364156,
                                               'events':24723000,
                                               'red_eff':1,
                                               'sumw':16619290.3298,
                                               'xsec':15317.171239},
    'Wmunu_PTV0_70_CFilterBVeto_1largeRjet1lep':{'DSID':364157,
                                                 'events':9847000,
                                                 'red_eff':1,
                                                 'sumw':5643599.11526,
                                                 'xsec':2431.204019},
    'Wmunu_PTV0_70_BFilter_1largeRjet1lep':{'DSID':364158,
                                            'events':17226200,
                                            'red_eff':1,
                                            'sumw':10403012.6599,
                                            'xsec':828.465384},
    'Wmunu_PTV70_140_CVetoBVeto_1largeRjet1lep':{'DSID':364159,
                                                 'events':14788000,
                                                 'red_eff':1,
                                                 'sumw':5418398.88082,
                                                 'xsec':617.439593},
    'Wmunu_PTV70_140_CFilterBVeto_1largeRjet1lep':{'DSID':364160,
                                                   'events':9853800,
                                                   'red_eff':1,
                                                   'sumw':3693885.78953,
                                                   'xsec':225.006704},
    'Wmunu_PTV70_140_BFilter_1largeRjet1lep':{'DSID':364161,
                                              'events':19639000,
                                              'red_eff':1,
                                              'sumw':7990084.35926,
                                              'xsec':76.213179},
    'Wmunu_PTV140_280_CVetoBVeto_1largeRjet1lep':{'DSID':364162,
                                                  'events':9882000,
                                                  'red_eff':1,
                                                  'sumw':6155495.28527,
                                                  'xsec':198.635592},
    'Wmunu_PTV140_280_CFilterBVeto_1largeRjet1lep':{'DSID':364163,
                                                    'events':7408000,
                                                    'red_eff':1,
                                                    'sumw':5260811.17463,
                                                    'xsec':96.233222},
    'Wmunu_PTV140_280_BFilter_1largeRjet1lep':{'DSID':364164,
                                               'events':24585000,
                                               'red_eff':1,
                                               'sumw':18222434.0789,
                                               'xsec':36.348467},
    'Wmunu_PTV280_500_CVetoBVeto_1largeRjet1lep':{'DSID':364165,
                                                  'events':4940000,
                                                  'red_eff':1,
                                                  'sumw':4325283.67358,
                                                  'xsec':38.299835},
    'Wmunu_PTV280_500_CFilterBVeto_1largeRjet1lep':{'DSID':364166,
                                                    'events':2958000,
                                                    'red_eff':1,
                                                    'sumw':2783968.68238,
                                                    'xsec':22.395647},
    'Wmunu_PTV280_500_BFilter_1largeRjet1lep':{'DSID':364167,
                                               'events':2919500,
                                               'red_eff':1,
                                               'sumw':2797023.37969,
                                               'xsec':8.768196},
    'Wmunu_PTV500_1000_1largeRjet1lep':{'DSID':364168,
                                        'events':5910500,
                                        'red_eff':1,
                                        'sumw':5941704.99235,
                                        'xsec':14.558821},
    'Wmunu_PTV1000_E_CMS_1largeRjet1lep':{'DSID':364169,
                                          'events':3959000,
                                          'red_eff':1,
                                          'sumw':4068015.22447,
                                          'xsec':1.198003},

    'Wenu_PTV0_70_CVetoBVeto_1largeRjet1lep':{'DSID':364170,
                                              'events':24740000,
                                              'red_eff':1,
                                              'sumw':16615214.8608,
                                              'xsec':15324.216356},

    'Wenu_PTV0_70_CFilterBVeto_1largeRjet1lep':{'DSID':364171,
                                                'events':9853500,
                                                'red_eff':1,
                                                'sumw':5647044.71225,
                                                'xsec':2430.656322},

    'Wenu_PTV0_70_BFilter_1largeRjet1lep':{'DSID':364172,
                                           'events':17242400,
                                           'red_eff':1,
                                           'sumw':10407897.8772,
                                           'xsec':832.203758},

    'Wenu_PTV70_140_CVetoBVeto_1largeRjet1lep':{'DSID':364173,
                                                'events':14660500,
                                                'red_eff':1,
                                                'sumw':5359689.22316,
                                                'xsec':618.6882},

    'Wenu_PTV70_140_CFilterBVeto_1largeRjet1lep':{'DSID':364174,
                                                  'events':9818400,
                                                  'red_eff':1,
                                                  'sumw':3714792.41865,
                                                  'xsec':223.63946},

    'Wenu_PTV70_140_BFilter_1largeRjet1lep':{'DSID':364175,
                                             'events':5401900,
                                             'red_eff':1,
                                             'sumw':2194437.53008,
                                             'xsec':94.875534},

    'Wenu_PTV140_280_CVetoBVeto_1largeRjet1lep':{'DSID':364176,
                                                 'events':9879000,
                                                 'red_eff':1,
                                                 'sumw':6159276.028,
                                                 'xsec':197.343129},

    'Wenu_PTV140_280_CFilterBVeto_1largeRjet1lep':{'DSID':364177,
                                                   'events':7360000,
                                                   'red_eff':1,
                                                   'sumw':5227943.44514,
                                                   'xsec':96.277568},

    'Wenu_PTV140_280_BFilter_1largeRjet1lep':{'DSID':364178,
                                              'events':24677800,
                                              'red_eff':1,
                                              'sumw':18298138.5816,
                                              'xsec':35.917295},

    'Wenu_PTV280_500_CVetoBVeto_1largeRjet1lep':{'DSID':364179,
                                                 'events':4923800,
                                                 'red_eff':1,
                                                 'sumw':4312357.01458,
                                                 'xsec':38.340533},

    'Wenu_PTV280_500_CFilterBVeto_1largeRjet1lep':{'DSID':364180,
                                                   'events':2963400,
                                                   'red_eff':1,
                                                   'sumw':2778654.28759,
                                                   'xsec':22.36999},

    'Wenu_PTV280_500_BFilter_1largeRjet1lep':{'DSID':364181,
                                              'events':2958000,
                                              'red_eff':1,
                                              'sumw':2835314.68179,
                                              'xsec':9.586345},

    'Wenu_PTV500_1000_1largeRjet1lep':{'DSID':364182,
                                       'events':5911800,
                                       'red_eff':1,
                                       'sumw':5998269.59452,
                                       'xsec':14.598599},

    'Wenu_PTV1000_E_CMS_1largeRjet1lep':{'DSID':364183,
                                         'events':3947000,
                                         'red_eff':1,
                                         'sumw':4075236.23897,
                                         'xsec':1.197518},

    'Wtaunu_PTV0_70_CVetoBVeto_1largeRjet1lep':{'DSID':364184,
                                                'events':24784000,
                                                'red_eff':1,
                                                'sumw':16726425.0218,
                                                'xsec':15324.887336},

    'Wtaunu_PTV0_70_CFilterBVeto_1largeRjet1lep':{'DSID':364185,
                                                  'events':9865600,
                                                  'red_eff':1,
                                                  'sumw':5671521.55269,
                                                  'xsec':2443.425881},

    'Wtaunu_PTV0_70_BFilter_1largeRjet1lep':{'DSID':364186,
                                             'events':17273200,
                                             'red_eff':1,
                                             'sumw':10498770.1084,
                                             'xsec':837.531038},

    'Wtaunu_PTV70_140_CVetoBVeto_1largeRjet1lep':{'DSID':364187,
                                                  'events':14808500,
                                                  'red_eff':1,
                                                  'sumw':5427023.47527,
                                                  'xsec':620.166885},

    'Wtaunu_PTV70_140_CFilterBVeto_1largeRjet1lep':{'DSID':364188,
                                                    'events':9270000,
                                                    'red_eff':1,
                                                    'sumw':3494336.03082,
                                                    'xsec':222.595303},

    'Wtaunu_PTV70_140_BFilter_1largeRjet1lep':{'DSID':364189,
                                               'events':9857000,
                                               'red_eff':1,
                                               'sumw':3969118.20687,
                                               'xsec':95.365521},

    'Wtaunu_PTV140_280_CVetoBVeto_1largeRjet1lep':{'DSID':364190,
                                                   'events':9899000,
                                                   'red_eff':1,
                                                   'sumw':6166514.76606,
                                                   'xsec':197.370776},

    'Wtaunu_PTV140_280_CFilterBVeto_1largeRjet1lep':{'DSID':364191,
                                                     'events':7405000,
                                                     'red_eff':1,
                                                     'sumw':5248104.98519,
                                                     'xsec':93.808553},

    'Wtaunu_PTV140_280_BFilter_1largeRjet1lep':{'DSID':364192,
                                                'events':24819900,
                                                'red_eff':1,
                                                'sumw':18407605.7617,
                                                'xsec':34.639523},

    'Wtaunu_PTV280_500_CVetoBVeto_1largeRjet1lep':{'DSID':364193,
                                                   'events':4931200,
                                                   'red_eff':1,
                                                   'sumw':4322848.66983,
                                                   'xsec':38.34009},

    'Wtaunu_PTV280_500_CFilterBVeto_1largeRjet1lep':{'DSID':364194,
                                                     'events':2956400,
                                                     'red_eff':1,
                                                     'sumw':2772305.06916,
                                                     'xsec':22.268425},

    'Wtaunu_PTV280_500_BFilter_1largeRjet1lep':{'DSID':364195,
                                                'events':2954100,
                                                'red_eff':1,
                                                'sumw':2830341.62344,
                                                'xsec':9.490847},

    'Wtaunu_PTV500_1000_1largeRjet1lep':{'DSID':364196,
                                         'events':5945000,
                                         'red_eff':1,
                                         'sumw':5983038.9473,
                                         'xsec':14.60345},

    'Wtaunu_PTV1000_E_CMS_1largeRjet1lep':{'DSID':364197,
                                           'events':3946000,
                                           'red_eff':1,
                                           'sumw':4057477.95297,
                                           'xsec':1.197324},

    # gluino-gluino -> stop-stop -> tttt + DM

    'GG_ttn1_1200_5000_1_1largeRjet1lep': {'DSID'    : 370114,
                                           'events'  : 100000,
                                           'red_eff' : 1,
                                           'sumw'    : 101591.347734,
                                           'xsec'    : 0.057037},

    'GG_ttn1_1200_5000_600_1largeRjet1lep': {'DSID'    : 370118,
                                             'events'  : 100000,
                                             'red_eff' : 1,
                                             'sumw'    : 101591.282303,
                                             'xsec'    : 0.057002},

    'GG_ttn1_1400_5000_1_1largeRjet1lep': {'DSID'    : 370129,
                                           'events'  : 100000,
                                           'red_eff' : 1,
                                           'sumw'    : 101197.830825,
                                           'xsec'    : 0.015756},

    'GG_ttn1_1600_5000_1_1largeRjet1lep': {'DSID'    : 370144,
                                           'events':199000,
                                           'red_eff' : 1,
                                           'sumw'    : 201048.136391,
                                           'xsec'    : 0.004747},

    # stop-stop -> tt + DM

    'TT_directTT_450_1_1largeRjet1lep': {'DSID'    : 388240,
                                         'events'  : 50000,
                                         'red_eff' : 1,
                                         'sumw'    : 52247.301193,
                                         'xsec'    : 0.88424},

    'TT_directTT_500_1_1largeRjet1lep': {'DSID'    : 387154,
                                         'events'  : 20000,
                                         'red_eff' : 1,
                                         'sumw'    : 20793.7352104,
                                         'xsec'    : 0.46603},

    'TT_directTT_500_200_1largeRjet1lep': {'DSID'    : 387157,
                                           'events'  : 50000,
                                           'red_eff' : 1,
                                           'sumw'    : 51998.4134001,
                                           'xsec'    : 0.46702},

    'TT_directTT_600_1_1largeRjet1lep': {'DSID'    : 387163,
                                         'events':69000,
                                         'red_eff' : 1,
                                         'sumw'    : 71506.9188489,
                                         'xsec'    : 0.15518},

    # chargino-neutralino -> WZ(->lvll)

    'C1N2_WZ_100p0_0p0_3L_2L7_1largeRjet1lep': {'DSID'    : 392226,
                                                'events'  : 25000,
                                                'red_eff' : 1,
                                                'sumw'    : 26928.7771142,
                                                'xsec'    : 15.82879625},

    'C1N2_WZ_350p0_0p0_3L_2L7_1largeRjet1lep': {'DSID'    : 392220,
                                                'events'  : 10000,
                                                'red_eff' : 1,
                                                'sumw'    : 10346.0705611,
                                                'xsec'    : 0.1418528975},

    'C1N2_WZ_400p0_0p0_3L_2L7_1largeRjet1lep': {'DSID'    : 392217,
                                                'events'  : 10000,
                                                'red_eff' : 1,
                                                'sumw'    : 10327.8154224,
                                                'xsec'    : 0.080689712},

    'C1N2_WZ_500p0_0p0_3L_2L7_1largeRjet1lep': {'DSID'    : 392223,
                                                'events':15000,
                                                'red_eff' : 1,
                                                'sumw'    : 15476.3430636,
                                                'xsec'    : 0.0301334215},

}

samples = {

    'data': {
        'list' : ['data_A','data_B','data_C','data_D'],
    },

    r'Background $Z,t\bar{t}$' : { # Z + ttbar
        'list' : ['Zee','Zmumu','ttbar_lep'],
        'color' : "#6b59d3" # purple
    },

    r'Background $ZZ^*$' : { # ZZ
        'list' : ['llll'],
        'color' : "#ff0000" # red
    },

    r'Signal ($m_H$ = 125 GeV)' : { # H -> ZZ -> llll
        'list' : ['ggH125_ZZ4lep','VBFH125_ZZ4lep','WH125_ZZ4lep','ZH125_ZZ4lep'],
        'color' : "#00cdff" # light blue
    },

}

# functions
def get_xsec_weight(sample):
    info = infos[sample]
    xsec_weight = (lumi*1000*info["xsec"])/(info["sumw"]*info["red_eff"]) #*1000 to go from fb-1 to pb-1
    return xsec_weight # return cross-section weight


def calc_weight(xsec_weight, events):
    return (
        xsec_weight
        * events.mcWeight
        * events.scaleFactor_PILEUP
        * events.scaleFactor_ELE
        * events.scaleFactor_MUON 
        * events.scaleFactor_LepTRIGGER
    )


def calc_mllll(lep_pt, lep_eta, lep_phi, lep_E):
    # construct awkward 4-vector array
    p4 = vector.zip({"pt": lep_pt, "eta": lep_eta, "phi": lep_phi, "E": lep_E})
    # calculate invariant mass of first 4 leptons
    # [:, i] selects the i-th lepton in each event
    # .M calculates the invariant mass
    return (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).M * MeV

# cut on lepton charge
# paper: "selecting two pairs of isolated leptons, each of which is comprised of two leptons with the same flavour and opposite charge"
def cut_lep_charge(lep_charge):
# throw away when sum of lepton charges is not equal to 0
# first lepton in each event is [:, 0], 2nd lepton is [:, 1] etc
    return lep_charge[:, 0] + lep_charge[:, 1] + lep_charge[:, 2] + lep_charge[:, 3] != 0

# cut on lepton type
# paper: "selecting two pairs of isolated leptons, each of which is comprised of two leptons with the same flavour and opposite charge"
def cut_lep_type(lep_type):
# for an electron lep_type is 11
# for a muon lep_type is 13
# throw away when none of eeee, mumumumu, eemumu
    sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
    return (sum_lep_type != 44) & (sum_lep_type != 48) & (sum_lep_type != 52)

def read_file(path,sample):
    start = time.time() # start the clock
    print("\tProcessing: "+sample) # print which sample is being processed
    data_all = [] # define empty list to hold all data for this sample
    
    # open the tree called mini using a context manager (will automatically close files/resources)
    with uproot.open(path + ":mini") as tree:
        numevents = tree.num_entries # number of events
        if 'data' not in sample: xsec_weight = get_xsec_weight(sample) # get cross-section weight
        for data in tree.iterate(['lep_pt','lep_eta','lep_phi',
                                  'lep_E','lep_charge','lep_type', 
                                  # add more variables here if you make cuts on them 
                                  'mcWeight','scaleFactor_PILEUP',
                                  'scaleFactor_ELE','scaleFactor_MUON',
                                  'scaleFactor_LepTRIGGER'], # variables to calculate Monte Carlo weight
                                 library="ak", # choose output type as awkward array
                                 entry_stop=numevents*fraction): # process up to numevents*fraction

            nIn = len(data) # number of events in this batch

            if 'data' not in sample: # only do this for Monte Carlo simulation files
                # multiply all Monte Carlo weights and scale factors together to give total weight
                data['totalWeight'] = calc_weight(xsec_weight, data)

            # cut on lepton charge using the function cut_lep_charge defined above
            data = data[~cut_lep_charge(data.lep_charge)]

            # cut on lepton type using the function cut_lep_type defined above
            data = data[~cut_lep_type(data.lep_type)]

            # calculation of 4-lepton invariant mass using the function calc_mllll defined above
            data['mllll'] = calc_mllll(data.lep_pt, data.lep_eta, data.lep_phi, data.lep_E)

            # array contents can be printed at any stage like this
            #print(data)

            # array column can be printed at any stage like this
            #print(data['lep_pt'])

            # multiple array columns can be printed at any stage like this
            #print(data[['lep_pt','lep_eta']])

            nOut = len(data) # number of events passing cuts in this batch
            data_all.append(data) # append array from this batch
            elapsed = time.time() - start # time taken to process
            print("\t\t nIn: "+str(nIn)+",\t nOut: \t"+str(nOut)+"\t in "+str(round(elapsed,1))+"s") # events before and after
    
    return ak.concatenate(data_all) # return array containing events passing all cuts

def get_data_from_files():

    data = {} # define empty dictionary to hold awkward arrays
    for s in samples: # loop over samples
        print('Processing '+s+' samples') # print which sample
        frames = [] # define empty list to hold data
        for val in samples[s]['list']: # loop over each file
            if s == 'data': prefix = "Data/" # Data prefix
            else: # MC prefix
                prefix = "MC/mc_"+str(infos[val]["DSID"])+"."
            fileString = tuple_path+prefix+val+".4lep.root" # file name to open
            temp = read_file(fileString,val) # call the function read_file defined below
            frames.append(temp) # append array returned from read_file to list of awkward arrays
        data[s] = ak.concatenate(frames) # dictionary entry is concatenated awkward arrays
    
    return data # return dictionary of awkward arrays

start = time.time() # time at start of whole processing
data = get_data_from_files() # process all files
elapsed = time.time() - start # time after whole processing
print("Time taken: "+str(round(elapsed,1))+"s") # print total time taken to process every file

#  extra variables needed to send the needed variables
xmin = 80 * GeV
xmax = 250 * GeV
step_size = 5 * GeV

bin_edges = np.arange(start=xmin, # The interval includes this value
                 stop=xmax+step_size, # The interval doesn't include this value
                 step=step_size ) # Spacing between values
bin_centres = np.arange(start=xmin+step_size/2, # The interval includes this value
                            stop=xmax+step_size/2, # The interval doesn't include this value
                            step=step_size ) # Spacing between values

data_x,_ = np.histogram(ak.to_numpy(data['data']['mllll']), 
                            bins=bin_edges ) # histogram the data

signal_x = ak.to_numpy(data[r'Signal ($m_H$ = 125 GeV)']['mllll'])
signal_weights = ak.to_numpy(data[r'Signal ($m_H$ = 125 GeV)'].totalWeight)
signal_color = samples[r'Signal ($m_H$ = 125 GeV)']['color']

mc_x = []
mc_weights = []
mc_colors = []
mc_labels = []

for s in samples: # loop over samples
    if s not in ['data', r'Signal ($m_H$ = 125 GeV)']: # if not data nor signal
        mc_x.append( ak.to_numpy(data[s]['mllll']) ) # append to the list of Monte Carlo histogram entries
        mc_weights.append( ak.to_numpy(data[s].totalWeight) ) # append to the list of Monte Carlo weights
        mc_colors.append( samples[s]['color'] ) # append to the list of Monte Carlo bar colors
        mc_labels.append( s ) # append to the list of Monte Carlo legend labels

# prepare data for csv packaging
# Convert data_x array to float before padding
data_x = data_x.astype(float)
# unpack lists of arrays into separate arrays
mc_x_a = mc_x[0]
mc_x_b = mc_x[1]

mc_weights_a = mc_weights[0]
mc_weights_b = mc_weights[1]

mc_labels_a = mc_labels[0]
mc_labels_b = mc_labels[1]

mc_colors = np.array(mc_colors)

# Determine the maximum length among all arrays
max_length = max(len(data_x), len(signal_x), len(signal_weights), len(mc_x_a), len(mc_x_b), len(mc_weights_a), len(mc_weights_b), len(mc_labels_a), len(mc_labels_b), max(len(x) for x in mc_x), max(len(x) for x in mc_weights), max(len(x) for x in mc_colors), max(len(x) for x in mc_labels), len(mc_colors))

# Pad the arrays with NaN values to make them the same length
data_x = np.pad(data_x, (0, max_length - len(data_x)), mode='constant', constant_values=np.nan)
signal_x = np.pad(signal_x, (0, max_length - len(signal_x)), mode='constant', constant_values=np.nan)
signal_weights = np.pad(signal_weights, (0, max_length - len(signal_weights)), mode='constant', constant_values=np.nan)
mc_colors = np.pad(mc_colors, (0, max_length - len(mc_colors)), mode='constant', constant_values=np.nan)

# Pad the lists within mc_x, mc_weights, mc_colors, and mc_labels
mc_x_a_padded = np.pad(mc_x_a, (0, max_length - len(mc_x_a)), mode='constant', constant_values=np.nan)
mc_x_b_padded = np.pad(mc_x_b, (0, max_length - len(mc_x_b)), mode='constant', constant_values=np.nan)

mc_weights_a_padded = np.pad(mc_weights_a, (0, max_length - len(mc_weights_a)), mode='constant', constant_values=np.nan)
mc_weights_b_padded = np.pad(mc_weights_b, (0, max_length - len(mc_weights_b)), mode='constant', constant_values=np.nan)

mc_labels_a_padded = np.pad(mc_labels_a, (0, max_length - len(mc_labels_a)), mode='constant', constant_values=np.nan)
mc_labels_b_padded = np.pad(mc_labels_b, (0, max_length - len(mc_labels_b)), mode='constant', constant_values=np.nan)

# Combine all variables into a dictionary
data_dict = {
    'data_x': data_x,
    'signal_x': signal_x,
    'signal_weights': signal_weights,
    'mc_colors' : mc_colors,
    'mc_x_a': mc_x_a_padded,
    'mc_x_b': mc_x_b_padded,
    'mc_weights_a': mc_weights_a_padded,
    'mc_weights_b': mc_weights_b_padded,
    'mc_labels_a': mc_labels_a_padded,
    'mc_labels_b': mc_labels_b_padded,
}


# Create DataFrame from the dictionary
df = pd.DataFrame(data_dict)

# Combine data into a dictionary
data_dict = {'dataframe': df, 'array': signal_color, 'list': mc_labels}

# Serialize the data using pickle
body = pickle.dumps(data_dict)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('172.30.160.1'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='my_queue')

# Send the message
channel.basic_publish(exchange='', routing_key='my_queue', body=body)

print("Data sent successfully.")
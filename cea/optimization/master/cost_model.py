# -*- coding: utf-8 -*-
"""
============================
Extra costs to an individual
============================

"""
from __future__ import division

import os

import cea.technologies.thermal_network as network
import numpy as np
import pandas as pd

import cea.resources.natural_gas as ngas
import cea.technologies.boilers as boiler
import cea.technologies.cogeneration as chp
import cea.technologies.furnace as furnace
import cea.technologies.heat_exchangers as hex
import cea.technologies.heatpumps as hp
import cea.technologies.photovoltaic as pv
import cea.technologies.photovoltaic_thermal as pvt
import cea.technologies.pumps as pumps
import cea.technologies.solar_collector as stc
import cea.technologies.thermal_storage as storage

__author__ = "Tim Vollrath"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Tim Vollrath", "Thuy-An Nguyen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def addCosts(indCombi, buildList, locator, dicoSupply, QUncoveredDesign, QUncoveredAnnual, solarFeat, ntwFeat, gv):
    """
    Computes additional costs / GHG emisions / primary energy needs
    for the individual
    addCosts = additional costs
    addCO2 = GHG emissions
    addPrm = primary energy needs

    :param indCombi: parameter indicating if the building is connected or not
    :param buildList: list of buildings in the district
    :param locator: input locator set to scenario
    :param dicoSupply: class containing the features of a specific individual
    :param QUncoveredDesign: hourly max of the heating uncovered demand
    :param QUncoveredAnnual: total heating uncovered
    :param solarFeat: solar features
    :param ntwFeat: network features
    :param gv: global variables
    :type indCombi: string
    :type buildList: list
    :type locator: string
    :type dicoSupply: class
    :type QUncoveredDesign: float
    :type QUncoveredAnnual: float
    :type solarFeat: class
    :type ntwFeat: class
    :type gv: class

    :return: returns the objectives addCosts, addCO2, addPrim
    :rtype: tuple
    """
    addcosts_Capex_a = 0
    addcosts_Opex_fixed = 0
    addCO2 = 0
    addPrim = 0
    nBuildinNtw = 0
    
    # Add the features from the disconnected buildings
    os.chdir(locator.get_optimization_disconnected_folder())
    CostDiscBuild = 0
    CO2DiscBuild = 0
    PrimDiscBuild = 0
    Capex_a_furnace = 0
    Capex_a_CCT = 0
    Capex_a_Boiler = 0
    Capex_a_Boiler_peak = 0
    Capex_a_Lake = 0
    Capex_a_Sewage = 0
    Capex_a_GHP = 0
    Capex_a_PV = 0
    Capex_a_SC = 0
    Capex_a_PVT = 0
    Capex_a_Boiler_backup = 0
    Capex_a_HEX = 0
    Capex_a_storage_HP = 0
    StorageInvC = 0
    NetworkCost = 0
    SubstHEXCost_capex = 0
    SubstHEXCost_opex = 0
    PVTHEXCost_Capex = 0
    PVTHEXCost_Opex = 0
    SCHEXCost_Capex = 0
    SCHEXCost_Opex = 0
    pumpCosts = 0
    GasConnectionInvCost = 0 
    
    for (index, building_name) in zip(indCombi, buildList):
        if index == "0":
            discFileName = "DiscOp_" + building_name + "_result.csv"
            df = pd.read_csv(discFileName)
            dfBest = df[df["Best configuration"] == 1]
            CostDiscBuild += dfBest["Total Costs [CHF]"].iloc[0] # [CHF]
            CO2DiscBuild += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0] # [kg CO2]
            PrimDiscBuild += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0] # [MJ-oil-eq]

        else:
            nBuildinNtw += 1
    
    addcosts_Capex_a += CostDiscBuild
    addCO2 += CO2DiscBuild
    addPrim += PrimDiscBuild
    
    # Add the features for the distribution

    if indCombi.count("1") > 0:
        os.chdir(locator.get_optimization_slave_results_folder())
        # Add the investment costs of the energy systems
        # Furnace
        if dicoSupply.Furnace_on == 1:
            P_design = dicoSupply.Furnace_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfFurnace = pd.read_csv(fNameSlavePP, usecols=["Q_Furnace"])
            arrayFurnace = np.array(dfFurnace)
            
            Q_annual =  0
            for i in range(int(np.shape(arrayFurnace)[0])):
                Q_annual += arrayFurnace[i][0]
            
            Capex_a_furnace, Opex_fixed_furnace = furnace.calc_Cinv_furnace(P_design, Q_annual, gv, locator)
            addcosts_Capex_a += Capex_a_furnace
            addcosts_Opex_fixed += Opex_fixed_furnace

        # CC
        if dicoSupply.CC_on == 1:
            CC_size = dicoSupply.CC_GT_SIZE 
            Capex_a_CCT, Opex_fixed_CCT = chp.calc_Cinv_CCT(CC_size, gv, locator)
            addcosts_Capex_a += Capex_a_CCT
            addcosts_Opex_fixed += Opex_fixed_CCT

        # Boiler Base
        if dicoSupply.Boiler_on == 1:
            Q_design = dicoSupply.Boiler_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfBoilerBase = pd.read_csv(fNameSlavePP, usecols=["Q_BoilerBase"])
            arrayBoilerBase = np.array(dfBoilerBase)
            
            Q_annual =  0
            for i in range(int(np.shape(arrayBoilerBase)[0])):
                Q_annual += arrayBoilerBase[i][0]
                
            Capex_a_Boiler, Opex_fixed_Boiler = boiler.calc_Cinv_boiler(Q_design, Q_annual, gv, locator)
            addcosts_Capex_a += Capex_a_Boiler
            addcosts_Opex_fixed += Opex_fixed_Boiler

        # Boiler Peak
        if dicoSupply.BoilerPeak_on == 1:
            Q_design = dicoSupply.BoilerPeak_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfBoilerPeak = pd.read_csv(fNameSlavePP, usecols=["Q_BoilerPeak"])
            arrayBoilerPeak = np.array(dfBoilerPeak)
            
            Q_annual =  0
            for i in range(int(np.shape(arrayBoilerPeak)[0])):
                Q_annual += arrayBoilerPeak[i][0]
            Capex_a_Boiler_peak, Opex_fixed_Boiler_peak = boiler.calc_Cinv_boiler(Q_design, Q_annual, gv, locator)
            addcosts_Capex_a += Capex_a_Boiler_peak
            addcosts_Opex_fixed += Opex_fixed_Boiler_peak
        
        # HP Lake
        if dicoSupply.HP_Lake_on == 1:
            HP_Size = dicoSupply.HPLake_maxSize
            Capex_a_Lake, Opex_fixed_Lake = hp.calc_Cinv_HP(HP_Size, gv, locator)
            addcosts_Capex_a += Capex_a_Lake
            addcosts_Opex_fixed += Opex_fixed_Lake

        # HP Sewage
        if dicoSupply.HP_Sew_on == 1:
            HP_Size = dicoSupply.HPSew_maxSize
            Capex_a_Sewage, Opex_fixed_Sewage = hp.calc_Cinv_HP(HP_Size, gv, locator)
            addcosts_Capex_a += Capex_a_Sewage
            addcosts_Opex_fixed += Opex_fixed_Sewage

        # GHP
        if dicoSupply.GHP_on == 1:
            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfGHP = pd.read_csv(fNameSlavePP, usecols=["E_GHP"])
            arrayGHP = np.array(dfGHP)
            
            GHP_Enom = np.amax(arrayGHP)
            Capex_a_GHP, Opex_fixed_GHP = hp.GHP_InvCost(GHP_Enom, gv, locator)
            addcosts_Capex_a += Capex_a_GHP * gv.EURO_TO_CHF
            addcosts_Opex_fixed += Opex_fixed_GHP * gv.EURO_TO_CHF

        # Solar technologies

        PV_peak = dicoSupply.SOLAR_PART_PV * solarFeat.SolarAreaPV * gv.nPV #kW
        Capex_a_PV, Opex_fixed_PV = pv.calc_Cinv_pv(PV_peak, locator)
        addcosts_Capex_a += Capex_a_PV
        addcosts_Opex_fixed += Opex_fixed_PV

        SC_area = dicoSupply.SOLAR_PART_SC * solarFeat.SolarAreaSC
        Capex_a_SC, Opex_fixed_SC = stc.calc_Cinv_SC(SC_area, gv, locator)
        addcosts_Capex_a += Capex_a_SC
        addcosts_Opex_fixed += Opex_fixed_SC

        PVT_peak = dicoSupply.SOLAR_PART_PVT * solarFeat.SolarAreaPVT * gv.nPVT #kW
        Capex_a_PVT, Opex_fixed_PVT = pvt.calc_Cinv_PVT(PVT_peak, gv, locator)
        addcosts_Capex_a += Capex_a_PVT
        addcosts_Opex_fixed += Opex_fixed_PVT

        # Back-up boiler
        Capex_a_Boiler_backup, Opex_fixed_Boiler_backup = boiler.calc_Cinv_boiler(QUncoveredDesign, QUncoveredAnnual, gv, locator)
        addcosts_Capex_a += Capex_a_Boiler_backup
        addcosts_Opex_fixed += Opex_fixed_Boiler_backup

        # Hex and HP for Heat recovery
        if dicoSupply.WasteServersHeatRecovery == 1:
            df = pd.read_csv(
                os.path.join(locator.get_optimization_network_results_folder(), dicoSupply.NETWORK_DATA_FILE),
                usecols=["Qcdata_netw_total"])
            array = np.array(df)
            QhexMax = np.amax(array)
            Capex_a_storage_HEX, Opex_fixed_storage_HEX = hex.calc_Cinv_HEX(QhexMax, gv, locator)
            addcosts_Capex_a += (Capex_a_storage_HEX)
            addcosts_Opex_fixed += Opex_fixed_storage_HEX
            
            df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                             usecols=["HPServerHeatDesignArray"])
            array = np.array(df)
            QhpMax = np.amax(array)
            Capex_a_storage_HP, Opex_fixed_storage_HP = hp.calc_Cinv_HP(QhpMax, gv, locator)
            addcosts_Capex_a += (Capex_a_storage_HP)
            addcosts_Opex_fixed += Opex_fixed_storage_HP

        if dicoSupply.WasteCompressorHeatRecovery == 1:
            df = pd.read_csv(
                os.path.join(locator.get_optimization_network_results_folder(), dicoSupply.NETWORK_DATA_FILE),
                usecols=["Ecaf_netw_total"])
            array = np.array(df)
            QhexMax = np.amax(array)

            Capex_a_storage_HEX, Opex_fixed_storage_HEX = hex.calc_Cinv_HEX(QhexMax, gv, locator)
            addcosts_Capex_a += (Capex_a_storage_HEX)
            addcosts_Opex_fixed += Opex_fixed_storage_HEX
            df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                             usecols=["HPCompAirDesignArray"])
            array = np.array(df)
            QhpMax = np.amax(array)
            Capex_a_storage_HP, Opex_fixed_storage_HP = hp.calc_Cinv_HP(QhpMax, gv, locator)
            addcosts_Capex_a += (Capex_a_storage_HP)
            addcosts_Opex_fixed += Opex_fixed_storage_HP
        addcosts_Capex_a += Capex_a_HEX
        
        # Heat pump solar to storage
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["HPScDesignArray", "HPpvt_designArray"])
        array = np.array(df)
        QhpMax_PVT = np.amax(array[:,1])
        QhpMax_SC = np.amax(array[:,0])
        Capex_a_storage_HEX, Opex_fixed_storage_HEX = hp.calc_Cinv_HP(QhpMax_PVT, gv, locator)
        Capex_a_storage_HP += (Capex_a_storage_HEX)
        addcosts_Opex_fixed += Opex_fixed_storage_HEX

        Capex_a_storage_HEX, Opex_fixed_storage_HEX = hp.calc_Cinv_HP(QhpMax_SC, gv, locator)
        Capex_a_storage_HP += (Capex_a_storage_HEX)
        addcosts_Opex_fixed += Opex_fixed_storage_HEX

        # HP for storage operation
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["E_aux_ch", "E_aux_dech", "Q_from_storage_used", "Q_to_storage"])
        array = np.array(df)
        QmaxHPStorage = 0
        for i in range(gv.DAYS_IN_YEAR * gv.HOURS_IN_DAY):
            if array[i][0] > 0:
                QmaxHPStorage = max(QmaxHPStorage, array[i][3] + array[i][0])
            elif array[i][1] > 0:
                QmaxHPStorage = max(QmaxHPStorage, array[i][2] + array[i][1])

        Capex_a_storage_HEX, Opex_fixed_storage_HEX = hp.calc_Cinv_HP(QmaxHPStorage, gv, locator)
        addcosts_Capex_a += (Capex_a_storage_HEX)
        addcosts_Opex_fixed += Opex_fixed_storage_HEX

        # Storage
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["Storage_Size"], nrows=1)
        StorageVol = np.array(df)[0][0]
        Capex_a_storage_HEX = storage.calc_Cinv_storage(StorageVol, gv)
        addcosts_Capex_a += Capex_a_storage_HEX


        
        # Costs from distribution configuration
        if gv.ZernezFlag == 1:
            NetworkCost += network.calc_Cinv_network_linear(gv.NetworkLengthZernez, gv) * nBuildinNtw / len(buildList)
        else:
            NetworkCost += ntwFeat.pipesCosts_DHN * nBuildinNtw / len(buildList)
        addcosts_Capex_a += NetworkCost

        # HEX (1 per building in ntw)
        for (index, building_name) in zip(indCombi, buildList):
            if index == "1":
                df = pd.read_csv(locator.get_optimization_substations_results_file(building_name),
                                 usecols=["Q_dhw", "Q_heating"])
                subsArray = np.array(df)
                
                Qmax = np.amax( subsArray[:,0] + subsArray[:,1] )
                Capex_a_building, Opex_fixed_building = hex.calc_Cinv_HEX(Qmax, gv, locator)
                addcosts_Capex_a += Capex_a_building
                addcosts_Opex_fixed += Opex_fixed_building


        # HEX for solar
        roof_area = np.array(pd.read_csv(locator.get_total_demand(), usecols=["Aroof_m2"]))

        areaAvail = 0
        for i in range( len(indCombi) ):
            index = indCombi[i]
            if index == "1":
                areaAvail += roof_area[i][0]
                
        for i in range( len(indCombi) ):
            index = indCombi[i]
            if index == "1":
                share = roof_area[i][0] / areaAvail
                #print share, "solar area share", buildList[i]
                
                SC_Qmax = solarFeat.SC_Qnom * dicoSupply.SOLAR_PART_SC * share
                Capex_a_HEX_SC, Opex_fixed_HEX_SC = hex.calc_Cinv_HEX(SC_Qmax, gv, locator)
                addcosts_Capex_a += Capex_a_HEX_SC
                addcosts_Opex_fixed += Opex_fixed_HEX_SC

                PVT_Qmax = solarFeat.PVT_Qnom * dicoSupply.SOLAR_PART_PVT * share
                Capex_a_HEX_PVT, Opex_fixed_HEX_PVT = hex.calc_Cinv_HEX(PVT_Qmax, gv, locator)
                addcosts_Capex_a += Capex_a_HEX_PVT
                addcosts_Opex_fixed += Opex_fixed_HEX_PVT

        # Pump operation costs
        pumpCosts = pumps.calc_Ctot_pump(dicoSupply, buildList, locator.get_optimization_network_results_folder(), ntwFeat, gv)
        addcosts_Capex_a += pumpCosts

    # import gas consumption data from:

    if indCombi.count("1") > 0:
        # import gas consumption data from:
        EgasPrimaryDataframe = pd.read_csv(locator.get_optimization_slave_primary_energy_by_source(dicoSupply.configKey),
            usecols=["EgasPrimaryPeakPower"])
        EgasPrimaryPeakPower = float(np.array(EgasPrimaryDataframe))
        GasConnectionInvCost = ngas.calc_Cinv_gas(EgasPrimaryPeakPower, gv)
    else:
        GasConnectionInvCost = 0.0
        
    addcosts_Capex_a += GasConnectionInvCost
    # Save data
    results = pd.DataFrame({
                            "Capex_a_SC":[Capex_a_SC],
                            "Opex_fixed_SC":[Opex_fixed_SC],
                            "Capex_a_PVT":[Capex_a_PVT],
                            "Opex_fixed_PVT":[Opex_fixed_PVT],
                            "Capex_a_Boiler_backup":[Capex_a_Boiler_backup],
                            "Opex_fixed_Boiler_backup":[Opex_fixed_Boiler_backup],
                            "Capex_a_storage_HEX":[Capex_a_storage_HEX],
                            "Opex_fixed_storage_HEX":[Opex_fixed_storage_HEX],
                            "Capex_a_storage_HP":[Capex_a_storage_HP],
                            "StorageInvC":[StorageInvC],
                            "StorageCostSum":[StorageInvC+Capex_a_storage_HP+Capex_a_HEX],
                            "NetworkCost":[NetworkCost],
                            "SubstHEXCost":[SubstHEXCost_capex],
                            "DHNInvestCost":[addcosts_Capex_a - CostDiscBuild],
                            "PVTHEXCost_Capex":[PVTHEXCost_Capex],
                            "CostDiscBuild":[CostDiscBuild],
                            "CO2DiscBuild":[CO2DiscBuild],
                            "PrimDiscBuild":[PrimDiscBuild],
                            "Capex_a_furnace":[Capex_a_furnace],
                            "Capex_a_Boiler":[Capex_a_Boiler],
                            "Capex_a_Boiler_peak":[Capex_a_Boiler_peak],
                            "Capex_a_Lake":[Capex_a_Lake],
                            "Capex_a_Sewage":[Capex_a_Sewage],
                            "SCHEXCost_Capex":[SCHEXCost_Capex],
                            "pumpCosts":[pumpCosts],
                            "Sum_CAPEX":[addcosts_Capex_a],
                            "Sum_OPEX_fixed": [addcosts_Opex_fixed],
                            "GasConnectionInvCa":[GasConnectionInvCost]
                            })
    results.to_csv(locator.get_optimization_slave_investment_cost_detailed(dicoSupply.configKey), sep=',')

      
    return (addcosts_Capex_a + addcosts_Opex_fixed, addCO2, addPrim)

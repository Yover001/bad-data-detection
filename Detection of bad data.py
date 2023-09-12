from pandapower.estimation import estimate
from pandapower.networks import *
from math import sqrt
import pandapower as pp
import numpy as np
import torch
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def get_net():
    return case89pegase()

def pass_meases_feedback(net, net2, v_stddev, pq_stddev, i_stddev):
    # bus`s 对于bus表，代码获取net中的vm_pu、p_mw和q_mvar的值，并使用pp.create_measurement函数在net2中创建对应的电压和功率测量值。如果p_mw或q_mvar的值不为0，则会添加相应的测量值
    for busIndex in net.bus.index:
        vn_pu = net.res_bus.vm_pu[busIndex]
        pp.create_measurement(net2, "v", "bus", vn_pu, v_stddev, element=busIndex)

        p_mw = net.res_bus.p_mw[busIndex]
        if p_mw != 0:
            pp.create_measurement(net2, "p", "bus", p_mw, pq_stddev, element=busIndex)
        q_mvar = net.res_bus.q_mvar[busIndex]
        if q_mvar != 0:
            pp.create_measurement(net2, "q", "bus", q_mvar, pq_stddev, element=busIndex)

    # line`s 对于line表，代码获取net中的p_from_mw、p_to_mw、q_from_mvar和q_to_mvar的值，并使用pp.create_measurement函数在net2中创建对应的功率测量值。测量值的类型为线路（"line"），并指定了测量值所属的线路索引（element）和方向（side）。
    for lineIndex in net.line.index:
        p_from_mw = net.res_line.p_from_mw[lineIndex]
        pp.create_measurement(net2, "p", "line", p_from_mw, pq_stddev, element=lineIndex, side="from")
        p_to_mw = net.res_line.p_to_mw[lineIndex]
        pp.create_measurement(net2, "p", "line", p_to_mw, pq_stddev, element=lineIndex, side="to")

        q_from_mvar = net.res_line.q_from_mvar[lineIndex]
        pp.create_measurement(net2, "q", "line", q_from_mvar, pq_stddev, element=lineIndex, side="from")
        q_to_mvar = net.res_line.q_to_mvar[lineIndex]
        pp.create_measurement(net2, "q", "line", q_to_mvar, pq_stddev, element=lineIndex, side="to")

    # trafo`s 对于trafo表，代码获取net中的p_hv_mw、p_lv_mw、q_hv_mvar和q_lv_mvar的值，并使用pp.create_measurement函数在net2中创建对应的功率测量值。测量值的类型为变压器（"trafo"），并指定了测量值所属的变压器索引（element）和侧面（side）。
    for trafoIndex in net.trafo.index:
        p_hv_mw = net.res_trafo.p_hv_mw[trafoIndex]
        pp.create_measurement(net2, "p", "trafo", p_hv_mw, pq_stddev, element=trafoIndex, side="hv")
        p_lv_mw = net.res_trafo.p_lv_mw[trafoIndex]
        pp.create_measurement(net2, "p", "trafo", p_lv_mw, pq_stddev, element=trafoIndex, side="lv")

        q_hv_mvar = net.res_trafo.q_hv_mvar[trafoIndex]
        pp.create_measurement(net2, "q", "trafo", q_hv_mvar, pq_stddev, element=trafoIndex, side="hv")
        q_lv_mvar = net.res_trafo.q_lv_mvar[trafoIndex]
        pp.create_measurement(net2, "q", "trafo", q_lv_mvar, pq_stddev, element=trafoIndex, side="lv")

    # trafo3w`s 对于trafo3w表，代码获取net中的p_hv_mw、p_lv_mw、p_mv_mw、q_hv_mvar、q_lv_mvar和q_mv_mvar的值，并使用pp.create_measurement函数在net2中创建对应的功率测量值。测量值的类型为三绕组变压器（"trafo3w"），并指定了测量值所属的变压器索引（element）和侧面（side）。
    for trafoIndex in net.trafo3w.index:

        p_hv_mw = net.res_trafo3w.p_hv_mw[trafoIndex]
        pp.create_measurement(net2, "p", "trafo3w", p_hv_mw, pq_stddev, element=trafoIndex, side="hv")
        p_lv_mw = net.res_trafo3w.p_lv_mw[trafoIndex]
        pp.create_measurement(net2, "p", "trafo3w", p_lv_mw, pq_stddev, element=trafoIndex, side="lv")
        p_mv_mw = net.res_trafo3w.p_mv_mw[trafoIndex]
        pp.create_measurement(net2, "p", "trafo3w", p_mv_mw, pq_stddev, element=trafoIndex, side="mv")

        q_hv_mvar = net.res_trafo3w.q_hv_mvar[trafoIndex]
        pp.create_measurement(net2, "q", "trafo3w", q_hv_mvar, pq_stddev, element=trafoIndex, side="hv")
        q_lv_mvar = net.res_trafo3w.q_lv_mvar[trafoIndex]
        pp.create_measurement(net2, "q", "trafo3w", q_lv_mvar, pq_stddev, element=trafoIndex, side="lv")
        q_mv_mvar = net.res_trafo3w.q_mv_mvar[trafoIndex]
        pp.create_measurement(net2, "q", "trafo3w", q_mv_mvar, pq_stddev, element=trafoIndex, side="mv")


#################################################################################################################################
def main():
    net = get_net()
    pp.runpp(net, calculate_voltage_angles=True, enforce_q_lims=False)
    net2 = get_net()

    v_stddev = 0.01 # pu
    pq_stddev = 0.01 # MW/Mvar
    i_stddev= 0.002 # kA

    pass_meases_feedback(net, net2, v_stddev, pq_stddev, i_stddev)                      # 生成的量测数据
    measurement = net2.measurement["value"].values
    # measurement_v = net2.measurement[net2.measurement['measurement_type'] == "v"]["value"].values
    # measurement_p = net2.measurement[net2.measurement['measurement_type'] == "p"]["value"].values
    # measurement_q = net2.measurement[net2.measurement['measurement_type'] == "q"]["value"].values
    # measurement_p_line = net2.measurement[(net2.measurement['measurement_type'] == "p") & (net2.measurement['element_type'] == "line")]["value"].values
    # measurement_q_line = net2.measurement[(net2.measurement['measurement_type'] == "q") & (net2.measurement['element_type'] == "line")]["value"].values


    success_chi2 = pp.estimation.chi2_analysis(net2, init='flat', tolerance=1e-06, maximum_iterations=10, calculate_voltage_angles=True, chi2_prob_false=0.05)
    success_rn_max = pp.estimation.remove_bad_data(net2,init = 'flat',tolerance = 1e-06,maximum_iterations = 10,calculate_voltage_angles = True,rn_max_threshold = 3.0)

if __name__ == "__main__":
    main()
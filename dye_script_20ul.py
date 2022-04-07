1 from config import *
2 
3 """this is used to check the 20 uL pipetting. 
4 
5 Briefly, the method involves picking up a tip, going to a specified dye well and drawing 20uL, then dispensing into another well. 
6 
7 """
8 
9 # Variables
10 tip_box_A1 = (18, -12)
11
12 well_dye = (127, -13) # slot 2, B1
13 well_smp_1 = (136,-13) # slot 2, C1
14 smp_number = 24
15
16
17 from machine_interface import MachineConnection
18 with MachineConnection('/var/run/dsf/dcs.sock') as m:
19    m.gcode("T0") # pickup tool
20    print("Tool picked up")
21    m.move(Z = clearance_height_tipbox_z)     
22    tips = 0 
23    for sample in range(smp_number):
24        # calculate tip pickup
25        pick_tip_x = tip_box_A1[0] + ((tips // tip_arrangement_colrow[1]) * tip_separation_xy[0])
26        pick_tip_y = tip_box_A1[1] + ((tips % tip_arrangement_colrow[1]) * tip_separation_xy[1])  
27        print(pick_tip_x, pick_tip_y, "tip pickup")
28        m.move(X = pick_tip_x, Y = pick_tip_y) # move above tip
29        m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pickup tip)
30        print("tip pickup sucessful")
31        m.move(X = well_dye[0], Y = well_dye[1]) # move to dye well
32        m.move(Z = wellplate_liquid_pickup_height_z)
33        m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
34        print("tip primed")
35        m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
36        m.move(Z = clearance_height_wellplate_z)
37        print("20ul collected from", well_dye[0], well_dye[1])
38        # calculate dispense well
39        smp_dispense_x = well_smp_1[0] + ((tips//tip_arrangement_colrow[1]) * well_separation_xy[0])
40        smp_dispense_y = well_smp_1[1] + ((tips%tip_arrangement_colrow[1]) * well_separation_xy[1])
41        tips += 1
42        m.move(X = smp_dispense_x, Y = smp_dispense_y) # move to dispense well
43        m.move(Z = wellplate_liquid_dispense_height_z)
44        m.gcode("""M98 P"/macros/dispense_blowout" """) # call the macro to dispense liquid
45        print("20ul dispensed on", smp_dispense_x, smp_dispense_y)
46        m.move(Z = clearance_height_wellplate_z)
47        m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to eject tip
48        print("tip ejected")
49        m.move(Z = clearance_height_tipbox_z)
50    m.gcode("T-1") # return tool to holder
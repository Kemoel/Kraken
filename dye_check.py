1 from config import *
2 
3 # this is for checking the 1uL pipetting. I want it to pick up a tip, go to a specified well and pick up 20uL dye, then move to another specified well and dispense 1uL in x number of wells. 
4 
5 # User Inputs
6 tip_box_A1 = (18, -12) #first tip to pick up
7 well_dye = (127, -13) # location of dye (slot 2, B1)
8 well_smp_1 = (163,-13) # location of sample 1 (slot 2, F1)
9 replicate_number = 4 # number of replicates for each draw
10 smp_number = 9 # total number of samples
11
12
13 from machine_interface import MachineConnection
14 with MachineConnection('/var/run/dsf/dcs.sock') as m:
15    m.gcode("T0") # pick up tool
16    print("Tool picked up")
17    m.move(Z = clearance_height_tipbox_z)     
18    tips = 0 
19    for sample in range(smp_number):
20        # calculate tip pickup location
21        pick_tip_x = tip_box_A1[0] + ((tips // tip_arrangement_colrow[1]) * tip_separation_xy[0])
22        pick_tip_y = tip_box_A1[1] + ((tips % tip_arrangement_colrow[1]) * tip_separation_xy[1])  
23        print(pick_tip_x, pick_tip_y, "tip pickup")
24        m.move(X = pick_tip_x, Y = pick_tip_y) # move above tip
25        m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pickup tip
26        print("tip pickup sucessful")
27        # collect dye 
28        m.move(X = well_dye[0], Y = well_dye[1]) 
29        m.move(Z = wellplate_liquid_pickup_height_z)
30        m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime time
31        print("tip primed")
32        m.gcode("""M98 P"/macros/draw_10ul_top" """) # call the macro to draw liquid
33        m.move(Z = clearance_height_wellplate_z)
34        print("10ul collected from", well_dye[0], well_dye[1])
35        # go to first well in dispense series
36        smp_dispense_x = well_smp_1[0] + ((tips//3) * well_separation_xy[0])
37        smp_dispense_y = well_smp_1[1] + ((tips%3) * (well_separation_xy[1] * 4))
38        tips += 1
39        wells = 0
40        # dispense 1 uL in each well
41        for sample in range(replicate_number):
42            smp_well_x = smp_dispense_x
43            smp_well_y = smp_dispense_y + (well_separation_xy[1] * wells)
44            m.move(X = smp_well_x, Y = smp_well_y)
45            m.move(Z = wellplate_liquid_dispense_height_z)
46            m.gcode("""M98 P"/macros/relative_dispense_1ul" """)
47            print("1ul dispensed on", smp_well_x, smp_well_y)
48            m.move(Z = clearance_height_wellplate_z)
49            wells += 1
50        m.gcode("""M98 P"/macros/eject_tip" """)
51        print("tip ejected")
52        m.move(Z = clearance_height_tipbox_z)
53    m.gcode("T-1")
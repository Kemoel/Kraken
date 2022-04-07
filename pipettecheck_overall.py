1 """
2 Name: pipettecheck_overall.py
3 
4 This script is used for mass-based validation of liquid handling.
5 
6 Important: Edit macro on line 25 (currently draw_10ul_top) to change plunger rod displacement 
7 """
8 
9 # locations
10 slot2_middle = (164,40) # liquid draw location; middle of slot 2
11 weigh_dish = (214,40) # liquid dispense location; edge of slot 3
12
13#EDIT MACRO USED FOR EACH RUN
14
15 from machine_interface import MachineConnection
16 with MachineConnection('/var/run/dsf/dcs.sock') as m:
17   
18    m.gcode("""M98 P"/macros/pickup_tip_A1" """) # pickup tip
19
20    m.move(X = slot2_middle[0], Y = slot2_middle[1]) # go to middle of slot 2
21    m.gcode("""M98 P"/macros/prime_tip" """) # prime tip
22
23    for x in range(5): # repeat 5 times
24        m.move(X = slot2_middle[0], Y = slot2_middle[1]) # go to middle of slot 2
25        m.gcode("""M98 P"/macros/draw_10ul_top" """) # EDIT ME
26        m.move(X = weigh_dish[0], Y = weigh_dish[1]) # go to weigh boat
27        m.gcode("""M98 P"/macros/dispense_blowout" """) # dispense all liquid
28    m.gcode("""M98 P"/macros/eject_tip" """) # after 5 replicates eject tip
29    
1   # Kraken layout and object locations
2 
3 
4   # slot locations
5   slot1_origin_xy = (8,-25) # absolute coordinate of top right corner of slot 1
6   slot_delta_xy = (100,151) # distance from top right corner of one slot to next (mm)
7 
8   # tip box
9   tip_A1_xy = (10,13) # distance from tip A1 to top right corner of slot (mm)
10  tip_separation_xy = (9,9) # distance between tips (mm)
11  tip_arrangement_colrow = (8,12) # number of columns (x) and rows (y) in tip box
12
13  # 96 well plate
14  well_A1_xy = (10,12) # distance in mm from well A1 to top right corner of slot
15  well_separation_xy = (9,9) # distance in mm between wells
16  well_arrangement_colrow = (8,12) # number of columns (x) and rows (y) in well plate
17
18  # MALDI plate holder
19  plate1_spotA1_xy = (66,12.8) # distance from plate 1 spotA1 to top right corner of slot (mm)
20  plate2_spotA1_xy = (66.6,73.3) # distance from plate 2 spotA1 to top right corner of slot (mm)
21  spot_separation_xy = (49.5/11,13.25/3) # distance between spots on plate (mm)
22  spot_arrangement_colrow = (12,8) # number of columns (x) and rows (y) on MALDI plate
23
24  # liquid pickup parameters
25  wellplate_liquid_pickup_height_z = 137
26  wellplate_liquid_mix_height_z = 135
27  wellplate_liquid_dispense_height_z = 135
28  maldi_dispense_height_z = 140.5 
29
30  # move parameters
31  clearance_height_wellplate_z = 153 
32  clearance_height_tipbox_z = 196 # tipbox clearance hight after picking up tip
33  clearance_height_maldi_z = 146 
34  tip_length = 20 
35
36  # liquid handling parameters
37 pipette_max_volume = 20 # uL 
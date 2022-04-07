1  from config import *
2  from input import *
3  
4  # this calculates the absolute coordinates of the top right point (well/tip) of any work item
5      # required imputs: item identity and slot location of item
6  def item_absolute_xy(slot1_origin_xy, slot_delta_xy, item_A1_xy, item_location): 
7      if(item_location <= 3):
8          x = slot1_origin_xy[0] + slot_delta_xy[0]*(item_location - 1) + item_A1_xy[0]
9          y = slot1_origin_xy[1] + item_A1_xy[1]
10         return (x,y)
11     else:
12         x = slot1_origin_xy[0] + slot_delta_xy[0]*(item_location - 4) + item_A1_xy[0]
13         y = slot1_origin_xy[1] + slot_delta_xy[1] + item_A1_xy[1]
14         return (x,y)
15 
16 # this takes single values in typical labelling format (A1 - H12) and turns the letters into numbers the computer can use
17     # this will work with both upper and lower case letters
18 def name_index_to_number_index_single(indicies_name_value):
19     if ord(indicies_name_value[0][0]) >= 97:
20         row_temp_x1 = ord(indicies_name_value[0][0]) - 97
21     else:
22         row_temp_x1 = ord(indicies_name_value[0][0]) - 65
23     row_temp_y1 = int(indicies_name_value[0][1:]) - 1
24     indicies_number_value = (row_temp_x1,row_temp_y1)
25     return indicies_number_value
26 
27 # this takes ranges in typical labelling format (A1 - H12) and turns the letters into numbers the computer can use
28     # this will work with both upper and lower case letters
29 def name_index_to_number_index(indicies_name_value):
30     indicies_number_value = []
31     for name_range in indicies_name_value:
32         if ord(indicies_name_value[name_range][0][0]) >= 97:
33             row_temp_x1 = ord(indicies_name_value[name_range][0][0]) - 97
34         else:
35             row_temp_x1 = ord(indicies_name_value[name_range][0][0]) - 65
36         if ord(indicies_name_value[name_range][1][0]) >= 97:
37             row_temp_x2 = ord(indicies_name_value[name_range][1][0]) - 97
38         else:
39             row_temp_x2 = ord(indicies_name_value[name_range][1][0]) - 65
40         row_temp_y1 = int(indicies_name_value[name_range][0][1:]) - 1
41         row_temp_y2 = int(indicies_name_value[name_range][1][1:]) - 1
42         indicies_number_value.append((row_temp_x1,row_temp_y1,row_temp_x2,row_temp_y2))
43     return indicies_number_value
44 
45 # calculate tip box clearance height; dependent on tipbox location
46 def clearance_height(tipbox_location, clearance_height_tipbox_z, tip_length):
47     if tipbox_location > 3: 
48         return clearance_height_tipbox_z + tip_length 
49     else:
50         return clearance_height_tipbox_z 
51 
52 # serial dilution function
53 def dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final):
54     from machine_interface import MachineConnection
55     with MachineConnection('/var/run/dsf/dcs.sock') as m:
56         m.gcode("T0") # pick up tool
57         print("Tool picked up")
58         m.move(Z = clearance_height_tipbox_z) # move to tipbox clearance height    
59         tip_counter = 0  
60         # define range of wells to be used
61         for well_range in well_limit_number: 
62             for well_counter_x in range(well_range[0],well_range[2]+1):
63                 well_counter_range_y_lower = 0
64                 well_counter_range_y_upper = well_arrangement_colrow[1] - 1
65                 if well_counter_x == well_range[0]:
66                     well_counter_range_y_lower = well_range[1]
67                 if well_counter_x == well_range[2]:
68                     well_counter_range_y_upper = well_range[3] - 1
69                 for well_counter_y in range(well_counter_range_y_lower,well_counter_range_y_upper+1):
70                     # calculate tip pickup location
71                     tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//(tip_arrangement_colrow[1])) * tip_separation_xy[0] # floor division
72                     tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%(tip_arrangement_colrow[1])) * tip_separation_xy[1] # tip pickup location (Y) = Top right tip location + ((remainder of tip counter/tip arrangment) * tip separation)
73                     tip_counter += 1
74                     print(tip_pickup_x, tip_pickup_y, "tip pickup")
75                     m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above pipette tip
76                     m.gcode("""M98 P"/macros/pickup_tip" """)  # call the macro to pick up tip
77                     # calculate pickup well location
78                     well_sample_pickup_x = wellplate_A1_absolute_location[0] + well_counter_x * well_separation_xy[0]
79                     well_sample_pickup_y = wellplate_A1_absolute_location[1] + well_counter_y * well_separation_xy[1]
80                     print(well_sample_pickup_x, well_sample_pickup_y, "draw from well")
81                     m.move(X = well_sample_pickup_x , Y = well_sample_pickup_y) # move above well
82                     m.move(Z = wellplate_liquid_pickup_height_z) # bed moves up, tip submerged
83                     m.gcode("""M98 P"/macros/prime_tip" """) # call the marco to prime tip
84                     m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
85                     m.move(Z = clearance_height_wellplate_z) # bed moves down
86                     # calculate dispense well
87                     well_sample_dispense_x = well_sample_pickup_x 
88                     well_sample_dispense_y = well_sample_pickup_y + well_separation_xy[1]
89                     if well_sample_dispense_y > (wellplate_A1_absolute_location[1] + (tip_arrangement_colrow[1]-1)*tip_separation_xy[1]): # if liquid was drawn from the last well in a column, move to top of next column to dispense
90                         well_sample_dispense_x = well_sample_pickup_x + well_separation_xy[0]
91                         well_sample_dispense_y = wellplate_A1_absolute_location[1]
92                     print(well_sample_dispense_x, well_sample_dispense_y, "dispense into well")
93                     m.move(X = well_sample_dispense_x , Y = well_sample_dispense_y) # move above well
94                     m.move(Z = wellplate_liquid_dispense_height_z) # bed moves up, tip submerged
95                     m.gcode("""M98 P"/macros/mix_liquid" """) # call the macro to mix liquid
96                     print("mixing done")
97                     m.move(Z = clearance_height_z) # bed moves down to tipbox clearance height           
98                     m.gcode("""M98 P"/macros/eject_tip" """)  # call the macro to throw out tip
99                     print("tip ejected")
100                    tip_counter_final = tip_counter # track of how many tips used
101    return tip_counter_final
102
103 # MALDI spotting function
104 def maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final):
105    from machine_interface import MachineConnection
106    with MachineConnection('/var/run/dsf/dcs.sock') as m:
107        m.gcode("T0") # pick up tool
108        print("Tool picked up")
109        m.move(Z = clearance_height_tipbox_z) # bed moves down to tipbox clearance height  
110        tip_counter = 0
111        tip_counter_final = 0
112        # For sample spot on MALDI plate
113            # define range of wells to be used
114        for well_range in well_limit_number:
115            for well_counter_x in range(well_range[0],well_range[2]+1):
116                well_counter_range_y_lower = 0
117                well_counter_range_y_upper = well_arrangement_colrow[1] - 1 
118                if well_counter_x == well_range[0]:
119                    well_counter_range_y_lower = well_range[1]
120                if well_counter_x == well_range[2]:
121                    well_counter_range_y_upper = well_range[3] - 1
122                for well_counter_y in range(well_counter_range_y_lower,well_counter_range_y_upper+1):
123                    # calculate tip pickup location
124                    tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//(tip_arrangement_colrow[1])) * tip_separation_xy[0]
125                    tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%(tip_arrangement_colrow[1])) * tip_separation_xy[1]
126                    print(tip_pickup_x, tip_pickup_y, "tip pickup")
127                    m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above top                  
128                    m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
129                    # calculate pickup well location
130                    well_sample_pickup_x = wellplate_A1_absolute_location[0] + well_counter_x * well_separation_xy[0]
131                    well_sample_pickup_y = wellplate_A1_absolute_location[1] + well_counter_y * well_separation_xy[1]
132                    print(well_sample_pickup_x, well_sample_pickup_y, "draw from well")
133                    m.move(X = well_sample_pickup_x , Y = well_sample_pickup_y) # move above well
134                    m.move(Z = wellplate_liquid_pickup_height_z)
135                    m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
136                    m.gcode("""M98 P"/macros/draw_20ul" """) # CHANGE FEED RATE IN MACRO # call the macro to draw liquid
137                    m.move(Z = clearance_height_wellplate_z)
138                    # calculate dispense location
139                    for replicate_count in range(0, number_of_replicates_m):
140                        spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * ((number_of_replicates_m * tip_counter + replicate_count) % spot_arrangement_colrow[0]))
141                        spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * ((number_of_replicates_m * tip_counter + replicate_count) // spot_arrangement_colrow[0])
142                        print(spot_dispense_x, spot_dispense_y, "dispense on spot")
143                        m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
144                        m.move(Z = maldi_dispense_height_z)                
145                        m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid                    
146                        m.move(Z = clearance_height_maldi_z)
147                    m.move(Z = clearance_height_z)            
148                    m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
149                    print("tip ejected")
150                    tip_counter += 1
151                    tip_counter_final = tip_counter
152
153        # For buffer spot on MALDI plate
154        for maldi_spot_count in range(0, tip_counter_final * number_of_replicates_m): 
155            if maldi_spot_count % number_of_replicates_m == 0:
156                m.move(Z = clearance_height_z)            
157                m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
158                print("tip ejected")
159                # calculate tip pickup location
160                tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//tip_arrangement_colrow[1]) * tip_separation_xy[0]
161                tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%tip_arrangement_colrow[1]) * tip_separation_xy[1]
162                print(tip_pickup_x, tip_pickup_y, "tip pickup")
163                m.move (Z = clearance_height_tipbox_z)
164                m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above tip            
165                m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
166                # calculate buffer location
167                buffer_location_x = wellplate_A1_absolute_location[0] + well_separation_xy[0] * buffer_location_number[0]
168                buffer_location_y = wellplate_A1_absolute_location[1] + well_separation_xy[1] * buffer_location_number[1]
169                print(buffer_location_x, buffer_location_y, "buffer taken from well")
170                m.move(X = buffer_location_x, Y = buffer_location_y) # move above buffer well
171                m.move( Z = wellplate_liquid_pickup_height_z)
172                m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
173                print("tip primed")
174                m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
175                print("liquid draw")
176                m.move(Z = clearance_height_wellplate_z)
177                tip_counter += 1
178                tip_counter_final = tip_counter
179            # calculate dispense location on MALDI plate
180            spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * (maldi_spot_count % spot_arrangement_colrow[0])) 
181            spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * (maldi_spot_count // spot_arrangement_colrow[0])
182            print(spot_dispense_x, spot_dispense_y, "buffer added to spot")
183            m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
184            m.move(Z = maldi_dispense_height_z)
185            m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid
186            print("buffer dispensed")
187            m.move(Z = clearance_height_maldi_z)
188
189
190        # Accept matrix addition
191            # this provides a pause in method for incubation and rinsing
192        while True:
193            continue_response = input("Would you like to proceed with adding matrix? [y] yes [n] no: ")
194            if continue_response == 'y':
195                break
196
197        # For matrix spot on MALDI plate
198        for maldi_spot_count in range(0, tip_counter_final * number_of_replicates_m):
199            if maldi_spot_count % number_of_replicates_m == 0:
200                m.move(Z = clearance_height_z)
201                m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
202                print("tip ejected")
203                m.move(Z = clearance_height_tipbox_z)
204                # calculate tip pickup location
205                tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//tip_arrangement_colrow[1]) * tip_separation_xy[0]
206                tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%tip_arrangement_colrow[1]) * tip_separation_xy[1]
207                print(tip_pickup_x, tip_pickup_y, "tip pickup")
208                m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above tip
209                m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
210                # calculate matrix location
211                matrix_location_x = wellplate_A1_absolute_location[0] + well_separation_xy[0] * matrix_location_number[0]
212                matrix_location_y = wellplate_A1_absolute_location[1] + well_separation_xy[1] * matrix_location_number[1]
213                print(matrix_location_x, matrix_location_y, "matrix taken from well")
214                m.move(X = matrix_location_x, Y = matrix_location_y) # move above matrix well
215                m.move( Z = wellplate_liquid_pickup_height_z)
216                m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
217                print("tip primed")
218                m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
219                print("liquid draw")                               
220                m.move(Z = clearance_height_wellplate_z)
221                tip_counter += 1
222                tip_counter_final = tip_counter
223            # Calculate dispense location on MALDI plate
224            spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * (maldi_spot_count % spot_arrangement_colrow[0])) 
225            spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * (maldi_spot_count // spot_arrangement_colrow[0])
226            m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
227            print(spot_dispense_x, spot_dispense_y, "matrix added to spot")
228            m.move(Z = maldi_dispense_height_z)
229            m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid
230            print("matrix dispense")
231            m.move(Z = clearance_height_maldi_z)
232        m.move(Z = clearance_height_z)
233        m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to eject tip
234        print("tip ejected")
235    return tip_counter_final
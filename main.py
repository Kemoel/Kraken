1 from config import *
2 from input import *
3 from lib import *
4 
5 def main():
6     tipbox_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, tip_A1_xy, tipbox_location)
7     wellplate_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, well_A1_xy, wellplate_location)        
8     clearance_height_z = clearance_height(tipbox_location, clearance_height_tipbox_z, tip_length)
9     tip_counter_final_main = 0
10    if process == 's':
11        well_limit_number = name_index_to_number_index(dilution_ranges_name) # translate wells used into computer language
12        tip_counter_final_main = dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final_main)
13    if process == 'm':
14        well_limit_number = {(0,0,(number_of_replicates_m-1) // 12,(number_of_replicates_m-1) % 12)}
15        maldi_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, plate1_spotA1_xy, maldiplate_location) #need to measure locations
16        buffer_location_number = name_index_to_number_index_single(buffer_location)
17        matrix_location_number = name_index_to_number_index_single(matrix_location)
18        tip_counter_final_main = maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final_main)
19    if process == 'sm':
20        well_limit_number = name_index_to_number_index(dilution_ranges_name) # translate wells used into computer language
21        maldi_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, plate1_spotA1_xy, maldiplate_location) #need to measure locations
22        buffer_location_number = name_index_to_number_index_single(buffer_location)
23        matrix_location_number = name_index_to_number_index_single(matrix_location)
24        # check info
25        tip_counter_final_main = dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final_main)
26        tip_counter_final_main = maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final_main)
27    from machine_interface import MachineConnection
28    with MachineConnection('/var/run/dsf/dcs.sock') as m:
29        m.gcode("T-1")
30
31
32 if __name__ == "__main__": # this needs fixed/more added
33    process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location = input_func()
34    main()
35    print("Serial dilution complete on",*dilution_ranges_name.values())1
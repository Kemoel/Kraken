1  import re
2  import lib
3  
4  
5  
6  # allowed values/limits
7  options_process = {'s' : 'serial dilution', 'm' : 'MALDI', 'sm' : 'serial dilution and MALDI plate spot'}
8  slot_range = range(1,6+1)
9  volume_range = range(1,20+1)
10 maldi_range = range(1,96+1)
11 maldi_spot_volume = 1 # Î¼L
12 
13 
14 # User inputs to define method
15 def input_func():
16     while True:
17 
18         agreement, end_flg = None, None
19         process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location = None, None, None, None, None, None, None, None
20 
21         print('---------------------------------------')
22         # method identification; all values optional 
23         method_name = input("Enter method name: ")
24         user_name = input("Enter user name: ")
25         date = input("Enter date: ")
26         comment = input("Comments: ")
27         print('---------------------------------------')
28 
29         # Select method
30         while True:
31             [print(key,':',value) for key, value in options_process.items()] # display process options (serial dilution, maldi, both)
32             process = input("What would you like to do? ") # user selects process 
33             if process in options_process: 
34                 break # exit loop if process selected in process options
35             print('invalid response') # return to start of loop if process selected not in options 
36         print('---------------------------------------')
37 
38         # Input object locations
39         while True:
40             try:
41                 tipbox_location = int(input("What slot is the tipbox in? ")) # enter slot number (integer value)
42             except:
43                 print('invalid response not a valid slot') # return if non-integer value is entered; stops error 
44             else:
45                 if tipbox_location in slot_range: 
46                     break # exit loop if slot number in range
47                 print('invalid response  not a valid slot') # return to start of loop if slot number not in range
48         print('---------------------------------------')
49 
50         while True:
51             try:
52                 wellplate_location = int(input("What slot is the 96 well plate in? ")) # enter slot number (integer value)
53             except:
54                 print('invalid response - not a valid slot') # stops error if non-integer value is entered
55             else: 
56                 if (wellplate_location in slot_range) and (wellplate_location != tipbox_location): 
57                     break # exit loop if slot number in range AND not already filled
58                 print('invalid response - not a valid slot') # return to start of loop if slot number not in range OR slot already filled
59         print('---------------------------------------')
60 
61         # For Serial Dilution then MALDI Plate Spot
62         if process == 'sm':
63             while True:
64                 try:
65                     maldiplate_location = int(input("What slot is the MALDI plate in? ")) # enter slot number (integer value)
66                 except:
67                     print('invalid response - not a valid slot') # stops error if non-integer value is entered
68                 else:
69                     if (maldiplate_location in slot_range) and (maldiplate_location != tipbox_location) and (maldiplate_location != wellplate_location):
70                         break # exit loop if slot number in range AND not already filled
71                     print('invalid response - not a valid slot') # return to start of loop if slot number not in range OR slot already filled
72             print('---------------------------------------')
73 
74         # Input sample details for serial dilution (number, name, desired dilution ranges)
75         if process == 's' or process == 'sm':
76             while True:
77                 try:
78                     number_of_samples_s = int(input("Number of samples: ")) # enter number of samples (integer)
79                 except:
80                     print('invalid response') # stops error if non-integer value is entered
81                 else:
82                     dilution_ranges_name = {} # create dictionary
83                     for counter_s in range(number_of_samples_s):
84                         dilution_name = input(f"Sample {counter_s+1} name: ") # enter sample name; can be letter or integer
85                         while dilution_name in dilution_ranges_name: # confirm sample name is unique
86                             print("All samples must have unique names.")
87                             dilution_name = input(f"Enter diffrent sample {counter_s+1} name: ") # enter new sample name if not unique
88                         range_temp = input(f"{dilution_name} - Sample Range (eg.A1-A6): ") # enter serial dilution range; single values not accepted
89                         while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2])[-][A-H]([1-9]|1[0-2]))$|^([A-H]([1-9]|1[0-2]))$'),range_temp)): # confirm dilution range is valid
90                             print("All samples must have valid range.")
91                             range_temp = input(f"{dilution_name} - Sample Range (eg.A1-A6): ") # enter new dilution range if not valid
92                         dilution_ranges_name[dilution_name] = tuple(range_temp.split('-'))
93                     if dilution_ranges_name != [('',)]: # WHAT IS THIS?
94                         break
95                     print('invalid response')
96             print('---------------------------------------')
97             
98             # unnecessary
99             # while True:
100            #     print("Valid volume range", volume_range[0], "-", volume_range[-1], "Î¼L")
101            #     dilution_volume = int(input("What is the transfer volume? "))
102            #     if dilution_volume in volume_range:
103            #         break
104            # print('---------------------------------------')
105        
106        # Input sammple details for maldi spot FOLLOWING serial dilution
107        if process == 'sm':
108            # Sample Number
109            while True:
110                agreement_sm = input("Spot all serial dilution wells on MALDI plate? [y] yes [n] no: ") # confirm sample number
111                if agreement_sm == 'y':
112                    break # exit loop if all serial dilution samples are to be spotted on MALDI plate
113                if agreement_sm == 'n': # specify range if subset of serial dilution samples are to be spotted on MALDI plate
114                    print('Specify range to spot on MALDI plate')
115                    sample_ranges_sm = {} # create dictionary of sample ranges
116                    for counter_sm in dilution_ranges_name: # for each named dilution range input samples to spot on MALDI plate
117                        range_temp = input(f'{counter_sm} - Sample Range (eg.A1-A6): ') #fix issue w putting single value in range
118                        while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2])[-][A-H]([1-9]|1[0-2]))$|^([A-H]([1-9]|1[0-2]))$'),range_temp)): # confirm sample range is valid
119                            print("All samples must have valid range.")
120                            dilution_name = input(f"Enter diffrent sample {counter_sm+1} range: ") # enter new sample range if not valid
121                        sample_ranges_sm[counter_sm] = tuple(range_temp.split('-')) # split tuple
122                    if sample_ranges_sm != [('',)]: # add check for overlapping dilution ranges/ out of range
123                        break
124                print('invalid response')
125            print('---------------------------------------')
126            # Replicate Number
127            while True:
128                try:
129                    number_of_replicates_m = int(input("Number of replicates for each sample: ")) # enter number of replicates (integer)
130                except:
131                    print('invalid response') # stops error if non-integer value is entered
132                else:
133                    break
134            print('---------------------------------------')
135            # Buffer Location
136            while True:
137                try:
138                    buffer_location = input("What well is the buffer in? (ex. A6) ") # enter buffer location
139                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),buffer_location)): # confirm location valid
140                        buffer_location = input("invalid response - not a valid well ")
141                except:
142                    print('invalid response')
143                else:
144                    buffer_location = tuple(buffer_location.split('-')) # ???????
145                    break
146            print('---------------------------------------')
147            # Matrix Location 
148            while True:
149                try:
150                    matrix_location = input("What well is the matrix in? (ex. A6) ") # enter matrix location
151                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),matrix_location)): # confirm location valid
152                        matrix_location = input("invalid response - not a valid well ")
153                except:
154                    print('invalid response')
155                else: #fix me pls
156                    matrix_location = tuple(matrix_location.split('-'))
157                    break
158            print('---------------------------------------')
159
160        # For MALDI Plate Spot
161        if process == 'm':
162            # MALDI plate location
163            while True:
164                try:
165                    maldiplate_location = int(input("What slot is the MALDI plate in? ")) # enter MALDI plate location (integer)
166                except:
167                    print('invalid response - not a valid slot')
168                else:
169                    if (maldiplate_location in slot_range) and (maldiplate_location != tipbox_location) and (maldiplate_location != wellplate_location):
170                        break # exit loop if location is in range and not already filled
171                    print('invalid response - not a valid slot')
172            print('---------------------------------------')
173            
174            # Sample number, location, replicates
175                # Here it is assumed sample 1 is in well A1; subsequent samples move down A until A12 then move to B1 and continue as such
176            while True:
177                try:
178                    number_of_samples_m = int(input("Number of samples: ")) # enter number of samples (integer)
179                    number_of_replicates_m = int(input("Number of replicates for each sample: ")) # enter number of replicates (integer)
180                except:
181                    print('invalid response') # stops error if non-integer entered
182                else:
183                    if(number_of_samples_m*number_of_replicates_m) <= maldi_range[-1]: # if number of samples greater than plate capacity return error
184                        break            
185                    print('Sample count exceeds plate.')   
186            print('---------------------------------------')
187            
188            # Buffer location
189            while True:
190                try:
191                    buffer_location = input("What well is the buffer in? (ex. A6) ") # enter buffer location
192                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),buffer_location)): # confirm location valid
193                        buffer_location = input("invalid response - not a valid well ")
194                except:
195                    print('invalid response')
196                else: # remove?
197                    buffer_location = tuple(buffer_location.split('-'))
198                    break
199            print('---------------------------------------')
200            while True:
201                try:
202                    matrix_location = input("What well is the matrix in? (ex. A6) ") # enter matrix location
203                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),matrix_location)): # confirm location valid
204                        matrix_location = input("invalid response - not a valid well ")
205                except:
206                    print('invalid response')
207                else: #fix me pls # remove?
208                    matrix_location = tuple(matrix_location.split('-'))
209                    break
210            print('---------------------------------------')
211            
212
213        # Method Summary: all input values printed at end of setup
214        print('Method Name:', method_name)
215        print('User:', user_name)
216        print('Date:', date)
217        print('Comments:', comment)
218        print('Process:', options_process[process])
219        print('Tipbox Slot:', tipbox_location)
220        print('96 Well Plate Slot:', wellplate_location)
221
222        # serial dilution
223        if process == 's':
224            print('Dilution Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
225            print('Transfer Volume (Î¼L):', dilution_volume)  # Not working rn because in macro
226
227        # maldi spot
228        if process == 'm':
229            print('MALDI Plate Slot:', maldiplate_location)
230            print('Number of Samples:', number_of_samples_m)
231            print('Number of Replicates:', number_of_replicates_m)
232            print('Buffer Location:', buffer_location)
233            print('Matrix Location:', matrix_location)
234            print(f'Default Spot Volume {maldi_spot_volume}Î¼L.')
235            print('Note: Samples collected from default locations.') # default locations as previously described
236
237        # combined method
238        if process == 'sm':
239            print('MALDI Plate Slot:', maldiplate_location)
240            print('Dilution Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
241            print('Transfer Volume (Î¼L):', dilution_volume) # Not working rn because in macro
242            if agreement_sm == 'y':
243                print('Sample Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
244            else:
245                print('Sample Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in sample_ranges_sm.items()]
246            print('Number of Replicates:', number_of_replicates_m)
247            print(f'Default spot volume {maldi_spot_volume}Î¼L.')
248        print('---------------------------------------')
249
250        # Method Confirmation
251        while agreement != 'n':
252            print('Ensure tip box is full.')
253            agreement = input("Review method. Correct? [y] yes [n] no: ")
254            if agreement == 'y': 
255                end_flg = True
256                break # If method correct, exit loop and start run
257            elif agreement == 'n':
258                print('restarting') 
259                break # if method incorrect, return to start of input         
260            else:
261                print('invalid response')
262        
263        if end_flg == True:
264            break
265    
266    # Start Run
267    return process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location, number_of_samples_m
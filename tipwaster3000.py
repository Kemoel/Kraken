from machine_interface import MachineConnection

# This program is sorta a joke, sorta not - it throws a row of pipette tips into the trash,
# starting from tip A0, in the back-middle bed slot.




with MachineConnection('/var/run/dsf/dcs.sock') as m:


    # First, we pickup the pipette head and move the work surface to a safe clearance plane.
    m.gcode("T0")
    m.move(Z = 150)


    for i in range(8):
        
        # For each of the pipette tips, move above them
        m.move(X = 117.8 + i * 9, Y = 139)
        # Call the macro to pick them up
        m.gcode("""M98 P"/macros/pickup_tip" """)
        # and call the macro to throw them out
        m.gcode("""M98 P"/macros/eject_tip" """)
        
    
    
    # Finally, put the pipette head back in its holder, ready to waste pipette tips another day.
    m.gcode("T-1")

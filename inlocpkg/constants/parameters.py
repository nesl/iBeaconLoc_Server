# ===== BEACON SETUP =====
# major, minor, x, y
BEACON_INFORMATION = ( (4, 0, 7.5, 0.25),
					   (4, 1, 0.25, 2.5),
					   (4, 2, 0.25, 8.0),
					   (4, 3, 7.25, 10.6),
					   (4, 4, 7.25, 4.1))

# user interfacegonna 
UI_MONITORSIZE = (1280,980) # pixels
UI_MAPSIZE = (9.1, 10.6) # meters

# estimation
ESTIMATION_PERIOD = 1.0 # seconds
WEIGHT_COEFFICIENT = 1.2
LOWPASS_COEFFICIENT = 0.75

# TX powers
TXPOW_HIGH = -74 
TXPOW_LOW  = -90

# Battery capacities
BATTERYCAP_2AA = (1.250*1.5*2.0)
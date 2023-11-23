import requests
import numpy as np
import h5py

QEC = "3.0.0" # Version number for challenge, can check with site for compatability, will provide appropriate error message when different to server to help communicate with teams that urgent updates are needed
URL = "https://sim.quantumnextgen.com.au/"

def load_dataset(filename,scenario):
    #input 1 is the file path string
    #input 2 is an integer from 0-1000 and is the scenario
    #this function loads and returns the 3x101x101 magnetic field dataset as well as 3x1 magnetic dipole.
    hf = h5py.File(filename,'r')
    subset = 'D%04d' % scenario #format is D0000 upto 1000
    data = hf.get(subset) 
    data = np.array(data)
    print('Scenario '+ subset + ' is loaded')

    mine_dipole = hf.get(subset).attrs['mine_dipole']
    print("The Dipole is: ", mine_dipole)
    hf.close()
    return data, mine_dipole

def load_answers(filename,scenario):
    #input is same as load_dataset
    #retruns 2xN array of mine positions
    #Will only work on training data 
    hf = h5py.File(filename,'r')
    subset = 'D%04d' % scenario #format is D0000 upt to 1000
    mine_positons = hf.get(subset).attrs['mine_position']
    hf.close()
    return mine_positons

def submit_answers(mine_estimates, stage, authkey):
    mine_estimates = serialize_array(mine_estimates)
    #creates JSON form data for HTTP request
    payload = {"answers":mine_estimates}
    
    #sends data to site, stores in variable r
    r = post_to_server(payload, (str(stage) + "/" + authkey))
    if r.status_code != 200:
        raise Exception(r.text)
    else:
        #return to user the actual value of the request, removing header and online data that is unneeded
        return r.text
    
def estimate_check(mine_positions,mine_estimates):
    #each input is a 2xN array where N is the number of mines/estimates.
    #for each row first element is the position in the East direction and the second is the position in the North direction.
    #Each input can have a diferent N.

    #this function returns false if the estimated number of mines is outside the accepeted 100%-110% range
    #otherwise this function returns the Hausdorff distance in meters.

    N_est = len(mine_estimates[0])
    N_mines = len(mine_positions[0])

    if N_est<N_mines:
        #print("False Negative!: Fail")
        return False
    if N_est>N_mines*1.1:
        #print('Over 10% False Positive!: Fail')
        return False

    from scipy.spatial.distance import directed_hausdorff

    #this direction is the main preformance index.
    haus_est = []
    haus_mines = []
    for i in range(N_est):
        haus_est.append([mine_estimates[0][i],mine_estimates[1][i]])
    for i in range(N_mines):
        haus_mines.append([mine_positions[0][i],mine_positions[1][i]])
    #this direction is the main preformance index.
    return directed_hausdorff(haus_mines, haus_est)[0]

def plot_data(data, mine_position):
    import matplotlib.pyplot as plt

    data = np.asarray(data)

    #Organise data
    mine_position = np.transpose(mine_position)
    bx = np.transpose(data[0,:,:])
    by = np.transpose(data[1,:,:])
    bz = np.transpose(data[2,:,:])

    Max_b = np.max(data)
    Min_b = np.min(data)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, sharey=True)
    im1 = ax1.imshow(bx,origin='lower', aspect='equal', vmin=Min_b, vmax=Max_b)
    im2 = ax2.imshow(by,origin='lower', aspect='equal', vmin=Min_b, vmax=Max_b)
    im3 = ax3.imshow(bz,origin='lower', aspect='equal', vmin=Min_b, vmax=Max_b)
    plt.scatter(mine_position[:,0],mine_position[:,1],marker='x', c='r')
    ax1.set(xlabel='Eastings (m)', ylabel='Northings (m)')
    ax2.set(xlabel='Eastings (m)')
    ax3.set(xlabel='Eastings (m)')
    cb = plt.colorbar(im1, ax = [ax1, ax2, ax3],location="bottom") # adding the colobar on the right
    cb.set_label(label='B (Tesla)')
    plt.show()

def plot_scenario(source, scenario):
    (data, dipole) = load_dataset(source, scenario)
    try:
        mine_positions = load_answers(source,scenario)
    except:
        mine_positions = [[],[]]
    plot_data(data, mine_positions)

def post_to_server(payload, ref=""):
    return requests.post(URL+ref, json=payload, headers={'QeC':QEC})

def get_from_server(payload, ref=""):
    return requests.get(URL+ref, json=payload, headers={'QEC':QEC})

def serialize_array(array):
    print(array)
    output = []
    for i in array:
        print(i)
        if isinstance(i, np.ndarray):
            i.tolist()
            output.append(serialize_array(i))
        elif isinstance(i, list):
            output.append(serialize_array(i))
        else:
            output.append(i)
    return output

# 
def survey_flight(filename, scenario):
    dr = Drone_Sim(filename, scenario)
    survey_path(dr)
    #shape array for 2d plotting
    bx = np.reshape(dr.b_east_drone, (101, 101)).T
    by = np.reshape(dr.b_north_drone, (101, 101)).T
    bz = np.reshape(dr.b_up_drone, (101, 101)).T
    #flip every 2nd row (raster back and forth flight)
    bx[:,1::2] = bx[::-1, 1::2]
    by[:,1::2] = by[::-1, 1::2]
    bz[:,1::2] = bz[::-1, 1::2]
    return [bx, by, bz]

# 
def survey_flight_online(token, scenario):
    dr = Drone_Sim_Online(token, scenario)
    survey_path(dr)
    #shape array for 2d plotting
    bx = np.reshape(dr.b_east_drone, (101, 101)).T
    by = np.reshape(dr.b_north_drone, (101, 101)).T
    bz = np.reshape(dr.b_up_drone, (101, 101)).T
    #flip every 2nd row (raster back and forth flight)
    bx[:,1::2] = bx[::-1, 1::2]
    by[:,1::2] = by[::-1, 1::2]
    bz[:,1::2] = bz[::-1, 1::2]
    return [bx, by, bz]

# 
def survey_path(drone):
    for i in range(drone.Borders[0],drone.Borders[1]):
        for k in range(drone.Borders[0],drone.Borders[1]):
            #we already have the 00 point
            if i==0 and k==0:
                continue
            #traveling back down the grid on odd k's
            if (i % 2) == 0:
                j = k
            else:
                j = 100-k
            drone.move(i,j)

# For brute force re-organisation
# TODO Average data if sharing the same point.
def reorg_dronedata(drone):
    east = np.empty((101,101), dtype=float)
    north = np.empty((101,101), dtype=float)
    up = np.empty((101,101), dtype=float)
    for i in range(drone.time_step):
        e = drone.position_East[i]
        n = drone.position_North[i]
        east[e][n] = drone.b_east_drone[i]
        north[e][n] = drone.b_north_drone[i]
        up[e][n] = drone.b_up_drone[i]
    return [east, north, up]

class Drone_Sim: # Capitalised to meet style guidelines.
    # CLASS VARIABLES
    start_Position_East = [0] # Determine where on Eastings the drone starts
    start_Position_North = [0] # Determine where on Northings the drone starts
    start_time_step = 0 # Determine what timestep the drone starts on
    
    Borders =[0,101] # Set borders of the area
    max_velovity = 0.283*10 # maximum velocity permitted per timestep
    
    #noise_mag = 0.3e-12 total magnitude (T)
    #sensor_noise = ((noise_mag**2)/3)**0.5
    sensor_noise = 1.7320508e-13
    
    Dataset = '\dataset_location.h5'

    def __init__(self, dataset_location, scenario_number): #changed to regular init Class, set dataset_location to optional
        # INSTANCE VARIABLES 
        (self.data, self.mine_dipole) = load_dataset(dataset_location,scenario_number) # loads specific scenario data
        self.position_East = [0] # sets starting east position
        self.position_North = [0] # sets starting north position
        self.time_step = self.start_time_step # set time step for scenario to 0
        self.b_east_drone = [] # Array for tracking reading at point in East
        self.b_north_drone = [] # Array for tracking reading at point in North 
        self.b_up_drone = [] # Array for tracking reading at point in Up

        self.perform_read() #Get the starting reading for 0,0

    def perform_read(self):
        b = self.data[:,self.position_East[-1],self.position_North[-1]] # for all three axis, get the reading at the last position (most recent) in East and North
        b=np.squeeze(b) #Pop out what we need
        noise_array = np.random.normal(0, self.sensor_noise,b.size) # Create a normalised noise reading for the three axis
        b_noise = np.sum(np.column_stack((b,noise_array)),axis=1) # Sum the noise to the true reading # consider b + noise_array, since we are adding matrixes
        self.b_east_drone.append(b_noise[0]) # Get noisified reading for east
        self.b_north_drone.append(b_noise[1]) # Get the noisified reading for north
        self.b_up_drone.append(b_noise[2]) # Get the noisified reading for up
        return b_noise

    def move(self, pos_east, pos_north):
        if pos_east > self.Borders[1] or pos_east < self.Borders[0] or pos_north > self.Borders[1] or pos_north < self.Borders[0]:
            #position outside bounds
            raise Exception("position exceeds bounds")
            return False
        if pos_east%1>0 or pos_north%1>0:
            #position not an integer
            raise Exception("position exceeds bounds")
            return False 
        if abs(self.position_East[-1]-pos_east) > 2 or abs(self.position_North[-1]-pos_north) > 2:
            #Going too fast
            raise Exception("moved too fast")
            return False
        
        self.time_step += 1

        self.position_East.append(pos_east)
        self.position_North.append(pos_north)

        self.perform_read()

########################
### ONLINE DRONE SIM ###
########################

class Drone_Sim_Online: # Capitalised to meet style guidelines.
    # CLASS VARIABLES
    start_Position_East = [0] # Determine where on Eastings the drone starts
    start_Position_North = [0] # Determine where on Northings the drone starts
    start_time_step = 0 # Determine what timestep the drone starts on
    
    Borders =[0,101] # Set borders of the area
    max_velovity = 0.283*10 # maximum velocity permitted per timestep

    token = ""

    def __init__(self, token, scenario_number): #changed to regular init Class, set dataset_location to optional
        # INSTANCE VARIABLES 
        self.token = token
        self.scenario = scenario_number
        self.ref = '3/'+self.token+'/'+str(self.scenario)
        # LOAD FROM ONLINE
        self.server_check()

    def perform_read(self):
        payload = {"move":[self.position_East[-1],self.position_North[-1]]}
        response = post_to_server(payload, self.ref)
        data = response.json()
        b_noise = data['b_noise']
        self.b_east_drone.append(b_noise[0])
        self.b_north_drone.append(b_noise[1]) # Get the noisified reading for north
        self.b_up_drone.append(b_noise[2]) # Get the noisified reading for up
        
    def move(self, pos_east, pos_north):
        if pos_east > self.Borders[1] or pos_east < self.Borders[0] or pos_north > self.Borders[1] or pos_north < self.Borders[0]:
            #position outside bounds
            raise Exception("position exceeds bounds")
            return False
        if pos_east%1>0 or pos_north%1>0:
            #position not an integer
            raise Exception("position exceeds bounds")
            return False 
        if abs(self.position_East[-1]-pos_east) > 2 or abs(self.position_North[-1]-pos_north) > 2:
            #Going too fast
            raise Exception("moved too fast")
            return False
        
        # ONLINE ACTIONS OCCUR HERE
        self.perform_read()

        self.time_step += 1
        self.position_East.append(pos_east)
        self.position_North.append(pos_north)
        # LOCAL ACTIONS FOR SPEED END HERE

    def server_check(self):
        response = get_from_server({},('3/'+self.token+'/'+str(self.scenario)))
        data = response.json()
        self.position_East = data['pos_east'] # sets starting east position
        self.position_North = data['pos_north'] # sets starting north position
        self.time_step = data['time_step'] # set time step for scenario to 0
        self.b_east_drone = data['b_east'] # Array for tracking reading at point in East
        self.b_north_drone = data['b_north'] # Array for tracking reading at point in North 
        self.b_up_drone = data['b_up'] # Array for tracking reading at point in Up
        self.mine_dipole = data['mine_dipole']
        print('Online Drone ' + str(self.scenario) + ' is loaded')
        print("The Dipole is: ", self.mine_dipole)
        # CONSIDER SEPARATE CALLS FOR B_EAST, B_NORTH, B_UP to keep calls small

    def get_current_pos(self):
        return [self.position_East[-1],self.position_North[-1]]
import requests
import numpy as np
import h5py

QEC = "1.0.0" # Version number for challenge, can check with site for compatability, will provide appropriate error message when different to server to help communicate with teams that urgent updates are needed
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


def post_to_server(payload, ref=""):
        return requests.post(URL+ref, json=payload, headers={'QeC':QEC})

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
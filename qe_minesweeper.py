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

    N_mines = np.size(mine_positions)
    N_est = np.size(mine_estimates)

    if N_est<N_mines:
        #print("False Negative!: Fail")
        return False
    if N_est>N_mines*1.1:
        #print('Over 10% False Positive!: Fail')
        return False

    from scipy.spatial.distance import directed_hausdorff

    #this direction is the main preformance index.
    return directed_hausdorff(mine_positions, mine_estimates)[0]

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
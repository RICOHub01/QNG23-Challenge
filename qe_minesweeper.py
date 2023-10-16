import requests
import numpy as np
import h5py

QEC = "0.1.0" # Version number for challenge, can check with site for compatability, will provide appropriate error message when different to server to help communicate with teams that urgent updates are needed
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
    #retruns Nx2 array of mine positions
    #Will only work on training data 
    hf = h5py.File(filename,'r')
    subset = 'D%04d' % scenario #format is D0000 upt to 1000
    mine_positons = hf.get(subset).attrs['mine_position']
    hf.close()
    return mine_positons

def submit_answers(mine_estimates, stage, authkey):
    #creates JSON form data for HTTP request
    payload = {"answers":mine_estimates}
    
    #sends data to site, stores in variable r
    r = post_to_server(payload, (stage + "/" + authkey))
    if r.status_code != 200:
        raise Exception(r.text)
    else:
        #return to user the actual value of the request, removing header and online data that is unneeded
        return r.text

def post_to_server(payload, ref=""):
        return requests.post(URL+ref, json=payload, headers={'QeC':QEC})
<p align="center">
  <img src="https://github.com/rdc-mitchell/qng23-challenge/blob/main/assets/images/Header.jpg?raw=true" alt="header"/>
</p>

# Stage 3 is now live

Key note for Stage 3, there is only 10 scenarios to be solved.

## Survey Option
**NOTE: IF YOU CHOOSE TO DOWNLOAD THE TEST DATA YOU WILL HAVE TWO HOURS TO SUBMIT IT FOR VALID ENTRY, AND YOU ARE AUTOMATICALLY ASSUMED TO HAVE TAKEN THE WORST POSSIBLE FLIGHT TIME FOR ALL SCENARIOS**

You can download the test dataset by modifying the following link with your team's authkey https://sim.quantumnextgen.com.au/3/{authkey} 

When running the `submit_answers()` function, make sure to change the stage parameter to 3.

## Drone Flight Option

You may access the serverside drone via the newly provided `Drone_Sim_Online` class.

When this class is initialised via a line like:
```
scenario_1_drone = Drone_Sim_Online(token, scenario_number=1)
``` 
It will no longer read the dataset on your computer, and instead request the information directly from the server using your token. This means that unlike the training portion, the drone is not reset everytime you recall it for the same scenario, and will instead persist across multiple attempts. This means you will have to adjust if your method fails or the connection falters mid-flight.

We have provided the new function `.get_current_pos()` as an easy way to check where the drone is currently in the scenario.

### Drone_Sim_Online
#### Initialisation
`Drone_Sim_Online(token, scenario)` uses the token provided to your team, along with the scenario to create a unique drone instance that is mostly matched locally on your machine.

#### Move
`.move(position_east, position_north)` will perform distance checks for error confirmation and then send the positions to the server for the magnetic reading in that spot in the scenario.

Returns `[b_noise_east, b_noise_north, b_noise_up]` for the new drone location.

#### Get Current Position
`.get_current_pos()` returns the current location of the drone, useful when accessing the drone at first to determine where in the scenario it has started.

Returns `[position_east, position_north]`

#### Submission
You submit like all other stages, using the `submit_answers()` function.

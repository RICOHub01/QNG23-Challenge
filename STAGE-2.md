<p align="center">
  <img src="https://github.com/rdc-mitchell/qng23-challenge/blob/main/assets/images/Header.jpg?raw=true" alt="header"/>
</p>

# Stage 2 is now live

NOTE: ONCE YOU DOWNLOAD THE TEST DATA YOU WILL HAVE TWO HOURS TO SUBMIT IT FOR VALID ENTRY

You can download your test dataset by modifying the following link with your team's authkey https://sim.quantumnextgen.com.au/2/{authkey} 

When running the `submit_answers()` function, make sure to change the stage parameter from 0 or 1 to 2.

# Stage 2

There are two major components to this in third and fourth weeks of the challenge; Training, and Stage 2.

[Training](#training) is completed offline, and uses the provided training dataset, along with functions `load_dataset()` and `load_answers()`.

[Stage 2](#stage-2) combines both elements, a fresh set of data and a time constraint. You will download a test dataset and use `load_dataset()` and `submit_answers()` to complete the stage and be scored against other teams.

# Formatting

## Datasets

Datasets are stored as hdf5 files.

Each of these hdf5 datasets contains individual scenarios denoted 'D0000' through to 'D1000'

### Magnetic Field

The primary data is a 3x101x101 double of magnetic field values where the first dimension is the vector field direction ordered in East, North and Up, and the remaining two dimensions are Eastings and Northings.

i.e. `data[2,:,:]` is the two dimensional B<sub>up</sub> data.

& `data[2,10,40]` is the B<sub>up</sub> data at Eastings 10m, Northings 40m

```python
Magnetic_Field=[
  B_east=[
    Easting_0=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_1=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_2=[Northing_0, Northing_1, Northing_2... Northing_1000]
    ...
    Easting_1000=[Northing_0, Northing_1, Northing_2... Northing_1000]
  ],
  B_north=[
    Easting_0=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_1=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_2=[Northing_0, Northing_1, Northing_2... Northing_1000]
    ...
    Easting_1000=[Northing_0, Northing_1, Northing_2... Northing_1000]
  ],
  B_up=[
    Easting_0=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_1=[Northing_0, Northing_1, Northing_2... Northing_1000],
    Easting_2=[Northing_0, Northing_1, Northing_2... Northing_1000]
    ...
    Easting_1000=[Northing_0, Northing_1, Northing_2... Northing_1000]
  ]
]
```
```python
[
  [
    [2.494e-14, −1.260e-13, −9.290e-16... −1.001e-14],
    [9.3936e-14, −1.6723e-15, 2.9003e-13... −2.165e-13],
    [−1.7494e-13, −4.8814e-13, 2.6513e-14... −1.4874e-13]
    ...
    [−2.6981e-13, 4.8392e-14, 2.3269e-13... −7.9502e-14]
  ],
  [
    [5.9242e-14, −9.0429e-14, 1.047e-13... −2.6437e-14],
    [−4.1591e-13, −1.5082e-13, −1.7875e-13... −1.5819e-13],
    [2.2981e-13, −2.3813e-13, 2.9374e-13... −1.4208e-14]
    ...
    [7.6692e-14, 1.9518e-13, −3.2368e-13... 1.5126e-13]
  ],
  [
    [2.6914e-13, −1.4688e-13, 3.7836e-13... 2.7123e-13],
    [1.2353e-13, −3.1824e-14, 5.3224e-14... 2.0195e-13],
    [−1.5399e-13, −9.9873e-14, 3.201e-13... 7.8072e-14]
    ...
    [−7.5997e-14, −2.1137e-14, −1.9027e-13... 1.0032e-14]
  ]
]
```



### Dipole

Each scenario also contains attributes.

The attribute `mine_dipole` returns a three-element array with the mine dipole moment in the East, North, Up directions in units of A.m<sup>2</sup>.

```python
Mine_Dipole=[Dipole_East, Dipole_North, Dipole_Up]
```
```python
[0.0004630278750465468,0.0035182684827414416,0.005924872028923108]
```

### Mine Positions

Some datasets will have the attribute `mine_position`, which returns an Nx2 array with the first dimension elements being mines and the second dimension corresponding to the East position followed by the North positions of the mine in meters.
```python
Mine_Positions=[
  Mine_Eastings=[Mine1Easting=Double, Mine2Easting=Double, Mine3Easting=Double...],
  Mine_Northings=[Mine1Northing=Double, Mine2Northing=Double, Mine3Northing=Double...]
]
```
```python
[
  [43.5456494880132,36.53926520147979,25.795604598985733,26.00725731020625,46.76380398701235,74.40935689205949,12.049736709577994,63.67528622219915,37.49943911758203,56.22751172065548,85.25082496219667,31.170562839713014,16.191380764031933,25.171771904128786,89.69654170791354],
  [42.88782514723049,63.02067125739154,84.62348991078048,38.23093548135795,86.34782302696689,48.99359079854869,12.257964403937498,35.4795505232131,16.856852683598085,19.26167625528886,20.890465106294087,72.90019680446693,64.79048887962827,13.513603935151961,36.62536487289766]
]
```

## Answers

Is an advanced configuration of [mine positions](#mine-positions), stacking 1000 instances of the datatype into a single array to represent answers for the entire dataset.

```python
Answers=[
  Scenario1_Mine_Positions[
    Mine_Eastings=[Mine1Easting=Double, Mine2Easting=Double, Mine3Easting=Double...],
    Mine_Northings=[Mine1Northing=Double, Mine2Northing=Double, Mine3Northing=Double...]
  ],
  Scenario2_Mine_Positions[
    Mine_Eastings=[Mine1Easting=Double, Mine2Easting=Double, Mine3Easting=Double...],
    Mine_Northings=[Mine1Northing=Double, Mine2Northing=Double, Mine3Northing=Double...]
  ],
  Scenario3_Mine_Positions[
    Mine_Eastings=[Mine1Easting=Double, Mine2Easting=Double, Mine3Easting=Double...],
    Mine_Northings=[Mine1Northing=Double, Mine2Northing=Double, Mine3Northing=Double...]
  ]
]
```
```python
[
  [
    [43.5456494880132,36.53926520147979,25.795604598985733,26.00725731020625,46.76380398701235,74.40935689205949,12.049736709577994,63.67528622219915,37.49943911758203,56.22751172065548,85.25082496219667,31.170562839713014,16.191380764031933,25.171771904128786,89.69654170791354],
    [42.88782514723049,63.02067125739154,84.62348991078048,38.23093548135795,86.34782302696689,48.99359079854869,12.257964403937498,35.4795505232131,16.856852683598085,19.26167625528886,20.890465106294087,72.90019680446693,64.79048887962827,13.513603935151961,36.62536487289766]
  ],
  [
    [36.261589206639215,86.50870571114635,43.46404467423455,22.653871151375036,62.58911552054529],
    [39.677616523499005,17.306013595479676,78.16553176036737,56.856900495052784,76.59495000471011]
  ],
  [
    [12.706235345527581,84.50917866228248,60.04606855352944,73.92687528518418,86.77987788590254],
    [55.909907295786056,31.39735602118308,17.198804284971196,35.7049710365495,74.345123410448]
  ]
]
```

# Training

In order to complete the challenge you will be required to use training data to 

## Documentation

### `load_dataset(filename, scenario)`

Open up the provided dataset and retrieve from the specified scenario (ranging from 0-999) the 3x101x101 magnetic field dataset as well as 3x1 magnetic dipole.

#### Example:

Open the dataset of scenario 4, load the 3 magnetic fields as `data`, and the 3x1 dipole data as `dipole`.
Then break the magnetic fields into their three vector fields; east, north and up.

```python
import qe_minesweeper

(data, dipole) = qe_minesweeper.load_dataset("dataset/stage2_training_dataset.h5", 4)

east = data[0]
north = data[1]
up = data[2]

print(dipole)

>>> [0.00018855036263420348,0.003962972901521309,0.005057922910620125]
```

### `load_answers(filename, scenario)`

Open up the provided dataset and retrieve from the specified scenario (ranging from 0-999) the Nx2 array containing the location of the mines in the scenario.

#### Example:

Open the dataset of scenario 76, and store the location of the five mines in the array `mine_locations`. Separate out the Eastings and Northings and assemble the location of Mine 1 in variable `mine_1`

```python
import qe_minesweeper

mine_locations = qe_minesweeper.load_answers("dataset/stage2_training_dataset.h5", 76)

east = mine_locations[0]
north = mine_locations[1]
mine_1 = (east[0], north[0])

print(mine_locations)
print(mine_1)

>>> [[35.138700415390886,25.657676745571052,52.15652811160456,54.44472370815717,35.53688743992102],[18.89473791201447,51.42367861186571,80.17380041971943,19.303343198901423,81.46877162392052]]
>>> (35.138700415390886, 18.89473791201447)
```

### `estimate_check(mine_positions, mine_estimates)`

Each input is a 2xN array where 2 is the East direction or North direction of the mines, and N is the number of mines/estimates.

ie. `mine_estimates[0]` = All the East directions of the mines \
ie. `mine_estimates[1]` = All the North directions of the mines \
ie. `mine_estimates[0][n]` & `mine_estimates[1][n]` = The East and North direction of mine n.

The first input of the function is the true known mine positions retrieved from a scenario in the dataset.
The second input of the function is the estimates of mine positions for the same scenario.

Each input can have a diferent N.

This function returns as `False` if the estimated number of mines is outside the accepted 100%-110% range.

Otherwise this function returns the Hausdorff distance in meters as a `double`.

#### Example:

Submit the `mine_positions` for `stage2_training_data.h5` and my own `mine_estimates` for scenario `9`, and recieve their Hausdorff distance in meters.

```python
import qe_minesweeper

mine_positions = qe_minesweeper.load_answers('stage2_training_data.h5',9)

our_estimates = [
  [43.5456494880132,36.53926520147979,25.795604598985733,26.00725731020625,46.76380398701235,74.40935689205949,12.049736709577994,63.67528622219915,37.49943911758203,56.22751172065548,85.25082496219667,31.170562839713014,16.191380764031933,25.171771904128786,89.69654170791354],
  [42.88782514723049,63.02067125739154,84.62348991078048,38.23093548135795,86.34782302696689,48.99359079854869,12.257964403937498,35.4795505232131,16.856852683598085,19.26167625528886,20.890465106294087,72.90019680446693,64.79048887962827,13.513603935151961,36.62536487289766]
]

result = qe_minesweeper.estimate_check(mine_positions, our_estimates)

print(result)

>>> 156.67916589066107
```

###

# Stage 2

Stage 2 will comprise of three steps.
1. Downloading a new set of test data from https://sim.quantumnextgen.com.au/2/{authkey}
2. Running your solution over the test data and producing an answer for all 1000 elements.
3. Submitting that answer to our servers using the same method as Stage 0 & 1, by running the `submit_answers()` function.

Note: 
1. This is an assessed component and thus will not have `load_answers()` available for the test dataset.
2. This is a timed component and thus once the dataset is downloaded from https://sim.quantumnextgen.com.au/2/{authkey} you will have **two hours** to run `submit_answers()` with your answers.

### `load_dataset(filename, scenario)`

Open up the provided dataset and retrieve from the specified scenario (ranging from 0-999) the 3x101x101 magnetic field dataset as well as 3x1 magnetic dipole.

#### Example:

Open the dataset of scenario 39, load the 3 magnetic fields as `data`, and the 3x1 dipole data as `dipole`.
Then break the magnetic fields into their three vector fields; east, north and up.

```python
import qe_minesweeper

(data, dipole) = qe_minesweeper.load_dataset("dataset/stage2_test_dataset.h5", 39)

east = data[0]
north = data[1]
up = data[2]

print(dipole)

>>> [0.00018855036263420348,0.003962972901521309,0.005057922910620125]
```

### `submit_answers(mine_estimates, stage, authkey)`

Provide an array of 1000xNx2 as estimates/answers for the locations of mines in the training set, along with an authkey to prove which team is submitting these answers.
The stage variable is provided to ensure that the answers are being submitted for the correct assessed dataset.

#### Example:

Submit an part of an array of mine_estimates for Stage 2, using authkey "Ty87nB".

```python
import qe_minesweeper

our_answers = [
  [
    [43.5456494880132,36.53926520147979,25.795604598985733,26.00725731020625,46.76380398701235,74.40935689205949,12.049736709577994,63.67528622219915,37.49943911758203,56.22751172065548,85.25082496219667,31.170562839713014,16.191380764031933,25.171771904128786,89.69654170791354],
    [42.88782514723049,63.02067125739154,84.62348991078048,38.23093548135795,86.34782302696689,48.99359079854869,12.257964403937498,35.4795505232131,16.856852683598085,19.26167625528886,20.890465106294087,72.90019680446693,64.79048887962827,13.513603935151961,36.62536487289766]
  ],
  [
    [36.261589206639215,86.50870571114635,43.46404467423455,22.653871151375036,62.58911552054529],
    [39.677616523499005,17.306013595479676,78.16553176036737,56.856900495052784,76.59495000471011]
  ],
  [
    [12.706235345527581,84.50917866228248,60.04606855352944,73.92687528518418,86.77987788590254],
    [55.909907295786056,31.39735602118308,17.198804284971196,35.7049710365495,74.345123410448]
  ]
]

response = qe_minesweeper.submit_answers(our_answers, 0, "Ty87nB")

print(response)

>>> "Error, answer does not contain 1000 scenarios"
```

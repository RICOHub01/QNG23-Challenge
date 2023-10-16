<p align="center">
  <img src="https://github.com/rdc-mitchell/qng23-challenge/blob/main/assets/images/Header.jpg?raw=true" alt="header"/>
</p>

# Stage 0 & 1

## Introduction

As per the problem brief:

Your task is to develop a method for analysing magnetic field images that identifies all of the land mines in a scenario and locates them with the greatest possible precision. You need to demonstrate this method by developing software that implements it automatically. You will be given the magnetic field images and corresponding locations of land mines for 1000 scenarios so that you can develop your method and software. Your solution will then be tested by you being provided with the magnetic field images of 1000 scenarios and being asked to return the locations of the land mines in each scenario. You will have two hours from receiving the test scenarios to return your results. If you do not locate all land mines in a scenario, then it does not count towards your score $` (N_{est} <N_{mines}) `$. If you locate more than 110% the total number of mines, then it does not count towards your score $` (N_{est}>1.1×N_{mines}) `$. If you find the correct number withing the 10% false positive limit, then the precision of your locating will be calculated by the Hausdorff distance from the set of true mine positions to your estimates (smaller is better).

There are three major components to this; Training, Stage 0, and Stage 1.

Training is completed offline, and uses the provided training dataset, along with functions load_dataset and load_answers.

Stage 0 is completed online, and uses the provided training dataset, along with the function submit_answers.

Stage 1 combines both elements, a fresh set of data and a time constraint. You will download a test dataset and use load_dataset and submit_answers to complete the stage and be scored against other teams.

# Formatting

## Datasets

Datasets are stored as hdf5 files.

These hdf5 Datasets contain individual scenarios denoted 'D0000' through to 'D1000'

The primary data is a 3x101x101 double of magnetic field values where the first dimension is the vector field direction ordered in East, North and Up, and the remaining two dimensions are Eastings and Northings

i.e. `data[2,:,:]` is the two dimensional B<sub>up</sub> data.

& `data[2,10,40]` is the B<sub>up</sub> data at Eastings 10m, Northings 40m

-------------------------

Each scenario also contains attributes.

The attribute "mine_dipole" returns a three-element array with the mine dipole moment in the East, North, Up directions in units of A.m<sup>2</sup>.

Some datasets will have the attribute "mine_position", which returns an Nx2 array with the first dimension elements being mines and the second dimension corresponding to the East position followed by the North positions of the mine in meters.

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

(data, dipole) = qe_minesweeper.load_dataset("dataset/stage1_training_dataset.h5", 4)

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

mine_locations = qe_minesweeper.load_answers("dataset/stage1_training_dataset.h5", 76)

east = mine_locations[0]
north = mine_locations[1]
mine_1 = (east[0], north[0])

print(mine_locations)
print(mine_1)

>>> [[35.138700415390886,25.657676745571052,52.15652811160456,54.44472370815717,35.53688743992102],[18.89473791201447,51.42367861186571,80.17380041971943,19.303343198901423,81.46877162392052]]
>>> (35.138700415390886, 18.89473791201447)
```

# Stage 0

Before 12pm, Wednesday 26 October, you will be required to demonstrate your participation and furthermore, capability to complete challenge.

You will demonstrate this by using the `submit_answers()` function to submit the mine locations for the training data to our server. This hurdle has been implemented to ensure you can proceed to **Stage 1** without issue and minimise risk when in the timed components of the challenge.

## Documentation

### `submit_answers(mine_estimates, stage, authkey)`

Provide an array of 1000xNx2 as estimates/answers for the locations of mines in the training set, along with an authkey to prove which team is submitting these answers.
The stage variable is provided to ensure that the answers are being submitted for the correct assessed dataset.

#### Example:

Submit an part of an array of mine_estimates for Stage 0, using authkey "Ty87nB".

```python
import qe_minesweeper

our_answers = [...]

response = qe_minesweeper.submit_answers(our_answers, 0, "Ty87nB")

print(response)

>>> "Error, answer does not contain 1000 scenarios"
```

# Stage 1

Stage 1 will comprise of three steps.
1. Downloading a new set of test data from https://sim.quantumnextgen.com.au/1/`authkey`
2. Running your solution over the test data and producing an answer for all 1000 elements.
3. Submitting that answer to our servers using the same method as Stage 0, by running the `submit_answers()` function.

Note: 
1. This is an assessed component and thus will not have `load_answers()` available for the test dataset.
2. This is a timed component and thus once the dataset is downloaded from https://sim.quantumnextgen.com.au/1/`authkey` you will have **two hours** to run `submit_answers()` with your answers.

### `load_dataset(filename, scenario)`

Open up the provided dataset and retrieve from the specified scenario (ranging from 0-999) the 3x101x101 magnetic field dataset as well as 3x1 magnetic dipole.

#### Example:

Open the dataset of scenario 39, load the 3 magnetic fields as `data`, and the 3x1 dipole data as `dipole`.
Then break the magnetic fields into their three vector fields; east, north and up.

```python
import qe_minesweeper

(data, dipole) = qe_minesweeper.load_dataset("dataset/stage1_test_dataset.h5", 39)

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

Submit an part of an array of mine_estimates for Stage 0, using authkey "Ty87nB".

```python
import qe_minesweeper

our_answers = [...]

response = qe_minesweeper.submit_answers(our_answers, 0, "Ty87nB")

print(response)

>>> "Error, answer does not contain 1000 scenarios"
```
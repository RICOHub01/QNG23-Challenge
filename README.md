<p align="center">
  <img src="https://github.com/ricohub01/qng23-challenge/blob/main/assets/images/Header.jpg?raw=true" alt="header"/>
</p>

# QNG23 Challenge Hub

[![GitHub release](https://img.shields.io/github/release/ricohub01/qng23-challenge.svg)](https://GitHub.com/ricohub01/qng23-challenge/releases/)

Welcome to the Quantum Next Generation 2023 Minesweeper Challenge

The following document is the hub that will contain: 
- Centralised source of content released on the challenge
- Key information to execute the challenge through the use of this python package
- Updates on changes and fixes to the challenge
- Uploads of the Q&A sessions and the leaderboard as we advance through the challenge

# Table of Contents
- Challenge Material
    - [Video Briefing](https://vimeo.com/869440571/e058164ca5?share=copy)
    - [Challenge Instructions](/assets/docs/QNG23%20Challenge%20instructions.pdf)
    - [Problem Brief](/assets/docs/QNG23%20Problem%20brief.pdf)
    - [Merch Form](https://forms.office.com/Pages/ResponsePage.aspx?id=GU5i_LU-u0uHril7jkukjXwnWWTBCM5Gk5WyPCsZZjVUNUVDNENZUTNWSzlBU0hJU1hUTVI1TlI5Vi4u)
    - Q&A
- Technical Guidance
    - [Installation](#installation)
    - [Software Dependenies](#software-dependencies)
- [Communication](#communication)
- Challenge Stages
    - [Stage 0](/STAGE-1.md) - Ends 12pm, Wednesday 26 October
    - [Stage 1](/STAGE-1.md) - 12pm Thursday, 26 October to 12pm Saturday, 28 October
    - Stage 2 - 12pm Thursday, 9 November to 12pm Saturday, 11 November
    - Stage 3 - 12pm Thursday, 23 November to 12pm Saturday, 25 November

# Technical Guidance

Python Version Required: `3.9+` 

## Installation
This GitHub repository will act as the framework for the challenge, as we advance through the stages of the challenge new documentation and code will be added to the repository and old code will be archived away into folders.

In addition, the datasets are made available through the Releases page along with zipped versions of the code for each stage. 

You can find the most recent version here: [![GitHub release](https://img.shields.io/github/release/ricohub01/qng23-challenge.svg)](https://GitHub.com/ricohub01/qng23-challenge/releases/)

This challenge package can be imported into any custom python script using the standard `import` feature. The documentation for each stage will outline the functions you need to call to complete challenge actions, as well as providing explanations about their parameters, their returns, and their role in the challenge.

### Example

At its most barebones, a Team folder for the challenge might look like so:
```bash
example-qng23-team-solution-folder
|   qng23-solution.py
|   qe_minesweeper.py
|   datasets/
|       stage1_training_dataset.h5
```

With the following line inputted at the top of `qng23-solution.py`, which should be your own custom python script.
```python
import qe_minesweeper
```
This will allow you to run the functions listed in `Documentation` that will help you complete the challenge.

## Software Dependencies
`qe_minesweeper.py` is dependent on three packages for it's internal functions to run:
- `requests`, which will need to be installed to engage with the online component of the challenge.
- `h5py`, which will need to be installed to read the significant datasets used within the challenge
- `numpy`, which will need to be installed to process the datasets into arrays

You can install `requests`, `numpy` and `h5py` *(if you do not already have them)* using `pip` or your choice of package manager.
```
python -m pip install requests
python -m pip install numpy
python -m pip install h5py
```

# Communication

Create an [issue  on GitHub](https://github.com/RICOHub01/QNG23-Challenge/issues)

Send an email to [support@quantumnextgen.com.au](mailto:support@quantumnextgen.com.au)

Attend a Q&A on 18th Oct, 17:00 via [Microsoft Teams](https://teams.microsoft.com/l/meetup-join/19%3ameeting_OGRiYzJlY2EtNjMxYi00MDhmLTkzMTYtZWUwMDU5MmMxZTg2%40thread.v2/0?context=%7b%22Tid%22%3a%22fc624e19-3eb5-4bbb-87ae-297b8e4ba48d%22%2c%22Oid%22%3a%22b289bda4-4d17-4592-9e22-17a7e487686b%22%7d)

> Meeting ID: 452 315 051 573 \
> Passcode: zsiqGp


Join Signal and chat in our [challenge group](https://signal.group/#CjQKIAB9t0m64V4PAwYP1NYVtYfAkoUx6DoRGidCKUoM11qMEhD4wyk4hU6KsNz0ZTT2V8EW)
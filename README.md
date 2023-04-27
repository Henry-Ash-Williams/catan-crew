# Catan Crew
Source files for Software Engineering 2023 at the University of Sussex

## Installation
> Make sure you are always in `/catan-crew` dir

### Install API
1. `git clone git@github.com:Henry-Ash-Williams/catan-crew`
2. `cd src`
3. `pip install rich fastapi pydantic watchfiles uvicorn`
4. `sudo apt install uvicorn` if you are on ubuntu, you don't need to pip install uvicorn

### Install Socket Server
1. `cd socket-server`
2. `npm install`

### Install the ui
1. `cd ui`
2. `npm install`

## Run the whole Web Application
### Running the API server
#### If on windows
1. `cd src`
2. `python3 uvicorn app:app --reload` or `python uvicorn app:app --reload`

#### If on Linux
1. `cd src`
2. `uvicorn app:app --reload`

### Run the socket server
1. `cd socket-server`
2. `node server.js`

### Run the client
1. `cd ui`
2. `npm start`

## Running the game in the terminal
1. `git checkout cli-testing`
2. `cd Sandbox`
3. `python3.10 main.py `

## The coordinate system:

```
         30  31  32  33
       19  20  21  22  23
      8   9  10  11  12  13
   34  35  36   0   1   2   3
     24  25  26  27  28  29
       14  15  16  17  18
         4   5   6   7
```

## Architecture
![System design](https://raw.githubusercontent.com/Henry-Ash-Williams/catan-crew/main/Simplified%20System%20Design.png?token=GHSAT0AAAAAAB52HUNZY7ATTXHOO2EVK7KIZCHZSIA)

# Statistics 
- 3051 lines of code in python 
- 1449 lines of code in typescript 
- 1062 lines of code in javascript
- 5562 total LOC 

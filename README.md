# AreaSelectorAPI
Svelte Area Selector | Postcode API 

## Create the db

`python PostSQL.py`


## How to run

Operating instructions:

1. Start the api: (requires python)

`python apirun.py`

This opens the server at localhost port 5002

`http://127.0.0.1:5002/`

2. In a new terminal run the svelte demo:

`cd selector && npm run dev`

3. open `http://127.0.0.1:5000/` and play. 





##  Open console output
`cmd + alt + I` and the selected code will be printed. 


To recieve / return this use `bind:select={your variablename}`
in the component definition.   
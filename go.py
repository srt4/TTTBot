import gameMaster as gm

setup = { 
  'rows':7,
  'columns':7,
  'k':5,
  'blocked':[(0,0),(0,6),(6,0),(6,6)],
  'existingXs':[],
  'existingOs':[],
  'debugging' : False,
  'timeLimit' : 1000,
  'runCount' : 100
  }

gm.runWith(
	'srt4KInARow',
	'distractoKInARow',
setup)


import json

class loadStartData():
    
    # Opening JSON file
    f = open('mocks/listado.json',)
    
    # returns JSON object as
    # a dictionary
    data = json.load(f)
        
    # Closing file
    f.close()
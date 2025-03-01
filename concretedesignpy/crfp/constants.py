def eRF(exposure,type):
    data = {
        "interior" : {
            "carbon" : 0.95,
            "glass" : 0.75,
            "aramid" : 0.85
        },
        "exterior" : {
            "carbon" : 0.85,
            "glass" : 0.65,
            "aramid" : 0.75
        },
        "aggressive" : {
            "carbon" : 0.85,
            "glass" : 0.50,
            "aramid" : 0.70
            },
    }
    results = data[exposure][type]
    return results
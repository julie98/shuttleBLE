import requests
from flask_httpauth import HTTPTokenAuth
from requests.auth import HTTPBasicAuth

# test the api for generating tokens
r = requests.post('http://localhost:5000/api/tokens', auth=HTTPBasicAuth('julie@test.com', 'julie123'))
print(r.text)
print(r.json)

# test the profile api
r = requests.get('http://localhost:5000/api/get_profile',
                 headers={"Authorization": "Bearer juZRMT/BNCVxSBssiR/Bk5Q55kp0sJ/2"})
print(r.text)
print(r.json)

# teat the api for saving GPS and Bluetooth data
payload1 = {"data": [{"timestamp": 1642522652.1387474,
                      "GPS":
                          {"latitude": 37.29044,
                           "longitude": -127.3212,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 1,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 1,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            }
                           ]
                      }]
            }

payload2 = {"data": [{"timestamp": 1642538652.1387474,
                      "GPS":
                          {"latitude": 37.29044,
                           "longitude": -127.3212,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 1,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 1,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 2,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }]
                      },
                     {"timestamp": 1642542652.2602519,
                      "GPS":
                          {"latitude": 37.29044,
                           "longitude": -127.3212,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 2,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 2,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 3,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }
                           ]
                      }
                     ]
            }

payload3 = {"data": [{"timestamp": 1642538652.1387455,
                      "GPS":
                          {"latitude": 37.29044,
                           "longitude": -127.3212,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 1,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 1,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 2,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }]
                      },
                     {"timestamp": 1642542652.2602528,
                      "GPS":
                          {"latitude": 28.37223,
                           "longitude": -135.7639,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 2,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 2,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 3,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }
                           ]
                      },
                     {"timestamp": 1642558723.5819537,
                      "GPS":
                          {"latitude": 32.32916,
                           "longitude": -289.3761,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 2,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 2,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 3,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }
                           ]
                      },
                     {"timestamp": 164259236.1359285,
                      "GPS":
                          {"latitude": 58.57206,
                           "longitude": -268.47195,
                           "horiz_acc": 5.0,
                           "vert_acc": 5.0,
                           "course": 273.123433,
                           "course_acc": 10.5,
                           "speed": 3.0,
                           "speed_acc": 0.5,
                           "heading": 87.12894
                           },
                      "BLE":
                          [{"major": 2,
                            "minor": 1,
                            "accuracy": 2.5,
                            "rssi": -75
                            },
                           {"major": 2,
                            "minor": 2,
                            "accuracy": 1.5,
                            "rssi": -65
                            },
                           {"major": 3,
                            "minor": 3,
                            "accuracy": 3.5,
                            "rssi": -65
                            }
                           ]
                      }
                     ]
            }

r = requests.post('http://localhost:5000/api/save_data', data=payload1)
print(r.text)
print(r.json)

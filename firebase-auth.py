import pyrebase

firebaseConfig = {
        'apiKey': "AIzaSyDCUeyq8-leE1xN0w5N5cDe9qVInF7pVnE",
        'authDomain': "events-hub-37537.firebaseapp.com",
        'databaseURL': "",
        'projectId': "events-hub-37537",
        'storageBucket': "events-hub-37537.appspot.com",
        'messagingSenderId': "873422473065",
        'appId': "1:873422473065:web:0e3d14b5193262feef5ff8",
        'measurementId': "G-D7ZS50SN45"
    }

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

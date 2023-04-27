curl localhost:8000/predict -X GET -H 'Content-Type: application/json' -d '{
        "houses": [
            {
                "MedInc": 1,
                "HouseAge": 1,
                "AveRooms": 3,
                "AveBedrms": 3,
                "Population": 3,
                "AveOccup": 5,
                "Latitude": 1,
                "Longitude": 1
            }
        ]
    }'

import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 100 }, // simulate ramp-up of traffic from 1 to 100 users over 3 minutes.
        { duration: '5m', target: 100 }, // stay at 100 users for 7 minutes
        { duration: '5s', target: 0 }, // ramp-down to 0 users
    ],
    thresholds: {
        'http_req_duration': ['p(99)<500'] // 99% of requests must complete below 1.5s
    },
};

const features = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]
const fixed = [1, 1, 1, 1, 1, 1, 0, 0]

const randInt = (max) => (Math.floor(Math.random() * max))

const generator = (cacheRate) => {
    const rand = Math.random()
    const input = rand > cacheRate
        ? features.reduce((acc, f) => {
            acc[f] = randInt(20)
            return acc
        }, {})
        : features.reduce((acc, f, idx) => {
            acc[f] = fixed[idx]
            return acc
        }, {})

    return {
        houses: [input]
    }
}

const NAMESPACE = 'winegarj'
const BASE_URL = `https://${NAMESPACE}.mids255.com`;
const CACHE_RATE = 0.5

export default () => {
    const healthRes = http.get(`${BASE_URL}/health`)
    check(healthRes, {
        'is 200': (r) => r.status === 200,
        'status healthy': (r) => r.json('status') === 'healthy',
    })

    const payload = JSON.stringify(generator(CACHE_RATE))
    const predictionRes = http.request('POST', `${BASE_URL}/predict`, payload)
    check(predictionRes, {
        'is 200': (r) => r.status === 200,
        'is number': (r) => parseFloat(r.json('predictions.0')),
    })
};


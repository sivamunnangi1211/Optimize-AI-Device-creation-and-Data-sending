let $injector = widgetContext.$scope.$injector;
let dialogs = $injector.get(widgetContext.servicesMap.get('dialogs'));
let assetService = $injector.get(widgetContext.servicesMap.get('assetService'));
let deviceService = $injector.get(widgetContext.servicesMap.get('deviceService'));

console.log(entityId);
console.log(widgetContext);

let localEntityId =entityId["id"];
console.log(localEntityId);

let building;
let highTemperatureLimit;
let area;
let enableHumidNMT;
let enableTempNMT;
let lowHumidityLimit;
let enableHumidNLT;
let highHumidityLimit;
let lowTemperatureLimit;
let location;
let plant;
let model;
let make;
let credentialsId;


// Define the ThingsBoard host and login credentials
const thingsboardHost = 'http://3.111.29.163:8080';
const username = 'tenant@thingsboard.org';  // Replace with your ThingsBoard username
const password = 'tenant';  // Replace with your ThingsBoard password

// Define the login API endpoint
const loginUrl = ${thingsboardHost}/api/auth/login;

// Define the login payload
const loginPayload = {
    username: username,
    password: password
};

// Function to login and obtain JWT token
async function login() {
    try {
        const loginResponse = await fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginPayload)
        });

        if (loginResponse.ok) {
            const loginData = await loginResponse.json();
            const jwtToken = loginData.token;
            console.log("Login successful, JWT token obtained.");
            return jwtToken;
        } else {
            console.error(Failed to login. Status code: ${loginResponse.status});
            console.error(Response: ${await loginResponse.text()});
            return null;
        }
    } catch (error) {
        console.error(Error logging in: ${error});
        return null;
    }
}




const url = ${thingsboardHost}/api/device/${localEntityId}/credentials;

// Function to fetch credentials
async function fetchCredentials(jwtToken) {
    try {
        // Perform the GET request
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'X-Authorization': Bearer ${jwtToken}
            }
        });

        // Check if the response is okay
        if (!response.ok) {
            throw new Error(Failed to fetch credentials. Status code: ${response.status});
        }

        // Parse the JSON response
        const data = await response.json();

        // Extract and print the credentialsId
        credentialsId = data.credentialsId;
        console.log('Credentials ID:', credentialsId);
    } catch (error) {
        console.error('Error:', error);
    }
}




async function fetchSharedAttributes(credentialsId) {
    
    try {
        const apiUrlCredentials = http://3.111.29.163:8080/api/v1/${credentialsId}/attributes?sharedKeys=Area%2CBuilding%2CEnable_Humid_NLT%2CEnable_Humid_NMT%2CEnable_Temp_NLT.%2CEnable_Temp_NMT%2CHigh%20Humidity%20Limit%2CHigh%20Temperature%20Limit%2CLocation%2CLow%20Humidity%20Limit%2CLow%20Temperature%20Limit%2CMake%2CModel%2CPlant;

        // Perform the GET request
        const response = await fetch(apiUrlCredentials, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            }
        });

        // Check if the response is okay
        if (!response.ok) {
            throw new Error(Failed to fetch shared attributes. Status code: ${response.status});
        }

        // Parse the JSON response
        const data = await response.json();

        // Extract shared attributes from the response
        const sharedAttributes = data.shared;

        // Assign each attribute to the variables
        building = sharedAttributes.Building;
        highTemperatureLimit = sharedAttributes['High Temperature Limit'];
        area = sharedAttributes.Area;
        enableHumidNMT = sharedAttributes.Enable_Humid_NMT;
        enableTempNMT = sharedAttributes.Enable_Temp_NMT;
        lowHumidityLimit = sharedAttributes['Low Humidity Limit'];
        enableHumidNLT = sharedAttributes.Enable_Humid_NLT;
        highHumidityLimit = sharedAttributes['High Humidity Limit'];
        lowTemperatureLimit = sharedAttributes['Low Temperature Limit'];
        location = sharedAttributes.Location;
        plant = sharedAttributes.Plant;
        model = sharedAttributes.Model;
        make = sharedAttributes.Make;

        // Log the variables to the console
        console.log('Building:', building);
        console.log('High Temperature Limit:', highTemperatureLimit);
        console.log('Area:', area);
        console.log('Enable Humid NMT:', enableHumidNMT);
        console.log('Enable Temp NMT:', enableTempNMT);
        console.log('Low Humidity Limit:', lowHumidityLimit);
        console.log('Enable Humid NLT:', enableHumidNLT);
        console.log('High Humidity Limit:', highHumidityLimit);
        console.log('Low Temperature Limit:', lowTemperatureLimit);
        console.log('Location:', location);
        console.log('Plant:', plant);
        console.log('Model:', model);
        console.log('Make:', make);

    } catch (error) {
        console.error('Error:', error);
    }
}

async function main() {
    const jwtToken = await login();
    if (jwtToken) {
       // await fetchSharedAttributes(jwtToken, entityId);
        // Execute the function
        await fetchCredentials(jwtToken);
        await fetchSharedAttributes(credentialsId);
    }
 
}

// Run the main function
main();
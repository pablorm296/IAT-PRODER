//Read config file
const configFile = cat("/docker-entrypoint-initdb.d/db_secrets")
// Read root secret
const rootSecretFile = cat("/docker-entrypoint-initdb.d/root_secret")

// ParseLines
const lines = configFile.split("\n")

// Loop through lines and remove any empty line
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line == "" || line.trim() == "") {
        lines.splice(i, 1);
    }
}

// Loop again, but his time create an object where we're going to store field:values pairs
var parsedConfig = {};
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const field = line.split(":")[0]
    const value = line.split(":")[1]
    parsedConfig[field] = value
}

// Check the parsed fields
const requiredFields = ["adminUserName", "appUserName", "adminUserPassword", "appUserPassword", "dbName"]
for (let i = 0; i < requiredFields.length; i++) {
    const fieldName = requiredFields[i];
    if (!parsedConfig.hasOwnProperty(fieldName)) {
        parsedConfig[fieldName] = "defaultChangeM3!#";
        print(`The required filed '${fieldName}' could not be found. Setting to default value!`);
    } else {
        print(`Field '${fieldName}' is set to '${parsedConfig[fieldName]}'`);
    }
}

// Parse root secret
const rootSecret = rootSecretFile.split("\n")[0]

// Change to admin
db = db.getSiblingDB("admin");   

//Authenticate
db.auth("root", rootSecret)

// Create main DataBase
db = db.getSiblingDB(parsedConfig["dbName"]);   

// Create IAT administrator
db.createUser({
    user: parsedConfig["adminUserName"],
    pwd: parsedConfig["adminUserPassword"],
    roles: [
        { role: "dbOwner", db: parsedConfig["dbName"] }
    ]
});

// Create IAT reader/writer
db.createUser({
    user: parsedConfig["appUserName"],
    pwd: parsedConfig["appUserPassword"],
    roles: [
        { role: "readWrite", db: parsedConfig["dbName"]},
    ]
});

// Insert results counter
db.Counter.insertOne({
    "counter_name": "n_results",
    "counter_value": 0,
    "scores_array": []
})
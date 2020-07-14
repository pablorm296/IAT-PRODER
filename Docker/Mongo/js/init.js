// Change to admin
db = db.getSiblingDB("admin");   

//Authenticate
db.auth("root", "wMvHrycPA5kTE9Px8YzE")

// Create main DataBase
db = db.getSiblingDB("DataInt_Auth");   

// Create main administrator
db.createUser({
    user: "DataInt_Auth_Admin",
    pwd: "DKpkFmQsrm5MNswqdfvd",
    roles: [
        { role: "dbOwner", db: "DataInt_Auth" }
    ]
});

// Create API reader/writer
db.createUser({
    user: "DataInt_Auth_API",
    pwd: "xbkhWj43PaG43rb96uQT",
    roles: [
        { role: "readWrite", db: "DataInt_Auth"},
    ]
});

// Create Python reader/writer
db.createUser({
    user: "DataInt_Auth_Python",
    pwd: "tqhzvUCP4WAmHM39B64e",
    roles: [
        { role: "readWrite", db: "DataInt_Auth"},
    ]
});
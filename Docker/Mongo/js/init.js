// Change to admin
db = db.getSiblingDB("admin");   

//Authenticate
db.auth("root", "wMvHrycPA5kTE9Px8YzE")

// Create main DataBase
db = db.getSiblingDB("IAT_PRODER");   

// Create IAT administrator
db.createUser({
    user: "iat_admin",
    pwd: "DKpkFmQsrm5MNswqdfvd",
    roles: [
        { role: "dbOwner", db: "IAT_PRODER" }
    ]
});

// Create IAT reader/writer
db.createUser({
    user: "iat_app",
    pwd: "xbkhWj43PaG43rb96uQT",
    roles: [
        { role: "readWrite", db: "IAT_PRODER"},
    ]
});
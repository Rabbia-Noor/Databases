// The official mongo image executes this only for a new/empty data volume.
const environment = process.env.LAB_ENV;
const databaseName = process.env.MONGO_INITDB_DATABASE;
const database = db.getSiblingDB(databaseName);

database.createUser({
  user: process.env.LAB_USERNAME,
  pwd: process.env.LAB_PASSWORD,
  roles: [{ role: "readWrite", db: databaseName }]
});
database.environment_info.insertOne({ _id: "environment", name: environment });
database.students.createIndex({ roll_no: 1 }, { unique: true });
database.students.insertOne({
  roll_no: "SEED-" + environment.toUpperCase(),
  name: environment.toUpperCase() + " Seed Student",
  environment: environment
});

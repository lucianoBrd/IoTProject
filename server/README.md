#Mini-projet for 4IRC students at CPE Lyon

## Installing the server
In a new raspbian installation:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python python-serial minicom
sudo usermod -aG dialout pi
```

Add a line into `rc.local`to start the game

For the db : 

in one term
```
docker pull mongo
docker rm mongodb
docker run --name mongodb -p 27017:27017 mongo
```

in another one
```
docker exec -it mongodb bash #to acceed to mongo 
mongo
use admin
db.createUser({
  user: "admin", 
  pwd: "secure", 
  roles: [ { role: "root", db: "admin" } ]
})
db.createCollection('iot')
```

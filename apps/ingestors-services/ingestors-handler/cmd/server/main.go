package main

import (
	"fmt"
	mongo "libs/sd-golang/utils-mongo"

	// "go.mongodb.org/mongo-driver/bson"
	"apps/ingestors-services/ingestors-handler/configs"
)

// type User struct {
//   Username string `bson:"username"`
//   Email    string `bson:"email"`
// }

func main() {
  config := configs.NewConfig()
  println(config.DBDriver)
  println(config.GetBDDriver())
  handler, err := mongo.NewMongoHandler(config.GetMongoUri(), config.GetMongoDBName())
  if err != nil {
      fmt.Printf("Failed to create MongoHandler: %v\n", err)
      return
  }

  defer handler.Close()

  // // create a new user document
  // user := &User{Username: "john", Email: "john@example.com"}
  // err = handler.Create(user)
  // if err != nil {
  //     fmt.Printf("Failed to create user: %v\n", err)
  //     return
  // }

  // // read the user document
  // filter := bson.M{"_id": "user1"}
  // var users []User
  // documents, err := handler.Read(filter)
  // if err != nil {
  //     fmt.Printf("Failed to read users: %v\n", err)
  //     return
  // }

  // for _, document := range documents {
  //     var user User
  //     bsonBytes, _ := bson.Marshal(document)
  //     bson.Unmarshal(bsonBytes, &user)
  //     users = append(users, user)
  // }

  // fmt.Printf("Users: %+v\n", users)

  // // update the user document
  // update := bson.M{"$set": bson.M{"email": "new-email@example.com"}}
  // err = handler.Update(filter, update)
  // if err != nil {
  //     fmt.Printf("Failed to update user: %v\n", err)
  //     return
  // }

  // // read the updated user document
  // documents, err = handler.Read(filter)
  // if err != nil {
  //     fmt.Printf("Failed to read users: %v\n", err)
  //     return
  // }

  // users = []User{}
  // for _, document := range documents {
  //     var user User
  //     bsonBytes, _ := bson.Marshal(document)
  //     bson.Unmarshal(bsonBytes, &user)
  //     users = append(users, user)
  // }

  // fmt.Printf("Users: %+v\n", users)

  // // delete the user document
  // err = handler.Delete(filter)
  // if err != nil {
  //     fmt.Printf("Failed to delete user: %v\n", err)
  //     return
  // }

  // // verify the user document has been deleted
  // documents, err = handler.Read(filter)
  // if err != nil {
  //     fmt.Printf("Failed to read users: %v\n", err)
  //     return
  // }

  // if len(documents) > 0 {
  //     fmt.Println("Failed to delete user")
  //     return
  // }

  // fmt.Println("User has been deleted")
}

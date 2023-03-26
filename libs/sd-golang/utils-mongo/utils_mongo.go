package utils_mongo

import (
  "context"

  "go.mongodb.org/mongo-driver/bson"
  "go.mongodb.org/mongo-driver/mongo"
  "go.mongodb.org/mongo-driver/mongo/options"
)

type MongoHandler struct {
  client     *mongo.Client
  collection *mongo.Collection
}

func NewMongoHandler(connectionString, dbName, collectionName string) (*MongoHandler, error) {
  clientOptions := options.Client().ApplyURI(connectionString)
  client, err := mongo.Connect(context.Background(), clientOptions)
  if err != nil {
      return nil, err
  }

  collection := client.Database(dbName).Collection(collectionName)

  return &MongoHandler{client: client, collection: collection}, nil
}

func (h *MongoHandler) Close() {
  h.client.Disconnect(context.Background())
}

func (h *MongoHandler) Create(document interface{}) error {
  _, err := h.collection.InsertOne(context.Background(), document)
  if err != nil {
      return err
  }
  return nil
}

func (h *MongoHandler) Read(filter bson.M) ([]interface{}, error) {
  var documents []interface{}
  cursor, err := h.collection.Find(context.Background(), filter)
  if err != nil {
      return nil, err
  }

  defer cursor.Close(context.Background())
  for cursor.Next(context.Background()) {
      var document bson.M
      if err := cursor.Decode(&document); err != nil {
          return nil, err
      }
      documents = append(documents, document)
  }

  if err := cursor.Err(); err != nil {
      return nil, err
  }

  return documents, nil
}

func (h *MongoHandler) Update(filter bson.M, update bson.M) error {
  _, err := h.collection.UpdateMany(context.Background(), filter, update)
  if err != nil {
      return err
  }
  return nil
}

func (h *MongoHandler) Delete(filter bson.M) error {
  _, err := h.collection.DeleteMany(context.Background(), filter)
  if err != nil {
      return err
  }
  return nil
}
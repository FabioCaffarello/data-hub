package utils_mongo

import (
  "context"

  "go.mongodb.org/mongo-driver/bson"
  "go.mongodb.org/mongo-driver/mongo"
  "go.mongodb.org/mongo-driver/mongo/options"
)

type MongoHandler struct {
  client     *mongo.Client
  dbName string
}

func NewMongoHandler(connectionString string, dbName string) (*MongoHandler, error) {
  clientOptions := options.Client().ApplyURI(connectionString)
  client, err := mongo.Connect(context.Background(), clientOptions)
  if err != nil {
      return nil, err
  }

  return &MongoHandler{client: client, dbName:dbName}, nil
}

func (h *MongoHandler) Close() {
  h.client.Disconnect(context.Background())
}

func (h *MongoHandler) GetCollection(collectionName string) *mongo.Collection {
  return h.client.Database(h.dbName).Collection(collectionName)
}


func (h *MongoHandler) Create(document interface{}, collectionName string) error {
  collection := h.GetCollection(collectionName)
  _, err := collection.InsertOne(context.Background(), document)
  if err != nil {
      return err
  }
  return nil
}

func (h *MongoHandler) Read(filter bson.M, collectionName string) ([]interface{}, error) {
  collection := h.GetCollection(collectionName)
  var documents []interface{}
  cursor, err := collection.Find(context.Background(), filter)
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

func (h *MongoHandler) Update(filter bson.M, update bson.M, collectionName string) error {
  collection := h.GetCollection(collectionName)
  _, err := collection.UpdateMany(context.Background(), filter, update)
  if err != nil {
      return err
  }
  return nil
}

func (h *MongoHandler) Delete(filter bson.M, collectionName string) error {
  collection := h.GetCollection(collectionName)
  _, err := collection.DeleteMany(context.Background(), filter)
  if err != nil {
      return err
  }
  return nil
}

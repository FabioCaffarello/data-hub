package database

import (
    "apps/ingestors-services/ingestors-handler/internal/entity"
    "libs/sd-golang/utils-mongo"
    "go.mongodb.org/mongo-driver/bson"
)

type InputMongo struct {
    handler *utils_mongo.MongoHandler
}

func NewInputMongo(handler *utils_mongo.MongoHandler) *InputMongo {
    return &InputMongo{handler: handler}
}

func (im *InputMongo) Create(input *entity.Input, collectionName string) error {
    return im.handler.Create(input, collectionName)
}

func (im *InputMongo) FindById(md5id string, collectionName string) (*entity.Input, error) {
    filter := bson.M{"id": md5id}
    documents, err := im.handler.Read(filter, collectionName)
    if err != nil {
        return nil, err
    }
    if len(documents) == 0 {
        return nil, nil
    }
    document := documents[0]
    input := &entity.Input{}
    bsonBytes, _ := bson.Marshal(document)
    bson.Unmarshal(bsonBytes, input)
    return input, nil
}

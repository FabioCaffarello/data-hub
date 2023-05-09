package utils_mongo


import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoHandlerSuite struct {
	suite.Suite
	handler *MongoHandler
  collection *mongo.Collection
  collectionName string
}

func (suite *MongoHandlerSuite) SetupSuite() {
	// Set up a test MongoDB instance
	clientOptions := options.Client().ApplyURI("mongodb://mongodb:27017")
	client, err := mongo.Connect(context.Background(), clientOptions)
	assert.NoError(suite.T(), err)

	dbName := "test-db"
	suite.collectionName = "test-collection"

	// Create a test collection
	suite.collection = client.Database(dbName).Collection(suite.collectionName)
	err = suite.collection.Drop(context.Background())
	assert.NoError(suite.T(), err)

	// Create a new MongoHandler instance
	handler, err := NewMongoHandler("mongodb://mongodb:27017", dbName)
	assert.NoError(suite.T(), err)
	suite.handler = handler
}

func (suite *MongoHandlerSuite) TearDownSuite() {
	// Drop the test collection
	err := suite.collection.Drop(context.Background())
	assert.NoError(suite.T(), err)

	// Disconnect the client
	err = suite.handler.client.Disconnect(context.Background())
	assert.NoError(suite.T(), err)
}

func (suite *MongoHandlerSuite) TestCreate() {
	// Create a test document and insert it into the collection
	document := bson.M{"_id": "usertest", "name": "Alice", "age": int32(30)}
	err := suite.handler.Create(document, suite.collectionName)
	assert.NoError(suite.T(), err)

	// Test that the document was inserted
	filter := bson.M{"_id": "usertest"}
	documents, err := suite.handler.Read(filter, suite.collectionName)
	assert.NoError(suite.T(), err)
	assert.Len(suite.T(), documents, 1)
	assert.Equal(suite.T(), document, documents[0].(bson.M))
}

func (suite *MongoHandlerSuite) TestUpdate() {
	// Create a test document and insert it into the collection
	document := bson.M{"_id": "usertest2", "name": "Bob", "age": int32(30)}
	err := suite.handler.Create(document, suite.collectionName)
	assert.NoError(suite.T(), err)

	// Update the document
	filter := bson.M{"_id": "usertest2"}
	update := bson.M{"$set": bson.M{"age": int32(31)}}
	err = suite.handler.Update(filter, update, suite.collectionName)
	assert.NoError(suite.T(), err)

	// Test that the document was updated
	filter = bson.M{"name": "Bob", "age": int32(31)}
	documents, err := suite.handler.Read(filter, suite.collectionName)
  document["age"] = int32(31)
	assert.NoError(suite.T(), err)
	assert.Len(suite.T(), documents, 1)
	assert.Equal(suite.T(), document, documents[0].(bson.M))
}

func (suite *MongoHandlerSuite) TestDelete() {
	// Create a test document and insert it into the collection
	document := bson.M{"_id": "usertest3", "name": "Juan", "age": int32(30)}
	err := suite.handler.Create(document, suite.collectionName)
	assert.NoError(suite.T(), err)

	// Delete the document
	filter := bson.M{"_id": "usertest3"}
	err = suite.handler.Delete(filter, suite.collectionName)
	assert.NoError(suite.T(), err)

	// Test that the document was deleted
	documents, err := suite.handler.Read(filter, suite.collectionName)
	assert.NoError(suite.T(), err)
	assert.Len(suite.T(), documents, 0)
}

func TestMongoHandlerSuite(t *testing.T) {
	suite.Run(t, new(MongoHandlerSuite))
}

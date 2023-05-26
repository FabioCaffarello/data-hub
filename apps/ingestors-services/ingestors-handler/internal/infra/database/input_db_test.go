package database

import (
	"context"
	"testing"
	"time"

	"apps/ingestors-services/ingestors-handler/internal/entity"
	"libs/sd-golang/utils-golang/idgen"
	"libs/sd-golang/utils-mongo"
)

type InputMongoSuite struct {
	handler  *utils_mongo.MongoHandler
	inputDB  *InputMongo
	testData map[string]interface{}
	testID   string
	collectionName   string
}

func (suite *InputMongoSuite) SetUpSuite(t *testing.T) {
	connectionString := "mongodb://mongodb:27017"
	dbName := "inputs"
	suite.collectionName = "ingestor-test"
	handler, err := utils_mongo.NewMongoHandler(connectionString, dbName)
	if err != nil {
		t.Fatalf("Error creating MongoHandler: %v", err)
	}
	suite.handler = handler

	suite.inputDB = NewInputMongo(handler)

	suite.testData = map[string]interface{}{
		"key1": "value1",
		"key2": 123,
	}
	input, err := entity.NewInput(suite.testData)
	if err != nil {
		t.Fatalf("Error creating Input: %v", err)
	}
	input.ProcessingDate = time.Date(2022, 3, 27, 0, 0, 0, 0, time.UTC)
	err = suite.inputDB.Create(input, suite.collectionName)
	if err != nil {
		t.Fatalf("Error creating Input: %v", err)
	}
	suite.testID = string(input.ID)
}

func (suite *InputMongoSuite) TestFindById(t *testing.T) {
	foundInput, err := suite.inputDB.FindById(suite.testID, suite.collectionName)
	if err != nil {
		t.Fatalf("Error finding Input by ID: %v", err)
	}
	if foundInput == nil {
		t.Fatalf("Input not found by ID")
	}
	if foundInput.ID != idgen.ID(suite.testID) {
		t.Fatalf("Input ID does not match expected")
	}
	if foundInput.ProcessingDate.Unix() != time.Date(2022, 3, 27, 0, 0, 0, 0, time.UTC).Unix() {
		t.Fatalf("Input ProcessingDate does not match expected")
	}
	if len(foundInput.Data) != len(suite.testData) {
		t.Fatalf("Input Data length does not match expected")
	}
}

func (suite *InputMongoSuite) TestFindByIdNonExistent(t *testing.T) {
	foundInput, err := suite.inputDB.FindById("non-existent-id", suite.collectionName)
	if err != nil {
		t.Fatalf("Error finding Input by ID: %v", err)
	}
	if foundInput != nil {
		t.Fatalf("Input should not be found with non-existent ID")
	}
}

func (suite *InputMongoSuite) TearDownSuite(t *testing.T) {
	// Drop the test collection
	err := suite.handler.GetCollection(suite.collectionName).Drop(context.Background())
	if err != nil {
		t.Fatalf("Error dropping test collection: %v", err)
	}

	// Disconnect the client
	suite.handler.Close()
}

func TestInputMongo(t *testing.T) {
	suite := &InputMongoSuite{}
	suite.SetUpSuite(t)
	defer suite.TearDownSuite(t)

	t.Run("FindById", suite.TestFindById)
	t.Run("FindByIdNonExistent", suite.TestFindByIdNonExistent)
}

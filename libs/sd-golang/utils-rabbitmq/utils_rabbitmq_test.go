package utils_rabbitmq

import (
	"testing"

	"github.com/stretchr/testify/suite"
)

type RabbitMQTestSuite struct {
	suite.Suite
	handler *RabbitMQHandler
}

func (suite *RabbitMQTestSuite) SetupTest() {
	var err error
	suite.handler, err = NewRabbitMQHandler("amqp://guest:guest@rabbitmq:5672/", []string{"test_queue"})
	suite.Require().NoError(err)
}

func (suite *RabbitMQTestSuite) TearDownTest() {
	suite.handler.Close()
}

func (suite *RabbitMQTestSuite) TestPublish() {
	msg := []byte("hello world")
	err := suite.handler.Publish("test_queue", msg)
	suite.Require().NoError(err)
}

func (suite *RabbitMQTestSuite) TestConsume() {
	msgs, err := suite.handler.Consume("test_queue")
	suite.Require().NoError(err)

	go func() {
		for msg := range msgs {
			suite.Require().NotEmpty(msg)
			suite.Require().Equal("hello world", string(msg))
			break
		}
	}()

	err = suite.handler.Publish("test_queue", []byte("hello world"))
	suite.Require().NoError(err)
}

func TestRabbitMQTestSuite(t *testing.T) {
	suite.Run(t, new(RabbitMQTestSuite))
}
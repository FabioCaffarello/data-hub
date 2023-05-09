package idgen

import (
	"testing"

	"github.com/stretchr/testify/suite"
)

type IDGenTestSuite struct {
	suite.Suite
}

func TestIDGenTestSuite(t *testing.T) {
	suite.Run(t, new(IDGenTestSuite))
}

func (suite *IDGenTestSuite) TestNewID() {
	data := "test data"
	expectedID := ID("eb733a00c0c9d336e65691a37ab54293")

	id, err := NewID(data)
	suite.Nil(err)
	suite.Equal(expectedID, id)
}

package entity

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
	"libs/sd-golang/utils-golang/idgen"
)

type InputSuite struct {
	suite.Suite
}

func (suite *InputSuite) TestNewInput() {
	data := map[string]interface{}{
		"day":   1,
		"month": 12,
		"year":  2021,
	}
	input, err := NewInput(data)
	assert.Nil(suite.T(), err)
	assert.NotNil(suite.T(), input)
	assert.NotEmpty(suite.T(), input.ID)
	assert.NotEmpty(suite.T(), input.FlagStatus)
	assert.Equal(suite.T(), data, input.Data)
}

func (suite *InputSuite) TestValidateSuccess() {
	input := &Input{
		ID: idgen.ID("test-id"),
		Data: map[string]interface{}{
			"day":   1,
			"month": 12,
			"year":  2021,
		},
    FlagStatus:     0,
		ProcessingDate: time.Now(),
	}

	err := input.Validate()
	suite.Nil(err)
}

func (suite *InputSuite) TestValidateError() {
	input := &Input{
		ID:             idgen.ID("test-id"),
		Data:           nil,
    FlagStatus:     0,
		ProcessingDate: time.Now(),
	}

	err := input.Validate()
	suite.NotNil(err)
	suite.Equal(ErrDataIsRequired, err)
}

func TestInputSuite(t *testing.T) {
	suite.Run(t, new(InputSuite))
}

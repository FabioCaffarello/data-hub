package entity

import (
	"encoding/json"
	"errors"
	"libs/sd-golang/utils-golang/idgen"
	"time"
)

var (
	ErrDataIsRequired = errors.New("data is required")
)

type Input struct {
	ID             idgen.ID               `json:"_id"`
	Data           map[string]interface{} `json:"data"`
  FlagStatus      int `json:"flag_status"`
	ProcessingDate time.Time              `json:"processing_date"`
}

func NewInput(data map[string]interface{}) (*Input, error) {
	dataBytes, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}
	id, err := idgen.NewID(string(dataBytes))
	if err != nil {
		return nil, err
	}
	input := &Input{
		ID:             id,
		Data:           data,
    FlagStatus:     0,
		ProcessingDate: time.Now(),
	}
	err = input.Validate()
	if err != nil {
		return nil, err
	}
	return input, nil
}

func (i *Input) Validate() error {
	if i.Data == nil {
		return ErrDataIsRequired
	}
	return nil
}

package entity

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGivenAnEmptyIdWhenCreateANewOrderThenShouldReceiveAnError(t *testing.T) {
	order := Order{}
	assert.Error(t, order.IsValid(), "invalid id")
}

func TestGivenAnEmptyPriceWhenCreateANewOrderThenShouldReceiveAnError(t *testing.T) {
	order := Order{Id: "123"}
	assert.Error(t, order.IsValid(), "invalid price")
}

func TestGivenAnEmptyTaxWhenCreateANewOrderThenShouldReceiveAnError(t *testing.T) {
	order := Order{Id: "123", Price: 10.0}
	assert.Error(t, order.IsValid(), "invalid tax")
}

func TestGivenAValidParamsWhenCallNewOrderThenShouldReceiveCreateOrderWithAllParams(t *testing.T) {
	order := Order{
    Id: "123",
    Price: 10.0,
    Tax: 2.0,
  }
	assert.Equal(t, "123", order.Id)
	assert.Equal(t, 10.0, order.Price)
	assert.Equal(t, 2.0, order.Tax)
  assert.Nil(t, order.IsValid())
}

func TestGivenAPriceAndTaxWhenCallCalculatePriceThenShouldSetFinalPrice(t *testing.T) {
  order, err := NewOrder("123", 10.0, 2.0)
  assert.Nil(t, err)
  assert.Nil(t, order.CalculateFinalPrice())
  assert.Equal(t, 12.0, order.FinalPrice)
}

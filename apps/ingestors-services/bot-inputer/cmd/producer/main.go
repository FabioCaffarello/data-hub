package main

import (
	"bot-inputer/internal/entity"
	"encoding/json"
	"math/rand"
	"time"

	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
)

func Publish(ch *amqp.Channel, order entity.Order) error {
	body, err := json.Marshal(order)
	if err != nil {
		return err
	}
	err = ch.Publish(
		"amq.direct",
		"",
		false,
		false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		},
	)
	if err != nil {
		return err
	}
	return nil
}

func GenerateOrders() entity.Order {
	return entity.Order{
		Id:    uuid.New().String(),
		Price: rand.Float64() * 100,
		Tax:   rand.Float64() * 10,
	}
}

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
	if err != nil {
		panic(err)
	}
	defer conn.Close()
	ch, err := conn.Channel()
	if err != nil {
		panic(err)
	}
	defer ch.Close()
	for i := 0; i < 100; i++ {
		Publish(ch, GenerateOrders())
		time.Sleep(300 * time.Millisecond)
	}
}

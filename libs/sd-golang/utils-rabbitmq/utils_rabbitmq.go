package utils_rabbitmq

import (
	"fmt"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"
)

type RabbitMQHandler struct {
	conn *amqp.Connection
	ch   *amqp.Channel
	qs   map[string]amqp.Queue
}

func NewRabbitMQHandler(amqpURI string, queueNames []string) (*RabbitMQHandler, error) {
	conn, err := amqp.Dial(amqpURI)
	if err != nil {
		panic(err)
	}

	ch, err := conn.Channel()
	if err != nil {
		panic(err)
	}

	qs := make(map[string]amqp.Queue)
	for _, queueName := range queueNames {
		q, err := ch.QueueDeclare(
			queueName, // name
			false,     // durable
			false,     // delete when unused
			false,     // exclusive
			false,     // no-wait
			nil,       // arguments
		)
		if err != nil {
			return nil, err
		}

		qs[queueName] = q
	}

	return &RabbitMQHandler{conn: conn, ch: ch, qs: qs}, nil
}

func (h *RabbitMQHandler) Close() {
	h.ch.Close()
	h.conn.Close()
}

func (h *RabbitMQHandler) Publish(queueName string, message []byte) error {
	q, ok := h.qs[queueName]
	if !ok {
		return fmt.Errorf("queue '%s' not found", queueName)
	}

	err := h.ch.Publish(
		"",       // exchange
		q.Name,   // routing key
		false,    // mandatory
		false,    // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        message,
		},
	)
	if err != nil {
		return err
	}

	log.Printf("Sent message to queue '%s': %s", queueName, message)
	return nil
}

func (h *RabbitMQHandler) Consume(queueName string) (<-chan []byte, error) {
	q, ok := h.qs[queueName]
	if !ok {
		return nil, fmt.Errorf("queue '%s' not found", queueName)
	}

	msgs, err := h.ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	if err != nil {
		return nil, err
	}

	ch := make(chan []byte)
	go func() {
		for d := range msgs {
			ch <- d.Body
		}
	}()
	return ch, nil
}
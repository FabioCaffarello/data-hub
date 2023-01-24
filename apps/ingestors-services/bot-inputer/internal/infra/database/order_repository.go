package database

import (
	"bot-inputer/internal/entity"
	"database/sql"
)

type OrderRepository struct {
  Db *sql.DB
}

func NewOrderRepository(db *sql.DB) *OrderRepository {
  return &OrderRepository{Db: db}
}

func (r *OrderRepository) Save(order *entity.Order) error {
  stmt, err := r.Db.Prepare("INSERT INTO orders (id, price, tax, final_price) VALUES (?, ?, ?, ?)")
  if err != nil {
    return err
  }
  _, err = stmt.Exec(order.Id, order.Price, order.Tax, order.FinalPrice)
  if err != nil {
    return err
  }
  return nil
}

func (r *OrderRepository) GetTotal() (float64, error) {
  var total float64
  err := r.Db.QueryRow("SELECT count(*) FROM orders").Scan(&total)
  if err != nil {
    return 0, err
  }
  return total, nil
}

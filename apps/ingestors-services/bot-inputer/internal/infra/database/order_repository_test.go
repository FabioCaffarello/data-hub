package database

import (
	"bot-inputer/internal/entity"
	"database/sql"
	"testing"

	"github.com/stretchr/testify/suite"
  _ "github.com/mattn/go-sqlite3"
)

type OrderRepositoryTestSuite struct {
	suite.Suite
	Db *sql.DB
}

func (suite *OrderRepositoryTestSuite) SetupSuite() {
	db, err := sql.Open("sqlite3", ":memory:")
	suite.NoError(err)
	db.Exec("CREATE TABLE orders (id varcahar(255) NOT NULL, price float NOT NULL, tax float NOT NULL, final_price float NOT NULL, PRIMARY KEY (id))")
	suite.Db = db
}

func (suite *OrderRepositoryTestSuite) TearDownTest() {
	suite.Db.Close()
}

func TestSuite(t *testing.T) {
	suite.Run(t, new(OrderRepositoryTestSuite))
}

func (suite *OrderRepositoryTestSuite) TestGivenAnOrderWhenSaveThenShouldSaveOrder() {
	order, err := entity.NewOrder("123", 10.0, 2.0)
	suite.NoError(err)
	suite.NoError(order.CalculateFinalPrice())
	repo := NewOrderRepository(suite.Db)
	err = repo.Save(order)
  suite.NoError(err)

	var orderResult entity.Order
	err = suite.Db.QueryRow("select id, price, tax, final_price form orders where id = ?", order.Id).
		Scan(&orderResult.Id, &orderResult.Price, &orderResult.Tax, &orderResult.FinalPrice)

	suite.NoError(err)
  suite.Equal(order.Id, orderResult.Id)
  suite.Equal(order.Price, orderResult.Price)
  suite.Equal(order.Tax, orderResult.Tax)
  suite.Equal(order.FinalPrice, orderResult.FinalPrice)
}

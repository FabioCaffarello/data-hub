package usecase

import (
	"bot-inputer/internal/entity"
	"bot-inputer/internal/infra/database"
	"database/sql"
	"testing"

	_ "github.com/mattn/go-sqlite3"
	"github.com/stretchr/testify/suite"
)

type CalculateFinalPriceUseCaseTestSuite struct {
	suite.Suite
	OrderRepository database.OrderRepository // FIXME entity.OrderRepositoryInterface
	Db              *sql.DB
}


func (suite *CalculateFinalPriceUseCaseTestSuite) SetupSuite() {
	db, err := sql.Open("sqlite3", ":memory:")
	suite.NoError(err)
	db.Exec("CREATE TABLE orders (id varcahar(255) NOT NULL, price float NOT NULL, tax float NOT NULL, final_price float NOT NULL, PRIMARY KEY (id))")
	suite.Db = db
}

func (suite *CalculateFinalPriceUseCaseTestSuite) TearDownTest() {
	suite.Db.Close()
}

func TestSuite(t *testing.T) {
	suite.Run(t, new(CalculateFinalPriceUseCaseTestSuite))
}

func (suite CalculateFinalPriceUseCaseTestSuite) TestCalculateFinalPrice() {
  order, err := entity.NewOrder("123", 10, 2)
	suite.NoError(err)
	order.CalculateFinalPrice()

  calculateFinalPriceInput := OrderInputDTO{
    Id: order.Id,
    Price: order.Price,
    Tax: order.Tax,
  }
  CalculateFinalPriceUseCase := NewCalculateFinalPriceUseCase(suite.OrderRepository)
  output, err := CalculateFinalPriceUseCase.Execute(calculateFinalPriceInput)
  suite.NoError(err)
  suite.Equal(order.Id, output.Id)
  suite.Equal(order.Price, output.Price)
  suite.Equal(order.Tax, output.Tax)
  suite.Equal(order.FinalPrice, output.FinalPrice)
}


package usecase

import "bot-inputer/internal/entity"

type GetTotalOutputDTO struct {
  Total float64
}

type GetTotalUseCase struct {
  OrderRepository entity.OrderRepositoryInterface
}

func NewGetTotalInterface(orderRepository entity.OrderRepositoryInterface) *GetTotalUseCase {
  return &GetTotalUseCase{
    OrderRepository: orderRepository,
  }
}

func (c *GetTotalUseCase) Execute() (*GetTotalOutputDTO, error) {
  total, err := c.OrderRepository.GetTotal()
  if err != nil {
    return nil, err
  }
  return &GetTotalOutputDTO{
    Total: total,
  }, nil
}

package database

import (
  "apps/ingestors-services/ingestors-handler/internal/entity"
)


type InputInterface interface {
  Create(input *entity.Input, collectionName string) error
  FindById(md5id string, collectionName string) (*entity.Input, error)
  // TODO: ADD FindAll
  // TODO: ADD Update
  // TODO: ADD Delete (danger)
  // TODO: ADD REPROCESS BY ID
}


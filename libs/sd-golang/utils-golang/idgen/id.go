package idgen

import (
	"crypto/md5"
	"encoding/hex"
)

type ID string

func NewID(data string) (ID, error) {
	hasher := md5.New()
	hasher.Write([]byte(data))
	id := hex.EncodeToString(hasher.Sum(nil))
	return ID(id), nil
}

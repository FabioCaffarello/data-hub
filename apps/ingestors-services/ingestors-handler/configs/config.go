package configs

import (
	"github.com/go-chi/jwtauth"
	"github.com/spf13/viper"
)


var cfg *conf

func NewConfig() *conf {
  return cfg
}

type conf struct {
  // TODO: Need to change for no exportable, but need to check viper docs...
	DBDriver      string           `mapstructure:"DB_DRIVER"`
	DBHost        string           `mapstructure:"DB_HOST"`
	DBPort        string           `mapstructure:"DB_PORT"`
	DBUser        string           `mapstructure:"DB_USER"`
	DBPassword    string           `mapstructure:"DB_PASSWORD"`
	DBName        string           `mapstructure:"DB_NAME"`
	WebServerPort string           `mapstructure:"DB_SERVER_PORT"`
	JWTScret      string           `mapstructure:"JWT_SECRET"`
	JWTExpiresIn  int              `mapstructure:"JWT_EXPIRESIN"`
  MongoUri      string           `mapstructure:"MONGO_URI"`
  MongoDBName   string           `mapstructure:"MONGO_DB_NAME"`
	TokenAuth     *jwtauth.JWTAuth
}

func (c *conf) GetBDDriver() string {
  return c.DBDriver
}

func (c *conf) GetMongoUri() string {
  return c.MongoUri
}

func (c *conf) GetMongoDBName() string {
  return c.MongoDBName
}

func init() {
	viper.SetConfigName("ingestor_handler_config")
	viper.SetConfigType("env")
	viper.AddConfigPath(".")
	viper.SetConfigFile(".env")
	viper.AutomaticEnv()
	err := viper.ReadInConfig()
	if err != nil {
		panic(err)
	}
	err = viper.Unmarshal(&cfg)
	if err != nil {
		panic(err)
	}
	cfg.TokenAuth = jwtauth.New("HS256", []byte(cfg.JWTScret), nil)
}

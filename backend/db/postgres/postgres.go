package postgres

import "fmt"

type Config struct {
	DBName   string
	Username string
	Password string
	Host     string
	Port     uint16
	SSLMode  sslMode
	TimeZone string // TODO: Look into timezone datatype
}

func (c Config) Connection() string {
	return fmt.Sprintf("host=%v user=%v password=%v dbname=%v port=%v sslmode=%v TimeZone=%v", c.Host, c.Username, c.Password, c.DBName, c.Port, c.SSLMode.getMode(), c.TimeZone)
}

package mysql

import "fmt"

type Config struct {
	DBName    string
	Username  string
	Password  string
	Host      string
	Port      uint16
	Charset   string
	ParseTime bool
	Loc       string
}

func (c Config) Connection() string {
	return fmt.Sprintf("%v:%v@tcp(%v:%v)/%v?charset=%v&parseTime=%t&loc=%v", c.Username, c.Password, c.Host, c.Port, c.DBName, c.Charset, c.ParseTime, c.Loc)
}

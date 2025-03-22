package db

type DBConfig interface {
	Connection() string
}

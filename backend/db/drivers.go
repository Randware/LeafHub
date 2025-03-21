package db

type SQLiteConfig struct {
	Path string
}

type MySQLConfig struct {
	DBName    string
	Username  string
	Password  string
	Host      string
	Port      uint16
	Charset   string
	ParseTime bool
	Loc       string
}

type PostgresConfig struct {
	DBName   string
	Username string
	Password string
	Host     string
	Port     uint16
	SSLmode  bool
	TimeZone string // TODO: Look into timezone datatype
}

package main

import (
	"backend/db"
	"backend/db/mysql"
	"backend/db/postgres"
	"backend/db/sqlite"
)

func main() {

	p := postgres.Config{
		DBName:   "Test",
		Username: "TestName",
		Password: "TestPassword",
		Port:     6900,
		Host:     "randware.org",
		SSLMode:  postgres.Require,
		TimeZone: "Local",
	}

	db.Start(p)

	s := sqlite.Config{
		Path: "C:\\User\\Me\\Temp",
	}

	db.Start(s)

	m := mysql.Config{
		DBName:    "TestDB",
		Username:  "TestUser",
		Password:  "TestPassword",
		Port:      6969,
		Host:      "randware.org",
		Loc:       "Local",
		Charset:   "UTF-8",
		ParseTime: true,
	}

	db.Start(m)
}

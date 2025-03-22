package db

import "fmt"

func Start(config DBConfig) {
	// TODO: I am going back to 505
	fmt.Println(config.Connection())
}

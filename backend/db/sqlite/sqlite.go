package sqlite

import "fmt"

type Config struct {
	Path string
}

func (c Config) Connection() string {
	return fmt.Sprintf("%v", c.Path)
}

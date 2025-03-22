package postgres

var (
	Default    = prefer{}
	Disable    = disable{}
	Prefer     = prefer{}
	Allow      = allow{}
	Require    = require{}
	VerifyCa   = verifyCa{}
	VerifyFull = verifyFull{}
)

type sslMode interface {
	getMode() string
}

type disable struct{}

func (d disable) getMode() string {
	return "disable"
}

type prefer struct{}

func (p prefer) getMode() string {
	return "prefer"
}

type allow struct{}

func (a allow) getMode() string {
	return "allow"
}

type require struct{}

func (r require) getMode() string {
	return "require"
}

type verifyCa struct{}

func (v verifyCa) getMode() string {
	return "verify-ca"
}

type verifyFull struct{}

func (v verifyFull) getMode() string {
	return "verify-full"
}

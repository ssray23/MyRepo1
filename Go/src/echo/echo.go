// echo.exe prints its arguments (separated by space) when run through command prompt
package main

import (
	"fmt"
	"os"
)

func main() {
	var s, sep string
	for i := 1; i < len(os.Args); i++ {
		s += sep + os.Args[i]
		sep = " ...  "
	}
	fmt.Println(s)
}
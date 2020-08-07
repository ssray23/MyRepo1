// echo2.exe prints its command-line arguments.
// $ echo2.exe Suddha Satta Ray
package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {

	fmt.Println(strings.Join(os.Args[1:], " "))
}

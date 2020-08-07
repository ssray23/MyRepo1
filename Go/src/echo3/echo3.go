// echo3.exe  prints its command-line arguments (including the command's name also i.e. echo3)
// $ echo3.exe Suddha Satta Ray  ((PRESS ENTER))
// $ echo3 Suddha Satta Ray
package main

import (
	"fmt"
	"os"
)

func main() {
	s, sep := "", ""
	for _, arg := range os.Args[0:] {
		s += sep + arg
		sep = " "
	}
	fmt.Println(s)

	// fmt.Println(os.Args[1:])

	// fmt.Println(strings.Join(os.Args[1:], ""))
}

// echo4.exe  prints its command-line arguments
// Print the index and value of each of its arguments, one per line.
// $ echo4.exe Suddha Satta Ray  ((PRESS ENTER))
//   0 Suddha
//   1 Satta
//   2 Ray

package main

import (
	"fmt"
	"os"
)

func main() {
	sep := "  ..  "
	for i, arg := range os.Args[1:] {
		fmt.Println(i, sep, arg)
	}
	// fmt.Println(s)
	// fmt.Println(os.Args[1:])
	// fmt.Println(strings.Join(os.Args[1:], ""))
}

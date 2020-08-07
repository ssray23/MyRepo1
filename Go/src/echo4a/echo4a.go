// echo4a.exe  prints its command-line arguments and displays elapsed time also
// Print the index and value of each of its arguments, one per line.
// $ echo4a.exe Suddha Satta Ray  ((PRESS ENTER))
//   0 Suddha
//   1 Satta
//   2 Ray

package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	start := time.Now()
	sep := " "
	for i, arg := range os.Args[1:] {
		fmt.Println(i, sep, arg)
	}
	fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())}

// echo2a.exe prints its command-line arguments and displayed elapsed time
// $ echo2.exe Suddha Satta Ray
// Suddha Satta Ray
package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {

    start := time.Now()
	fmt.Println(strings.Join(os.Args[1:], " "))
	fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())
}

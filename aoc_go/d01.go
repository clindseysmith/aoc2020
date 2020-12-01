package main

import (
    "fmt"
    "os"
    "bufio"
    "strconv"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func main() {
    file, err := os.Open("../d01_input.txt")
    check(err)
    scanner := bufio.NewScanner(file)
    scanner.Split(bufio.ScanLines)
    data := make([]int, 0)
    for scanner.Scan() {
        num, err := strconv.Atoi(scanner.Text())
        check(err)
        data = append(data, num)
    }

    m := make(map[int]bool)
    for idx1 := 0; idx1 < len(data); idx1++ {
        num := data[idx1]
        if m[2020-num] {
            fmt.Println("PART1:", num, 2020-num, num*(2020-num))
        } else {
            m[num] = true
        }
        m2 := make(map[int]bool)
        for idx2 := 0; idx2 < len(data); idx2++ {
            num2 := data[idx2]
            if m2[2020-num-num2] {
                fmt.Println("PART2:", num, num2, 2020-num-num2, num*num2*(2020-num-num2))
            } else {
                m2[num2] = true
            }
        }
    }
}


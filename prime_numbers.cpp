#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;
using namespace std::chrono;

// Function 1: Basic prime check
bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }
    return true;
}

// Function 2: Optimized prime check
bool isPrimeOptimized(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    int limit = sqrt(n);
    for (int i = 3; i <= limit; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Function 3: Sieve of Eratosthenes - finds all primes up to n
vector<int> sieveOfEratosthenes(int n) {
    vector<bool> prime(n + 1, true);
    vector<int> primes;
    
    prime[0] = prime[1] = false;
    
    for (int p = 2; p * p <= n; p++) {
        if (prime[p]) {
            for (int i = p * p; i <= n; i += p) {
                prime[i] = false;
            }
        }
    }
    
    for (int i = 2; i <= n; i++) {
        if (prime[i]) {
            primes.push_back(i);
        }
    }
    
    return primes;
}

// Function 4: Generate first n prime numbers
vector<int> generateNPrimes(int n) {
    vector<int> primes;
    int candidate = 2;
    
    while (primes.size() < n) {
        if (isPrime(candidate)) {
            primes.push_back(candidate);
        }
        candidate++;
    }
    
    return primes;
}

// Function 5: Check if a number is prime using trial division
bool isPrimeTrial(long long n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }
    return true;
}

// Function 6: Find prime factors of a number
vector<int> primeFactors(int n) {
    vector<int> factors;
    
    // Handle factor 2
    while (n % 2 == 0) {
        factors.push_back(2);
        n /= 2;
    }
    
    // Handle odd factors
    for (int i = 3; i <= sqrt(n); i += 2) {
        while (n % i == 0) {
            factors.push_back(i);
            n /= i;
        }
    }
    
    // If n is still greater than 2, it's a prime factor
    if (n > 2) {
        factors.push_back(n);
    }
    
    return factors;
}

// Function 7: Check for twin primes
void findTwinPrimes(int limit) {
    cout << "\n🔗 Twin Primes up to " << limit << ":" << endl;
    cout << "Twin primes are pairs of primes that differ by 2." << endl;
    
    for (int i = 2; i <= limit - 2; i++) {
        if (isPrime(i) && isPrime(i + 2)) {
            cout << "(" << i << ", " << i + 2 << ") ";
        }
    }
    cout << endl;
}

// Display functions
void displayPrimes(const vector<int>& primes) {
    cout << "Primes: ";
    for (int i = 0; i < primes.size(); i++) {
        cout << primes[i];
        if (i < primes.size() - 1) cout << ", ";
    }
    cout << endl;
}

void displayFactors(int n, const vector<int>& factors) {
    cout << "Prime factors of " << n << ": ";
    for (int i = 0; i < factors.size(); i++) {
        cout << factors[i];
        if (i < factors.size() - 1) cout << " × ";
    }
    cout << endl;
}

int main() {
    cout << "🔢 PRIME NUMBERS IN C++ - Comprehensive Demo" << endl;
    cout << "=============================================" << endl;
    
    // Demo 1: Check individual numbers
    cout << "\n1️⃣ Prime Check Demo:" << endl;
    vector<int> testNumbers = {2, 17, 25, 97, 100, 101, 997};
    
    for (int num : testNumbers) {
        cout << num << " is " << (isPrime(num) ? "PRIME" : "NOT PRIME") << endl;
    }
    
    // Demo 2: Find primes up to 100 using Sieve
    cout << "\n2️⃣ Sieve of Eratosthenes - Primes up to 100:" << endl;
    auto start = high_resolution_clock::now();
    vector<int> primes100 = sieveOfEratosthenes(100);
    auto end = high_resolution_clock::now();
    
    displayPrimes(primes100);
    cout << "📊 Total: " << primes100.size() << " primes" << endl;
    auto duration = duration_cast<microseconds>(end - start);
    cout << "⏱️  Time: " << duration.count() << " microseconds" << endl;
    
    // Demo 3: Generate first 20 primes
    cout << "\n3️⃣ First 20 Prime Numbers:" << endl;
    vector<int> first20 = generateNPrimes(20);
    displayPrimes(first20);
    
    // Demo 4: Prime factorization
    cout << "\n4️⃣ Prime Factorization Demo:" << endl;
    vector<int> factorizeNumbers = {12, 60, 100, 315, 1001};
    
    for (int num : factorizeNumbers) {
        vector<int> factors = primeFactors(num);
        displayFactors(num, factors);
    }
    
    // Demo 5: Performance comparison
    cout << "\n5️⃣ Performance Comparison:" << endl;
    cout << "Testing primality of 982,451,653..." << endl;
    
    long long bigNumber = 982451653;
    
    start = high_resolution_clock::now();
    bool result1 = isPrimeTrial(bigNumber);
    end = high_resolution_clock::now();
    auto time1 = duration_cast<microseconds>(end - start);
    
    cout << "Result: " << bigNumber << " is " << (result1 ? "PRIME" : "NOT PRIME") << endl;
    cout << "Time taken: " << time1.count() << " microseconds" << endl;
    
    // Demo 6: Twin primes
    findTwinPrimes(50);
    
    // Demo 7: Interactive section
    cout << "\n6️⃣ Interactive Prime Checker:" << endl;
    cout << "Enter a number to check if it's prime (0 to exit): ";
    
    int userInput;
    while (cin >> userInput && userInput != 0) {
        if (userInput < 0) {
            cout << "Please enter a positive number." << endl;
        } else {
            bool result = isPrime(userInput);
            cout << userInput << " is " << (result ? "PRIME ✅" : "NOT PRIME ❌") << endl;
            
            if (!result && userInput > 1) {
                vector<int> factors = primeFactors(userInput);
                displayFactors(userInput, factors);
            }
        }
        cout << "\nEnter another number (0 to exit): ";
    }
    
    cout << "\n🎯 Prime Number Facts:" << endl;
    cout << "• There are infinitely many prime numbers (Euclid's theorem)" << endl;
    cout << "• 2 is the only even prime number" << endl;
    cout << "• All primes > 3 are of the form 6k±1" << endl;
    cout << "• The largest known prime has over 24 million digits!" << endl;
    cout << "\nThank you for exploring prime numbers! 🚀" << endl;
    
    return 0;
}

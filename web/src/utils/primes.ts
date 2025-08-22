/**
 * Check if a number is prime
 */
export function isPrime(n: number): boolean {
  if (n < 2) return false
  if (n === 2) return true
  if (n % 2 === 0) return false
  
  for (let i = 3; i <= Math.sqrt(n); i += 2) {
    if (n % i === 0) return false
  }
  return true
}

/**
 * Get the next prime number >= n
 */
export function nextPrime(n: number): number {
  let candidate = Math.max(2, Math.floor(n))
  while (!isPrime(candidate)) {
    candidate++
  }
  return candidate
}

/**
 * Get all prime numbers up to n
 */
export function getPrimesUpTo(n: number): number[] {
  const primes: number[] = []
  for (let i = 2; i <= n; i++) {
    if (isPrime(i)) {
      primes.push(i)
    }
  }
  return primes
}
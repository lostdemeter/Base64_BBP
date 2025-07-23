"""
BBP-like Base-64 Formula for π
==============================

This module implements a BBP-like formula for calculating π in base 64,
based on a known decomposition using arctan series in base -64 and base -1024.

Formula: π/4 = (1/16) Σ[n=0 to ∞] (-1)^n / 64^n * (8/(4n+1) + 4/(4n+2) + 1/(4n+3))
             + (1/256) Σ[n=0 to ∞] (-1)^n / 1024^n * (32/(4n+1) + 8/(4n+2) + 1/(4n+3))

This provides an exact formula, allowing high accuracy limited only by precision and terms.

Author: Adapted from experimental code
Date: 2025
"""

from decimal import Decimal, getcontext
import math

class BBPBase64:
    """
    BBP-like formula for π in base 64

    This class implements the formula:
    π/4 = (1/16) Σ[n=0 to ∞] (-1)^n / 64^n * (8/(4n+1) + 4/(4n+2) + 1/(4n+3))
          + (1/256) Σ[n=0 to ∞] (-1)^n / 1024^n * (32/(4n+1) + 8/(4n+2) + 1/(4n+3))
    """

    def __init__(self, precision=100):
        """
        Initialize the BBP Base-64 calculator

        Args:
            precision (int): Decimal precision for calculations (default: 100)
        """
        self.precision = precision
        getcontext().prec = precision

    def calculate_pi(self, num_terms=100):
        """
        Calculate π using the BBP-like base-64 formula

        Args:
            num_terms (int): Maximum number of terms to sum for each series (default: 100)

        Returns:
            Decimal: Approximation of π
        """
        # First sum: base -64 part
        sum1 = Decimal(0)
        for n in range(num_terms):
            sign = Decimal(-1) ** n
            denom = Decimal(64) ** n
            term1 = Decimal(8) / (4 * n + 1)
            term2 = Decimal(4) / (4 * n + 2)
            term3 = Decimal(1) / (4 * n + 3)
            coeff = term1 + term2 + term3
            term = sign * coeff / denom
            sum1 += term
            if abs(term) < Decimal(10) ** (-self.precision + 10):
                break
        sum1 /= 16

        # Second sum: base -1024 part
        sum2 = Decimal(0)
        for n in range(num_terms):
            sign = Decimal(-1) ** n
            denom = Decimal(1024) ** n
            term1 = Decimal(32) / (4 * n + 1)
            term2 = Decimal(8) / (4 * n + 2)
            term3 = Decimal(1) / (4 * n + 3)
            coeff = term1 + term2 + term3
            term = sign * coeff / denom
            sum2 += term
            if abs(term) < Decimal(10) ** (-self.precision + 10):
                break
        sum2 /= 256

        return Decimal(4) * (sum1 + sum2)

    def calculate_with_convergence_info(self, max_terms=200):
        """
        Calculate π and show convergence information

        Args:
            max_terms (int): Maximum number of terms to use

        Returns:
            tuple: (final_result, convergence_info)
        """
        convergence_info = []
        pi_sum = Decimal(0)

        checkpoints = [10, 25, 50, 75, 100, 150, 200]
        checkpoint_idx = 0

        # Since there are two sums, we'll approximate convergence by terms in the main sum
        sum1 = Decimal(0)
        sum2 = self._compute_sum2(max_terms)  # Compute full sum2 as it converges fast

        for n in range(max_terms):
            sign = Decimal(-1) ** n
            denom = Decimal(64) ** n
            term1 = Decimal(8) / (4 * n + 1)
            term2 = Decimal(4) / (4 * n + 2)
            term3 = Decimal(1) / (4 * n + 3)
            coeff = term1 + term2 + term3
            term = sign * coeff / denom
            sum1 += term

            current_sum1 = sum1 / 16
            current_pi = Decimal(4) * (current_sum1 + sum2 / 256)

            # Record convergence at checkpoints
            if checkpoint_idx < len(checkpoints) and n + 1 == checkpoints[checkpoint_idx]:
                convergence_info.append((n + 1, current_pi))
                checkpoint_idx += 1

            # Early termination
            if abs(term) < Decimal(10) ** (-self.precision + 10):
                break

        return current_pi, convergence_info

    def _compute_sum2(self, max_terms):
        sum2 = Decimal(0)
        for n in range(max_terms):
            sign = Decimal(-1) ** n
            denom = Decimal(1024) ** n
            term1 = Decimal(32) / (4 * n + 1)
            term2 = Decimal(8) / (4 * n + 2)
            term3 = Decimal(1) / (4 * n + 3)
            coeff = term1 + term2 + term3
            term = sign * coeff / denom
            sum2 += term
            if abs(term) < Decimal(10) ** (-self.precision + 10):
                break
        return sum2

    def compare_with_pi(self, result=None, num_terms=100):
        """
        Compare the formula result with the true value of π

        Args:
            result (Decimal, optional): Pre-calculated result. If None, calculates it.
            num_terms (int): Number of terms to use if calculating

        Returns:
            dict: Comparison information
        """
        if result is None:
            result = self.calculate_pi(num_terms)

        # High-precision π for comparison
        pi_reference = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")

        # Count matching digits
        result_str = str(result)
        pi_str = str(pi_reference)

        matches = 0
        for i in range(min(len(result_str), len(pi_str))):
            if result_str[i] == pi_str[i]:
                matches += 1
            else:
                break

        error = abs(result - pi_reference)
        relative_error = error / pi_reference

        return {
            'result': result,
            'reference': pi_reference,
            'matching_digits': matches - 1,  # Subtract 1 for the integer part '3'
            'absolute_error': error,
            'relative_error': relative_error,
            'result_str': result_str[:30],
            'reference_str': pi_str[:30]
        }

    def extract_base64_digits(self, start_digit=0, num_digits=10):
        """
        Extract specific digits of π in base 64 (experimental)

        This is a simplified implementation - true BBP digit extraction
        would require more sophisticated modular arithmetic.

        Args:
            start_digit (int): Starting digit position
            num_digits (int): Number of digits to extract

        Returns:
            list: Base-64 digits
        """
        # Calculate π with high precision
        pi_val = self.calculate_pi(num_terms=200)

        # Convert to base 64 (simplified approach)
        # Remove integer part
        fractional_part = pi_val - int(pi_val)

        digits = []
        for i in range(num_digits + start_digit):
            fractional_part *= 64
            digit = int(fractional_part)
            digits.append(digit)
            fractional_part -= digit

        return digits[start_digit:]


def demo():
    """Demonstration of the BBP Base-64 formula"""
    print("BBP-like Base-64 Formula for π")
    print("=" * 50)

    # Create calculator
    calc = BBPBase64(precision=150)

    print("Formula: π/4 = (1/16) Σ[n=0 to ∞] (-1)^n / 64^n * (8/(4n+1) + 4/(4n+2) + 1/(4n+3))\n"
          "             + (1/256) Σ[n=0 to ∞] (-1)^n / 1024^n * (32/(4n+1) + 8/(4n+2) + 1/(4n+3))")
    print()

    # Calculate π
    print("Calculating π...")
    result = calc.calculate_pi(num_terms=100)

    # Compare with true π
    comparison = calc.compare_with_pi(result)

    print(f"Result:     {comparison['result_str']}")
    print(f"π (true):   {comparison['reference_str']}")
    print(f"Matching digits: {comparison['matching_digits']}")
    print(f"Absolute error:  {comparison['absolute_error']:.2e}")
    print(f"Relative error:  {comparison['relative_error']:.2e}")
    print()

    # Show convergence
    print("Convergence Analysis:")
    print("-" * 30)
    result_conv, conv_info = calc.calculate_with_convergence_info()

    for terms, value in conv_info:
        comp = calc.compare_with_pi(value)
        print(f"Terms: {terms:3d} | Matching digits: {comp['matching_digits']} | Value: {str(value)[:20]}...")

    print()

    # Extract some base-64 digits
    print("First 10 base-64 digits of π (fractional part):")
    digits = calc.extract_base64_digits(0, 10)
    print(f"Base-64: {digits}")
    print(f"Decimal equivalents: {[f'{d}/64' for d in digits[:5]]}")


if __name__ == "__main__":
    demo()

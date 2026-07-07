"""
Test Suite for SCS-CN Runoff Calculation Module
AI-Augmented Software Engineering - Smart Water Lab Series

Comprehensive test coverage including:
1. Core formula correctness
2. Physical boundary conditions
3. Edge cases and error handling
4. Vectorized operations
5. Physical constraints validation

Test Framework: pytest
Run with: python -m pytest test_scscn.py -v
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scscn_runoff import calculate_runoff, calculate_S, calculate_Ia, runoff_coefficient


# =============================================================================
# TEST GROUP 1: Expected Results (Known Values)
# =============================================================================

class TestKnownValues:
    """Test against known expected results."""

    def test_example_from_experiment(self):
        """
        Test the example from the experiment document:
        P = 50mm, CN = 80
        Expected: S = 63.5, Ia = 12.7, Q = 13.8
        """
        P, CN = 50.0, 80
        S = calculate_S(CN)
        Ia = calculate_Ia(CN)
        Q = calculate_runoff(P, CN)

        assert S == pytest.approx(63.5, abs=0.1)
        assert Ia == pytest.approx(12.7, abs=0.1)
        assert Q == pytest.approx(13.8, abs=0.2)

    def test_low_cn_woods(self):
        """Test with low CN (woods, good condition): CN = 60"""
        P, CN = 100.0, 60
        Q = calculate_runoff(P, CN)
        S = calculate_S(CN)

        assert S == pytest.approx(169.33, abs=0.1)
        assert Q > 0
        assert Q <= P  # Physical constraint

    def test_high_cn_paved(self):
        """Test with high CN (paved area): CN = 95"""
        P, CN = 50.0, 95
        Q = calculate_runoff(P, CN)
        S = calculate_S(CN)

        assert S == pytest.approx(13.37, abs=0.1)
        assert Q > 0
        assert Q <= P

    def test_maximum_cn(self):
        """Test boundary: CN = 100 (impervious surface)"""
        P, CN = 50.0, 100
        Q = calculate_runoff(P, CN)
        S = calculate_S(CN)
        Ia = calculate_Ia(CN)

        assert S == 0.0
        assert Ia == 0.0
        # When S=0, Q = P^2 / P = P
        assert Q == pytest.approx(P, abs=0.1)


# =============================================================================
# TEST GROUP 2: Boundary Conditions
# =============================================================================

class TestBoundaryConditions:
    """Test physical boundary conditions."""

    def test_no_rainfall(self):
        """Test P = 0: No rainfall means no runoff."""
        Q = calculate_runoff(0, 80)
        assert Q == 0.0

    def test_p_less_than_ia(self):
        """Test P < Ia: Runoff should be 0."""
        # For CN=80, Ia = 12.7, so P=10 should give Q=0
        Q = calculate_runoff(10, 80)
        assert Q == 0.0

    def test_p_equal_to_ia(self):
        """Test P = Ia: Boundary case, runoff should be 0."""
        CN = 80
        Ia = calculate_Ia(CN)
        Q = calculate_runoff(Ia, CN)
        assert Q == 0.0

    def test_p_slightly_above_ia(self):
        """Test P just above Ia: Small runoff should occur."""
        CN = 80
        Ia = calculate_Ia(CN)
        Q = calculate_runoff(Ia + 1, CN)
        assert Q > 0
        assert Q <= Ia + 1

    def test_p_very_large(self):
        """Test very large rainfall: Q should approach P."""
        P, CN = 1000.0, 80
        Q = calculate_runoff(P, CN)
        # For large P, Q should be close to P (but never exceed it)
        assert Q <= P
        assert Q > 0.9 * P  # Should be very close to P


# =============================================================================
# TEST GROUP 3: Physical Constraints
# =============================================================================

class TestPhysicalConstraints:
    """Test that physical constraints are always satisfied."""

    @pytest.mark.parametrize("P", [0, 5, 10, 25, 50, 100, 200])
    @pytest.mark.parametrize("CN", [60, 70, 80, 90, 95, 99])
    def test_q_never_exceeds_p(self, P, CN):
        """Physical constraint: Runoff cannot exceed rainfall."""
        Q = calculate_runoff(P, CN)
        assert Q <= P, f"Q={Q} exceeds P={P} for CN={CN}"

    @pytest.mark.parametrize("P", [0, 5, 10, 25, 50, 100])
    @pytest.mark.parametrize("CN", [60, 70, 80, 90, 95])
    def test_q_never_negative(self, P, CN):
        """Physical constraint: Runoff cannot be negative."""
        Q = calculate_runoff(P, CN)
        assert Q >= 0, f"Q={Q} is negative for P={P}, CN={CN}"

    def test_higher_cn_more_runoff(self):
        """Physical constraint: Higher CN produces more runoff."""
        P = 50.0
        cn_values = [60, 70, 80, 90, 95]
        runoff_values = [calculate_runoff(P, cn) for cn in cn_values]

        for i in range(len(runoff_values) - 1):
            assert runoff_values[i] <= runoff_values[i + 1], \
                f"CN={cn_values[i]} gives more runoff than CN={cn_values[i+1]}"

    def test_cn_100_maximum_runoff(self):
        """CN=100 should produce maximum possible runoff."""
        P = 50.0
        Q_max = calculate_runoff(P, 100)
        # For CN=100, Q should approximately equal P
        assert Q_max == pytest.approx(P, rel=0.01)


# =============================================================================
# TEST GROUP 4: Error Handling
# =============================================================================

class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_negative_p(self):
        """Test negative rainfall raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            calculate_runoff(-10, 80)

    def test_cn_zero(self):
        """Test CN = 0 raises ValueError."""
        with pytest.raises(ValueError, match="0, 100"):
            calculate_runoff(50, 0)

    def test_cn_negative(self):
        """Test negative CN raises ValueError."""
        with pytest.raises(ValueError, match="0, 100"):
            calculate_runoff(50, -10)

    def test_cn_greater_than_100(self):
        """Test CN > 100 raises ValueError."""
        with pytest.raises(ValueError, match="0, 100"):
            calculate_runoff(50, 105)

    def test_non_numeric_p(self):
        """Test non-numeric P raises TypeError."""
        with pytest.raises(TypeError):
            calculate_runoff("rain", 80)

    def test_non_numeric_cn(self):
        """Test non-numeric CN raises TypeError."""
        with pytest.raises(TypeError):
            calculate_runoff(50, "eighty")


# =============================================================================
# TEST GROUP 5: Vectorized Operations
# =============================================================================

class TestVectorizedOperations:
    """Test vectorized (numpy array) operations."""

    def test_array_p_scalar_cn(self):
        """Test array of P values with scalar CN."""
        P_values = np.array([0, 10, 25, 50, 100])
        CN = 80
        Q_values = calculate_runoff(P_values, CN)

        assert len(Q_values) == len(P_values)
        assert np.all(Q_values >= 0)
        assert np.all(Q_values <= P_values)

    def test_scalar_p_array_cn(self):
        """Test scalar P with array of CN values."""
        P = 50.0
        CN_values = np.array([60, 70, 80, 90, 95])
        Q_values = calculate_runoff(P, CN_values)

        assert len(Q_values) == len(CN_values)
        assert np.all(Q_values >= 0)
        assert np.all(Q_values <= P)
        # Check monotonicity
        assert np.all(np.diff(Q_values) >= 0)

    def test_array_p_array_cn(self):
        """Test array of P with array of CN (broadcast)."""
        P_values = np.array([25, 50, 75])
        CN_values = np.array([70, 80, 90])
        Q_values = calculate_runoff(P_values, CN_values)

        assert len(Q_values) == len(P_values)
        assert np.all(Q_values >= 0)


# =============================================================================
# TEST GROUP 6: Runoff Coefficient
# =============================================================================

class TestRunoffCoefficient:
    """Test runoff coefficient calculations."""

    def test_coefficient_range(self):
        """Runoff coefficient should be between 0 and 1."""
        C = runoff_coefficient(50, 80)
        assert 0 <= C <= 1

    def test_coefficient_zero_rainfall(self):
        """Coefficient should be 0 when P=0."""
        C = runoff_coefficient(0, 80)
        assert C == 0.0

    def test_coefficient_cn_100(self):
        """Coefficient should be close to 1 for CN=100."""
        C = runoff_coefficient(100, 100)
        assert C == pytest.approx(1.0, abs=0.01)


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    # Run with pytest if available, otherwise run basic tests
    try:
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Manual test runner
        tests = [
            ("Example from experiment", lambda: calculate_runoff(50, 80)),
            ("No rainfall", lambda: calculate_runoff(0, 80)),
            ("P < Ia", lambda: calculate_runoff(10, 80)),
            ("Boundary P=Ia", lambda: calculate_runoff(calculate_Ia(80), 80)),
            ("CN=100", lambda: calculate_runoff(50, 100)),
        ]

        print("\nRunning SCS-CN Runoff Tests")
        print("=" * 50)
        for name, test_fn in tests:
            try:
                result = test_fn()
                print(f"✅ {name}: Q = {result:.2f} mm")
            except Exception as e:
                print(f"❌ {name}: {e}")

        # Physical constraint check
        print("\nPhysical Constraint Checks")
        print("=" * 50)
        all_pass = True
        for P in [0, 10, 25, 50, 100, 200]:
            for CN in [60, 70, 80, 90, 95]:
                Q = calculate_runoff(P, CN)
                if Q > P:
                    print(f"❌ FAIL: Q={Q:.2f} > P={P} for CN={CN}")
                    all_pass = False
        if all_pass:
            print("✅ All physical constraints satisfied (Q <= P for all test cases)")

"""
Experiment 2: Hydrological Modeling - SCS-CN Runoff Calculation
AI-Augmented Software Engineering - Smart Water Lab Series

This module implements the Soil Conservation Service Curve Number (SCS-CN) method,
the most widely used approach for estimating direct runoff from rainfall.

Physical Background:
    The SCS-CN model calculates surface runoff using:
        Q = (P - Ia)^2 / (P - Ia + S)
    Where:
        S = (25400 / CN) - 254
        Ia = 0.2 * S
        Q = Runoff depth (mm)
        P = Rainfall depth (mm)
        CN = Curve Number (0-100)

Physical Boundary Conditions:
    - If P < Ia: No runoff occurs, Q = 0
    - Runoff cannot exceed rainfall: Q <= P
    - CN = 100: Impervious surface (maximum runoff)
    - CN = 0: All water infiltrates (Q = 0)

Reference:
    USDA NRCS National Engineering Handbook, Part 630
"""

import numpy as np
from typing import Union


def calculate_runoff(P: Union[float, np.ndarray],
                     CN: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate runoff depth using the SCS-CN method.

    Formula:
        Q = (P - Ia)^2 / (P - Ia + S)  [when P >= Ia]
        Q = 0                           [when P < Ia]
    Where:
        S = (25400 / CN) - 254
        Ia = 0.2 * S

    Physical Constraints Enforced:
        1. Q = 0 when P < Ia (no runoff before initial abstraction)
        2. Q <= P (runoff cannot exceed rainfall)
        3. CN must be in range (0, 100]
        4. P must be non-negative

    Args:
        P: Rainfall depth in millimeters (mm). Must be >= 0.
        CN: Curve Number (dimensionless, range 0-100).
            Higher values indicate less infiltration.
            - Woods, good condition: 60-70
            - Pasture, fair condition: 75-85
            - Cultivated, straight row: 80-90
            - Urban, residential: 75-95
            - Paved areas: 95-100

    Returns:
        Runoff depth Q in millimeters (mm).

    Raises:
        ValueError: If P < 0 or CN <= 0 or CN > 100.
        TypeError: If inputs are not numeric.

    Examples:
        >>> calculate_runoff(50, 80)
        13.80...
        >>> calculate_runoff(5, 80)  # P < Ia
        0.0
        >>> calculate_runoff(0, 80)  # No rainfall
        0.0
    """
    # Input validation
    if not isinstance(P, (int, float, np.ndarray)):
        raise TypeError(f"P must be numeric, got {type(P).__name__}")
    if not isinstance(CN, (int, float, np.ndarray)):
        raise TypeError(f"CN must be numeric, got {type(CN).__name__}")

    # Convert to numpy arrays for vectorized operations
    P = np.asarray(P, dtype=float)
    CN = np.asarray(CN, dtype=float)

    # Validate ranges
    if np.any(P < 0):
        raise ValueError("Rainfall P must be non-negative")
    if np.any(CN <= 0) or np.any(CN > 100):
        raise ValueError("Curve Number CN must be in range (0, 100]")

    # Calculate potential maximum retention S (mm)
    S = (25400.0 / CN) - 254.0

    # Calculate initial abstraction Ia (mm)
    Ia = 0.2 * S

    # Initialize runoff array
    Q = np.zeros_like(P, dtype=float)

    # Apply SCS-CN formula where P >= Ia
    # Mask for valid calculation (P >= Ia)
    valid_mask = P >= Ia

    if np.any(valid_mask):
        P_valid = P[valid_mask]
        S_valid = S[valid_mask] if S.size > 1 else S
        Ia_valid = Ia[valid_mask] if Ia.size > 1 else Ia

        # Calculate runoff for valid cases
        numerator = (P_valid - Ia_valid) ** 2
        denominator = P_valid - Ia_valid + S_valid

        # Avoid division by zero (shouldn't happen with valid inputs, but safety check)
        denom_mask = denominator > 0
        Q_valid = np.zeros_like(P_valid, dtype=float)
        Q_valid[denom_mask] = numerator[denom_mask] / denominator[denom_mask]

        # Assign back to full array
        Q[valid_mask] = Q_valid

    # Physical constraint: Q cannot exceed P
    Q = np.minimum(Q, P)

    # Physical constraint: Q cannot be negative
    Q = np.maximum(Q, 0)

    # Return scalar if inputs were scalars
    if Q.size == 1:
        return float(Q.item())
    return Q


def calculate_S(CN: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate potential maximum retention S from Curve Number.

    Formula: S = (25400 / CN) - 254

    Args:
        CN: Curve Number (0-100]

    Returns:
        Potential maximum retention S in mm.
    """
    CN = np.asarray(CN, dtype=float)
    if np.any(CN <= 0) or np.any(CN > 100):
        raise ValueError("CN must be in range (0, 100]")
    S = (25400.0 / CN) - 254.0
    return float(S) if S.size == 1 else S


def calculate_Ia(CN: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate initial abstraction Ia from Curve Number.

    Formula: Ia = 0.2 * S = 0.2 * ((25400 / CN) - 254)

    Args:
        CN: Curve Number (0-100]

    Returns:
        Initial abstraction Ia in mm.
    """
    S = calculate_S(CN)
    Ia = 0.2 * S
    return Ia


def runoff_coefficient(P: float, CN: float) -> float:
    """
    Calculate the runoff coefficient (C = Q / P).

    Args:
        P: Rainfall depth in mm.
        CN: Curve Number.

    Returns:
        Runoff coefficient (0 to 1).
    """
    if P == 0:
        return 0.0
    Q = calculate_runoff(P, CN)
    return Q / P


if __name__ == "__main__":
    # Example calculation
    P = 50.0  # mm
    CN = 80   # Urban residential area

    S = calculate_S(CN)
    Ia = calculate_Ia(CN)
    Q = calculate_runoff(P, CN)
    C = runoff_coefficient(P, CN)

    print(f"SCS-CN Runoff Calculation")
    print(f"{'='*40}")
    print(f"Rainfall (P): {P} mm")
    print(f"Curve Number (CN): {CN}")
    print(f"Max Retention (S): {S:.2f} mm")
    print(f"Initial Abstraction (Ia): {Ia:.2f} mm")
    print(f"Runoff Depth (Q): {Q:.2f} mm")
    print(f"Runoff Coefficient (C): {C:.4f}")
    print(f"Q <= P check: {Q <= P} ✅")

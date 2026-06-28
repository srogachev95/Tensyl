from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    GeneralizedResultant,
    GeneralizedStrain,
    HomogenizationResult,
    IsotropicMaterial,
    ReducedOrthotropicProperties,
    ValidityReport,
    generalized_strain,
    isotropic_plate,
)
from tensyl.verification import assert_hyperelastic_consistency


def _stiffness() -> ABDStiffness:
    A = np.diag([10.0, 12.0, 3.0])
    B = np.diag([1.0, 2.0, 0.5])
    D = np.diag([5.0, 6.0, 1.5])
    As = np.diag([4.0, 4.5])
    return ABDStiffness(A=A, B=B, D=D, As=As)


def test_abd_stiffness_assembles_expected_tangent() -> None:
    stiffness = _stiffness()

    assert stiffness.C8.shape == (8, 8)
    np.testing.assert_allclose(stiffness.C8[0:3, 0:3], stiffness.A)
    np.testing.assert_allclose(stiffness.C8[0:3, 3:6], stiffness.B)
    np.testing.assert_allclose(stiffness.C8[3:6, 0:3], stiffness.B)
    np.testing.assert_allclose(stiffness.C8[6:8, 6:8], stiffness.As)
    np.testing.assert_allclose(stiffness.C8, stiffness.C8.T)
    assert stiffness.A.base is stiffness.C8


def test_abd_stiffness_energy_resultants_and_tangent_are_consistent() -> None:
    stiffness = _stiffness()
    eta = generalized_strain(np.array([0.01, -0.02, 0.03, 0.004, -0.003, 0.002, 0.05, -0.04]))

    resultants = stiffness.resultants(eta)
    eta_array = np.asarray(eta)
    resultant_array = np.asarray(resultants)

    assert isinstance(eta, np.ndarray)
    assert isinstance(resultants, np.ndarray)
    np.testing.assert_allclose(resultant_array, stiffness.constant_tangent @ eta_array)
    np.testing.assert_allclose(resultant_array, stiffness.tangent(eta) @ eta_array)
    assert stiffness.energy(eta) == pytest.approx(0.5 * float(eta_array @ resultant_array))
    assert_hyperelastic_consistency(stiffness, eta)


def test_generalized_vector_constructors_are_public_boundary_types() -> None:
    eta = generalized_strain(np.zeros(8))
    resultant = stiffness_resultant = _stiffness().resultants(eta)

    assert GeneralizedStrain(eta) is eta
    assert GeneralizedResultant(resultant) is stiffness_resultant
    assert np.asarray(eta).flags.writeable is False
    assert np.asarray(resultant).flags.writeable is False


def test_abd_stiffness_is_hashable_and_readonly() -> None:
    stiffness = _stiffness()

    assert hash(stiffness) == hash(_stiffness())
    with pytest.raises(ValueError, match="assignment destination is read-only"):
        stiffness.C8[0, 0] = 99.0
    with pytest.raises(ValueError, match="assignment destination is read-only"):
        stiffness.A[0, 0] = 99.0


def test_abd_stiffness_rejects_bad_shapes_and_nonsymmetric_blocks() -> None:
    with pytest.raises(ValueError, match="A must have shape"):
        ABDStiffness(
            A=np.zeros((2, 2)),
            B=np.zeros((3, 3)),
            D=np.zeros((3, 3)),
            As=np.zeros((2, 2)),
        )

    with pytest.raises(ValueError, match="B must be symmetric"):
        ABDStiffness(
            A=np.eye(3),
            B=np.array([[1.0, 2.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
            D=np.eye(3),
            As=np.eye(2),
        )


def test_abd_stiffness_rejects_bad_eta_shape() -> None:
    stiffness = _stiffness()

    with pytest.raises(ValueError, match="eta must have shape"):
        stiffness.energy(np.zeros(7))


def test_reduced_orthotropic_properties_recover_isotropic_plate_constants() -> None:
    material = IsotropicMaterial(E=70.0e9, nu=0.3)
    thickness = 0.012
    stiffness = isotropic_plate(material, thickness=thickness)

    reduced = stiffness.reduced_orthotropic_properties(t_eff=thickness)

    assert isinstance(reduced, ReducedOrthotropicProperties)
    assert reduced.t_eff == pytest.approx(thickness)
    assert pytest.approx(material.E) == reduced.E1
    assert pytest.approx(material.E) == reduced.E2
    assert pytest.approx(material.E / (2.0 * (1.0 + material.nu))) == reduced.G12
    assert reduced.nu12 == pytest.approx(material.nu)
    assert reduced.nu21 == pytest.approx(material.nu)
    assert reduced.warnings == ()
    assert reduced.metadata["source"] == "reduced_orthotropic_properties"


def test_reduced_orthotropic_properties_recover_known_orthotropic_compliance() -> None:
    t_eff = 0.25
    E1 = 120.0
    E2 = 60.0
    G12 = 25.0
    nu12 = 0.28
    nu21 = nu12 * E2 / E1
    compliance = np.array(
        [
            [1.0 / E1, -nu12 / E1, 0.0],
            [-nu21 / E2, 1.0 / E2, 0.0],
            [0.0, 0.0, 1.0 / G12],
        ]
    )
    A = np.linalg.inv(compliance) * t_eff
    stiffness = ABDStiffness(A=A, B=np.zeros((3, 3)), D=np.eye(3), As=np.eye(2))

    reduced = stiffness.reduced_orthotropic_properties(t_eff=t_eff)

    assert pytest.approx(E1) == reduced.E1
    assert pytest.approx(E2) == reduced.E2
    assert pytest.approx(G12) == reduced.G12
    assert reduced.nu12 == pytest.approx(nu12)
    assert reduced.nu21 == pytest.approx(nu21)


def test_homogenization_result_delegates_reduced_orthotropic_properties() -> None:
    stiffness = isotropic_plate(IsotropicMaterial(E=10.0, nu=0.25), thickness=0.2)
    validity = ValidityReport(
        h_over_R=None,
        p_over_R=None,
        p_over_L_response=None,
        coupling_ratios={},
        warnings=(),
    )
    result = HomogenizationResult(
        stiffness=stiffness,
        validity=validity,
        diagnostics={},
        assumptions=(),
        source="imported",
    )

    reduced = result.reduced_orthotropic_properties(t_eff=0.2)

    assert reduced == stiffness.with_validity(validity).reduced_orthotropic_properties(t_eff=0.2)


def test_reduced_orthotropic_properties_reject_invalid_inputs() -> None:
    stiffness = _stiffness()

    with pytest.raises(ValueError, match="t_eff must be finite and positive"):
        stiffness.reduced_orthotropic_properties(t_eff=0.0)
    with pytest.raises(ValueError, match="tolerance must be finite and nonnegative"):
        stiffness.reduced_orthotropic_properties(t_eff=1.0, tolerance=-1.0)

    singular = ABDStiffness(
        A=np.diag([1.0, 0.0, 1.0]),
        B=np.zeros((3, 3)),
        D=np.eye(3),
        As=np.eye(2),
    )
    with pytest.raises(ValueError, match="A block must be invertible"):
        singular.reduced_orthotropic_properties(t_eff=1.0)


def test_reduced_orthotropic_properties_warn_about_discarded_terms() -> None:
    A = np.array(
        [
            [10.0, 1.0, 0.2],
            [1.0, 12.0, 0.3],
            [0.2, 0.3, 4.0],
        ]
    )
    B = np.diag([0.1, 0.0, 0.0])
    D = np.array(
        [
            [5.0, 0.0, 0.4],
            [0.0, 6.0, 0.5],
            [0.4, 0.5, 2.0],
        ]
    )
    validity = ValidityReport(
        h_over_R=None,
        p_over_R=None,
        p_over_L_response=None,
        coupling_ratios={"B_fro": 0.2},
        warnings=("membrane_bending_coupling_exceeds_threshold",),
    )
    stiffness = ABDStiffness(A=A, B=B, D=D, As=np.eye(2), validity=validity)

    reduced = stiffness.reduced_orthotropic_properties(t_eff=1.0, tolerance=1.0e-12)

    assert reduced.warnings == (
        "membrane_bending_coupling_discarded",
        "off_axis_membrane_coupling_discarded",
        "off_axis_bending_coupling_discarded",
        "validity_membrane_bending_coupling_exceeds_threshold",
    )

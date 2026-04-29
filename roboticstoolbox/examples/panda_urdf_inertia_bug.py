import os
import tempfile
import traceback

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="mplconfig-"))

import roboticstoolbox as rtb


def print_link_summary(robot: rtb.Robot) -> None:
    print(f"robot: {robot.name}")
    print(f"n: {robot.n}")
    print("links:")

    for i, link in enumerate(robot.links):
        parent_name = None if link.parent is None else link.parent.name
        parent_jindex = None if link.parent is None else link.parent.jindex
        print(
            f"  {i:02d} {link.name:<18}"
            f" isjoint={link.isjoint!s:<5}"
            f" jindex={str(link.jindex):<4}"
            f" parent={str(parent_name):<18}"
            f" parent_jindex={str(parent_jindex):<4}"
            f" mass={link.m}"
        )


def test_inertia(robot: rtb.Robot, q: np.ndarray, label: str) -> bool:
    print(f"\nTesting inertia at {label}: {np.array2string(q, precision=4)}")

    try:
        M = robot.inertia(q)
    except Exception:
        print("inertia(q) raised an exception:")
        print(traceback.format_exc())
        return False

    print(f"inertia shape: {M.shape}")
    print(M)
    print(f"symmetric: {np.allclose(M, M.T)}")
    print(f"finite: {np.isfinite(M).all()}")
    return True


def main() -> int:
    panda = rtb.models.URDF.Panda()

    print_link_summary(panda)

    arm_masses = [link.m for link in panda.links[: panda.n + 2]]
    print(f"\narm link masses: {arm_masses}")
    print(f"all arm link masses are zero: {all(m == 0.0 for m in arm_masses)}")

    ok = True
    ok &= test_inertia(panda, panda.qz, "qz")
    ok &= test_inertia(panda, panda.qr, "qr")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

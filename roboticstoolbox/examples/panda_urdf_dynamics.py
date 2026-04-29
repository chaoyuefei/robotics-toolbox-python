import numpy as np
import roboticstoolbox as rtb


def main() -> None:
    panda_urdf = rtb.models.URDF.Panda()
    panda_dh = rtb.models.DH.Panda()

    print("URDF arm link masses:")
    print([link.m for link in panda_urdf.links if link.isjoint][: panda_urdf.n])

    M_urdf = panda_urdf.inertia(panda_urdf.qz)
    M_dh = panda_dh.inertia(panda_dh.qz)

    print("\nURDF Panda inertia(qz):")
    print(M_urdf)
    print("\nDH Panda inertia(qz):")
    print(M_dh)
    print("\nmax |URDF - DH| at qz:")
    print(np.max(np.abs(M_urdf - M_dh)))


if __name__ == "__main__":
    main()

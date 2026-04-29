#!/usr/bin/env python

import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3


class Panda(Robot):
    """
    Class that imports a Panda URDF model

    ``Panda()`` is a class which imports a Franka-Emika Panda robot definition
    from a URDF file.  The model describes its kinematic and graphical
    characteristics.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.URDF.Panda()
        >>> print(robot)

    Defined joint configurations are:

    - qz, zero joint angle configuration, 'L' shaped configuration
    - qr, vertical 'READY' configuration
    - qs, arm is stretched out in the x-direction
    - qn, arm is at a nominal non-singular configuration

    .. codeauthor:: Jesse Haviland
    .. sectionauthor:: Peter Corke
    """

    def __init__(self, load_dynamics: bool = True):

        links, name, urdf_string, urdf_filepath = self.URDF_read(
            "franka_description/robots/panda_arm_hand.urdf.xacro"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Franka Emika",
            gripper_links=links[9],
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        self.grippers[0].tool = SE3(0, 0, 0.1034)

        self.qdlim = np.array(
            [2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100, 3.0, 3.0]
        )

        self.qr = np.array([0, -0.3, 0, -2.2, 0, 2.0, np.pi / 4])
        self.qz = np.zeros(7)

        if load_dynamics and self._has_missing_arm_dynamics():
            self._apply_arm_dynamics_from_dh()

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    def _apply_arm_dynamics_from_dh(self):
        """
        Load Panda arm dynamics from the DH model.

        The Franka xacro bundled with RTB contains no <inertial> blocks, so
        the URDF model otherwise has zero mass and inertia for every arm link.
        The DH Panda model in RTB includes arm masses and inertia tensors, and
        we copy those onto the corresponding URDF joint links as a fallback.

        Notes
        -----
        - This only populates the 7 arm joints.
        - The available DH model does not define link COM offsets, so ``r`` is
          copied as-is from the DH links (currently zeros).
        - The hand/finger dynamics remain as parsed from the URDF/xacro.
        """

        dh_panda = rtb.models.DH.Panda()
        arm_links = sorted(
            (link for link in self.links if link.isjoint and link.jindex is not None),
            key=lambda link: link.jindex,
        )

        if len(arm_links) < dh_panda.n:  # pragma nocover
            raise ValueError(
                f"expected at least {dh_panda.n} joint links in Panda URDF, "
                f"got {len(arm_links)}"
            )

        for urdf_link, dh_link in zip(arm_links[: dh_panda.n], dh_panda.links):
            urdf_link.m = dh_link.m
            urdf_link.r = dh_link.r
            urdf_link.I = dh_link.I

    def _has_missing_arm_dynamics(self) -> bool:
        arm_links = sorted(
            (link for link in self.links if link.isjoint and link.jindex is not None),
            key=lambda link: link.jindex,
        )

        return all(link.m == 0.0 and np.allclose(link.I, 0.0) for link in arm_links[:7])


if __name__ == "__main__":  # pragma nocover

    r = Panda()

    r.qz

    for link in r.grippers[0].links:
        print(link)

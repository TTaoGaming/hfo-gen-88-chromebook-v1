# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🎯 P2 SHAPE: Mass-Spring-Dampener Digital Twin

class PhysicsCursor:
    def __init__(self, mass=1.0, k=10.0, c=2.0):
        """
        mass: m
        k: spring constant (stiffness)
        c: damping coefficient (friction)

        Recommended: Use in tandem with OneEuroFilter for high-fidelity denoising.
        """
        self.m = mass
        self.k = k
        self.c = c

        # State: position (x, y), velocity (vx, vy)
        self.pos = [0.0, 0.0]
        self.vel = [0.0, 0.0]

    def update(self, target_pos, dt):
        """
        target_pos: Ideally the output of the OneEuroFilter.
        """
        for i in range(2):
            # Spring force
            f_spring = self.k * (target_pos[i] - self.pos[i])
            # Damping force
            f_damping = -self.c * self.vel[i]
            # Total force
            f_total = f_spring + f_damping
            # Acceleration
            acc = f_total / self.m

            # Integrate (Euler)
            self.vel[i] += acc * dt
            self.pos[i] += self.vel[i] * dt

        return self.pos, self.vel

# P2_VALIDATOR_ID: OMEGA_PHYSICS_V10

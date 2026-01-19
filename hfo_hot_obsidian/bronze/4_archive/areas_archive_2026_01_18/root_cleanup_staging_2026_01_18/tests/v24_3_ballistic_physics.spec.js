// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
// 🧪 V24.3 BALLISTIC PHYSICS VALIDATION

const planck = require('planck-js');

class PlanckPhysicsAdapter {
    constructor(stiffness = 0.5, dampingRatio = 0.7) {
        this.world = planck.World({ gravity: planck.Vec2(0, 0) });
        this.cursorBody = this.world.createBody({
            type: 'dynamic',
            position: planck.Vec2(0, 0),
            linearDamping: 2.0 // Ballistic Damping
        });
        this.cursorBody.createFixture(planck.Circle(0.01), { density: 1.0 });

        this.anchorBody = this.world.createBody({
            type: 'static',
            position: planck.Vec2(0, 0)
        });

        this.joint = this.world.createJoint(planck.DistanceJoint({
            bodyA: this.anchorBody,
            bodyB: this.cursorBody,
            localAnchorA: planck.Vec2(0, 0),
            localAnchorB: planck.Vec2(0, 0),
            length: 0,
            frequencyHz: 5.0,
            dampingRatio: dampingRatio
        }));
    }

    setBallistic(enabled) {
        if (enabled) {
            this.joint.setFrequency(0.0); // Detach joint -> momentum only
        } else {
            this.joint.setFrequency(5.0); // Re-attach joint
        }
    }

    reset(x, y) {
        this.cursorBody.setPosition(planck.Vec2(x, y));
        this.cursorBody.setLinearVelocity(planck.Vec2(0, 0));
        this.anchorBody.setPosition(planck.Vec2(x, y));
    }

    update(targetX, targetY, dt) {
        this.anchorBody.setPosition(planck.Vec2(targetX, targetY));
        this.world.step(dt / 1000);
        const pos = this.cursorBody.getPosition();
        return { x: pos.x, y: pos.y };
    }

    getVelocity() {
        return this.cursorBody.getLinearVelocity();
    }
}

async function testBallisticMomentum() {
    console.log("🚀 STARTING V24.3 BALLISTIC PHYSICS TEST");
    const adapter = new PlanckPhysicsAdapter(0.5, 0.7);

    // Initial state
    adapter.reset(0, 0);
    console.log("1. Initial Position: (0,0)");

    // Move to create velocity
    console.log("2. Moving to (100, 100) over 100ms...");
    for (let i = 0; i < 10; i++) {
        adapter.update(10 * i, 10 * i, 16.6); // 10 steps of ~16ms
    }

    let velBefore = adapter.getVelocity();
    console.log(`- Velocity Before Coast: x=${velBefore.x.toFixed(2)}, y=${velBefore.y.toFixed(2)}`);

    // Enable Ballistic Coasting
    console.log("3. Enabling Ballistic Coasting (Detaching Joint)...");
    adapter.setBallistic(true);

    // Keep updating the anchor but notice the cursor drifts
    let lastPos = { x: 0, y: 0 };
    for (let i = 0; i < 5; i++) {
        let pos = adapter.update(0, 0, 16.6); // Anchor resets to 0, but cursor should drift
        console.log(`- Coast Step ${i}: Cursor Pos=(${pos.x.toFixed(2)}, ${pos.y.toFixed(2)})`);
        lastPos = pos;
    }

    if (Math.abs(lastPos.x) > 0.1) {
        console.log("✅ PASS: Cursor maintained momentum after joint detachment.");
    } else {
        console.log("❌ FAIL: Cursor stopped instantly.");
    }

    // Re-attach
    console.log("4. Disabling Ballistic Coasting (Re-attaching Joint)...");
    adapter.setBallistic(false);
    let finalPos = adapter.update(0, 0, 16.6);
    console.log(`- Final Pos after Re-attach: (${finalPos.x.toFixed(2)}, ${finalPos.y.toFixed(2)})`);

    if (Math.abs(finalPos.x) < Math.abs(lastPos.x)) {
        console.log("✅ PASS: Cursor returned towards anchor after re-attachment.");
    } else {
        console.log("❌ FAIL: Cursor didn't return.");
    }
}

testBallisticMomentum().catch(console.error);

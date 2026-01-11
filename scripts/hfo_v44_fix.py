import re
import os

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v44.html'

with open(filepath, 'r') as f:
    content = f.read()

# 1. Global State Replacements
content = content.replace('PORT_0_POINTER_READY', 'ARMED')
content = content.replace('PORT_7_POINTER_COMMITTED', 'COMMITTED')

# 2. Refactor port5Immunize validTransitions
new_transitions = """            const validTransitions = {
                'IDLE': ['IDLE', 'ARMING'],
                'ARMING': ['IDLE', 'ARMING', 'ARMED'],
                'ARMED': ['IDLE', 'ARMED', 'COMMITTING', 'COMMITTED'],
                'COMMITTING': ['IDLE', 'ARMED', 'COMMITTING', 'COMMITTED'],
                'COMMITTED': ['IDLE', 'COMMITTED', 'RELEASING', 'ARMED'],
                'RELEASING': ['IDLE', 'ARMED', 'RELEASING', 'COMMITTED']
            };"""

pattern_transitions = r'const validTransitions = \{.*?\};'
content = re.sub(pattern_transitions, new_transitions, content, flags=re.DOTALL)

# 3. Refactor port6Assimilate logic
# We want to remove the redundant mirror logic and just rely on FSM
new_assimilate = """        const port6Assimilate = (hand, gestureName, score, now, isFacing, confidence = 1.0) => {
            // P5 HardGate Validation with Coasting Support
            // Note: We process first to get the predicted next state, or we peek.
            // For now, we trust FSM and validate the result.
            const fsmRes = hand.fsm.process(gestureName, now, score, isFacing);
            
            const auditResult = port5Immunize(hand, fsmRes.state, confidence);

            if (auditResult === 'ALLOW') {
                return fsmRes;
            } else if (auditResult === 'COAST') {
                hand.fsm.lastTimestamp = now;
                hand.isCoasting = true;
                return { state: hand.fsm.state, pointerEvent: 'none' };
            } else {
                hand.fsm.lastTimestamp = now;
                return { state: hand.fsm.state, pointerEvent: 'none' };
            }
        };"""

pattern_assimilate = r'const port6Assimilate = \(hand, gestureName, score, now, isFacing, confidence = 1\.0\) => \{.*?return hand\.fsm\.process\(gestureName, now, score, isFacing\);'
content = re.sub(pattern_assimilate, new_assimilate, content, flags=re.DOTALL)

# 4. Fix isDown property check (was missed in global replace if it had strings)
content = content.replace("isDown: (h.fsm.state === 'COMMITTED')", "isDown: (h.fsm.state === 'COMMITTED')") # Already handled by global

with open(filepath, 'w') as f:
    f.write(content)
print("V44 Fixed.")

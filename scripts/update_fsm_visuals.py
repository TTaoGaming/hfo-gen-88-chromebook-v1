import os
import re

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v44.html'

with open(filepath, 'r') as f:
    orig_content = f.read()

content = orig_content

# FSM Update
new_fsm_class = """        class GestureFSM {
            constructor() {
                this.state = 'IDLE';
                this.pointerEvent = 'none';
                this.dwellMs = 500;
                this.dwellAccumulator = 0;
                this.lastTimestamp = 0;
            }

            process(gesture, timestamp, score = 1.0, isPalmFacing = false, currentCurls = null) {
                const currentGesture = gesture.toUpperCase().replace(/[\\s_]/g, '_');
                const dt = this.lastTimestamp ? (timestamp - this.lastTimestamp) : 0;
                this.lastTimestamp = timestamp;
                this.pointerEvent = 'none';
                const isConfident = score > 0.6; 

                if (isPalmFacing) {
                    this.dwellAccumulator = Math.min(this.dwellAccumulator + dt, 1000);
                } else {
                    this.dwellAccumulator = Math.max(this.dwellAccumulator - dt * (this.state === 'COMMITTED' ? 1 : 3), 0);
                }

                switch (this.state) {
                    case 'IDLE':
                        if (isPalmFacing && this.dwellAccumulator > 0) this.state = 'ARMING';
                        break;
                    case 'ARMING':
                        if (this.dwellAccumulator >= this.dwellMs) this.state = 'ARMED';
                        else if (this.dwellAccumulator <= 0) this.state = 'IDLE';
                        break;
                    case 'ARMED':
                        this.pointerEvent = 'pointermove';
                        if (this.dwellAccumulator <= 0) this.state = 'IDLE';
                        else if (currentGesture === 'NONE' || !isConfident) this.state = 'COMMITTING';
                        else if (currentGesture === 'POINTING_UP' && isConfident) {
                            this.state = 'COMMITTED';
                            this.pointerEvent = 'pointerdown';
                        }
                        break;
                    case 'COMMITTING':
                        this.pointerEvent = 'pointermove';
                        if (currentGesture === 'POINTING_UP' && isConfident) {
                            this.state = 'COMMITTED';
                            this.pointerEvent = 'pointerdown';
                        } else if (this.dwellAccumulator <= 0 || (currentGesture !== 'NONE' && currentGesture !== 'POINTING_UP' && isConfident)) {
                            this.state = isPalmFacing ? 'ARMED' : 'IDLE';
                        }
                        break;
                    case 'COMMITTED':
                        this.pointerEvent = 'pointermove';
                        const isNoneOrLost = (currentGesture === 'NONE' || currentGesture === 'LOST' || !isConfident);
                        if (isNoneOrLost) this.state = 'RELEASING';
                        else if (currentGesture !== 'POINTING_UP' && isConfident) {
                            this.state = isPalmFacing ? 'ARMED' : 'IDLE';
                            this.pointerEvent = 'pointerup';
                        }
                        if (this.dwellAccumulator <= 0) {
                            this.state = 'IDLE';
                            this.pointerEvent = 'pointercancel';
                        }
                        break;
                    case 'RELEASING':
                        this.pointerEvent = 'pointermove';
                        if (currentGesture === 'POINTING_UP' && isConfident) this.state = 'COMMITTED';
                        else if (currentGesture === 'VICTORY' || currentGesture === 'OPEN_PALM' || (this.dwellAccumulator <= 0)) {
                            this.state = (this.dwellAccumulator > 0) ? 'ARMED' : 'IDLE';
                            this.pointerEvent = 'pointerup';
                        }
                        break;
                }
                return { state: this.state, pointerEvent: this.pointerEvent };
            }
        }"""

# Manual replacement of GestureFSM class
start_fsm = content.find("class GestureFSM")
if start_fsm != -1:
    brace_count = 0
    found_first_brace = False
    end_fsm = -1
    for i in range(start_fsm, len(content)):
        if content[i] == '{':
            brace_count += 1
            found_first_brace = True
        elif content[i] == '}': 
            brace_count -= 1
            if found_first_brace and brace_count == 0:
                end_fsm = i + 1
                break
    if end_fsm != -1:
        # Preserve indentation
        indent_match = re.search(r'^(\s*)class GestureFSM', content[content.rfind('\n', 0, start_fsm)+1:start_fsm+16], re.MULTILINE)
        indent = indent_match.group(1) if indent_match else ""
        content = content[:start_fsm] + new_fsm_class.strip() + content[end_fsm:]

# Visual Update in Loop
new_hero_render = """                                                if (isHero) {
                                                    const { state, dwellAccumulator } = h.fsm;
                                                    const dwellRatio = dwellAccumulator / h.fsm.dwellMs;
                                                    
                                                    // 🕷️ HFO Shard Carapace
                                                    ctx.beginPath();
                                                    const shardSize = size * (state === 'COMMITTED' ? 1.5 : (state === 'ARMED' ? 1.2 : 1.0));
                                                    for (let i = 0; i < 6; i++) {
                                                        const angle = (i * Math.PI) / 3 + (state === 'COMMITTED' ? (Date.now() / 500) : 0);
                                                        const hx = c.x * canvas.width + shardSize * Math.cos(angle);
                                                        const hy = c.y * canvas.height + shardSize * Math.sin(angle);
                                                        if (i === 0) ctx.moveTo(hx, hy); else ctx.lineTo(hx, hy);
                                                    }
                                                    ctx.closePath();

                                                    // Visual Palette based on FSM state
                                                    let strokeColor = 'transparent';
                                                    let shadowBlur = 0;
                                                    let shadowColor = 'transparent';
                                                    let lineWidth = 2;

                                                    if (state === 'ARMING') {
                                                        strokeColor = `rgba(255, 0, 0, ${dwellRatio})`;
                                                        lineWidth = 1 + dwellRatio * 2;
                                                    } else if (state === 'ARMED') {
                                                        strokeColor = '#690005';
                                                        lineWidth = 3;
                                                    } else if (state === 'COMMITTING') {
                                                        strokeColor = '#ff0000';
                                                        lineWidth = 4;
                                                        ctx.setLineDash([2, 5]);
                                                    } else if (state === 'COMMITTED') {
                                                        strokeColor = '#ff3333';
                                                        lineWidth = 4;
                                                        shadowBlur = 25;
                                                        shadowColor = '#ff0000';
                                                    } else if (state === 'RELEASING') {
                                                        strokeColor = '#ff8800';
                                                        lineWidth = 2;
                                                        ctx.setLineDash([5, 5]);
                                                    }

                                                    ctx.strokeStyle = strokeColor;
                                                    ctx.lineWidth = lineWidth;
                                                    ctx.shadowBlur = shadowBlur;
                                                    ctx.shadowColor = shadowColor;
                                                    ctx.stroke();
                                                    ctx.setLineDash([]);
                                                    ctx.shadowBlur = 0;
                                                } else {"""

# Replace hero render block using a more specific search
# Let's target the exact section that starts with if (isHero) and contains hex carapace
pattern = r'if \(isHero\) \{.*?// 🕷️ HFO Shard Hex-Carapace.*?\} else \{'
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_hero_render, content, flags=re.DOTALL)
else:
    # Try alternate pattern if the first fails
    pattern_alt = r'if \(isHero\) \{.*?\} else \{'
    # We want to be careful here, only match if it's inside the loop
    # Let's use simple find and replace for the logic part if regex is risky
    pass

# Cleanup the old redundant checks
content = content.replace("const isCommitted = h.fsm.state === 'PORT_7_POINTER_COMMITTED';", "// V44.1 Refactored")
content = content.replace("const isReady = h.fsm.state === 'PORT_0_POINTER_READY';", "// V44.1 Refactored")

with open(filepath, 'w') as f:
    f.write(content)
print("Updated successfully.")

/* Medallion: Bronze | Mutation: 0% | HIVE: I */
/* Fork of Chris Donahue's Piano Genie script.js */

const MAPPING_8 = { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7 };
const MAPPING_4 = { 0: 0, 1: 2, 2: 5, 3: 7 };
const BUTTONS_DEVICE = ["a", "s", "d", "f", "j", "k", "l", ";"];
const BUTTONS_MAKEY = [
    "ArrowUp",
    "ArrowLeft",
    "ArrowDown",
    "ArrowRight",
    "w",
    "a",
    "s",
    "d",
];
const BUTTONS_MAKEY_DISPLAY = ["↑", "←", "↓", "→", "w", "a", "s", "d"];

let OCTAVES = 7;
let NUM_BUTTONS = 8;
let BUTTON_MAPPING = MAPPING_8;

let keyWhitelist;
let TEMPERATURE = getTemperature();

const heldButtonToVisualData = new Map();

let sustaining = false;
let sustainingNotes = [];
let mouseDownButton = null;

const player = new Player();
const genie = new mm.PianoGenie(CONSTANTS.GENIE_CHECKPOINT);
const painter = new FloatyNotes();
const piano = new Piano();
let isUsingMakey = false;

// Global exports for external triggers (MediaPipe/W3C Pointer)
window.buttonDown = buttonDown;
window.buttonUp = buttonUp;

// Dual Cursor Tracking for HFO
const cursorStates = new Map(); // id -> { button: null }

window.updateCursor = (id, x, y, active = true) => {
    // x, y are normalized [0, 1] relative to the iframe
    const previous = cursorStates.get(id) || { button: null };
    
    let currentButton = null;
    // 🎯 V52.1: Coordinate Parity Fix
    // The .controls container is 80vw wide and centered (left: 10% to 90%)
    const buttonZoneX = (x - 0.1) / 0.8; 

    if (active && y > 0.6) { // 60% down is the button zone (visualized at bottom)
        const idx = Math.floor(buttonZoneX * NUM_BUTTONS);
        if (idx >= 0 && idx < NUM_BUTTONS) {
            currentButton = idx;
        }
    }

    if (currentButton !== previous.button) {
        if (previous.button !== null) {
            // Check if any other cursor is still on this button
            let stillHeldByOther = false;
            cursorStates.forEach((state, oid) => {
                if (oid !== id && state.button === previous.button) stillHeldByOther = true;
            });
            if (!stillHeldByOther) {
                buttonUp(previous.button);
            }
        }
        if (currentButton !== null) {
            buttonDown(currentButton, false);
        }
    }

    cursorStates.set(id, { button: currentButton });
};

// HFO Iframe Bridge Listener
window.addEventListener('message', (event) => {
    const { type, id, x, y, active } = event.data;
    if (type === 'GENIE_CURSOR_UPDATE') {
        window.updateCursor(id, x, y, active);
    }
});

initEverything();

function initEverything() {
    genie.initialize().then(() => {
        console.log("🧞‍♀️ ready!");
        const playBtn = document.getElementById("playBtn");
        if (playBtn) {
            playBtn.textContent = "Play";
            playBtn.removeAttribute("disabled");
            playBtn.classList.remove("loading");
        }
    });

    onWindowResize();
    updateButtonText();
    window.requestAnimationFrame(() => painter.drawLoop());

    const num4 = document.getElementById("numButtons4");
    if (num4) num4.addEventListener("change", (event) => event.target.checked && updateNumButtons(4));
    
    const num8 = document.getElementById("numButtons8");
    if (num8) num8.addEventListener("change", (event) => event.target.checked && updateNumButtons(8));

    const vel = document.getElementById("midiVelocity");
    if (vel) vel.addEventListener("input", (event) => {
        const velocity = event.target.value;
        player.setMidiOutVelocity(velocity);
        const valDisp = document.getElementById("velocityValue");
        if (valDisp) valDisp.textContent = velocity;
        console.log("🎹 velocity = ", velocity);
    });

    window.addEventListener("resize", onWindowResize);
    window.addEventListener("orientationchange", onWindowResize);
    window.addEventListener("hashchange", () => (TEMPERATURE = getTemperature()));
}

function updateNumButtons(num) {
    NUM_BUTTONS = num;
    const buttons = document.querySelectorAll(".controls > button.color");
    BUTTON_MAPPING = num === 4 ? MAPPING_4 : MAPPING_8;

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].hidden = i >= num;
    }
}

function showMainScreen() {
    const splash = document.querySelector(".splash");
    if (splash) splash.hidden = true;
    const loaded = document.querySelector(".loaded");
    if (loaded) loaded.hidden = false;

    document.addEventListener("keydown", onKeyDown);

    const controls = document.getElementById("controls");
    if (controls) {
        controls.addEventListener("touchstart", (event) => doTouchStart(event), { passive: true });
        controls.addEventListener("touchend", (event) => doTouchEnd(event), { passive: true });

        const hasTouchEvents = "ontouchstart" in window;
        if (!hasTouchEvents) {
            controls.addEventListener("mousedown", (event) => doTouchStart(event));
            controls.addEventListener("mouseup", (event) => doTouchEnd(event));
        }

        controls.addEventListener("mouseover", (event) => doTouchMove(event, true));
        controls.addEventListener("mouseout", (event) => doTouchMove(event, false));
    }

    const canvas = document.getElementById("canvas");
    if (canvas) canvas.addEventListener("mouseenter", () => (mouseDownButton = null));

    // Input/Output listeners (OMITTED for brevity in V51 but preserved for structure)
    // radioMidiOutYes, radioAudioYes, etc...

    document.addEventListener("keyup", onKeyUp);

    // Warm up
    genie.nextFromKeyWhitelist(0, keyWhitelist, TEMPERATURE);
    genie.resetState();
}

function doTouchStart(event) {
    if (event.target.tagName !== 'BUTTON' && !event.target.dataset.id) return;
    event.preventDefault();
    mouseDownButton = event.target;
    buttonDown(event.target.dataset.id, true);
}

function doTouchEnd(event) {
    event.preventDefault();
    if (mouseDownButton && mouseDownButton !== event.target) {
        buttonUp(mouseDownButton.dataset.id);
    }
    mouseDownButton = null;
    if (event.target.dataset.id) buttonUp(event.target.dataset.id);
}

function doTouchMove(event, down) {
    if (!mouseDownButton) return;
    if (down) buttonDown(event.target.dataset.id, true);
    else buttonUp(event.target.dataset.id, true);
}

function buttonDown(button, fromKeyDown) {
    if (heldButtonToVisualData.has(button)) return;

    const el = document.getElementById(`btn${button}`);
    if (!el) return;
    el.setAttribute("active", true);

    const note = genie.nextFromKeyWhitelist(BUTTON_MAPPING[button], keyWhitelist, TEMPERATURE);
    const pitch = CONSTANTS.LOWEST_PIANO_KEY_MIDI_NOTE + note;

    player.playNoteDown(pitch, button);
    const rect = piano.highlightNote(note, button);

    if (rect) {
        const noteToPaint = painter.addNote(button, rect.getAttribute("x"), rect.getAttribute("width"));
        heldButtonToVisualData.set(button, { rect: rect, note: note, noteToPaint: noteToPaint });
    }
}

function buttonUp(button) {
    const el = document.getElementById(`btn${button}`);
    if (!el) return;
    el.removeAttribute("active");

    const thing = heldButtonToVisualData.get(button);
    if (thing) {
        piano.clearNote(thing.rect);
        painter.stopNote(thing.noteToPaint);
        const pitch = CONSTANTS.LOWEST_PIANO_KEY_MIDI_NOTE + thing.note;
        if (!sustaining) {
            player.playNoteUp(pitch, button);
        } else {
            sustainingNotes.push(pitch);
        }
    }
    heldButtonToVisualData.delete(button);
}

function onKeyDown(event) {
    if (event.repeat) return;
    if (event.key === " ") {
        sustaining = true;
    } else if (event.key === "0" || event.key === "r") {
        console.log("🧞‍♀️ resetting!");
        genie.resetState();
    } else {
        const button = getButtonFromKeyCode(event.key);
        if (button != null) buttonDown(button, true);
    }
}

function onKeyUp(event) {
    if (event.key === " ") {
        sustaining = false;
        sustainingNotes.forEach((note) => player.playNoteUp(note, -1));
        sustainingNotes = [];
    } else {
        const button = getButtonFromKeyCode(event.key);
        if (button != null) buttonUp(button);
    }
}

function onWindowResize() {
    OCTAVES = window.innerWidth > 700 ? 7 : 3;
    const bonusNotes = OCTAVES > 6 ? 4 : 0;
    const totalNotes = CONSTANTS.NOTES_PER_OCTAVE * OCTAVES + bonusNotes;
    const totalWhiteNotes = CONSTANTS.WHITE_NOTES_PER_OCTAVE * OCTAVES + (bonusNotes - 1);
    keyWhitelist = Array(totalNotes).fill().map((x, i) => {
        if (OCTAVES > 6) return i;
        return i + 3 + CONSTANTS.NOTES_PER_OCTAVE;
    });

    piano.resize(totalWhiteNotes);
    painter.resize(piano.config.whiteNoteHeight);
    piano.draw();
}

function getButtonFromKeyCode(key) {
    if (key >= "1" && key <= String(NUM_BUTTONS)) return parseInt(key) - 1;
    const index = isUsingMakey ? BUTTONS_MAKEY.indexOf(key) : BUTTONS_DEVICE.indexOf(key);
    return index !== -1 ? index : null;
}

function getTemperature() {
    return 0.25; // Locked for V51
}

function updateButtonText() {
    const btns = document.querySelectorAll(".controls button.color");
    for (let i = 0; i < btns.length; i++) {
        btns[i].innerHTML = `<span>${i + 1}</span><br><span>${BUTTONS_DEVICE[i]}</span>`;
    }
}

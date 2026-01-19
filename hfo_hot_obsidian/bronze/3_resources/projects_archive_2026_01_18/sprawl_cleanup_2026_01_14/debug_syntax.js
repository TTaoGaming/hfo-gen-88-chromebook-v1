// Medallion: Bronze | Mutation: 0% | HIVE: E -->
const fs = require('fs');

const content = fs.readFileSync('/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v20_7.html', 'utf8');

// Extract all <script> blocks
const scripts = content.match(/<script[^>]*>([\s\S]*?)<\/script>/g);

if (scripts) {
    scripts.forEach((script, i) => {
        let code = script.replace(/<script[^>]*>/, '').replace(/<\/script>/, '');

        try {
            console.log(`Checking script ${i}...`);
            // Check syntax by creating a function
            new Function(code);
            console.log(`Script ${i} is syntactically correct.`);
        } catch (err) {
            console.error(`Error in script ${i}:`, err.message);
            // Try to find the context of the error
            if (err.message.includes('initializer')) {
                console.log("Found it! Searching for uninitialized const in code...");
                const lines = code.split('\n');
                lines.forEach((line, lineIdx) => {
                    if (line.includes('const') && !line.includes('=') && !line.includes('{') && !line.includes('[')) {
                        console.log(`Potential culprit at Line ${lineIdx + 1}: ${line.trim()}`);
                    }
                });
            }
        }
    });
} else {
    console.log("No scripts found.");
}

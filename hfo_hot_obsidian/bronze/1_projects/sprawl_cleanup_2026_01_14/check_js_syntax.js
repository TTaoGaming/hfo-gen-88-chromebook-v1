// Medallion: Bronze | Mutation: 0% | HIVE: E -->
const fs = require('fs');

const content = fs.readFileSync('/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v19.html', 'utf8');

// Extract all <script> blocks
const scripts = content.match(/<script[^>]*>([\s\S]*?)<\/script>/g);

if (scripts) {
    scripts.forEach((script, i) => {
        // Remove the <script> tags
        let code = script.replace(/<script[^>]*>/, '').replace(/<\/script>/, '');

        // If it's the module script, we can check it
        if (script.includes('type="module"')) {
            console.log(`Checking script ${i}...`);
            try {
                // We use a trick to check syntax by wrapping in an async function
                new Function(`async () => { ${code} }`);
                console.log(`Script ${i} is syntactically correct.`);
            } catch (err) {
                console.error(`Error in script ${i}:`, err.message);
                // Print the code around the error if possible (Function doesn't give line numbers usually)
            }
        }
    });
} else {
    console.log("No scripts found.");
}

import html from "eslint-plugin-html";
import js from "@eslint/js";

export default [
    js.configs.recommended,
    {
        files: ["**/*.html", "**/*.js"],
        plugins: {
            html
        },
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
            globals: {
                // Browser
                window: "readonly",
                document: "readonly",
                console: "readonly",
                performance: "readonly",
                requestAnimationFrame: "readonly",
                setTimeout: "readonly",
                setInterval: "readonly",
                clearTimeout: "readonly",
                clearInterval: "readonly",
                navigator: "readonly",
                URL: "readonly",
                URLSearchParams: "readonly",
                Blob: "readonly",
                PointerEvent: "readonly",
                MouseEvent: "readonly",
                Image: "readonly",
                ImageData: "readonly",
                CanvasRenderingContext2D: "readonly",
                HTMLVideoElement: "readonly",
                HTMLCanvasElement: "readonly",
                // HFO Globals
                systemState: "readonly",
                Zod: "readonly",
                MediaPipe: "readonly",
                HandLandmarker: "readonly",
                FilesetResolver: "readonly",
                Babylon: "readonly",
                BABYLON: "readonly",
                GoldenLayout: "readonly",
                OpenFeature: "readonly",
                DataFabricSchema: "readonly",
                P1Bridger: "readonly",
                BabylonJuiceSubstrate: "readonly",
                logMission: "readonly",
                isFlagEnabled: "readonly",
                updateVisualPanels: "readonly",
                drawResults: "readonly",
                TutorialSystem: "readonly",
                hfoTelemetry: "readonly",
                hfoPlayer: "readonly",
                hfoTutorial: "readonly",
                hfoState: "writable",
                hfoMockResults: "writable",
                nz: "readonly"
            }
        },
        rules: {
            "no-undef": "error",
            "no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
            "no-unreachable": "error",
            "no-redeclare": "error",
            "no-dupe-args": "error",
            "no-dupe-keys": "error",
            "no-const-assign": "error",
            "no-inner-declarations": "off"
        }
    }
];

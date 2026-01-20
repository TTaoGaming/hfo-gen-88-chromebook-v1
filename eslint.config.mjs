// Medallion: Bronze | Mutation: 0% | HIVE: V
import html from "eslint-plugin-html";

export default [
  {
    files: ["**/*.html"],
    plugins: { html },
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
  },
];

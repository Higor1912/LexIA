module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#2c3e50",        // Azul acinzentado escuro
          "primary-focus": "#34495e",   // Versão mais clara do primary
          "base-100": "#ffffff",        // Branco para fundo principal
          "base-200": "#f8f9fa",        // Cinza muito claro para fundo secundário
          "base-300": "#e9ecef",        // Cinza claro para elementos terciários
          "base-content": "#343a40",    // Cinza escuro para texto principal
          "neutral": "#6c757d",         // Cinza médio para elementos neutros
          "neutral-content": "#f8f9fa", // Texto sobre elementos neutros
          "accent": "#495057",          // Cor de destaque sutil
          "accent-content": "#f8f9fa",  // Texto sobre cor de destaque
        },
      },
    ],
  },
}
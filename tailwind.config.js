module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'custom': {
          'dark': '#383838',      // Cinza muito escuro
          'gray': '#808080',      // Cinza médio
          'light': '#a3a3a3',     // Cinza claro
          'lighter': '#d4d4d4',   // Cinza mais claro
          'lightest': '#f5f5f5',  // Cinza quase branco
        }
      }
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#383838",
          "primary-focus": "#808080",
          "base-100": "#ffffff",
          "base-200": "#f5f5f5",
          "base-300": "#d4d4d4",
          "base-content": "#383838",
        },
      },
    ],
  },
}
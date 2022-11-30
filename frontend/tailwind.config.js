/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "rgba(135,62,0,1)", //red
        secondary: "rgba(254,242,0,0.1)", //yellow
        accent: "rgb(215,0,8)", //orange
        active: "rgba(135,62,0,0.9)",
        passive: "#E9ABAB",
        disabled: "#AEB4B7",
      }
    },
    container: {
      center: true
    }
  },
  plugins: [
    // require('@/tailwindcss/forms'),
  ],
}


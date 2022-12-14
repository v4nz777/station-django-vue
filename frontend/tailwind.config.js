/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "rgb(48,105,179)", //red
        secondary: "rgba(254,228,64,0.2)", //yellow
        accent: "rgb(215,0,8)", //orange,
        contrast: "white", // invert to primary
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


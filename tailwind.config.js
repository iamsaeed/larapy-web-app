/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./resources/**/*.{vue,js,html}",
    "./resources/views/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'larapy': {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
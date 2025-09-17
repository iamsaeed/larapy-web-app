import './bootstrap.js';
import { createApp } from 'vue';
import TestComponent from './components/TestComponent.vue';

// Create main Vue app (Laravel-like approach)
const app = createApp({
  data() {
    return {
      message: 'Larapy + Vue.js Application Ready!'
    }
  },
  mounted() {
    console.log('Vue app mounted successfully');
  }
});

// Register components globally (Laravel-like)
app.component('test-component', TestComponent);

// Mount the app immediately (DOM is ready since script is at end of body)
const appElement = document.getElementById('app');
if (appElement) {
  app.mount('#app');
}

// Make Vue available globally for debugging
window.Vue = { createApp };
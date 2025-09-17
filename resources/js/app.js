import './bootstrap.js';
import { createApp } from 'vue';
import TestComponent from './components/TestComponent.vue';

// Create main Vue app with in-DOM template (Laravel-like approach)
// This preserves existing HTML content and enhances it with Vue
const app = createApp();

// Register components globally (Laravel-like)
app.component('test-component', TestComponent);

// Mount the app immediately (DOM is ready since script is at end of body)
app.mount('#app');

// Make Vue available globally for debugging
window.Vue = { createApp };
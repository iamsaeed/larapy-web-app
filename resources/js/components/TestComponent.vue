<template>
  <div class="bg-white rounded-lg p-6 card-shadow max-w-sm">
    <h3 class="text-xl font-semibold mb-4 text-gray-800">Vue.js Test Component</h3>
    <div class="space-y-4">
      <p class="text-gray-600">{{ message }}</p>
      <div class="flex items-center space-x-2">
        <button
          @click="decrement"
          class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
          :disabled="count <= 0"
        >
          -
        </button>
        <span class="text-lg font-bold text-blue-600 min-w-[2rem] text-center">{{ count }}</span>
        <button
          @click="increment"
          class="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
        >
          +
        </button>
      </div>
      <p class="text-sm text-gray-500">
        You've clicked {{ count }} time{{ count !== 1 ? 's' : '' }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestComponent',
  data() {
    return {
      message: 'Vue.js is working with Vite!',
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++;
    },
    decrement() {
      if (this.count > 0) {
        this.count--;
      }
    }
  }
}
</script>
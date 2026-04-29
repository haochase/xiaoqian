<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// No script needed for root component
</script>

<style>
#app {
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff, #e0e7ff);
  display: flex;
  flex-direction: column;
}
</style>

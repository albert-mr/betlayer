<template>
  <Suspense>
    <template #default>
      <DebateScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script setup>
import DebateScreen from "./components/DebateScreen.vue";
</script>

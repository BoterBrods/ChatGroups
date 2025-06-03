<template>
  <div class="rooms-container">
    <h2>Выбор комнаты</h2>
    <div class="user-info">
      <p><strong>Имя:</strong> {{ name }}</p>
      <p><strong>Номер варианта:</strong> {{ variant }}</p>
    </div>
    <p>Пока здесь будет выбор комнат...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const name = ref('');
const variant = ref('');

onMounted(() => {
  name.value = localStorage.getItem('username') || '';
  variant.value = localStorage.getItem('variant') || '';
});
</script>

<style scoped>
.rooms-container {
  max-width: 600px;
  margin: 5rem auto;
  padding: 2rem;
  background: #e9f7ef;
  border-radius: 8px;
}
.user-info {
  margin-top: 1rem;
}
</style>

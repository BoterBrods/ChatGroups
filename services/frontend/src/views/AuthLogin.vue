<template>
  <div class="auth-container">
    <h2>Вход в чат</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Имя" required />
      <input v-model="variant" type="number" placeholder="Номер варианта" required />
      <button type="submit">Войти</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const variant = ref('');
const error = ref('');
const router = useRouter();

async function handleLogin() {
  error.value = '';
  try {
    const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
      username: username.value,
      variant: parseInt(variant.value),
    });

    const { name: name, variant_number } = response.data;
    localStorage.setItem('username', name);
    localStorage.setItem('variant', variant_number);
    router.push('/rooms');
  } catch (err) {
    console.error(err);
    error.value = 'Ошибка входа. Проверьте имя и номер варианта.';
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 5rem auto;
  padding: 2rem;
  background: #f0f0f0;
  border-radius: 8px;
}
input, button {
  display: block;
  width: 100%;
  margin-top: 1rem;
  padding: 0.75rem;
}
button {
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>

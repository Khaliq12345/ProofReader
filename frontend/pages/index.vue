<script setup>
import Loading from '../components/Loading.vue';
import {useAuth} from '../composables/useAuth'
const {isLoginExpired } = useAuth();
const router = useRouter();
onMounted(async () => {
  if (isLoginExpired()) {
    router.push('/login');
      } else {
        router.push('/dashboard');
      }
  
});
</script>

<template>
  <div class="w-full h-100 flex flex-col align-middle justify-center items-center">
    <Loading />
    <div class="container mx-auto p-4 text-center">
      <p>Loading ... </p>
    </div>
  </div>
</template>
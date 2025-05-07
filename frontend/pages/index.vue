<script setup>
import Loading from '../components/Loading.vue';

const router = useRouter();
onMounted(async () => {
  router.push('/login');
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
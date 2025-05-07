<script setup lang="ts">
// LogOut
const router = useRouter();
const handleLogout = async () => {
  // Supprimer les informations de session
  sessionStorage.removeItem('AccessToken');
  sessionStorage.removeItem('RefreshToken');
  sessionStorage.removeItem('ExpiresAt');
  router.push('/login');
};
</script>

<template>
  <div class="mb-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold ">Welcome Back !</h1>
            <p class="text-gray-900 mt-1">Submit Files & Get Analysis results</p>
          </div>
          <!-- LogOut Button -->
          <UButton variant="ghost" icon="i-heroicons-arrow-left-end-on-rectangle" @click="handleLogout"
            class="text-error-500 cursor-pointer">
            Log Out
          </UButton>
        </div>
      </div>
</template>

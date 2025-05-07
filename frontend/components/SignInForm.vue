<script setup lang="ts">
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const error = ref('')
const router = useRouter()
// const config = useRuntimeConfig();
// const urlAPI = config.public.urlAPI;
defineEmits(['signup'])
// Handle User's login
const handleLogin = async () => {
    isLoading.value = true
    error.value = ''
    try {
        // Login
        // const response = await $fetch('/api/login', {
        //     method: 'POST',
        //     headers: {
        //         'Accept': 'application/json',
        //     },
        //     params: {
        //         email: email.value,
        //         password: password.value,
        //     },
        // }) as any
        // // Store tokens
        // sessionStorage.setItem('AccessToken', response.data.details.session.access_token);
        // sessionStorage.setItem('RefreshToken', response.data.details.session.refresh_token);
        // sessionStorage.setItem('ExpiresAt', response.data.details.session.expires_at);
        // // 
        router.push('/dashboard') // 
    } catch (err: any) {
        console.error('Erreur lors de la connexion:', err);
        error.value = err.response?.data?.message || 'Invalid Credentials or server error !';
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <div class="m-5">
        <div class="text-center space-y-2">
            <UIcon size="50" name="i-heroicons-user-circle" class="w-12 h-12 mx-auto text-info-500" />
            <h1 class="text-3xl font-bold ">Sign In</h1>
            <h4 class="my-3">Access your Dashboard</h4>
        </div>
        <form @submit.prevent="handleLogin" class="space-y-4">
            <UAlert v-if="error" :title="error" icon="i-heroicons-exclamation-circle" color="error" variant="subtle" />
            <UFormField label="Email" name="email" required>
                <UInput required v-model="email" type="email" placeholder="youremail@email.com" icon="i-heroicons-envelope"
                    size="lg" class="w-full [&_input]:text-black [&_input]:dark:text-black"  autofocus />
            </UFormField>
            <UFormField label="Password" name="password" required>
                <UInput required v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••"
                    icon="i-heroicons-lock-closed" class="w-full [&_input]:text-black [&_input]:dark:text-black"  size="lg">
                    <template #trailing>
                        <UButton variant="ghost" :icon="showPassword ? 'i-heroicons-eye-slash' : 'i-heroicons-eye'"
                             @click="showPassword = !showPassword" />
                    </template>
                </UInput>
            </UFormField>
            <div class="my-5"></div>
            <UButton class="text-white" type="submit" block size="lg" color="primary" :loading="isLoading"
                label="Log In" />
            <div class="text-center">
                <h5>Don't have an account ? <a @click="$emit('signup')" class="text-info-500">Sign Up</a></h5>
            </div>
        </form>
    </div>
</template>

<style scoped>
h1 {
    font-weight: bold;
    margin: 0;
}

h2 {
    text-align: center;
}

p {
    font-size: 14px;
    font-weight: 100;
    line-height: 20px;
    letter-spacing: 0.5px;
    margin: 20px 0 30px;
}

span {
    font-size: 12px;
}

a {
    font-size: 14px;
    text-decoration: none;
    margin: 15px 0;
    cursor: pointer;
}
</style>

  import {useAuth} from '../composables/useAuth'
  export default defineNuxtRouteMiddleware((to, from) => {
    const router = useRouter();
    const {isLoginExpired } = useAuth();
    if (import.meta.client) {
      if (isLoginExpired()) {
        return router.push('/login');
      }
    }
  });
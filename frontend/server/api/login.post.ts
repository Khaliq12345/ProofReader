export default defineEventHandler(async (event) => {
  const query = getQuery(event); 
  // const headers = getRequestHeaders(event);
  const config = useRuntimeConfig();
  const urlAPI = config.public.urlAPI;

  const params = {
    email: query.email,
    password: query.password,
  };


  try {
    const response = await $fetch(event.path, {
      baseURL: urlAPI,
      method: 'POST',
      params: params, // 
    });

    return response; // 


  } catch (err: any) {
    console.error("Erreur lors de l'appel à l'API distante :", err?.message);
    return createError({
      statusCode: err?.response?.status || 500,
      statusMessage: err?.response?.data?.message || "Erreur serveur",
    });
  }
});

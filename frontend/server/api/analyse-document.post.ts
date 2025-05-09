export default defineEventHandler(async (event) => {
  // const query = getQuery(event); 
  const body = await readBody(event);
  const config = useRuntimeConfig();
  const urlAPI = config.public.urlAPI;

  try {
    const response = await $fetch("analyse-document", {
      baseURL: urlAPI,
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
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

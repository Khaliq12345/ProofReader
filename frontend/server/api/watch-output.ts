export default defineEventHandler(async (event) => {
    const { folder } = getQuery(event)
    if (!folder) throw createError({ statusCode: 400, message: 'Paramètre folder manquant' })
  
    const storage = useStorage('outputs')
    const watchPath = `${folder}`
  
    // Créer un stream SSE (Server-Sent Events)
    const stream = new ReadableStream({
      async start(controller) {
        // Callback pour les changements
        const handleChange = async (event: string, key: string) => {
            let newKey  = key.split('outputs:').pop()??""
            console.log("event ", event, " newkey ", newKey, " watchPath ", watchPath)
          if (newKey.startsWith(watchPath)) {
            console.log('in right folder')
            const fileData = await storage.getItemRaw(newKey)
            console.log('filedata', fileData)
            if (fileData) {
              controller.enqueue(`data: ${JSON.stringify({
                event: 'new-file',
                file: newKey.replace(`${watchPath}:`, `${watchPath}/`),
                timestamp: new Date().toISOString()
              })}\n\n`)
            }
          }
        }
  
        // Démarrer la surveillance
        storage.watch(handleChange)
  
        // Nettoyage quand le client se déconnecte
        event.node.req.on('close', () => {
          storage.unwatch()
          controller.close()
        })
      }
    })
  
    // Configurer les headers SSE
    setHeader(event, 'Content-Type', 'text/event-stream')
    setHeader(event, 'Cache-Control', 'no-cache')
    setHeader(event, 'Connection', 'keep-alive')
  
    // Retourner le stream
    return sendStream(event, stream)
  })
export default defineEventHandler(async (event) => {
    const { file } = getQuery(event)
    if (!file) throw createError({ statusCode: 400, message: 'Paramètre file manquant' })
  
    const storage = useStorage('outputs')
    const fileData = await storage.getItemRaw(file as any)
  
    if (!fileData) {
      throw createError({ statusCode: 404, message: 'Fichier introuvable' })
    }
  
    setHeader(event, 'Content-Type', 'application/octet-stream')
    setHeader(event, 'Content-Disposition', `attachment; filename="${file}"`)
    
    return fileData
  })
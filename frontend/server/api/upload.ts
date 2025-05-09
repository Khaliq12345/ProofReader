
export default defineEventHandler(async (event) => {
    const formData = await readMultipartFormData(event);
    if (!formData || formData.length === 0) {
      throw createError({
        statusCode: 400,    statusMessage: "No files uploaded",  });
    }
    // upload file to local storage
    const storage = useStorage('uploads')
    formData.forEach((file) => {
        storage.setItemRaw(`${file.filename}`, file.data)
    })
    const outPutStorage = useStorage('ouputs')
    outPutStorage.watch((event, key: string) => {
          console.log("Got Event -- ", event, " key ", key)
        })
    return {'status': 'success'}
})
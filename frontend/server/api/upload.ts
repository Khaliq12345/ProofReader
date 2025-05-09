
export default defineEventHandler(async (event) => {
    const formData = await readMultipartFormData(event);
    console.log(formData)
    if (!formData || formData.length === 0) {
      throw createError({
        statusCode: 400,    statusMessage: "No files uploaded",  });
    }

    const filenames: string[] = []

    // upload file to local storage
    const storage = useStorage('uploads')

    formData.forEach((file) => {
        console.log(file.filename, file.name)
        const fileName = `${Date.now()}-${file.filename}`;
        storage.setItemRaw(fileName, file.data)
        filenames.push(fileName)
    })


    return filenames
})
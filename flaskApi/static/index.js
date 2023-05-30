const dropArea = document.querySelector(".drop-area")
const dragText = dropArea.querySelector("h2")
const button = document.querySelector("buttonSubmit")
const input = dropArea.querySelector("#file")
const form = document.querySelector('.formUploadImage');



input.addEventListener("change", (e) => {
    dropArea.classList.add("active")
})
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault()
    dropArea.classList.add("active")
    dragText.textContent = "Drop out to load the file"
})
dropArea.addEventListener("dragleave", (e) => {
    e.preventDefault()
    dropArea.classList.remove("active");
    dragText.textContent = "Drag and drop your image"
})
dropArea.addEventListener("drop", (e) => {
    e.preventDefault()
    input.files = e.dataTransfer.files;
    const files = e.dataTransfer.files
    showFiles(files)
    dropArea.classList.remove("active")
    dragText.textContent = "Drag and drop your image"
})
dropArea.addEventListener("click", (e) => {
    input.click()
})
button.addEventListener("click", (e) => {
    submitForm()
})
function submitForm() {
  form.submit()
}
function showFiles (files){
    if(files.length != undefined){
        const file = files[0]
        processFile(file)
    }
}
function processFile (file){
    const validExtensions = ['image/jpeg', 'image/jpg', 'image/png']
    if(validExtensions.includes(file.type)){
        const fileReader = new FileReader()
         const id = `file-${Math.random().toString(32).substring(7)}`
        fileReader.addEventListener('load', (e) => {
        const fileUrl = fileReader.result
        const image = `
            <div id="${id}" class="file-container">
                <img src="${fileUrl}" alt="${file.name}" width="50">
                <div class="status">
                    <span>${file.name}</span>  
                    <span class="status-text">
                        Loaded
                    </span>
              </div>
              </div>`
            const html = document.querySelector("#preview").innerHTML;
            document.querySelector('#preview').innerHTML = image + html

        }
    )
        fileReader.readAsDataURL(file)
    }else{
        alert('Invalid extension')
    }

}
   async function uploadFile(files){
        const formData = new FormData()
        formData.append("file",files)
        try{
           const response =   await fetch("http://localhost:5000/classification", {
                method: "POST",
                body: formData
            })
            if (response.ok){
                console.log("Image sent successfully")
            }else {
                console.log("error sending image")
            }
        }catch(error){
            console.log(error.data)
        }

    }



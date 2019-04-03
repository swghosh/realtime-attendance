var fileInput = document.querySelector('input[name=image]')
var imageHolder = document.querySelector('img.uploaded')

fileInput.addEventListener('change', function() {
    var file = this.files[0]
    var fileReader = new FileReader()

    fileReader.readAsDataURL(file)
    
    fileReader.addEventListener('load', function() {
        imageHolder.classList.remove('disabled')
        imageHolder.src = fileReader.result
        setTimeout(function() {
            document.body.scrollTop = document.body.scrollHeight
        }, 1000)
    })
})

var submitButton = document.querySelector('button[type=submit]')

submitButton.addEventListener('click', function() {
    var apiRes = new XMLHttpRequest()
    apiRes.open('POST', '/api/attendance/mark')
    apiRes.setRequestHeader('Content-Type', 'application/json')
    apiRes.addEventListener('readystatechange', function() {
        if(this.readyState == 4 && this.status == 200) {
            var apiRes = JSON.parse(this.responseText)
            console.log(apiRes)
        }
    })
    var imageAsB64 = imageHolder.src.split(',')[1]
    apiRes.send(JSON.stringify({"image": imageAsB64}))
})

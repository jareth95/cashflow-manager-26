const usernameField = document.querySelector('#usernameField')
const feebackField = document.querySelector('.invalid_feedback')
const emailField = document.querySelector('#emailField')
const emailFeebackField = document.querySelector('.invalid_email_feedback')
const usernameSuccessOutput = document.querySelector('.username-success-output')
const emailSuccessOutput = document.querySelector('.email-success-output')
const showPasswordToggle = document.querySelector('#showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')


const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent == 'SHOW') {
        showPasswordToggle.textContent = 'HIDE'
        passwordField.setAttribute('type','text')
    } else {
        showPasswordToggle.textContent = 'SHOW'
        passwordField.setAttribute('type','password')
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value
    emailSuccessOutput.textContent = `Checking ${emailVal}`

    emailSuccessOutput.style.display = 'block'
    emailField.classList.remove('is-invalid')
    emailFeebackField.style.display = 'none'
    emailFeebackField.innerHTML = ''

    if(emailVal.length > 0){
        fetch('/authentication/validate-email', {
            body: JSON.stringify({'email': emailVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            emailSuccessOutput.style.display = 'none'
            if(data.email_error){
                submitBtn.disabled = true
                emailField.classList.add('is-invalid')
                emailFeebackField.style.display = 'block'
                emailFeebackField.innerHTML = `<p>${data.email_error}</p>`
            } else {
                if (!usernameField.classList.contains('is-invalid')) {
                    submitBtn.removeAttribute('disabled')
                }
            }
        })
    }
})

usernameField.addEventListener('keyup', (e)=> {
    const usernameVal = e.target.value
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameSuccessOutput.style.display = 'block'
    usernameField.classList.remove('is-invalid')
    feebackField.style.display = 'none'
    feebackField.innerHTML = ''

    if(usernameVal.length > 0){
        fetch('/authentication/validate-username', {
            body: JSON.stringify({'username': usernameVal}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSuccessOutput.style.display = 'none'
            if(data.username_error){
                submitBtn.disabled = true
                usernameField.classList.add('is-invalid')
                feebackField.style.display = 'block'
                feebackField.innerHTML = `<p>${data.username_error}</p>`
            } else {
                if (!emailField.classList.contains('is-invalid')) {
                    submitBtn.removeAttribute('disabled')
                }
            }
        })
    }
})
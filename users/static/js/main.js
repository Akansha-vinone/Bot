function validate_password(){
    const element = document.getElementById('messages')
    const newDiv = document.createElement('div')
    newDiv.inneHTML = `
        <p> New Html</>
    `
    element.appendChild(newDiv)

    password.addeventListener('click',appendHTML)
}

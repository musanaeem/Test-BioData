const form = document.getElementById("id_form");
const username = document.getElementById("id_username");
const firstName = document.getElementById("id_first_name");
const lastName = document.getElementById("id_last_name");
const email = document.getElementById("id_email");
const password = document.getElementById("id_password1");
const passwordConfirmation = document.getElementById("id_password2");
const submit = document.getElementById("submit")

// results object used to check if all fields are validated
const results = {
    "username": false,
    "first_name": false,
    "last_name": false,
    "email": false,
    "passwords": false
};

const functions = {
    "username": validateUsername,
    "first_name": validateFirstName,
    "last_name": validateLastName,
    "email": validateEmail,
    "password1": validatePasswords,
    "password2": validatePasswords
}


window.onload = () => {

    inputs = document.getElementsByTagName("input");

    for (input of inputs){
        if(input.type != "hidden" && input.id != "submit"){
            let placeholder = input.name;
            input.placeholder = placeholder.replace("_"," ");

            input.className = "form-control";
            input.onblur = functions[input.name.trim()];
        }
    }
}

function validateUsername(){
    // In case there was already an error displayed
    clearError(username);
    const usernameValue = username.value.trim();
    results['username'] = isValidUsername(usernameValue);
    unlockOrLockSubmit();
}


// Clears any errors that are displayed on a field already
function clearError(input){
    smallElement = input.parentElement.querySelector("small");
    if(smallElement)
        smallElement.remove();
}


function isValidUsername(usernameValue){
    const usernameRegex = /^[\w-]+$/;
    const message = "Invalid username entered. Please only use a combination of alphanumeric, _ and -";
    return validationForUsernameOrName(usernameValue, username, usernameRegex, message);
}


function validationForUsernameOrName(value, input, regex, message){
    
    if (value.length < 3 || value.length > 15){
        setErrorFor(input, "The length should be 3-15 characters. please try again.");
        return false;
    }

    if(!regex.test(value)){
        setErrorFor(input, message);
        return false;
    }

    return true;
}


function setErrorFor(input, message){

    const formControl = input.parentElement;

    oldSmall = formControl.querySelector("small");
    if (oldSmall){
        oldSmall.remove();
    }

    const small = document.createElement("small");
    small.innerText = message;

    formControl.appendChild(small);
}


function validateFirstName(){
    clearError(firstName);
    const firstNameValue = firstName.value.trim();

    results['first_name'] = isValidName(firstNameValue, firstName);
    unlockOrLockSubmit();
}


function isValidName(name_value, nameInput){
    const nameRegex = /^[a-z]+$/i;
    const message = "Invalid name entered. Please only use alphabets";
    return validationForUsernameOrName(name_value, nameInput, nameRegex, message);

}


function validateLastName(){
    clearError(lastName);

    const lastNameValue = lastName.value.trim();

    results['last_name']= isValidName(lastNameValue, lastName);
    unlockOrLockSubmit();
}


function validateEmail(){
    clearError(email);

    const emailValue = email.value.trim();
    results['email']= isValidEmail(emailValue);
    unlockOrLockSubmit();
}

function isValidEmail(emailValue){
    const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    if(!emailRegex.test(emailValue)){
        setErrorFor(email, "Invalid Email. The email format entered is not valid.");
        return false;
    }

    return true;
}


function validatePasswords(){
    clearError(password);

    const passwordValue = password.value.trim();
    const passwordConfirmationValue = passwordConfirmation.value.trim();
   
    results['passwords'] = areValidPasswords(passwordValue, passwordConfirmationValue);
    unlockOrLockSubmit();
}


function areValidPasswords(passwordValue, passwordConfirmationValue){
    passwordRegex = /(.*[0-9].*[!@#$%^&*()<>?/.,`~].*)|(.*[!@#$%^&*()<>?/.,`~].*[0-9].*)/;

        if(passwordValue != passwordConfirmationValue){
            setErrorFor(password, "Password fields do not match. Please try again.");
            return false;
        }
        if(passwordValue.length < 6 || passwordValue.length > 15){
            setErrorFor(password, "Password length should be between 6 and 15 characters.");
            return false;
        }
        if(!passwordRegex.test(passwordValue)){
            setErrorFor(password, "Invalid password. Password should contain numbers and symbols.");
            return false;
        }

        return true;

}

function unlockOrLockSubmit(){
    submit.disabled = !Object.values(results).every((result) => result);
}

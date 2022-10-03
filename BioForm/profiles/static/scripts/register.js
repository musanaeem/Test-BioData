const form = document.getElementById("form");
const username = document.getElementById("username");
const first_name = document.getElementById("first-name");
const last_name = document.getElementById("last-name");
const email = document.getElementById("email");
const password1 = document.getElementById("password");
const password2 = document.getElementById("password-confirmation");

// results object used to check if all fields are validated
results = {
    "username": false,
    "first_name": false,
    "last_name": false,
    "email": false,
    "passwords": false
};


function validate_username(){
    // In case there was already an error displayed
    clear_error(username);
    const username_value = username.value.trim();
    results['username'] = is_valid_username(username_value);
    unlock_or_lock_submit()
}


// Clears any errors that are displayed on a field already
function clear_error(input){
    small_element = input.parentElement.querySelector("small")
    if(small_element)
        small_element.remove();
}


function is_valid_username(username_value){
    const username_regex = /^[\w-]+$/;
    const message = "Invalid username entered. Please only use a combination of alphanumeric, _ and -";
    return validation_for_username_or_name(username_value, username, username_regex, message);
}


function validation_for_username_or_name(value, input, regex, message){
    
    if (value.length >= 3 && value.length <= 15)
        if(regex.test(value))
            return true;
        else
            set_error_for(input, message);
    else
        set_error_for(input, "The length should be 3-15 characters. please try again.");

    return false;
}


function set_error_for(input, message){

    const form_control = input.parentElement;

    old_small = form_control.querySelector("small");
    if (old_small)
        old_small.remove();

    const small = document.createElement("small");
    small.innerText = message;

    form_control.appendChild(small);
}


function validate_first_name(){
    clear_error(first_name)
    const first_name_value = first_name.value.trim();

    results['first_name'] = is_valid_name(first_name_value, first_name);
    unlock_or_lock_submit()
}


function is_valid_name(name_value, name_input){
    const name_regex = /^[a-z]+$/i;
    const message = "Invalid name entered. Please only use alphabets";
    return validation_for_username_or_name(name_value, name_input, name_regex, message);

}


function validate_last_name(){
    clear_error(last_name);

    const last_name_value = last_name.value.trim();

    results['last_name']= is_valid_name(last_name_value, last_name);
    unlock_or_lock_submit()
}


function validate_email(){
    clear_error(email);

    const email_value = email.value.trim();
    results['email']= is_valid_email(email_value);
    unlock_or_lock_submit()
}

function is_valid_email(email_value){
    const email_regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    if(email_value != "")
        if(email_regex.test(email_value))
            return true;
        else
            set_error_for(email, "Invalid Email. The email format entered is not valid.");
    else
        set_error_for(email, "Field can not be empty. Please enter a valid value");
    
    return false;
}


function validate_passwords(){
    clear_error(password1);

    const password1_value = password1.value.trim();
    const password2_value = password2.value.trim();
   
    results['passwords'] = are_valid_passwords(password1_value, password2_value);
    unlock_or_lock_submit()
}


function are_valid_passwords(password1_value, password2_value){
    password_regex = /(.*[0-9].*[!@#$%^&*()<>?/.,`~].*)|(.*[!@#$%^&*()<>?/.,`~].*[0-9].*)/;

        if(password1_value == password2_value)
            if(password1_value.length > 5 && password1_value.length < 16)
                if(password_regex.test(password1_value))
                    return true;
                else
                    set_error_for(password1, "Invalid password. Password should contain numbers and symbols.");
            else
                set_error_for(password1, "Password length should be between 6 and 15 characters.");
        else
            set_error_for(password1, "Password fields do not match. Please try again.");
 
    return false;
}

function unlock_or_lock_submit(){
    submit = document.getElementById("submit")
    if (Object.values(results).every((result) => result)){
        submit.disabled = false;
    }
    else{
        submit.disabled = true;
    }
}

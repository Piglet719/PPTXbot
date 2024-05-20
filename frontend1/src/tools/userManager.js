

var user = null;
var lastUser =  localStorage.getItem('user');
if(lastUser){
    user = JSON.parse(lastUser)
}

function updateUser(username){
    user = {username};
    localStorage.setItem('user', JSON.stringify(user));




    // var a = {
    //     abc : 123,
    //     key2 : 'Hello'
    // }
    // JSON.stringify(a) => '{ "abc" : 123, "key2": "Hello" }'

}

function logout(){
    user = null
}


export default {
    user,
    updateUser,
    logout
}
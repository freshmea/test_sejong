struct User{
    name: String,
    email: String
}

impl User {
    fn new(name: &str) -> User {
        User {
            name: name.to_string(),
            email: format!("{}@bindsoft.co.kr", name)
        }
    }
}

fn get_user_result(name: &str) -> Result<User, String> {
    if name == "최수길" {
        Ok(User::new(name))
    } else {
        Err("name is wrong".to_string())
    }
}

fn main() {
    // a ! is a macro
    println!("Hello, world!");
    // default not mutable variable
    // let user = User::new("최수길");
    // mutable variable
    let mut user = User::new("최수길");
    user.name = "최수길2".to_string();
    println!("name: {}, email: {}", user.name, user.email);
    let user_option = get_user_result("최수길1");
    // println!("user_option: {:?}", user_option.name);
    match user_option {
        Ok(user) => println!("user_option: {:?}", user.name),
        Err(err) => println!("user_option: {:?}", err)
    }
}

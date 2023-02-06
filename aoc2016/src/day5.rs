use md5;

pub fn generator(input: &str) -> String {
    input.to_string()
}

pub fn part_1(input: &str) -> String {
    let mut decoded = String::new();

    for i in 0.. {
        let hash = md5::compute(format!("{}{}", input, i));
        let hash = format!("{:x}", hash);
        if hash.starts_with("00000") {
            decoded.push(hash.chars().nth(5).unwrap());
            if decoded.len() == 8 {
                break;
            }
        }
    }

    decoded
}

pub fn part_2(input: &str) -> String {
    let mut decoded = String::from("________");

    for i in 0.. {
        let hash = md5::compute(format!("{}{}", input, i));
        let hash = format!("{:x}", hash);
        if hash.starts_with("00000") {
            let pos = hash.chars().nth(5).unwrap().to_digit(10).unwrap_or(9) as usize;
            if pos < 8 && decoded.chars().nth(pos).unwrap() == '_' {
                decoded.replace_range(pos..pos + 1, &hash.chars().nth(6).unwrap().to_string());
                if !decoded.contains('_') {
                    break;
                }
            }
        }
    }

    decoded
}

#[cfg(test)]
mod tests {
    use super::*;
}

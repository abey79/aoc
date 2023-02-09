use rayon::prelude::*;

pub fn generator(input: &str) -> String {
    input.to_string()
}

pub fn part_1(input: &str) -> String {
    let mut decoded = String::new();

    for i in 0.. {
        let hash = md5::compute(format!("{input}{i}"));
        let hash = format!("{hash:x}");
        if hash.starts_with("00000") {
            decoded.push(hash.chars().nth(5).unwrap());
            if decoded.len() == 8 {
                break;
            }
        }
    }

    decoded
}

#[allow(dead_code)]
pub fn part_2(input: &str) -> String {
    let mut decoded = String::from("________");

    for i in 0.. {
        let hash = md5::compute(format!("{input}{i}"));
        let hash = format!("{hash:x}");
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

struct Match {
    pos: u8,
    c: char,
}

fn check_hash(input: &str, seed: usize) -> Option<Match> {
    let hash = md5::compute(format!("{input}{seed}"));
    let hash = format!("{hash:x}");

    if hash.starts_with("00000") {
        let pos = hash.chars().nth(5).unwrap().to_digit(10).unwrap_or(9) as usize;
        if pos < 8 {
            return Some(Match {
                pos: pos as u8,
                c: hash.chars().nth(6).unwrap(),
            });
        }
    }

    None
}

pub fn part_2_thread(input: &str) -> String {
    let mut decoded = String::from("________");

    const BATCH_SIZE: usize = 100000;

    for batch in 0.. {
        let matches: Vec<Match> = (batch * BATCH_SIZE..(batch + 1) * BATCH_SIZE)
            .into_par_iter()
            .map(|i| check_hash(input, i))
            .filter(|m| m.is_some())
            .map(|m| m.unwrap())
            .collect();

        for m in matches {
            if decoded.chars().nth(m.pos as usize).unwrap() == '_' {
                decoded.replace_range(m.pos as usize..m.pos as usize + 1, &m.c.to_string());
                if !decoded.contains('_') {
                    return format!("{decoded} (batches: {batch}x{BATCH_SIZE})");
                }
            }
        }
    }

    "Failed!".to_string()
}

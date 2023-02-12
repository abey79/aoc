// Note: it seems that the md5 crate is one of the slowest in Rust ecosystem. md-5 looks faster.

#[derive(Debug, Clone, Copy)]
struct Hash([u8; 32]);

impl Hash {
    fn from_salt(salt: &str, i: usize, stretched: bool) -> Hash {
        let mut digest = md5::compute(format!("{salt}{i}"));
        if stretched {
            for _ in 0..2016 {
                digest = md5::compute(format!("{digest:x}"));
            }
        }

        let mut res = [0u8; 32];
        for i in 0..16 {
            let byte = digest.0[i];
            res[2 * i + 1] = byte & 0xf;
            res[2 * i] = byte >> 4;
        }

        Hash(res)
    }

    fn first_triple(&self) -> Option<u8> {
        self.0
            .windows(3)
            .filter(|w| w[0] == w[1] && w[1] == w[2])
            .map(|w| w[0])
            .next()
    }

    fn quintuples(&self) -> Vec<u8> {
        self.0
            .windows(5)
            .filter(|w| w[0] == w[1] && w[1] == w[2] && w[2] == w[3] && w[3] == w[4])
            .map(|w| w[0])
            .collect()
    }
}

pub fn find_keys(input: &str, stretched: bool) -> usize {
    const BUFFER_SIZE: usize = 1000;
    let mut buffer: Vec<_> = (0..BUFFER_SIZE)
        .map(|i| Hash::from_salt(input, i, stretched))
        .collect();
    let mut quintuples_count = [0; 16];

    // count the quintuples in the buffer
    for hash in &buffer {
        for quintuple in hash.quintuples() {
            quintuples_count[quintuple as usize] += 1;
        }
    }

    let mut index = 0;
    let mut key_found = 0;
    loop {
        // pop hash and update quintuple counts
        let hash = buffer[index % BUFFER_SIZE];
        for quintuple in hash.quintuples() {
            quintuples_count[quintuple as usize] -= 1;
        }

        // push new hash and update quintuple counts
        let new_hash = Hash::from_salt(input, index + BUFFER_SIZE, stretched);
        buffer[index % BUFFER_SIZE] = new_hash;
        for quintuple in new_hash.quintuples() {
            quintuples_count[quintuple as usize] += 1;
        }

        // test current hash validity
        if let Some(triple) = hash.first_triple() {
            if quintuples_count[triple as usize] > 0 {
                key_found += 1;
                println!("key found at index {index}");
                if key_found == 64 {
                    return index;
                }
            }
        }

        index += 1;
    }
}

pub fn part_1(input: &str) -> usize {
    find_keys(input, false)
}

pub fn part_2(input: &str) -> usize {
    find_keys(input, true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash() {
        let hash = Hash::from_salt("abc", 18, false);
        assert!(hash.first_triple().is_some());
    }

    #[test]
    fn test_day_1() {
        assert_eq!(part_1("abc"), 22728);
    }

    #[test]
    fn test_day_2() {
        assert_eq!(part_2("abc"), 22551);
    }
}

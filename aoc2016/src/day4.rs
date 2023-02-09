use itertools::Itertools;
use std::collections::HashMap;

pub fn generator(input: &str) -> Vec<String> {
    input.lines().map(|s| s.to_string()).collect()
}

pub fn part_1(input: &[String]) -> i64 {
    let mut sum = 0;

    for line in input {
        let line = line.replace("]", "");
        let (room_id, checksum) = line.split_once("[").unwrap();
        let (room, id) = room_id.rsplit_once("-").unwrap();

        let mut counts: HashMap<char, i32> = HashMap::new();
        for c in room.replace("-", "").chars() {
            *counts.entry(c).or_default() += 1;
        }

        let this_checksum = counts
            .keys()
            .sorted_by_key(|c| 1000 * counts.get(c).unwrap() + (999 - **c as i32)) // UGLY!
            .rev()
            .take(5)
            .collect::<String>();

        // checking out solution on reddit:
        // counts.iter().map(|(c, n)| (-n, *c)).sorted().take(5).map(|(_, c)| c).collect::<String>()
        //
        // works because tuple can be compared lexicographically, so (-n, *c) is sorted by n first

        if this_checksum == checksum {
            sum += id.parse::<i64>().unwrap();
        }
    }

    sum
}

pub fn part_2(input: &[String]) -> i64 {
    for line in input {
        let line = line.replace("]", "");
        let (room_id, checksum) = line.split_once("[").unwrap();
        let (room, id) = room_id.rsplit_once("-").unwrap();

        let mut counts: HashMap<char, i32> = HashMap::new();
        for c in room.replace("-", "").chars() {
            *counts.entry(c).or_default() += 1;
        }

        let this_checksum = counts
            .keys()
            .sorted_by_key(|c| 1000 * counts.get(c).unwrap() + (999 - **c as i32))
            .rev()
            .take(5)
            .collect::<String>();

        if this_checksum == checksum {
            let mut decrypted = String::new();
            for c in room.chars() {
                if c == '-' {
                    decrypted.push(' ');
                } else {
                    let c = ((c as u32 - b'a' as u32 + (id.parse::<u32>().unwrap() % 26)) % 26)
                        as u8
                        + b'a';
                    decrypted.push(c as char);
                }
            }

            if decrypted == "northpole object storage" {
                return id.parse::<i64>().unwrap();
            }
        }
    }
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = generator("aaaaa-bbb-z-y-x-123[abxyz]");
        assert_eq!(part_1(&input), 123);
    }
}

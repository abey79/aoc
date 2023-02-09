use std::collections::HashSet;

pub fn generator(input: &str) -> Vec<String> {
    input.lines().map(|s| s.to_string()).collect()
}

fn has_abba(input: &str) -> bool {
    if input.len() < 4 {
        return false;
    }

    input
        .as_bytes()
        .windows(4)
        .any(|w| w[0] == w[3] && w[1] == w[2] && w[0] != w[1])
}

fn has_tsl(input: &str) -> bool {
    let parts = input.split(|c| c == '[' || c == ']').collect::<Vec<&str>>();

    parts.iter().step_by(2).any(|s| has_abba(s))
        && parts.iter().skip(1).step_by(2).all(|s| !has_abba(s))
}

pub fn part_1(input: &[String]) -> i64 {
    input.iter().map(|s| if has_tsl(s) { 1 } else { 0 }).sum()
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct Bab {
    a: u8,
    b: u8,
}

impl Bab {
    fn reverse(&self) -> Bab {
        Bab {
            a: self.b,
            b: self.a,
        }
    }
}

fn extract_bab(input: &str) -> Vec<Bab> {
    input
        .as_bytes()
        .windows(3)
        .filter(|w| w[0] == w[2] && w[0] != w[1])
        .map(|w| Bab { a: w[1], b: w[0] })
        .collect()
}

fn has_ssl(input: &str) -> bool {
    let parts = input.split(|c| c == '[' || c == ']').collect::<Vec<&str>>();

    let supernet_bab: HashSet<Bab> =
        HashSet::from_iter(parts.iter().step_by(2).flat_map(|s| extract_bab(s)));
    let hypernet_bab: HashSet<Bab> = HashSet::from_iter(
        parts
            .iter()
            .skip(1)
            .step_by(2)
            .flat_map(|s| extract_bab(s))
            .map(|b| b.reverse()),
    );

    supernet_bab.intersection(&hypernet_bab).next().is_some()
}

pub fn part_2(input: &[String]) -> i64 {
    input.iter().map(|s| if has_ssl(s) { 1 } else { 0 }).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = generator("abba[mnop]qrst");
        assert_eq!(part_1(&input), 1);

        let input = generator("abfa[mnop]qrst");
        assert_eq!(part_1(&input), 0);

        let input = generator("abfa[mnop]");
        assert_eq!(part_1(&input), 0);

        let input = generator("abba[mnop]qrst");
        assert_eq!(part_1(&input), 1);

        let input = generator("abba[mnop]qrst[asadfsadf]");
        assert_eq!(part_1(&input), 1);

        let input = generator("abba[mnop]qrst[assadfsadf]");
        assert_eq!(part_1(&input), 0);
    }
}

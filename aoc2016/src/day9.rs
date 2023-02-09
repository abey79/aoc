pub fn generator(input: &str) -> Vec<char> {
    input.chars().filter(|c| !c.is_whitespace()).collect()
}

enum State {
    Normal,
    Marker,
}

pub fn part_1(input: &[char]) -> usize {
    let mut i = 0;
    let mut state = State::Normal;
    let mut cnt = 0;
    let mut marker_start = 0;

    while i < input.len() {
        match state {
            State::Normal => {
                if input[i] == '(' {
                    state = State::Marker;
                    marker_start = i;
                } else {
                    cnt += 1;
                }

                i += 1;
            }
            State::Marker => {
                while input[i] != ')' {
                    i += 1;
                }

                let marker = &input[marker_start + 1..i];
                let marker_parts: Vec<usize> = marker
                    .split(|x| *x == 'x')
                    .map(|s| s.iter().collect::<String>().parse().unwrap())
                    .collect();
                let char_count = marker_parts[0];
                let repeat_count = marker_parts[1];

                cnt += char_count * repeat_count;

                state = State::Normal;
                i += 1 + char_count;
            }
        }
    }

    cnt
}

pub fn part_2(input: &[char]) -> usize {
    let mut i = 0;
    let mut state = State::Normal;
    let mut cnt = 0;
    let mut marker_start = 0;

    while i < input.len() {
        match state {
            State::Normal => {
                if input[i] == '(' {
                    state = State::Marker;
                    marker_start = i;
                } else {
                    cnt += 1;
                }

                i += 1;
            }
            State::Marker => {
                while input[i] != ')' {
                    i += 1;
                }

                let marker = &input[marker_start + 1..i];
                let marker_parts: Vec<usize> = marker
                    .split(|x| *x == 'x')
                    .map(|s| s.iter().collect::<String>().parse().unwrap())
                    .collect();
                let char_count = marker_parts[0];
                let repeat_count = marker_parts[1];

                cnt += part_2(&input[i + 1..i + 1 + char_count]) * repeat_count;

                state = State::Normal;
                i += 1 + char_count;
            }
        }
    }

    cnt
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part_2_should_work() {
        assert_eq!(part_2(&generator("X(8x2)(3x3)ABCY")), 20);

        assert_eq!(
            part_2(&generator("(27x12)(20x12)(13x14)(7x10)(1x12)A")),
            241920
        );

        assert_eq!(
            part_2(&generator(
                "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
            )),
            445
        );
    }
}

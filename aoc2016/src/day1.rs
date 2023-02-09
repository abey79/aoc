pub struct Step {
    turn_right: bool,
    block: i64,
}

pub fn generator(input: &str) -> Vec<Step> {
    input
        .split(", ")
        .map(|s| {
            let mut chars = s.chars();
            let c = chars.next().unwrap();
            let block = chars.as_str().parse().unwrap();
            match c {
                'R' => Step {
                    turn_right: true,
                    block,
                },
                'L' => Step {
                    turn_right: false,
                    block,
                },
                _ => panic!("Invalid input"),
            }
        })
        .collect()
}

pub fn part_1(input: &[Step]) -> u64 {
    let mut pos = (0, 0);
    let mut dir = (0, 1);

    for step in input {
        if step.turn_right {
            dir = (-dir.1, dir.0);
        } else {
            dir = (dir.1, -dir.0);
        }

        pos = (pos.0 + dir.0 * step.block, pos.1 + dir.1 * step.block);
    }

    pos.0.unsigned_abs() + pos.1.unsigned_abs()
}

pub fn part_2(input: &[Step]) -> u64 {
    let mut pos: (i64, i64) = (0, 0);
    let mut dir = (0, 1);
    let mut visited = std::collections::HashSet::new();

    for step in input {
        if step.turn_right {
            dir = (-dir.1, dir.0);
        } else {
            dir = (dir.1, -dir.0);
        }

        for _ in 0..step.block {
            pos = (pos.0 + dir.0, pos.1 + dir.1);

            if visited.contains(&pos) {
                return pos.0.unsigned_abs() + pos.1.unsigned_abs();
            } else {
                visited.insert(pos);
            }
        }
    }

    unreachable!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_2() {
        assert_eq!(part_2(&generator("R8, R4, R4, R8")), 4);
    }
}

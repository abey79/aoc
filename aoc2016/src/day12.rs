use std::collections::HashMap;

#[derive(Debug)]
pub struct Op {
    op: String,
    arg1: Option<String>,
    arg2: Option<String>,
}

pub fn generator(input: &str) -> Vec<Op> {
    input
        .lines()
        .map(|s| {
            let parts: Vec<_> = s.split(" ").map(|s| s).collect();
            Op {
                op: parts[0].to_string(),
                arg1: parts.get(1).map(|s| s.to_string()),
                arg2: parts.get(2).map(|s| s.to_string()),
            }
        })
        .collect()
}

pub fn cpu(input: &[Op], init: [i64; 4]) -> i64 {
    let mut regs = HashMap::new();
    regs.insert("a", init[0]);
    regs.insert("b", init[1]);
    regs.insert("c", init[2]);
    regs.insert("d", init[3]);

    let mut pc = 0;

    while pc < input.len() {
        let op = &input[pc];

        match op {
            Op {
                op,
                arg1: Some(arg1),
                arg2: Some(arg2),
            } if op == "cpy" => {
                let val = arg1
                    .parse::<i64>()
                    .unwrap_or_else(|_| *regs.get(arg1.as_str()).unwrap());
                *regs.get_mut(arg2.as_str()).unwrap() = val;
                pc += 1;
            }
            Op {
                op,
                arg1: Some(arg1),
                arg2: None,
            } if op == "inc" => {
                *regs.get_mut(arg1.as_str()).unwrap() += 1;
                pc += 1;
            }
            Op {
                op,
                arg1: Some(arg1),
                arg2: None,
            } if op == "dec" => {
                *regs.get_mut(arg1.as_str()).unwrap() -= 1;
                pc += 1;
            }
            Op {
                op,
                arg1: Some(arg1),
                arg2: Some(arg2),
            } if op == "jnz" => {
                // arg1 may be a register or a literal
                let val = arg1
                    .parse::<i64>()
                    .unwrap_or_else(|_| *regs.get(arg1.as_str()).unwrap());
                if val != 0 {
                    pc = (pc as isize
                        + arg2
                            .parse::<isize>()
                            .unwrap_or_else(|_| *regs.get(arg2.as_str()).unwrap() as isize))
                        as usize;
                } else {
                    pc += 1;
                }
            }
            _ => panic!("Invalid input {op:?}"),
        }
    }

    regs["a"]
}

pub fn part_1(input: &[Op]) -> i64 {
    cpu(input, [0, 0, 0, 0])
}

pub fn part_2(input: &[Op]) -> i64 {
    cpu(input, [0, 0, 1, 0])
}

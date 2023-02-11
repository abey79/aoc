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
            let parts: Vec<_> = s.split(' ').collect();
            Op {
                op: parts[0].to_string(),
                arg1: parts.get(1).map(|s| s.to_string()),
                arg2: parts.get(2).map(|s| s.to_string()),
            }
        })
        .collect()
}

pub fn reg_to_idx(reg: &str) -> usize {
    // would have been cleaner to encapsulate this in a `Regs` struct
    match reg {
        "a" => 0,
        "b" => 1,
        "c" => 2,
        "d" => 3,
        _ => panic!("Invalid register"),
    }
}

pub fn cpu(input: &[Op], init: [i64; 4]) -> i64 {
    let mut regs = init;
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
                    .unwrap_or_else(|_| regs[reg_to_idx(arg1)]);
                regs[reg_to_idx(arg2)] = val;
                pc += 1;
            }
            Op {
                op,
                arg1: Some(arg1),
                arg2: None,
            } if op == "inc" => {
                regs[reg_to_idx(arg1)] += 1;
                pc += 1;
            }
            Op {
                op,
                arg1: Some(arg1),
                arg2: None,
            } if op == "dec" => {
                regs[reg_to_idx(arg1)] -= 1;
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
                    .unwrap_or_else(|_| regs[reg_to_idx(arg1)]);
                if val != 0 {
                    pc = (pc as isize
                        + arg2
                            .parse::<isize>()
                            .unwrap_or_else(|_| regs[reg_to_idx(arg2)] as isize))
                        as usize;
                } else {
                    pc += 1;
                }
            }
            _ => panic!("Invalid input {op:?}"),
        }
    }

    regs[0]
}

pub fn part_1(input: &[Op]) -> i64 {
    cpu(input, [0, 0, 0, 0])
}

pub fn part_2(input: &[Op]) -> i64 {
    cpu(input, [0, 0, 1, 0])
}

fn main() {
    println!("{}", rom2dec("MMMIM"));
    println!("{}", dec2rom(3999, 0));
}

const LEGEND_KEYS_SORTED: [&str; 7] = ["I", "V", "X", "L", "C", "D", "M"];

fn legend(numeral: &str) -> Option<u32> {
    match numeral {
        "I" => Some(1),
        "V" => Some(5),
        "X" => Some(10),
        "L" => Some(50),
        "C" => Some(100),
        "D" => Some(500),
        "M" => Some(1000),
        _ => None
    }
}

fn rom2dec(numerals: &str) -> u32 {
    let mut total: u32 = 0;
    let mut prev_dval: u32 = 0;

    for numeral_digit in numerals.chars() {
        let dval: u32 = legend(&String::from(numeral_digit)).unwrap();
        if prev_dval <= dval {
            total += dval;
        } else {
            total -= dval;
        }
        prev_dval = dval;
    }
    
    return total;
}

fn dec2rom(mut number: u32, notation: u8) -> String {
    let mut out: String = String::from("");
    
    while number > 0 {
        // Descending order, prioritise higher values
        for key in LEGEND_KEYS_SORTED.iter().rev() {
            let value = legend(&key).unwrap();
            
            // If able to subtract
            if value <= number {
                number -= value;
                out += key;
                break;
            }

            // No subtractive numerals in Additive mode
            if notation == 1 {
                continue;
            }
            
            // If able to subtract reduced numeral
            // Ex. If not X but IX works (9)
            let mut reducer: f32 = value as f32;
            // Normalise to upper 10^n
            if reducer.to_string().chars().next().unwrap().to_string() == "5" {
                reducer *= 2.0;
            }

            let mut delta_numeral: Option<String> = None;
            let mut delta_value: Option<u32> = None;

            while reducer >= 1.0 {
                reducer *= 0.1;

                let mut subkey: String = String::from("");
                let mut subvalue: u32 = 0;

                // Find key and value for subtractive numeral
                for _k in LEGEND_KEYS_SORTED {
                    let _v: u32 = legend(_k).unwrap();
                    if reducer as u32 == _v {
                        subkey = _k.to_string();
                        subvalue = _v;
                        break;
                    }
                }

                if (value - subvalue) <= number && subvalue > 0 {
                    delta_numeral = Some(subkey + key);
                    delta_value = Some(value - subvalue);
                }

                if notation != 2 {
                    break;
                }
            }

            if delta_numeral.is_some() && delta_value.is_some() {
                number -= delta_value.unwrap();
                out += &delta_numeral.unwrap();
            }
        }
    }

    return out;
}

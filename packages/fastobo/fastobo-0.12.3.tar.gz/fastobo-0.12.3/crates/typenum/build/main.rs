use std::env;
use std::fmt;
use std::fs::File;
use std::io::Write;
use std::path::Path;

#[cfg(feature = "const-generics")]
mod generic_const_mappings;
mod op;
mod tests;

pub enum UIntCode {
    Term,
    Zero(Box<UIntCode>),
    One(Box<UIntCode>),
}

pub enum IntCode {
    Zero,
    Pos(Box<UIntCode>),
    Neg(Box<UIntCode>),
}

impl fmt::Display for UIntCode {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            UIntCode::Term => write!(f, "UTerm"),
            UIntCode::Zero(ref inner) => write!(f, "UInt<{}, B0>", inner),
            UIntCode::One(ref inner) => write!(f, "UInt<{}, B1>", inner),
        }
    }
}

impl fmt::Display for IntCode {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            IntCode::Zero => write!(f, "Z0"),
            IntCode::Pos(ref inner) => write!(f, "PInt<{}>", inner),
            IntCode::Neg(ref inner) => write!(f, "NInt<{}>", inner),
        }
    }
}

pub fn gen_uint(u: u64) -> UIntCode {
    let mut result = UIntCode::Term;
    let mut x = 1u64 << 63;
    while x > u {
        x >>= 1
    }
    while x > 0 {
        result = if x & u > 0 {
            UIntCode::One(Box::new(result))
        } else {
            UIntCode::Zero(Box::new(result))
        };
        x >>= 1;
    }
    result
}

pub fn gen_int(i: i64) -> IntCode {
    use std::cmp::Ordering::{Equal, Greater, Less};

    match i.cmp(&0) {
        Greater => IntCode::Pos(Box::new(gen_uint(i as u64))),
        Less => IntCode::Neg(Box::new(gen_uint(i.abs() as u64))),
        Equal => IntCode::Zero,
    }
}

#[cfg_attr(
    feature = "no_std",
    deprecated(
        since = "1.3.0",
        note = "the `no_std` flag is no longer necessary and will be removed in the future"
    )
)]
pub fn no_std() {}

#[cfg_attr(
    feature = "force_unix_path_separator",
    deprecated(
        since = "1.17.0",
        note = "the `force_unix_path_separator` flag is no longer necessary and will be removed in the future"
    )
)]
pub fn force_unix_path_separator() {}

const HIGHEST: u64 = 1024;
fn uints() -> impl Iterator<Item = u64> {
    // Use hardcoded values to avoid issues with cross-compilation.
    // See https://github.com/paholg/typenum/issues/162
    let first2: u32 = 11; // (highest as f64).log(2.0).round() as u32 + 1;
    let first10: u32 = 4; // (highest as f64).log(10.0) as u32 + 1;
    (0..(HIGHEST + 1))
        .chain((first2..64).map(|i| 2u64.pow(i)))
        .chain((first10..20).map(|i| 10u64.pow(i)))
}

// fixme: get a warning when testing without this
#[allow(dead_code)]
fn main() {
    println!("cargo:rerun-if-changed=build/main.rs"); // Allow caching the generation if `src/*` files change.

    let out_dir = env::var("OUT_DIR").unwrap();
    let dest = Path::new(&out_dir).join("consts.rs");

    let mut f = File::create(&dest).unwrap();

    no_std();
    force_unix_path_separator();

    // Header stuff here!
    write!(
        f,
        "
/**
Type aliases for many constants.

This file is generated by typenum's build script.

For unsigned integers, the format is `U` followed by the number. We define aliases for

- Numbers 0 through {highest}
- Powers of 2 below `u64::MAX`
- Powers of 10 below `u64::MAX`

These alias definitions look like this:

```rust
use typenum::{{B0, B1, UInt, UTerm}};

# #[allow(dead_code)]
type U6 = UInt<UInt<UInt<UTerm, B1>, B1>, B0>;
```

For positive signed integers, the format is `P` followed by the number and for negative
signed integers it is `N` followed by the number. For the signed integer zero, we use
`Z0`. We define aliases for

- Numbers -{highest} through {highest}
- Powers of 2 between `i64::MIN` and `i64::MAX`
- Powers of 10 between `i64::MIN` and `i64::MAX`

These alias definitions look like this:

```rust
use typenum::{{B0, B1, UInt, UTerm, PInt, NInt}};

# #[allow(dead_code)]
type P6 = PInt<UInt<UInt<UInt<UTerm, B1>, B1>, B0>>;
# #[allow(dead_code)]
type N6 = NInt<UInt<UInt<UInt<UTerm, B1>, B1>, B0>>;
```

# Example
```rust
# #[allow(unused_imports)]
use typenum::{{U0, U1, U2, U3, U4, U5, U6}};
# #[allow(unused_imports)]
use typenum::{{N3, N2, N1, Z0, P1, P2, P3}};
# #[allow(unused_imports)]
use typenum::{{U774, N17, N10000, P1024, P4096}};
```

We also define the aliases `False` and `True` for `B0` and `B1`, respectively.
*/
#[allow(missing_docs)]
pub mod consts {{
    use crate::uint::{{UInt, UTerm}};
    use crate::int::{{PInt, NInt}};

    pub use crate::bit::{{B0, B1}};
    pub use crate::int::Z0;

    pub type True = B1;
    pub type False = B0;
",
        highest = HIGHEST,
    )
    .unwrap();

    for u in uints() {
        writeln!(f, "    pub type U{} = {};", u, gen_uint(u)).unwrap();
        if u <= ::std::i64::MAX as u64 && u != 0 {
            let i = u as i64;
            writeln!(
                f,
                "    pub type P{i} = PInt<U{i}>; pub type N{i} = NInt<U{i}>;",
                i = i
            )
            .unwrap();
        }
    }
    write!(f, "}}").unwrap();

    tests::build_tests().unwrap();

    op::write_op_macro().unwrap();

    #[cfg(feature = "const-generics")]
    generic_const_mappings::emit_impls().unwrap();
}

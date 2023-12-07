#![allow(dead_code)]
#![cfg(feature = "suggestions")]

use darling::{FromDeriveInput, FromMeta};
use syn::parse_quote;

#[derive(Debug, FromDeriveInput)]
#[darling(attributes(suggest))]
struct Lorem {
    ipsum: String,
    dolor: Dolor,
}

#[derive(Debug, FromMeta)]
struct Dolor {
    sit: bool,
}

#[test]
fn suggest_dolor() {
    let input: syn::DeriveInput = parse_quote! {
        #[suggest(ipsum = "Hello", dolorr(sit))]
        pub struct Foo;
    };

    let result = Lorem::from_derive_input(&input).unwrap_err();
    assert_eq!(2, result.len());
    assert!(format!("{}", result).contains("Did you mean"));
}

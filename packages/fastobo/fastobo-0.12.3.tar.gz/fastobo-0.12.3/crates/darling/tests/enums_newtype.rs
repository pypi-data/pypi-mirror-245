use darling::{FromDeriveInput, FromMeta};
use syn::parse_quote;

#[derive(Debug, Default, PartialEq, Eq, FromMeta)]
#[darling(default)]
pub struct Amet {
    hello: bool,
    world: String,
}

#[derive(Debug, PartialEq, Eq, FromMeta)]
#[darling(rename_all = "snake_case")]
pub enum Lorem {
    Ipsum(bool),
    Dolor(String),
    Sit(Amet),
}

#[derive(Debug, PartialEq, Eq, FromDeriveInput)]
#[darling(attributes(hello))]
pub struct Holder {
    lorem: Lorem,
}

impl PartialEq<Lorem> for Holder {
    fn eq(&self, other: &Lorem) -> bool {
        self.lorem == *other
    }
}

#[test]
fn bool_word() {
    let di = parse_quote! {
        #[hello(lorem(ipsum))]
        pub struct Bar;
    };

    let pr = Holder::from_derive_input(&di).unwrap();
    assert_eq!(pr, Lorem::Ipsum(true));
}

#[test]
fn bool_literal() {
    let di = parse_quote! {
        #[hello(lorem(ipsum = false))]
        pub struct Bar;
    };

    let pr = Holder::from_derive_input(&di).unwrap();
    assert_eq!(pr, Lorem::Ipsum(false));
}

#[test]
fn string_literal() {
    let di = parse_quote! {
        #[hello(lorem(dolor = "Hello"))]
        pub struct Bar;
    };

    let pr = Holder::from_derive_input(&di).unwrap();
    assert_eq!(pr, Lorem::Dolor("Hello".to_string()));
}

#[test]
fn struct_nested() {
    let di = parse_quote! {
        #[hello(lorem(sit(world = "Hello", hello = false)))]
        pub struct Bar;
    };

    let pr = Holder::from_derive_input(&di).unwrap();
    assert_eq!(
        pr,
        Lorem::Sit(Amet {
            hello: false,
            world: "Hello".to_string(),
        })
    );
}

#[test]
#[should_panic]
fn format_mismatch() {
    let di = parse_quote! {
        #[hello(lorem(dolor(world = "Hello", hello = false)))]
        pub struct Bar;
    };

    Holder::from_derive_input(&di).unwrap();
}

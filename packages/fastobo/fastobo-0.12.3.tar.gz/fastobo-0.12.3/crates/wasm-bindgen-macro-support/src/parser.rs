use std::cell::{Cell, RefCell};
use std::char;
use std::str::Chars;

use ast::OperationKind;
use backend::ast;
use backend::util::{ident_ty, ShortHash};
use backend::Diagnostic;
use proc_macro2::{Ident, Span, TokenStream, TokenTree};
use quote::ToTokens;
use syn::ext::IdentExt;
use syn::parse::{Parse, ParseStream, Result as SynResult};
use syn::spanned::Spanned;
use syn::{ItemFn, Lit, MacroDelimiter, ReturnType};

use crate::ClassMarker;

thread_local!(static ATTRS: AttributeParseState = Default::default());

/// Javascript keywords which are not keywords in Rust.
const JS_KEYWORDS: [&str; 20] = [
    "class",
    "case",
    "catch",
    "debugger",
    "default",
    "delete",
    "export",
    "extends",
    "finally",
    "function",
    "import",
    "instanceof",
    "new",
    "null",
    "switch",
    "this",
    "throw",
    "var",
    "void",
    "with",
];
#[derive(Default)]
struct AttributeParseState {
    parsed: Cell<usize>,
    checks: Cell<usize>,
    unused_attrs: RefCell<Vec<Ident>>,
}

/// Parsed attributes from a `#[wasm_bindgen(..)]`.
#[cfg_attr(feature = "extra-traits", derive(Debug))]
pub struct BindgenAttrs {
    /// List of parsed attributes
    pub attrs: Vec<(Cell<bool>, BindgenAttr)>,
}

macro_rules! attrgen {
    ($mac:ident) => {
        $mac! {
            (catch, Catch(Span)),
            (constructor, Constructor(Span)),
            (method, Method(Span)),
            (static_method_of, StaticMethodOf(Span, Ident)),
            (js_namespace, JsNamespace(Span, Vec<String>, Vec<Span>)),
            (module, Module(Span, String, Span)),
            (raw_module, RawModule(Span, String, Span)),
            (inline_js, InlineJs(Span, String, Span)),
            (getter, Getter(Span, Option<Ident>)),
            (setter, Setter(Span, Option<Ident>)),
            (indexing_getter, IndexingGetter(Span)),
            (indexing_setter, IndexingSetter(Span)),
            (indexing_deleter, IndexingDeleter(Span)),
            (structural, Structural(Span)),
            (r#final, Final(Span)),
            (readonly, Readonly(Span)),
            (js_name, JsName(Span, String, Span)),
            (js_class, JsClass(Span, String, Span)),
            (inspectable, Inspectable(Span)),
            (is_type_of, IsTypeOf(Span, syn::Expr)),
            (extends, Extends(Span, syn::Path)),
            (no_deref, NoDeref(Span)),
            (vendor_prefix, VendorPrefix(Span, Ident)),
            (variadic, Variadic(Span)),
            (typescript_custom_section, TypescriptCustomSection(Span)),
            (skip_typescript, SkipTypescript(Span)),
            (skip_jsdoc, SkipJsDoc(Span)),
            (main, Main(Span)),
            (start, Start(Span)),
            (wasm_bindgen, WasmBindgen(Span, syn::Path)),
            (wasm_bindgen_futures, WasmBindgenFutures(Span, syn::Path)),
            (skip, Skip(Span)),
            (typescript_type, TypeScriptType(Span, String, Span)),
            (getter_with_clone, GetterWithClone(Span)),

            // For testing purposes only.
            (assert_no_shim, AssertNoShim(Span)),
        }
    };
}

macro_rules! methods {
    ($(($name:ident, $variant:ident($($contents:tt)*)),)*) => {
        $(methods!(@method $name, $variant($($contents)*));)*

        fn enforce_used(self) -> Result<(), Diagnostic> {
            // Account for the fact this method was called
            ATTRS.with(|state| state.checks.set(state.checks.get() + 1));

            let mut errors = Vec::new();
            for (used, attr) in self.attrs.iter() {
                if used.get() {
                    continue
                }
                let span = match attr {
                    $(BindgenAttr::$variant(span, ..) => span,)*
                };
                errors.push(Diagnostic::span_error(*span, "unused wasm_bindgen attribute"));
            }
            Diagnostic::from_vec(errors)
        }

        fn check_used(self) {
            // Account for the fact this method was called
            ATTRS.with(|state| {
                state.checks.set(state.checks.get() + 1);

                state.unused_attrs.borrow_mut().extend(
                    self.attrs
                    .iter()
                    .filter_map(|(used, attr)| if used.get() { None } else { Some(attr) })
                    .map(|attr| {
                        match attr {
                            $(BindgenAttr::$variant(span, ..) => {
                                syn::parse_quote_spanned!(*span => $name)
                            })*
                        }
                    })
                );
            });
        }
    };

    (@method $name:ident, $variant:ident(Span, String, Span)) => {
        fn $name(&self) -> Option<(&str, Span)> {
            self.attrs
                .iter()
                .find_map(|a| match &a.1 {
                    BindgenAttr::$variant(_, s, span) => {
                        a.0.set(true);
                        Some((&s[..], *span))
                    }
                    _ => None,
                })
        }
    };

    (@method $name:ident, $variant:ident(Span, Vec<String>, Vec<Span>)) => {
        fn $name(&self) -> Option<(&[String], &[Span])> {
            self.attrs
                .iter()
                .find_map(|a| match &a.1 {
                    BindgenAttr::$variant(_, ss, spans) => {
                        a.0.set(true);
                        Some((&ss[..], &spans[..]))
                    }
                    _ => None,
                })
        }
    };

    (@method $name:ident, $variant:ident(Span, $($other:tt)*)) => {
        #[allow(unused)]
        fn $name(&self) -> Option<&$($other)*> {
            self.attrs
                .iter()
                .find_map(|a| match &a.1 {
                    BindgenAttr::$variant(_, s) => {
                        a.0.set(true);
                        Some(s)
                    }
                    _ => None,
                })
        }
    };

    (@method $name:ident, $variant:ident($($other:tt)*)) => {
        #[allow(unused)]
        fn $name(&self) -> Option<&$($other)*> {
            self.attrs
                .iter()
                .find_map(|a| match &a.1 {
                    BindgenAttr::$variant(s) => {
                        a.0.set(true);
                        Some(s)
                    }
                    _ => None,
                })
        }
    };
}

impl BindgenAttrs {
    /// Find and parse the wasm_bindgen attributes.
    fn find(attrs: &mut Vec<syn::Attribute>) -> Result<BindgenAttrs, Diagnostic> {
        let mut ret = BindgenAttrs::default();
        loop {
            let pos = attrs
                .iter()
                .enumerate()
                .find(|&(_, m)| m.path().segments[0].ident == "wasm_bindgen")
                .map(|a| a.0);
            let pos = match pos {
                Some(i) => i,
                None => return Ok(ret),
            };
            let attr = attrs.remove(pos);
            let tokens = match attr.meta {
                syn::Meta::Path(_) => continue,
                syn::Meta::List(syn::MetaList {
                    delimiter: MacroDelimiter::Paren(_),
                    tokens,
                    ..
                }) => tokens,
                syn::Meta::List(_) | syn::Meta::NameValue(_) => {
                    bail_span!(attr, "malformed #[wasm_bindgen] attribute")
                }
            };
            let mut attrs: BindgenAttrs = syn::parse2(tokens)?;
            ret.attrs.append(&mut attrs.attrs);
            attrs.check_used();
        }
    }

    attrgen!(methods);
}

impl Default for BindgenAttrs {
    fn default() -> BindgenAttrs {
        // Add 1 to the list of parsed attribute sets. We'll use this counter to
        // sanity check that we call `check_used` an appropriate number of
        // times.
        ATTRS.with(|state| state.parsed.set(state.parsed.get() + 1));
        BindgenAttrs { attrs: Vec::new() }
    }
}

impl Parse for BindgenAttrs {
    fn parse(input: ParseStream) -> SynResult<Self> {
        let mut attrs = BindgenAttrs::default();
        if input.is_empty() {
            return Ok(attrs);
        }

        let opts = syn::punctuated::Punctuated::<_, syn::token::Comma>::parse_terminated(input)?;
        attrs.attrs = opts.into_iter().map(|c| (Cell::new(false), c)).collect();
        Ok(attrs)
    }
}

macro_rules! gen_bindgen_attr {
    ($(($method:ident, $($variants:tt)*),)*) => {
        /// The possible attributes in the `#[wasm_bindgen]`.
        #[cfg_attr(feature = "extra-traits", derive(Debug))]
        pub enum BindgenAttr {
            $($($variants)*,)*
        }
    }
}
attrgen!(gen_bindgen_attr);

impl Parse for BindgenAttr {
    fn parse(input: ParseStream) -> SynResult<Self> {
        let original = input.fork();
        let attr: AnyIdent = input.parse()?;
        let attr = attr.0;
        let attr_span = attr.span();
        let attr_string = attr.to_string();
        let raw_attr_string = format!("r#{}", attr_string);

        macro_rules! parsers {
            ($(($name:ident, $($contents:tt)*),)*) => {
                $(
                    if attr_string == stringify!($name) || raw_attr_string == stringify!($name) {
                        parsers!(
                            @parser
                            $($contents)*
                        );
                    }
                )*
            };

            (@parser $variant:ident(Span)) => ({
                return Ok(BindgenAttr::$variant(attr_span));
            });

            (@parser $variant:ident(Span, Ident)) => ({
                input.parse::<Token![=]>()?;
                let ident = input.parse::<AnyIdent>()?.0;
                return Ok(BindgenAttr::$variant(attr_span, ident))
            });

            (@parser $variant:ident(Span, Option<Ident>)) => ({
                if input.parse::<Token![=]>().is_ok() {
                    let ident = input.parse::<AnyIdent>()?.0;
                    return Ok(BindgenAttr::$variant(attr_span, Some(ident)))
                } else {
                    return Ok(BindgenAttr::$variant(attr_span, None));
                }
            });

            (@parser $variant:ident(Span, syn::Path)) => ({
                input.parse::<Token![=]>()?;
                return Ok(BindgenAttr::$variant(attr_span, input.parse()?));
            });

            (@parser $variant:ident(Span, syn::Expr)) => ({
                input.parse::<Token![=]>()?;
                return Ok(BindgenAttr::$variant(attr_span, input.parse()?));
            });

            (@parser $variant:ident(Span, String, Span)) => ({
                input.parse::<Token![=]>()?;
                let (val, span) = match input.parse::<syn::LitStr>() {
                    Ok(str) => (str.value(), str.span()),
                    Err(_) => {
                        let ident = input.parse::<AnyIdent>()?.0;
                        (ident.to_string(), ident.span())
                    }
                };
                return Ok(BindgenAttr::$variant(attr_span, val, span))
            });

            (@parser $variant:ident(Span, Vec<String>, Vec<Span>)) => ({
                input.parse::<Token![=]>()?;
                let (vals, spans) = match input.parse::<syn::ExprArray>() {
                    Ok(exprs) => {
                        let mut vals = vec![];
                        let mut spans = vec![];

                        for expr in exprs.elems.iter() {
                            if let syn::Expr::Lit(syn::ExprLit {
                                lit: syn::Lit::Str(ref str),
                                ..
                            }) = expr {
                                vals.push(str.value());
                                spans.push(str.span());
                            } else {
                                return Err(syn::Error::new(expr.span(), "expected string literals"));
                            }
                        }

                        (vals, spans)
                    },
                    Err(_) => {
                        let ident = input.parse::<AnyIdent>()?.0;
                        (vec![ident.to_string()], vec![ident.span()])
                    }
                };
                return Ok(BindgenAttr::$variant(attr_span, vals, spans))
            });
        }

        attrgen!(parsers);

        Err(original.error(if attr_string.starts_with('_') {
            "unknown attribute: it's safe to remove unused attributes entirely."
        } else {
            "unknown attribute"
        }))
    }
}

struct AnyIdent(Ident);

impl Parse for AnyIdent {
    fn parse(input: ParseStream) -> SynResult<Self> {
        input.step(|cursor| match cursor.ident() {
            Some((ident, remaining)) => Ok((AnyIdent(ident), remaining)),
            None => Err(cursor.error("expected an identifier")),
        })
    }
}

/// Conversion trait with context.
///
/// Used to convert syn tokens into an AST, that we can then use to generate glue code. The context
/// (`Ctx`) is used to pass in the attributes from the `#[wasm_bindgen]`, if needed.
trait ConvertToAst<Ctx> {
    /// What we are converting to.
    type Target;
    /// Convert into our target.
    ///
    /// Since this is used in a procedural macro, use panic to fail.
    fn convert(self, context: Ctx) -> Result<Self::Target, Diagnostic>;
}

impl<'a> ConvertToAst<(&ast::Program, BindgenAttrs)> for &'a mut syn::ItemStruct {
    type Target = ast::Struct;

    fn convert(
        self,
        (program, attrs): (&ast::Program, BindgenAttrs),
    ) -> Result<Self::Target, Diagnostic> {
        if !self.generics.params.is_empty() {
            bail_span!(
                self.generics,
                "structs with #[wasm_bindgen] cannot have lifetime or \
                 type parameters currently"
            );
        }
        let mut fields = Vec::new();
        let js_name = attrs
            .js_name()
            .map(|s| s.0.to_string())
            .unwrap_or(self.ident.to_string());
        let is_inspectable = attrs.inspectable().is_some();
        let getter_with_clone = attrs.getter_with_clone();
        for (i, field) in self.fields.iter_mut().enumerate() {
            match field.vis {
                syn::Visibility::Public(..) => {}
                _ => continue,
            }
            let (js_field_name, member) = match &field.ident {
                Some(ident) => (ident.unraw().to_string(), syn::Member::Named(ident.clone())),
                None => (i.to_string(), syn::Member::Unnamed(i.into())),
            };

            let attrs = BindgenAttrs::find(&mut field.attrs)?;
            if attrs.skip().is_some() {
                attrs.check_used();
                continue;
            }

            let js_field_name = match attrs.js_name() {
                Some((name, _)) => name.to_string(),
                None => js_field_name,
            };

            let comments = extract_doc_comments(&field.attrs);
            let getter = shared::struct_field_get(&js_name, &js_field_name);
            let setter = shared::struct_field_set(&js_name, &js_field_name);

            fields.push(ast::StructField {
                rust_name: member,
                js_name: js_field_name,
                struct_name: self.ident.clone(),
                readonly: attrs.readonly().is_some(),
                ty: field.ty.clone(),
                getter: Ident::new(&getter, Span::call_site()),
                setter: Ident::new(&setter, Span::call_site()),
                comments,
                generate_typescript: attrs.skip_typescript().is_none(),
                generate_jsdoc: attrs.skip_jsdoc().is_none(),
                getter_with_clone: attrs.getter_with_clone().or(getter_with_clone).copied(),
                wasm_bindgen: program.wasm_bindgen.clone(),
            });
            attrs.check_used();
        }
        let generate_typescript = attrs.skip_typescript().is_none();
        let comments: Vec<String> = extract_doc_comments(&self.attrs);
        attrs.check_used();
        Ok(ast::Struct {
            rust_name: self.ident.clone(),
            js_name,
            fields,
            comments,
            is_inspectable,
            generate_typescript,
            wasm_bindgen: program.wasm_bindgen.clone(),
        })
    }
}

fn get_ty(mut ty: &syn::Type) -> &syn::Type {
    while let syn::Type::Group(g) = ty {
        ty = &g.elem;
    }

    ty
}

fn get_expr(mut expr: &syn::Expr) -> &syn::Expr {
    while let syn::Expr::Group(g) = expr {
        expr = &g.expr;
    }

    expr
}

impl<'a> ConvertToAst<(&ast::Program, BindgenAttrs, &'a Option<ast::ImportModule>)>
    for syn::ForeignItemFn
{
    type Target = ast::ImportKind;

    fn convert(
        self,
        (program, opts, module): (&ast::Program, BindgenAttrs, &'a Option<ast::ImportModule>),
    ) -> Result<Self::Target, Diagnostic> {
        let mut wasm = function_from_decl(
            &self.sig.ident,
            &opts,
            self.sig.clone(),
            self.attrs.clone(),
            self.vis.clone(),
            false,
            None,
            false,
        )?
        .0;
        let catch = opts.catch().is_some();
        let variadic = opts.variadic().is_some();
        let js_ret = if catch {
            // TODO: this assumes a whole bunch:
            //
            // * The outer type is actually a `Result`
            // * The error type is a `JsValue`
            // * The actual type is the first type parameter
            //
            // should probably fix this one day...
            extract_first_ty_param(wasm.ret.as_ref())?
        } else {
            wasm.ret.clone()
        };

        let operation_kind = operation_kind(&opts);

        let kind = if opts.method().is_some() {
            let class = wasm.arguments.get(0).ok_or_else(|| {
                err_span!(self, "imported methods must have at least one argument")
            })?;
            let class = match get_ty(&class.ty) {
                syn::Type::Reference(syn::TypeReference {
                    mutability: None,
                    elem,
                    ..
                }) => &**elem,
                _ => bail_span!(
                    class.ty,
                    "first argument of method must be a shared reference"
                ),
            };
            let class_name = match get_ty(class) {
                syn::Type::Path(syn::TypePath {
                    qself: None,
                    ref path,
                }) => path,
                _ => bail_span!(class, "first argument of method must be a path"),
            };
            let class_name = extract_path_ident(class_name)?;
            let class_name = opts
                .js_class()
                .map(|p| p.0.into())
                .unwrap_or_else(|| class_name.to_string());

            let kind = ast::MethodKind::Operation(ast::Operation {
                is_static: false,
                kind: operation_kind,
            });

            ast::ImportFunctionKind::Method {
                class: class_name,
                ty: class.clone(),
                kind,
            }
        } else if let Some(cls) = opts.static_method_of() {
            let class = opts
                .js_class()
                .map(|p| p.0.into())
                .unwrap_or_else(|| cls.to_string());
            let ty = ident_ty(cls.clone());

            let kind = ast::MethodKind::Operation(ast::Operation {
                is_static: true,
                kind: operation_kind,
            });

            ast::ImportFunctionKind::Method { class, ty, kind }
        } else if opts.constructor().is_some() {
            let class = match js_ret {
                Some(ref ty) => ty,
                _ => bail_span!(self, "constructor returns must be bare types"),
            };
            let class_name = match get_ty(class) {
                syn::Type::Path(syn::TypePath {
                    qself: None,
                    ref path,
                }) => path,
                _ => bail_span!(self, "return value of constructor must be a bare path"),
            };
            let class_name = extract_path_ident(class_name)?;
            let class_name = opts
                .js_class()
                .map(|p| p.0.into())
                .unwrap_or_else(|| class_name.to_string());

            ast::ImportFunctionKind::Method {
                class: class_name,
                ty: class.clone(),
                kind: ast::MethodKind::Constructor,
            }
        } else {
            ast::ImportFunctionKind::Normal
        };

        let shim = {
            let ns = match kind {
                ast::ImportFunctionKind::Normal => (0, "n"),
                ast::ImportFunctionKind::Method { ref class, .. } => (1, &class[..]),
            };
            let data = (ns, &self.sig.ident, module);
            format!(
                "__wbg_{}_{}",
                wasm.name
                    .chars()
                    .filter(|c| c.is_ascii_alphanumeric())
                    .collect::<String>(),
                ShortHash(data)
            )
        };
        if let Some(span) = opts.r#final() {
            if opts.structural().is_some() {
                let msg = "cannot specify both `structural` and `final`";
                return Err(Diagnostic::span_error(*span, msg));
            }
        }
        let assert_no_shim = opts.assert_no_shim().is_some();

        let mut doc_comment = String::new();
        // Extract the doc comments from our list of attributes.
        wasm.rust_attrs.retain(|attr| {
            /// Returns the contents of the passed `#[doc = "..."]` attribute,
            /// or `None` if it isn't one.
            fn get_docs(attr: &syn::Attribute) -> Option<String> {
                if attr.path().is_ident("doc") {
                    if let syn::Meta::NameValue(syn::MetaNameValue {
                        value:
                            syn::Expr::Lit(syn::ExprLit {
                                lit: Lit::Str(str), ..
                            }),
                        ..
                    }) = &attr.meta
                    {
                        Some(str.value())
                    } else {
                        None
                    }
                } else {
                    None
                }
            }

            if let Some(docs) = get_docs(attr) {
                if !doc_comment.is_empty() {
                    // Add newlines between the doc comments
                    doc_comment.push('\n');
                }
                // Add this doc comment to the complete docs
                doc_comment.push_str(&docs);

                // Remove it from the list of regular attributes
                false
            } else {
                true
            }
        });

        let ret = ast::ImportKind::Function(ast::ImportFunction {
            function: wasm,
            assert_no_shim,
            kind,
            js_ret,
            catch,
            variadic,
            structural: opts.structural().is_some() || opts.r#final().is_none(),
            rust_name: self.sig.ident,
            shim: Ident::new(&shim, Span::call_site()),
            doc_comment,
            wasm_bindgen: program.wasm_bindgen.clone(),
            wasm_bindgen_futures: program.wasm_bindgen_futures.clone(),
        });
        opts.check_used();

        Ok(ret)
    }
}

impl ConvertToAst<(&ast::Program, BindgenAttrs)> for syn::ForeignItemType {
    type Target = ast::ImportKind;

    fn convert(
        self,
        (program, attrs): (&ast::Program, BindgenAttrs),
    ) -> Result<Self::Target, Diagnostic> {
        let js_name = attrs
            .js_name()
            .map(|s| s.0)
            .map_or_else(|| self.ident.to_string(), |s| s.to_string());
        let typescript_type = attrs.typescript_type().map(|s| s.0.to_string());
        let is_type_of = attrs.is_type_of().cloned();
        let shim = format!("__wbg_instanceof_{}_{}", self.ident, ShortHash(&self.ident));
        let mut extends = Vec::new();
        let mut vendor_prefixes = Vec::new();
        let no_deref = attrs.no_deref().is_some();
        for (used, attr) in attrs.attrs.iter() {
            match attr {
                BindgenAttr::Extends(_, e) => {
                    extends.push(e.clone());
                    used.set(true);
                }
                BindgenAttr::VendorPrefix(_, e) => {
                    vendor_prefixes.push(e.clone());
                    used.set(true);
                }
                _ => {}
            }
        }
        attrs.check_used();
        Ok(ast::ImportKind::Type(ast::ImportType {
            vis: self.vis,
            attrs: self.attrs,
            doc_comment: None,
            instanceof_shim: shim,
            is_type_of,
            rust_name: self.ident,
            typescript_type,
            js_name,
            extends,
            vendor_prefixes,
            no_deref,
            wasm_bindgen: program.wasm_bindgen.clone(),
        }))
    }
}

impl<'a> ConvertToAst<(&ast::Program, BindgenAttrs, &'a Option<ast::ImportModule>)>
    for syn::ForeignItemStatic
{
    type Target = ast::ImportKind;

    fn convert(
        self,
        (program, opts, module): (&ast::Program, BindgenAttrs, &'a Option<ast::ImportModule>),
    ) -> Result<Self::Target, Diagnostic> {
        if let syn::StaticMutability::Mut(_) = self.mutability {
            bail_span!(self.mutability, "cannot import mutable globals yet")
        }

        let default_name = self.ident.to_string();
        let js_name = opts
            .js_name()
            .map(|p| p.0)
            .unwrap_or(&default_name)
            .to_string();
        let shim = format!(
            "__wbg_static_accessor_{}_{}",
            self.ident,
            ShortHash((&js_name, module, &self.ident)),
        );
        opts.check_used();
        Ok(ast::ImportKind::Static(ast::ImportStatic {
            ty: *self.ty,
            vis: self.vis,
            rust_name: self.ident.clone(),
            js_name,
            shim: Ident::new(&shim, Span::call_site()),
            wasm_bindgen: program.wasm_bindgen.clone(),
        }))
    }
}

impl ConvertToAst<BindgenAttrs> for syn::ItemFn {
    type Target = ast::Function;

    fn convert(self, attrs: BindgenAttrs) -> Result<Self::Target, Diagnostic> {
        match self.vis {
            syn::Visibility::Public(_) => {}
            _ if attrs.start().is_some() => {}
            _ => bail_span!(self, "can only #[wasm_bindgen] public functions"),
        }
        if self.sig.constness.is_some() {
            bail_span!(
                self.sig.constness,
                "can only #[wasm_bindgen] non-const functions"
            );
        }

        let ret = function_from_decl(
            &self.sig.ident,
            &attrs,
            self.sig.clone(),
            self.attrs,
            self.vis,
            false,
            None,
            false,
        )?;
        attrs.check_used();
        Ok(ret.0)
    }
}

pub(crate) fn is_js_keyword(keyword: &str) -> bool {
    JS_KEYWORDS.contains(&keyword)
}

/// Construct a function (and gets the self type if appropriate) for our AST from a syn function.
#[allow(clippy::too_many_arguments)]
fn function_from_decl(
    decl_name: &syn::Ident,
    opts: &BindgenAttrs,
    sig: syn::Signature,
    attrs: Vec<syn::Attribute>,
    vis: syn::Visibility,
    allow_self: bool,
    self_ty: Option<&Ident>,
    is_from_impl: bool,
) -> Result<(ast::Function, Option<ast::MethodSelf>), Diagnostic> {
    if sig.variadic.is_some() {
        bail_span!(sig.variadic, "can't #[wasm_bindgen] variadic functions");
    }
    if !sig.generics.params.is_empty() {
        bail_span!(
            sig.generics,
            "can't #[wasm_bindgen] functions with lifetime or type parameters",
        );
    }

    assert_no_lifetimes(&sig)?;

    let syn::Signature { inputs, output, .. } = sig;

    let replace_self = |t: syn::Type| {
        let self_ty = match self_ty {
            Some(i) => i,
            None => return t,
        };
        let path = match get_ty(&t) {
            syn::Type::Path(syn::TypePath { qself: None, path }) => path.clone(),
            other => return other.clone(),
        };
        let new_path = if path.segments.len() == 1 && path.segments[0].ident == "Self" {
            self_ty.clone().into()
        } else {
            path
        };
        syn::Type::Path(syn::TypePath {
            qself: None,
            path: new_path,
        })
    };

    let replace_colliding_arg = |i: &mut syn::PatType| {
        if let syn::Pat::Ident(ref mut i) = *i.pat {
            let ident = i.ident.to_string();
            if is_js_keyword(ident.as_str()) {
                i.ident = Ident::new(format!("_{}", ident).as_str(), i.ident.span());
            }
        }
    };

    let mut method_self = None;
    let arguments = inputs
        .into_iter()
        .filter_map(|arg| match arg {
            syn::FnArg::Typed(mut c) => {
                replace_colliding_arg(&mut c);
                c.ty = Box::new(replace_self(*c.ty));
                Some(c)
            }
            syn::FnArg::Receiver(r) => {
                if !allow_self {
                    panic!("arguments cannot be `self`")
                }
                assert!(method_self.is_none());
                if r.reference.is_none() {
                    method_self = Some(ast::MethodSelf::ByValue);
                } else if r.mutability.is_some() {
                    method_self = Some(ast::MethodSelf::RefMutable);
                } else {
                    method_self = Some(ast::MethodSelf::RefShared);
                }
                None
            }
        })
        .collect::<Vec<_>>();

    let ret = match output {
        syn::ReturnType::Default => None,
        syn::ReturnType::Type(_, ty) => Some(replace_self(*ty)),
    };

    let (name, name_span, renamed_via_js_name) = if let Some((js_name, js_name_span)) =
        opts.js_name()
    {
        let kind = operation_kind(opts);
        let prefix = match kind {
            OperationKind::Setter(_) => "set_",
            _ => "",
        };
        let name = if prefix.is_empty() && opts.method().is_none() && is_js_keyword(js_name) {
            format!("_{}", js_name)
        } else {
            format!("{}{}", prefix, js_name)
        };
        (name, js_name_span, true)
    } else {
        let name =
            if !is_from_impl && opts.method().is_none() && is_js_keyword(&decl_name.to_string()) {
                format!("_{}", decl_name)
            } else {
                decl_name.to_string()
            };
        (name, decl_name.span(), false)
    };
    Ok((
        ast::Function {
            arguments,
            name_span,
            name,
            renamed_via_js_name,
            ret,
            rust_attrs: attrs,
            rust_vis: vis,
            r#unsafe: sig.unsafety.is_some(),
            r#async: sig.asyncness.is_some(),
            generate_typescript: opts.skip_typescript().is_none(),
            generate_jsdoc: opts.skip_jsdoc().is_none(),
            variadic: opts.variadic().is_some(),
        },
        method_self,
    ))
}

pub(crate) trait MacroParse<Ctx> {
    /// Parse the contents of an object into our AST, with a context if necessary.
    ///
    /// The context is used to have access to the attributes on `#[wasm_bindgen]`, and to allow
    /// writing to the output `TokenStream`.
    fn macro_parse(self, program: &mut ast::Program, context: Ctx) -> Result<(), Diagnostic>;
}

impl<'a> MacroParse<(Option<BindgenAttrs>, &'a mut TokenStream)> for syn::Item {
    fn macro_parse(
        self,
        program: &mut ast::Program,
        (opts, tokens): (Option<BindgenAttrs>, &'a mut TokenStream),
    ) -> Result<(), Diagnostic> {
        match self {
            syn::Item::Fn(mut f) => {
                let opts = opts.unwrap_or_default();
                if let Some(path) = opts.wasm_bindgen() {
                    program.wasm_bindgen = path.clone();
                }
                if let Some(path) = opts.wasm_bindgen_futures() {
                    program.wasm_bindgen_futures = path.clone();
                }

                if opts.main().is_some() {
                    opts.check_used();
                    return main(program, f, tokens);
                }

                let no_mangle = f
                    .attrs
                    .iter()
                    .enumerate()
                    .find(|(_, m)| m.path().is_ident("no_mangle"));
                if let Some((i, _)) = no_mangle {
                    f.attrs.remove(i);
                }
                let comments = extract_doc_comments(&f.attrs);
                // If the function isn't used for anything other than being exported to JS,
                // it'll be unused when not building for the wasm target and produce a
                // `dead_code` warning. So, add `#[allow(dead_code)]` before it to avoid that.
                tokens.extend(quote::quote! { #[allow(dead_code)] });
                f.to_tokens(tokens);
                if opts.start().is_some() {
                    if !f.sig.generics.params.is_empty() {
                        bail_span!(&f.sig.generics, "the start function cannot have generics",);
                    }
                    if !f.sig.inputs.is_empty() {
                        bail_span!(&f.sig.inputs, "the start function cannot have arguments",);
                    }
                }
                let method_kind = ast::MethodKind::Operation(ast::Operation {
                    is_static: true,
                    kind: operation_kind(&opts),
                });
                let rust_name = f.sig.ident.clone();
                let start = opts.start().is_some();
                program.exports.push(ast::Export {
                    comments,
                    function: f.convert(opts)?,
                    js_class: None,
                    method_kind,
                    method_self: None,
                    rust_class: None,
                    rust_name,
                    start,
                    wasm_bindgen: program.wasm_bindgen.clone(),
                    wasm_bindgen_futures: program.wasm_bindgen_futures.clone(),
                });
            }
            syn::Item::Struct(mut s) => {
                let opts = opts.unwrap_or_default();
                program.structs.push((&mut s).convert((program, opts))?);
                s.to_tokens(tokens);
            }
            syn::Item::Impl(mut i) => {
                let opts = opts.unwrap_or_default();
                (&mut i).macro_parse(program, opts)?;
                i.to_tokens(tokens);
            }
            syn::Item::ForeignMod(mut f) => {
                let opts = match opts {
                    Some(opts) => opts,
                    None => BindgenAttrs::find(&mut f.attrs)?,
                };
                f.macro_parse(program, opts)?;
            }
            syn::Item::Enum(mut e) => {
                let opts = match opts {
                    Some(opts) => opts,
                    None => BindgenAttrs::find(&mut e.attrs)?,
                };
                e.macro_parse(program, (tokens, opts))?;
            }
            syn::Item::Const(mut c) => {
                let opts = match opts {
                    Some(opts) => opts,
                    None => BindgenAttrs::find(&mut c.attrs)?,
                };
                c.macro_parse(program, opts)?;
            }
            _ => {
                bail_span!(
                    self,
                    "#[wasm_bindgen] can only be applied to a function, \
                     struct, enum, impl, or extern block",
                );
            }
        }

        Ok(())
    }
}

impl<'a> MacroParse<BindgenAttrs> for &'a mut syn::ItemImpl {
    fn macro_parse(self, program: &mut ast::Program, opts: BindgenAttrs) -> Result<(), Diagnostic> {
        if self.defaultness.is_some() {
            bail_span!(
                self.defaultness,
                "#[wasm_bindgen] default impls are not supported"
            );
        }
        if self.unsafety.is_some() {
            bail_span!(
                self.unsafety,
                "#[wasm_bindgen] unsafe impls are not supported"
            );
        }
        if let Some((_, path, _)) = &self.trait_ {
            bail_span!(path, "#[wasm_bindgen] trait impls are not supported");
        }
        if !self.generics.params.is_empty() {
            bail_span!(
                self.generics,
                "#[wasm_bindgen] generic impls aren't supported"
            );
        }
        let name = match get_ty(&self.self_ty) {
            syn::Type::Path(syn::TypePath {
                qself: None,
                ref path,
            }) => path,
            _ => bail_span!(
                self.self_ty,
                "unsupported self type in #[wasm_bindgen] impl"
            ),
        };
        let mut errors = Vec::new();
        for item in self.items.iter_mut() {
            if let Err(e) = prepare_for_impl_recursion(item, name, program, &opts) {
                errors.push(e);
            }
        }
        Diagnostic::from_vec(errors)?;
        opts.check_used();
        Ok(())
    }
}

// Prepare for recursion into an `impl` block. Here we want to attach an
// internal attribute, `__wasm_bindgen_class_marker`, with any metadata we need
// to pass from the impl to the impl item. Recursive macro expansion will then
// expand the `__wasm_bindgen_class_marker` attribute.
//
// Note that we currently do this because inner items may have things like cfgs
// on them, so we want to expand the impl first, let the insides get cfg'd, and
// then go for the rest.
fn prepare_for_impl_recursion(
    item: &mut syn::ImplItem,
    class: &syn::Path,
    program: &ast::Program,
    impl_opts: &BindgenAttrs,
) -> Result<(), Diagnostic> {
    let method = match item {
        syn::ImplItem::Fn(m) => m,
        syn::ImplItem::Const(_) => {
            bail_span!(
                &*item,
                "const definitions aren't supported with #[wasm_bindgen]"
            );
        }
        syn::ImplItem::Type(_) => bail_span!(
            &*item,
            "type definitions in impls aren't supported with #[wasm_bindgen]"
        ),
        syn::ImplItem::Macro(_) => {
            // In theory we want to allow this, but we have no way of expanding
            // the macro and then placing our magical attributes on the expanded
            // functions. As a result, just disallow it for now to hopefully
            // ward off buggy results from this macro.
            bail_span!(&*item, "macros in impls aren't supported");
        }
        syn::ImplItem::Verbatim(_) => panic!("unparsed impl item?"),
        other => bail_span!(other, "failed to parse this item as a known item"),
    };

    let ident = extract_path_ident(class)?;

    let js_class = impl_opts
        .js_class()
        .map(|s| s.0.to_string())
        .unwrap_or(ident.to_string());

    let wasm_bindgen = &program.wasm_bindgen;
    let wasm_bindgen_futures = &program.wasm_bindgen_futures;
    method.attrs.insert(
        0,
        syn::Attribute {
            pound_token: Default::default(),
            style: syn::AttrStyle::Outer,
            bracket_token: Default::default(),
            meta: syn::parse_quote! { #wasm_bindgen::prelude::__wasm_bindgen_class_marker(#class = #js_class, wasm_bindgen = #wasm_bindgen, wasm_bindgen_futures = #wasm_bindgen_futures) },
        },
    );

    Ok(())
}

impl<'a> MacroParse<&ClassMarker> for &'a mut syn::ImplItemFn {
    fn macro_parse(
        self,
        program: &mut ast::Program,
        ClassMarker {
            class,
            js_class,
            wasm_bindgen,
            wasm_bindgen_futures,
        }: &ClassMarker,
    ) -> Result<(), Diagnostic> {
        program.wasm_bindgen = wasm_bindgen.clone();
        program.wasm_bindgen_futures = wasm_bindgen_futures.clone();

        match self.vis {
            syn::Visibility::Public(_) => {}
            _ => return Ok(()),
        }
        if self.defaultness.is_some() {
            panic!("default methods are not supported");
        }
        if self.sig.constness.is_some() {
            bail_span!(
                self.sig.constness,
                "can only #[wasm_bindgen] non-const functions",
            );
        }

        let opts = BindgenAttrs::find(&mut self.attrs)?;
        let comments = extract_doc_comments(&self.attrs);
        let (function, method_self) = function_from_decl(
            &self.sig.ident,
            &opts,
            self.sig.clone(),
            self.attrs.clone(),
            self.vis.clone(),
            true,
            Some(class),
            true,
        )?;
        let method_kind = if opts.constructor().is_some() {
            ast::MethodKind::Constructor
        } else {
            let is_static = method_self.is_none();
            let kind = operation_kind(&opts);
            ast::MethodKind::Operation(ast::Operation { is_static, kind })
        };
        program.exports.push(ast::Export {
            comments,
            function,
            js_class: Some(js_class.to_string()),
            method_kind,
            method_self,
            rust_class: Some(class.clone()),
            rust_name: self.sig.ident.clone(),
            start: false,
            wasm_bindgen: program.wasm_bindgen.clone(),
            wasm_bindgen_futures: program.wasm_bindgen_futures.clone(),
        });
        opts.check_used();
        Ok(())
    }
}

fn import_enum(enum_: syn::ItemEnum, program: &mut ast::Program) -> Result<(), Diagnostic> {
    let mut variants = vec![];
    let mut variant_values = vec![];

    for v in enum_.variants.iter() {
        match v.fields {
            syn::Fields::Unit => (),
            _ => bail_span!(v.fields, "only C-Style enums allowed with #[wasm_bindgen]"),
        }

        let (_, expr) = match &v.discriminant {
            Some(pair) => pair,
            None => {
                bail_span!(v, "all variants must have a value");
            }
        };
        match get_expr(expr) {
            syn::Expr::Lit(syn::ExprLit {
                attrs: _,
                lit: syn::Lit::Str(str_lit),
            }) => {
                variants.push(v.ident.clone());
                variant_values.push(str_lit.value());
            }
            expr => bail_span!(
                expr,
                "enums with #[wasm_bindgen] cannot mix string and non-string values",
            ),
        }
    }

    program.imports.push(ast::Import {
        module: None,
        js_namespace: None,
        kind: ast::ImportKind::Enum(ast::ImportEnum {
            vis: enum_.vis,
            name: enum_.ident,
            variants,
            variant_values,
            rust_attrs: enum_.attrs,
            wasm_bindgen: program.wasm_bindgen.clone(),
        }),
    });

    Ok(())
}

impl<'a> MacroParse<(&'a mut TokenStream, BindgenAttrs)> for syn::ItemEnum {
    fn macro_parse(
        self,
        program: &mut ast::Program,
        (tokens, opts): (&'a mut TokenStream, BindgenAttrs),
    ) -> Result<(), Diagnostic> {
        if self.variants.is_empty() {
            bail_span!(self, "cannot export empty enums to JS");
        }
        let generate_typescript = opts.skip_typescript().is_none();

        // Check if the first value is a string literal
        if let Some((_, expr)) = &self.variants[0].discriminant {
            if let syn::Expr::Lit(syn::ExprLit {
                lit: syn::Lit::Str(_),
                ..
            }) = get_expr(expr)
            {
                opts.check_used();
                return import_enum(self, program);
            }
        }
        let js_name = opts
            .js_name()
            .map(|s| s.0)
            .map_or_else(|| self.ident.to_string(), |s| s.to_string());
        opts.check_used();

        let has_discriminant = self.variants[0].discriminant.is_some();

        match self.vis {
            syn::Visibility::Public(_) => {}
            _ => bail_span!(self, "only public enums are allowed with #[wasm_bindgen]"),
        }

        let variants = self
            .variants
            .iter()
            .enumerate()
            .map(|(i, v)| {
                match v.fields {
                    syn::Fields::Unit => (),
                    _ => bail_span!(v.fields, "only C-Style enums allowed with #[wasm_bindgen]"),
                }

                // Require that everything either has a discriminant or doesn't.
                // We don't really want to get in the business of emulating how
                // rustc assigns values to enums.
                if v.discriminant.is_some() != has_discriminant {
                    bail_span!(
                        v,
                        "must either annotate discriminant of all variants or none"
                    );
                }

                let value = match &v.discriminant {
                    Some((_, expr)) => match get_expr(expr) {
                        syn::Expr::Lit(syn::ExprLit {
                            attrs: _,
                            lit: syn::Lit::Int(int_lit),
                        }) => match int_lit.base10_digits().parse::<u32>() {
                            Ok(v) => v,
                            Err(_) => {
                                bail_span!(
                                    int_lit,
                                    "enums with #[wasm_bindgen] can only support \
                                 numbers that can be represented as u32"
                                );
                            }
                        },
                        expr => bail_span!(
                            expr,
                            "enums with #[wasm_bindgen] may only have \
                             number literal values",
                        ),
                    },
                    None => i as u32,
                };

                let comments = extract_doc_comments(&v.attrs);
                Ok(ast::Variant {
                    name: v.ident.clone(),
                    value,
                    comments,
                })
            })
            .collect::<Result<Vec<_>, Diagnostic>>()?;

        let mut values = variants.iter().map(|v| v.value).collect::<Vec<_>>();
        values.sort();
        let hole = values
            .windows(2)
            .find_map(|window| {
                if window[0] + 1 != window[1] {
                    Some(window[0] + 1)
                } else {
                    None
                }
            })
            .unwrap_or(*values.last().unwrap() + 1);
        for value in values {
            assert!(hole != value);
        }

        let comments = extract_doc_comments(&self.attrs);

        self.to_tokens(tokens);

        program.enums.push(ast::Enum {
            rust_name: self.ident,
            js_name,
            variants,
            comments,
            hole,
            generate_typescript,
            wasm_bindgen: program.wasm_bindgen.clone(),
        });
        Ok(())
    }
}

impl MacroParse<BindgenAttrs> for syn::ItemConst {
    fn macro_parse(self, program: &mut ast::Program, opts: BindgenAttrs) -> Result<(), Diagnostic> {
        // Shortcut
        if opts.typescript_custom_section().is_none() {
            bail_span!(self, "#[wasm_bindgen] will not work on constants unless you are defining a #[wasm_bindgen(typescript_custom_section)].");
        }

        match get_expr(&self.expr) {
            syn::Expr::Lit(syn::ExprLit {
                lit: syn::Lit::Str(litstr),
                ..
            }) => {
                program.typescript_custom_sections.push(litstr.value());
            }
            expr => {
                bail_span!(expr, "Expected a string literal to be used with #[wasm_bindgen(typescript_custom_section)].");
            }
        }

        opts.check_used();

        Ok(())
    }
}

impl MacroParse<BindgenAttrs> for syn::ItemForeignMod {
    fn macro_parse(self, program: &mut ast::Program, opts: BindgenAttrs) -> Result<(), Diagnostic> {
        let mut errors = Vec::new();
        if let Some(other) = self.abi.name.filter(|l| l.value() != "C") {
            errors.push(err_span!(
                other,
                "only foreign mods with the `C` ABI are allowed"
            ));
        }
        let js_namespace = opts.js_namespace().map(|(s, _)| s.to_owned());
        let module = module_from_opts(program, &opts)
            .map_err(|e| errors.push(e))
            .unwrap_or_default();
        for item in self.items.into_iter() {
            let ctx = ForeignItemCtx {
                module: module.clone(),
                js_namespace: js_namespace.clone(),
            };
            if let Err(e) = item.macro_parse(program, ctx) {
                errors.push(e);
            }
        }
        Diagnostic::from_vec(errors)?;
        opts.check_used();
        Ok(())
    }
}

struct ForeignItemCtx {
    module: Option<ast::ImportModule>,
    js_namespace: Option<Vec<String>>,
}

impl MacroParse<ForeignItemCtx> for syn::ForeignItem {
    fn macro_parse(
        mut self,
        program: &mut ast::Program,
        ctx: ForeignItemCtx,
    ) -> Result<(), Diagnostic> {
        let item_opts = {
            let attrs = match self {
                syn::ForeignItem::Fn(ref mut f) => &mut f.attrs,
                syn::ForeignItem::Type(ref mut t) => &mut t.attrs,
                syn::ForeignItem::Static(ref mut s) => &mut s.attrs,
                _ => panic!("only foreign functions/types allowed for now"),
            };
            BindgenAttrs::find(attrs)?
        };

        let js_namespace = item_opts
            .js_namespace()
            .map(|(s, _)| s.to_owned())
            .or(ctx.js_namespace);
        let module = ctx.module;

        let kind = match self {
            syn::ForeignItem::Fn(f) => f.convert((program, item_opts, &module))?,
            syn::ForeignItem::Type(t) => t.convert((program, item_opts))?,
            syn::ForeignItem::Static(s) => s.convert((program, item_opts, &module))?,
            _ => panic!("only foreign functions/types allowed for now"),
        };

        program.imports.push(ast::Import {
            module,
            js_namespace,
            kind,
        });

        Ok(())
    }
}

pub fn module_from_opts(
    program: &mut ast::Program,
    opts: &BindgenAttrs,
) -> Result<Option<ast::ImportModule>, Diagnostic> {
    if let Some(path) = opts.wasm_bindgen() {
        program.wasm_bindgen = path.clone();
    }

    if let Some(path) = opts.wasm_bindgen_futures() {
        program.wasm_bindgen_futures = path.clone();
    }

    let mut errors = Vec::new();
    let module = if let Some((name, span)) = opts.module() {
        if opts.inline_js().is_some() {
            let msg = "cannot specify both `module` and `inline_js`";
            errors.push(Diagnostic::span_error(span, msg));
        }
        if opts.raw_module().is_some() {
            let msg = "cannot specify both `module` and `raw_module`";
            errors.push(Diagnostic::span_error(span, msg));
        }
        Some(ast::ImportModule::Named(name.to_string(), span))
    } else if let Some((name, span)) = opts.raw_module() {
        if opts.inline_js().is_some() {
            let msg = "cannot specify both `raw_module` and `inline_js`";
            errors.push(Diagnostic::span_error(span, msg));
        }
        Some(ast::ImportModule::RawNamed(name.to_string(), span))
    } else if let Some((js, span)) = opts.inline_js() {
        let i = program.inline_js.len();
        program.inline_js.push(js.to_string());
        Some(ast::ImportModule::Inline(i, span))
    } else {
        None
    };
    Diagnostic::from_vec(errors)?;
    Ok(module)
}

/// Get the first type parameter of a generic type, errors on incorrect input.
fn extract_first_ty_param(ty: Option<&syn::Type>) -> Result<Option<syn::Type>, Diagnostic> {
    let t = match ty {
        Some(t) => t,
        None => return Ok(None),
    };
    let path = match *get_ty(t) {
        syn::Type::Path(syn::TypePath {
            qself: None,
            ref path,
        }) => path,
        _ => bail_span!(t, "must be Result<...>"),
    };
    let seg = path
        .segments
        .last()
        .ok_or_else(|| err_span!(t, "must have at least one segment"))?;
    let generics = match seg.arguments {
        syn::PathArguments::AngleBracketed(ref t) => t,
        _ => bail_span!(t, "must be Result<...>"),
    };
    let generic = generics
        .args
        .first()
        .ok_or_else(|| err_span!(t, "must have at least one generic parameter"))?;
    let ty = match generic {
        syn::GenericArgument::Type(t) => t,
        other => bail_span!(other, "must be a type parameter"),
    };
    match get_ty(ty) {
        syn::Type::Tuple(t) if t.elems.is_empty() => return Ok(None),
        _ => {}
    }
    Ok(Some(ty.clone()))
}

/// Extract the documentation comments from a Vec of attributes
fn extract_doc_comments(attrs: &[syn::Attribute]) -> Vec<String> {
    attrs
        .iter()
        .filter_map(|a| {
            // if the path segments include an ident of "doc" we know this
            // this is a doc comment
            if a.path().segments.iter().any(|s| s.ident == "doc") {
                let tokens = match &a.meta {
                    syn::Meta::Path(_) => None,
                    syn::Meta::List(list) => Some(list.tokens.clone()),
                    syn::Meta::NameValue(name_value) => Some(name_value.value.to_token_stream()),
                };

                Some(
                    // We want to filter out any Puncts so just grab the Literals
                    tokens.into_iter().flatten().filter_map(|t| match t {
                        TokenTree::Literal(lit) => {
                            let quoted = lit.to_string();
                            Some(try_unescape(&quoted).unwrap_or(quoted))
                        }
                        _ => None,
                    }),
                )
            } else {
                None
            }
        })
        //Fold up the [[String]] iter we created into Vec<String>
        .fold(vec![], |mut acc, a| {
            acc.extend(a);
            acc
        })
}

// Unescapes a quoted string. char::escape_debug() was used to escape the text.
fn try_unescape(mut s: &str) -> Option<String> {
    s = s.strip_prefix('"').unwrap_or(s);
    s = s.strip_suffix('"').unwrap_or(s);
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars();
    while let Some(c) = chars.next() {
        if c == '\\' {
            let c = chars.next()?;
            match c {
                't' => result.push('\t'),
                'r' => result.push('\r'),
                'n' => result.push('\n'),
                '\\' | '\'' | '"' => result.push(c),
                'u' => {
                    if chars.next() != Some('{') {
                        return None;
                    }
                    let (c, next) = unescape_unicode(&mut chars)?;
                    result.push(c);
                    if next != '}' {
                        return None;
                    }
                }
                _ => return None,
            }
        } else {
            result.push(c);
        }
    }
    Some(result)
}

fn unescape_unicode(chars: &mut Chars) -> Option<(char, char)> {
    let mut value = 0;
    for (i, c) in chars.enumerate() {
        match (i, c.to_digit(16)) {
            (0..=5, Some(num)) => value = (value << 4) | num,
            (1.., None) => return Some((char::from_u32(value)?, c)),
            _ => break,
        }
    }
    None
}

/// Check there are no lifetimes on the function.
fn assert_no_lifetimes(sig: &syn::Signature) -> Result<(), Diagnostic> {
    struct Walk {
        diagnostics: Vec<Diagnostic>,
    }

    impl<'ast> syn::visit::Visit<'ast> for Walk {
        fn visit_lifetime(&mut self, i: &'ast syn::Lifetime) {
            self.diagnostics.push(err_span!(
                i,
                "it is currently not sound to use lifetimes in function \
                 signatures"
            ));
        }
    }
    let mut walk = Walk {
        diagnostics: Vec::new(),
    };
    syn::visit::Visit::visit_signature(&mut walk, sig);
    Diagnostic::from_vec(walk.diagnostics)
}

/// Extracts the last ident from the path
fn extract_path_ident(path: &syn::Path) -> Result<Ident, Diagnostic> {
    for segment in path.segments.iter() {
        match segment.arguments {
            syn::PathArguments::None => {}
            _ => bail_span!(path, "paths with type parameters are not supported yet"),
        }
    }

    match path.segments.last() {
        Some(value) => Ok(value.ident.clone()),
        None => {
            bail_span!(path, "empty idents are not supported");
        }
    }
}

pub fn reset_attrs_used() {
    ATTRS.with(|state| {
        state.parsed.set(0);
        state.checks.set(0);
        state.unused_attrs.borrow_mut().clear();
    })
}

pub fn check_unused_attrs(tokens: &mut TokenStream) {
    ATTRS.with(|state| {
        assert_eq!(state.parsed.get(), state.checks.get());
        let unused_attrs = &*state.unused_attrs.borrow();
        if !unused_attrs.is_empty() {
            tokens.extend(quote::quote! {
                // Anonymous scope to prevent name clashes.
                const _: () = {
                    #(let #unused_attrs: ();)*
                };
            });
        }
    })
}

fn operation_kind(opts: &BindgenAttrs) -> ast::OperationKind {
    let mut operation_kind = ast::OperationKind::Regular;
    if let Some(g) = opts.getter() {
        operation_kind = ast::OperationKind::Getter(g.clone());
    }
    if let Some(s) = opts.setter() {
        operation_kind = ast::OperationKind::Setter(s.clone());
    }
    if opts.indexing_getter().is_some() {
        operation_kind = ast::OperationKind::IndexingGetter;
    }
    if opts.indexing_setter().is_some() {
        operation_kind = ast::OperationKind::IndexingSetter;
    }
    if opts.indexing_deleter().is_some() {
        operation_kind = ast::OperationKind::IndexingDeleter;
    }
    operation_kind
}

pub fn link_to(opts: BindgenAttrs) -> Result<ast::LinkToModule, Diagnostic> {
    let mut program = ast::Program::default();
    let module = module_from_opts(&mut program, &opts)?.ok_or_else(|| {
        Diagnostic::span_error(Span::call_site(), "`link_to!` requires a module.")
    })?;
    if let ast::ImportModule::Named(p, s) | ast::ImportModule::RawNamed(p, s) = &module {
        if !p.starts_with("./") && !p.starts_with("../") && !p.starts_with('/') {
            return Err(Diagnostic::span_error(
                *s,
                "`link_to!` does not support module paths.",
            ));
        }
    }
    opts.enforce_used()?;
    program.linked_modules.push(module);
    Ok(ast::LinkToModule(program))
}

fn main(program: &ast::Program, mut f: ItemFn, tokens: &mut TokenStream) -> Result<(), Diagnostic> {
    if f.sig.ident != "main" {
        bail_span!(&f.sig.ident, "the main function has to be called main");
    }
    if let Some(constness) = f.sig.constness {
        bail_span!(&constness, "the main function cannot be const");
    }
    if !f.sig.generics.params.is_empty() {
        bail_span!(&f.sig.generics, "the main function cannot have generics");
    }
    if !f.sig.inputs.is_empty() {
        bail_span!(&f.sig.inputs, "the main function cannot have arguments");
    }

    let r#return = f.sig.output;
    f.sig.output = ReturnType::Default;
    let body = f.block;

    let wasm_bindgen = &program.wasm_bindgen;
    let wasm_bindgen_futures = &program.wasm_bindgen_futures;

    if f.sig.asyncness.take().is_some() {
        f.block = Box::new(
            syn::parse2(quote::quote! {
                {
                    async fn __wasm_bindgen_generated_main() #r#return #body
                    #wasm_bindgen_futures::spawn_local(
                        async move {
                            use #wasm_bindgen::__rt::Main;
                            let __ret = __wasm_bindgen_generated_main();
                            (&mut &mut &mut #wasm_bindgen::__rt::MainWrapper(Some(__ret.await))).__wasm_bindgen_main()
                        },
                    )
                }
            })
            .unwrap(),
        );
    } else {
        f.block = Box::new(
            syn::parse2(quote::quote! {
                {
                    fn __wasm_bindgen_generated_main() #r#return #body
                    use #wasm_bindgen::__rt::Main;
                    let __ret = __wasm_bindgen_generated_main();
                    (&mut &mut &mut #wasm_bindgen::__rt::MainWrapper(Some(__ret))).__wasm_bindgen_main()
                }
            })
            .unwrap(),
        );
    }

    f.to_tokens(tokens);

    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_try_unescape() {
        use super::try_unescape;
        assert_eq!(try_unescape("hello").unwrap(), "hello");
        assert_eq!(try_unescape("\"hello").unwrap(), "hello");
        assert_eq!(try_unescape("hello\"").unwrap(), "hello");
        assert_eq!(try_unescape("\"hello\"").unwrap(), "hello");
        assert_eq!(try_unescape("hello\\\\").unwrap(), "hello\\");
        assert_eq!(try_unescape("hello\\n").unwrap(), "hello\n");
        assert_eq!(try_unescape("hello\\u"), None);
        assert_eq!(try_unescape("hello\\u{"), None);
        assert_eq!(try_unescape("hello\\u{}"), None);
        assert_eq!(try_unescape("hello\\u{0}").unwrap(), "hello\0");
        assert_eq!(try_unescape("hello\\u{000000}").unwrap(), "hello\0");
        assert_eq!(try_unescape("hello\\u{0000000}"), None);
    }
}

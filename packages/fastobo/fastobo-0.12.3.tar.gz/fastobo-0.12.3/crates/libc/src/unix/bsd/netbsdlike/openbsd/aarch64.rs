pub type c_long = i64;
pub type c_ulong = u64;
pub type c_char = u8;
pub type ucontext_t = sigcontext;

s! {
    pub struct sigcontext {
        __sc_unused: ::c_int,
        pub sc_mask: ::c_int,
        pub sc_sp: ::c_ulong,
        pub sc_lr: ::c_ulong,
        pub sc_elr: ::c_ulong,
        pub sc_spsr: ::c_ulong,
        pub sc_x: [::c_ulong; 30],
        pub sc_cookie: ::c_long,
    }
}

// should be pub(crate), but that requires Rust 1.18.0
cfg_if! {
    if #[cfg(libc_const_size_of)] {
        #[doc(hidden)]
        pub const _ALIGNBYTES: usize = ::mem::size_of::<::c_long>() - 1;
    } else {
        #[doc(hidden)]
        pub const _ALIGNBYTES: usize = 8 - 1;
    }
}

pub const _MAX_PAGE_SHIFT: u32 = 12;

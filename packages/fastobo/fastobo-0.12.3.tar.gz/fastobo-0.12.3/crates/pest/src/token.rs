// pest. The Elegant Parser
// Copyright (c) 2018 Dragoș Tiselice
//
// Licensed under the Apache License, Version 2.0
// <LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0> or the MIT
// license <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. All files in the project carrying such notice may not be copied,
// modified, or distributed except according to those terms.

use crate::position::Position;

/// A token generated by a `Parser`.
#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub enum Token<'i, R> {
    /// The starting `Position` of a matched `Rule`
    Start {
        /// matched rule
        rule: R,
        /// starting position
        pos: Position<'i>,
    },
    /// The ending `Position` of a matched `Rule`
    End {
        /// matched rule
        rule: R,
        /// ending position
        pos: Position<'i>,
    },
}

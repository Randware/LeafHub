use serde_json::Value;
use std::{collections::HashMap, path::Path};

pub trait ConfigState {}

#[derive(Default)]
pub struct Builder<'a> {
    pub(crate) path: Option<&'a str>,
    pub(crate) format: Option<FileFormat>,
    pub(crate) default_values: Option<HashMap<String, Box<dyn Fn(&String) -> Value>>>,
}

impl<'a> Builder<'a> {
    pub(crate) fn new(path: &'a str, format: FileFormat) -> Self {
        Builder {
            path: Some(path),
            format: Some(format),
            default_values: None,
        }
    }
}

impl ConfigState for Builder<'_> {}

pub struct Finished;
impl ConfigState for Finished {}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum FileFormat {
    Yaml,
    Toml,
    Json,
    Xml,
}

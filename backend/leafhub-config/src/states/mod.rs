use erased_serde::Serialize as ErasedSerialize;
use serde_json::Value;
use std::{collections::HashMap, fs::File, path::Path};

pub trait ConfigState {}

#[derive(Default)]
pub struct Builder<'a> {
    pub(crate) path: Option<&'a str>,
    pub(crate) format: Option<FileFormat>,
    pub(crate) default_values: Option<HashMap<String, Box<dyn ErasedSerialize>>>,
    pub(crate) override_existing: bool,
}

impl<'a> Builder<'a> {
    #[allow(dead_code)]
    pub(crate) fn new(path: &'a str, format: FileFormat) -> Self {
        Builder {
            path: Some(path),
            format: Some(format),
            default_values: None,
            override_existing: false,
        }
    }
}

impl ConfigState for Builder<'_> {}

pub struct Finished {
    file: File,
    values: HashMap<String, Box<dyn ErasedSerialize>>,
}

impl ConfigState for Finished {}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum FileFormat {
    Yaml,
    Toml,
    Json,
}

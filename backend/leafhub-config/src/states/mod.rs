use serde_json::Value;
use std::{
    collections::HashMap,
    fs::File,
    io::{self, Read},
    marker::PhantomData,
    path::Path,
};

pub trait ConfigState {}

#[derive(Default)]
pub struct Builder<'b> {
    pub(crate) path: Option<&'b str>,
    pub(crate) format: Option<FileFormat>,
    pub(crate) default_values: Option<HashMap<String, serde_json::Value>>,
    pub(crate) override_file: bool,
    pub(crate) override_stored: bool,
}

impl<'b> Builder<'b> {
    #[allow(dead_code)]
    pub(crate) fn new(path: &'b str, format: FileFormat) -> Self {
        Builder {
            path: Some(path),
            format: Some(format),
            default_values: None,
            override_file: false,
            override_stored: false,
        }
    }
}

impl ConfigState for Builder<'_> {}

pub struct Finished<'f> {
    pub(crate) _lifetime: PhantomData<&'f ()>,
    pub(crate) file: File,
    pub(crate) values: HashMap<String, serde_json::Value>,
}

impl ConfigState for Finished<'_> {}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum FileFormat {
    Yaml,
    Toml,
    Json,
    Cbor,
    MessagePack,
    Pickle,
    Ron,
    Bson,
    Avro,
    Json5,
    Url,
}

impl FileFormat {
    pub fn deserialize<R: Read>(&self, reader: R) -> io::Result<HashMap<String, Value>> {
        let map = match self {
            FileFormat::Yaml => todo!(),
            FileFormat::Toml => todo!(),
            FileFormat::Json => todo!(),
            FileFormat::Cbor => todo!(),
            FileFormat::MessagePack => todo!(),
            FileFormat::Pickle => todo!(),
            FileFormat::Ron => todo!(),
            FileFormat::Bson => todo!(),
            FileFormat::Avro => todo!(),
            FileFormat::Json5 => todo!(),
            FileFormat::Url => todo!(),
        };
        todo!()
    }
}

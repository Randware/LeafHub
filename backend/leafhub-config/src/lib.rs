mod states;
use erased_serde::Serialize as ErasedSerialize;
use serde::{Deserialize, Serialize, de::DeserializeOwned};
use serde_json::Value;
use states::{Builder, ConfigState, FileFormat, Finished};
use std::{
    collections::HashMap,
    fs::OpenOptions,
    io::{self, Error, ErrorKind},
};

pub struct Config<State>
where
    State: ConfigState,
{
    state: State,
}

impl<'a, State: ConfigState> Config<State> {
    pub fn new() -> Config<Builder<'a>> {
        Config {
            state: Builder::default(),
        }
    }
}

impl<'a> Config<Builder<'a>> {
    /// Sets the FileFormat of the config file
    pub fn with_format(mut self, format: FileFormat) -> Self {
        self.state.format = Some(format);
        self
    }

    /// Sets the path where the config will be loaded/saved to
    pub fn with_path(mut self, path: &'a str) -> Self {
        self.state.path = Some(path);
        self
    }

    /// Adds a default key and value to the Config.
    /// If the expression returns `None`, then no default parameter gets added.
    /// This is usefule, in case you want to check for environment variables.
    ///
    /// # Parameters
    ///
    /// - `name`: The name of the key
    /// - `mapper`: The expression that produces the Value
    pub fn add_default<S, F, T>(mut self, name: String, mapper: F) -> Self
    where
        F: Fn(&String) -> Option<T> + 'static,
        T: ErasedSerialize + 'static,
    {
        // Initialize the HashMap if it isn't already (only the case on first time methode call)
        if self.state.default_values.is_none() {
            self.state.default_values = Some(HashMap::new());
        }

        // Executes the mapper
        let mapped_value = mapper(&name);
        // Do nothing when `None` gets returned
        if mapped_value.is_none() {
            return self;
        }
        let mut hash_map = self.state.default_values.unwrap();
        hash_map.insert(name, Box::new(mapped_value.unwrap()));
        self.state.default_values = Some(hash_map);
        self
    }

    // If enabled overrides any existing file that lies at the set path
    pub fn override_existing(mut self, override_existing: bool) -> Self {
        self.state.override_existing = override_existing;
        self
    }

    pub fn finish(mut self) -> Result<Config<Finished>, Error> {
        // Checks if the user set a path
        if let Some(path) = self.state.path {
            let mut config = OpenOptions::new();
            config.read(true).write(true);

            // Set the correct flags for the config
            if self.state.override_existing {
                config.truncate(true);
            } else {
                config.create(true);
            }

            let config = config.open(self.state.path.unwrap())?;

            //TODO: Finish up the state transition
        } else {
            return Err(Error::new(
                ErrorKind::InvalidInput,
                "Provide a path to the Config",
            ));
        }

        todo!();
    }
}

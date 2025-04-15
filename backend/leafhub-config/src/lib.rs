mod states;
use std::collections::HashMap;

use serde::{Deserialize, Serialize, de::DeserializeOwned};
use serde_json::Value;
use states::{Builder, ConfigState, FileFormat, Finished};

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
    ///
    /// # Parameters
    ///
    /// - `name`: The name of the key
    /// - `mapper`: The expression that produces the Value
    pub fn add_default<S, F, T>(mut self, name: S, mapper: F) -> Self
    where
        S: Into<String>,
        F: Fn(&String) -> Option<T> + 'static,
        T: Serialize + DeserializeOwned + 'static,
    {
        // Initialize the HashMap if it isn't already (only the case on first time methode call)
        if self.state.default_values.is_none() {
            self.state.default_values = Some(HashMap::new());
        }

        let mapper = Box::new(move |s: &String| -> Value {
            serde_json::to_value(mapper(s)).unwrap_or(Value::Null)
        });
        let mut hash_map = self.state.default_values.unwrap();
        hash_map.insert(name.into(), mapper);
        self.state.default_values = Some(hash_map);
        self
    }

    pub fn finish(mut self) -> Config<Finished> {
        todo!()
    }
}

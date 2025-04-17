mod states;
use serde::{Deserialize, Serialize, de::DeserializeOwned};
use serde_json::Value;
use states::{Builder, ConfigState, FileFormat, Finished};
use std::{
    collections::HashMap,
    fs::OpenOptions,
    io::{self, Error, ErrorKind},
    marker::PhantomData,
};

pub struct Config<'cfg, State>
where
    State: ConfigState,
{
    state: State,
    _lifetime: PhantomData<&'cfg ()>,
}

impl<'cfg, State: ConfigState> Config<'cfg, State> {
    pub fn new<'b>() -> Config<'cfg, Builder<'b>>
    where
        'cfg: 'b,
    {
        Config {
            state: Builder::default(),
            _lifetime: PhantomData,
        }
    }
}

impl<'cfg, 'b> Config<'cfg, Builder<'b>>
where
    'cfg: 'b,
{
    /// Sets the FileFormat of the config file
    pub fn with_format(mut self, format: FileFormat) -> Self {
        self.state.format = Some(format);
        self
    }

    /// Sets the path where the config will be loaded/saved to
    pub fn with_path(mut self, path: &'b str) -> Self {
        self.state.path = Some(path);
        self
    }

    /// If enabled overrides any existing *file* that lies at the set path and ignores its values
    pub fn override_file(mut self, override_existing: bool) -> Self {
        self.state.override_file = override_existing;
        self
    }

    /// If enabled overrides stored values from the file with the set default values.
    ///
    /// # Example
    /// So if there is a key/value like: __"key1" -> "val1"__ in the file and
    /// the user provided a default value: __"key1" -> "super important val"__ the
    /// value from the file gets overriden with the default one.
    ///
    /// This isn't the case normally, because default values
    /// only get used if there are no values already stored with that key
    pub fn override_stored(mut self, override_stored: bool) -> Self {
        self.state.override_stored = override_stored;
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
        T: Serialize + 'static,
    {
        // Initialize the HashMap if it isn't already (only the case on first time methode call)
        if self.state.default_values.is_none() {
            self.state.default_values = Some(HashMap::new());
        }

        // Executes the mapper
        let mapped_value = mapper(&name);
        // Do nothing when `None` gets returned
        if let Some(val) = mapped_value {
            // Serialize the value into json for an universal type.
            // If that fails do nothing
            let mapped_value = if let Ok(valid_value) = serde_json::to_value(val) {
                valid_value
            } else {
                return self;
            };

            let mut hash_map = self.state.default_values.unwrap();
            hash_map.insert(name, mapped_value);
            self.state.default_values = Some(hash_map);
            self
        } else {
            self
        }
    }

    pub fn finish<'f>(mut self) -> Result<Config<'cfg, Finished<'f>>, Error>
    where
        'cfg: 'f,
    {
        // Checks if the user set a path
        let path = self
            .state
            .path
            .ok_or_else(|| Error::new(ErrorKind::InvalidInput, "Provide a path to the Config"))?;

        let format = self.state.format.unwrap_or(FileFormat::Toml);

        let mut config = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(self.state.override_file)
            .open(path)?;

        // Load the values from the actual file if the user wants to ignore the old ones
        let mut values = if self.state.override_file {
            HashMap::new()
        } else {
            //TODO: DOCUMENT THAT THE CONFIG FILE GETS IGNORED WHEN IT CAN NOT BE DESERIALIZED!!!
            format.deserialize(&mut config).unwrap_or_default()
        };

        if let Some(defaults) = self.state.default_values {
            for (key, val) in defaults {
                if !values.contains_key(&key) || self.state.override_stored {
                    //TODO: Document the panic
                    values.insert(
                        key,
                        serde_json::to_value(val)
                            .expect("The given default could not be serialized"),
                    );
                }
            }
        }

        Ok(Config {
            state: Finished {
                _lifetime: PhantomData,
                values: values,
                file: config,
            },
            _lifetime: PhantomData,
        })
    }
}

impl<'cfg, 'f> Config<'cfg, Finished<'f>>
where
    'cfg: 'f,
{
    pub fn get<T: DeserializeOwned>(&self, key: &str) -> Option<T> {
        self.state
            .values
            .get(key)
            .and_then(|val| serde_json::from_value(val.clone()).ok())
    }

    /// Adds a given key and value to the config
    ///
    /// # Panics
    /// This function panics if the given can not be serialized.
    /// To avoid a panic use [`try_add`](fn@try_add) to get an Error instead
    pub fn add<T: Serialize>(&mut self, key: &str, value: T) {
        self.state.values.insert(
            key.to_string(),
            serde_json::to_value(value).expect("Could not serialize given value"),
        );
    }

    /// Adds a given key and value to the config
    ///
    /// # Returns
    ///
    /// - `Ok(())`: when everything went fine
    /// - `Err(serde_json::Error)`: When the type could not be serialized
    pub fn try_add<T: Serialize>(&mut self, key: &str, value: T) -> Result<(), serde_json::Error> {
        self.state
            .values
            .insert(key.to_string(), serde_json::to_value(value)?);
        Ok(())
    }
}

{
  description = "Development flake for the LeafHub microcontroller firmware";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }: {
    devShells.x86_64-linux.default = let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in pkgs.mkShell {
      buildInputs = with pkgs; [
        python310
        nodejs_23
        mpremote
        openssl
      ];

      shellHook = ''
        SRC_DIR="src"
        WEBUI_DIR="webui"
        PUBLIC_DIR="$SRC_DIR/public"
        KEYS_DIR="$SRC_DIR/keys"
        HAL_DIR="hal"

        echo ""
        echo "Successfully entered LeafHub firmware development environment"
        echo ""
        echo "The following commands are available:"
        echo "  - monitor: Connect to the serial port to monitor output"
        echo "  - flash: Flashes the src folder onto the microcontroller"
        echo "  - format: Formats the microcontrollers filesystem"
        echo "  - webui: Compile the svelte webui into the src/public folder"
        echo "  - hal <name>: Flash the HAL (Hardware Abstraction Layer) files onto the controller"
        echo "  - keys: Generate new SSL keys into the src directory"
        echo ""
        echo "Warning: These provided commands automatically detect connected controllers, make sure there is only one!"
        echo ""

        webui() {
          echo "Ensuring node_modules are installed ..."
          cd $WEBUI_DIR && npm install
          cd ..

          echo "Compiling webui to src/public ..."
          
          if [ ! -d "$WEBUI_DIR" ]; then
            echo "Error: $WEBUI_DIR directory not found in the current directory."
            return 1
          fi
          
          echo "Compiling svelte website ..."
          cd $WEBUI_DIR && npm run build || { cd ..; return 1; }
          cd ..
          
          echo "Removing unnecessary build files ..."
          if [ -d "$PUBLIC_DIR/_app" ]; then
            echo "Found _app directory at $PUBLIC_DIR/_app, removing..."
            rm -rf "$PUBLIC_DIR/_app"
            
            if [ -d "$PUBLIC_DIR/_app" ]; then
              echo "Warning: Failed to remove _app directory. It may require manual removal."
            else
              echo "_app directory successfully removed."
            fi
          else
            echo "No _app directory found at $PUBLIC_DIR/_app"
          fi
          
          echo "Compiled webui to $SRC_DIR/public" 
        }

        format() {
          echo "Formatting filesystem ..."

          mpremote connect auto exec "$(cat <<EOF
        import os

        def clear(directory):
            for file_info in os.ilistdir(directory):
                file_name, file_type = file_info[0:2]
                if file_name == 'boot.py':
                    continue
                file_full_name = "{}/{}".format(directory, file_name)
                if file_type == 0x8000:
                    os.remove(file_full_name)
                else:
                    clear(file_full_name)
                    os.rmdir(file_full_name)

        clear("/")
        print("Successfully formatted file system")
        EOF
          )"
        }

        hal() {
          if [ -z "$1" ]; then
            echo "Please provide a HAL file: hal <name>"
            return 1
          fi

          HAL_FILE="$HAL_DIR/$1.py"

          if [ -f "$HAL_FILE" ]; then
            echo "Found $HAL_FILE HAL file"
          else
            echo "No '$1' HAL file could be found in '$HAL_DIR' directory"
            return 1
          fi

          echo "Flashing HAL files to controller ..."
          mpremote connect auto fs cp "$HAL_FILE" ":/hardware.py"
        }

        keys() {
          echo "Generating ssl keys ..."

          echo "Creating $KEYS_DIR directory"
          mkdir -p "$KEYS_DIR"

          echo "Generating keys in DER format..."
          openssl req -x509 -newkey rsa:512 -nodes -subj "/CN=LeafHubSmartPot/O=/C=" -keyout $KEYS_DIR/temp_key.pem -out $KEYS_DIR/temp_cert.pem -days 36500
          openssl rsa -in $KEYS_DIR/temp_key.pem -outform DER -out $KEYS_DIR/key.der
          openssl x509 -in $KEYS_DIR/temp_cert.pem -outform DER -out $KEYS_DIR/cert.der
          rm $KEYS_DIR/temp_key.pem $KEYS_DIR/temp_cert.pem

          echo "Finished key generation"
        }

        monitor() {
          echo "Connecting to serial output ..."
          mpremote repl
        }

        flash() {
          if [ ! -d "$SRC_DIR" ]; then
            echo "Error: $SRC_DIR directory not found in the current directory."
            return 1
          fi

          # keys
          # trap "rm -rf $KEYS_DIR" RETURN # Remove keys at the end of function

          echo "Flashing '$SRC_DIR' directory to Raspberry Pi Pico on '$SERIAL_PORT' ..."

          directories=$(find "$SRC_DIR" -type d | sort)
          for dir in $directories; do
            if [ "$dir" != "$SRC_DIR" ]; then
              dest_dir="$(echo "$dir" | sed "s|$SRC_DIR/||")"
              echo "Creating directory: /$dest_dir"
              mpremote connect auto fs mkdir ":/$dest_dir" || true
            fi
          done

          for file in $(find "$SRC_DIR" -type f); do
            dest_path="$(echo "$file" | sed "s|$SRC_DIR/||")"
            echo "Copying $file to /:$dest_path"
            mpremote connect auto fs cp "$file" ":/$dest_path"
          done

          echo "Resetting the Raspberry Pi Pico ..."
          mpremote connect auto reset
        }
      '';
    };
  };
}

{
  description = "Nix flake for flashing Raspberry Pi Pico W with mpremote, resetting it, and connecting to serial output using tio";

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
        tio
      ];

      shellHook = ''
        PICO_PORT="/dev/ttyACM0"
        SRC_DIR="src"
        WEBUI_DIR="webui"
        PUBLIC_DIR="$SRC_DIR/public"
        KEYS_DIR="$SRC_DIR/keys"

        echo "Successfully entered Raspberry Pi Pico development environment"
        echo ""
        echo "The following commands are available:"
        echo "  - monitor: Connect to the serial port to monitor output"
        echo "  - flash: Flashes the src folder onto the pico"
        echo "  - format: Formats the picos filesystem"
        echo "  - webui: Compile the svelte webui into the src/public folder"
        echo "  - keys: Generate new SSL keys into the src directory"

        webui() {
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
          mpremote exec --no-follow "import os, machine, rp2; os.umount('/'); bdev = rp2.Flash(); os.VfsLfs2.mkfs(bdev, progsize=256); vfs = os.VfsLfs2(bdev, progsize=256); os.mount(vfs, '/'); machine.reset()" || exit
          echo "Successfully formatted file system"
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
          # Connect to the serial output
          echo "Connecting to serial output ..."
          tio $PICO_PORT
        }

        flash() {
          if [ ! -d "$SRC_DIR" ]; then
            echo "Error: $SRC_DIR directory not found in the current directory."
            return 1
          fi

          keys
          trap "rm -rf $KEYS_DIR" RETURN # Remove keys at the end of function

          echo "Flashing '$SRC_DIR' directory to Raspberry Pi Pico on '$PICO_PORT' ..."

          directories=$(find "$SRC_DIR" -type d | sort)
          for dir in $directories; do
            if [ "$dir" != "$SRC_DIR" ]; then
              dest_dir="$(echo "$dir" | sed "s|$SRC_DIR/||")"
              echo "Creating directory: /$dest_dir"
              mpremote connect $PICO_PORT fs mkdir ":/$dest_dir" || true
            fi
          done

          for file in $(find "$SRC_DIR" -type f); do
            dest_path="$(echo "$file" | sed "s|$SRC_DIR/||")"
            echo "Copying $file to /:$dest_path"
            mpremote connect $PICO_PORT fs cp "$file" ":/$dest_path"
          done

          echo "Resetting the Raspberry Pi Pico ..."
          mpremote connect $PICO_PORT reset
        }

      '';
    };
  };
}

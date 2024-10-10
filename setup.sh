#!/bin/bash

# Get the current working directory
CURRENT_DIR=$(pwd)
TARGET_DIR="$CURRENT_DIR/AutoReplyBot"

# Clone the GitHub repository
git clone https://github.com/HimanshuSingh82/Auto-Reply-AI-Chatbot.git

# Change to the target directory
cd "$TARGET_DIR"

# Create a Python virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create the AutoReplyBot.sh script
cat <<EOL > "$CURRENT_DIR/AutoReplyBot.sh"
#!/bin/bash
cd "$TARGET_DIR"
echo "$TARGET_DIR"
source myenv/bin/activate
python main.py
EOL

# Make the created script executable
chmod +x "$CURRENT_DIR/AutoReplyBot.sh"

echo "Setup complete. Run AutoReplyBot.sh to start the app."